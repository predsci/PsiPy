"""
Tools for reading POT3D output files.
"""
import glob
from pathlib import Path

import numpy as np
import xarray as xr

from .util import read_hdf4

__all__ = ["get_pot3d_variables"]


def _read_pot3d(file_path: Path) -> xr.Dataset:
    """
    Read a single POT3D file.

    Parameters
    ----------
    path :
        Path to the file.
    """
    if not file_path.suffix == ".hdf":
        raise ValueError("File path must point ot a hdf file.")

    data, coords = read_hdf4(file_path.resolve())

    dims = ["phi", "theta", "r"]
    # Convert from co-latitude to latitude
    coords[1] = np.pi / 2 - np.array(coords[1])
    # Get variable name
    var = file_path.name.split(".")[0]
    # Add time
    data = xr.Dataset({var: xr.DataArray(data=data, coords=coords, dims=dims)})
    return data


def get_pot3d_variables(directory):
    """
    Return a list of variables present in a given directory.

    Parameters
    ----------
    directory :
        Path to the folder containing the POT3D data files.

    Returns
    -------
    var_names : list
        List of variable names present in the given directory.
    """
    files = glob.glob(str(Path(directory) / "*.hdf"))
    # Get the variable name from the filename
    var_names = [Path(f).stem for f in files]
    # Only return unique names
    var_names = list(set(var_names))
    if not len(var_names):
        raise FileNotFoundError(f"No variable files found in {directory}")
    var_names.sort()
    return var_names
