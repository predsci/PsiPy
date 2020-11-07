"""
Tools for reading MAS (Magnetohydrodynamics on a sphere) model outputs.
"""
from pathlib import Path

import numpy as np
import xarray as xr

from .util import read_hdf


# A mapping from the MAS filenames to the names they are given within the
# data array
_mas_files = ['vr', 'vp', 'vt']


def read_mas_files(path):
    """
    Parameters
    ----------
    path :
        Path to the folder containing the MAS data files.

    Returns
    -------
    data : xarray.DataArray
    """
    mas_path = Path(path)
    data_arrays = {}
    for var in _mas_files:
        fpath = mas_path / f'{var}002.hdf'
        data, coords = read_hdf(fpath)
        dims = ['phi', 'theta', 'r']
        data = xr.DataArray(data=data, coords=coords, dims=dims)
        data_arrays[var] = data

    return data_arrays
