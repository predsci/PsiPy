"""
Tools for reading MAS (Magnetohydrodynamics on a sphere) model outputs.

Files come in two types, .hdf or .h5. In both cases filenames always have the
structure '{var}{timestep}.{extension}', where:

- 'var' is the variable name
- 'timestep' is the three digit (zero padded) timestep
- 'extension' is '.hdf' or '.h5'
"""
import glob
import os
from pathlib import Path
from typing import List

import numpy as np
import xarray as xr

from .util import read_hdf4, read_hdf5

__all__ = ["read_mas_file", "get_mas_variables", "convert_hdf_to_netcdf"]


def get_mas_filenames(directory: os.PathLike, var: str) -> List[str]:
    """
    Get all MAS filenames in a given directory for a given variable.
    """
    directory = Path(directory)
    return sorted(glob.glob(str(directory / f"{var}*")))


def read_mas_file(directory, var):
    """
    Read in a set of MAS output files.

    Parameters
    ----------
    directory :
        Directory to look in.
    var : str
        Variable name.

    Returns
    -------
    data : xarray.DataArray
        Loaded data.
    """
    files = get_mas_filenames(directory, var)
    if not len(files):
        raise FileNotFoundError(
            f'Could not find file for variable "{var}" in ' f"directory {directory}"
        )

    if Path(files[0]).suffix == ".nc":
        return xr.open_mfdataset(files, parallel=True)

    data = [_read_mas(f, var) for f in files]
    return xr.concat(data, dim="time")


def _read_mas(path, var):
    """
    Read a single MAS file.
    """
    f = Path(path)
    if f.suffix == ".hdf":
        data, coords = read_hdf4(f)
    elif f.suffix == ".h5":
        data, coords = read_hdf5(f)

    dims = ["phi", "theta", "r", "time"]
    # Convert from co-latitude to latitude
    coords[1] = np.pi / 2 - np.array(coords[1])
    # Add time
    data = data.reshape(data.shape + (1,))
    coords.append([get_timestep(path)])
    data = xr.Dataset({var: xr.DataArray(data=data, coords=coords, dims=dims)})
    return data


def convert_hdf_to_netcdf(directory, var):
    """
    Read in a set of HDF files, and save them out to NetCDF files.

    This is helpful to convert files for loading lazily using dask.

    Warnings
    --------
    This will create a new set of files that same size as *all* the files
    read in. Make sure you have enough disk space before using this function!
    """
    files = get_mas_filenames(directory, var)

    for f in files:
        print(f"Processing {f}...")
        f = Path(f)
        data = _read_mas(f, var)
        new_dir = (f.parent / ".." / "netcdf").resolve()
        new_dir.mkdir(exist_ok=True)
        new_path = (new_dir / f.name).with_suffix(".nc")
        data.to_netcdf(new_path)
        del data


def get_mas_variables(path):
    """
    Return a list of variables present in a given directory.

    Parameters
    ----------
    path :
        Path to the folder containing the MAS data files.

    Returns
    -------
    var_names : list
        List of variable names present in the given directory.
    """
    files = glob.glob(str(path / "*[0-9][0-9][0-9].*"))
    # Get the variable name from the filename
    # Here we take the filename before .hdf, and remove the last three
    # characters which give the timestep
    var_names = [Path(f).stem.split(".")[0][:-3] for f in files]
    if not len(var_names):
        raise FileNotFoundError(f"No variable files found in {path}")
    # Use list(set()) to get unique values
    return list(set(var_names))


def get_timestep(path: os.PathLike) -> int:
    """
    Extract the timestep from a given MAS output filename.
    """
    fname = Path(path).stem
    for i, char in enumerate(fname):
        if char.isdigit():
            return int(fname[i:])

    raise RuntimeError(f"Failed to parse timestamp from {path}")
