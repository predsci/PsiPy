"""
Tools for reading MAS (Magnetohydrodynamics on a sphere) model outputs.
"""
from pathlib import Path

import numpy as np
import xarray as xr

from .util import read_hdf


__all__ = ['read_mas_files']

# MAS variable names
# TODO: check if cs is always present?
_mas_vars = ['vr', 'vp', 'vt', 'va', 't', 'rho', 'p',
             'jt', 'jr', 'jp', 'br', 'bt', 'br']


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
    for var in _mas_vars:
        fpath = mas_path / f'{var}002.hdf'
        data, coords = read_hdf(fpath)
        dims = ['phi', 'theta', 'r']
        # Convert from co-latitude to latitude
        coords[1] = np.pi / 2 - np.array(coords[1])
        data = xr.DataArray(data=data, coords=coords, dims=dims)
        data_arrays[var] = data

    return data_arrays
