"""
Tools for reading MAS (Magnetohydrodynamics on a sphere) model outputs.
"""
import glob
from pathlib import Path

import numpy as np
import xarray as xr

from .util import read_hdf4, read_hdf5


__all__ = ['read_mas_files']


def read_mas_files(path):
    """
    Read in a full set of MAS output files.

    Parameters
    ----------
    path :
        Path to the folder containing the MAS data files.

    Returns
    -------
    data : dict
        A mapping from variable names to `xarray.DataArray`, containing all
        the variables from the MAS output.
    """
    mas_path = Path(path)
    data_arrays = {}
    # Loop through all the .hdf or .h5 files. They all end in three numbers,
    # so use this to distinguish from boundary condidtion hdf files
    for f in glob.glob(str(mas_path / '*[0-9][0-9][0-9].h*')):
        f = Path(f)
        if f.suffix == '.hdf':
            data, coords = read_hdf4(f)
        elif f.suffix == '.h5':
            data, coords = read_hdf5(f)

        dims = ['phi', 'theta', 'r']
        # Convert from co-latitude to latitude
        coords[1] = np.pi / 2 - np.array(coords[1])
        data = xr.DataArray(data=data, coords=coords, dims=dims)

        # Get the variable name from the filename
        # Here we take the filename before .hdf, and remove the last three
        # characters which give the timestep
        var = Path(f).stem.split('.h')[0][:-3]
        data_arrays[var] = data

    if not len(data_arrays):
        raise FileNotFoundError(f'Did not find any MAS files at {mas_path}')
    return data_arrays
