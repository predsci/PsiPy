"""
Tools for reading POT3D output files.
"""
from pathlib import Path

import numpy as np
import xarray as xr

from .util import read_hdf4


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
