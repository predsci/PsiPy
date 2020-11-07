"""
Tools for reading MAS (Magnetohydrodynamics on a sphere) model outputs.
"""
from pathlib import Path

import numpy as np

from .util import HDF4File


def read_hdf():
    fname = Path('data/corona/vr002.hdf')
    # Load the HDF4 file
    # In all PSI files the data is stored in "Data-Set-2"
    with HDF4File(fname) as sd_id:
        sds_id = sd_id.select('Data-Set-2')
        print(sds_id)

        # Get the scalar data
        f = sds_id.get()
        print(f.shape)
