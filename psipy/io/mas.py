"""
Tools for reading MAS (Magnetohydrodynamics on a sphere) model outputs.
"""
from pathlib import Path

import numpy as np
import xarray as xr

from .util import read_hdf


def read_mas_files(path):
    """
    Parameters
    ----------
    path :
        Path to the folder containing the MAS data files.
    """
    mas_path = Path(path)
    fpath = mas_path / 'vr002.hdf'
    data, coords = read_hdf(fpath)
    dims = ['phi', 'theta', 'r']
    data = xr.DataArray(data=data, coords=coords, dims=dims)
    return data
