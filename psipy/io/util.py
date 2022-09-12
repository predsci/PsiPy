import os

import h5py as h5
import numpy as np
import pyhdf.SD as h4

__all__ = ["read_hdf4", "read_hdf5"]


class HDF4File:
    """
    A context manager for automatically opening/closing HDF4 files
    """

    def __init__(self, file_name):
        file_name = str(file_name)
        if not os.path.exists(file_name):
            raise FileNotFoundError(f"Could not find {file_name}")
        self.file_obj = h4.SD(file_name)

    def __enter__(self):
        return self.file_obj

    def __exit__(self, type, value, traceback):
        self.file_obj.end()


def read_hdf4(path, sds_id="Data-Set-2"):
    """
    Read a HDF4 file.

    Reads a single dataset from a single HDF4 file, returning the scalar data
    and associated coordinates.

    Parameters
    ----------
    path :
        Path to the file.
    sds_id : str, optional
        ID of the dataset to get.

    Returns
    -------
    data : ndarray
        Scalar data.
    coords : list of ndarray
        Cooordinates values along each axis of the data.
    """
    # Load the HDF4 file
    # In all PSI files the data is stored in "Data-Set-2"
    with HDF4File(path) as sd_id:
        sds_id = sd_id.select("Data-Set-2")

        # Get the scalar data
        data = sds_id.get()
        # Get coordinate information
        coords = [sds_id.dim(i).getscale() for i in range(np.ndim(data))]

    return data, coords


def read_hdf5(path, dataset_name="Data"):
    """
    Read a HDF5 file.

    Reads a single dataset from a single HDF5 file, returning the scalar data
    and associated coordinates.

    Parameters
    ----------
    path :
        Path to the file.
    dataset_name : str, optional
        ID of the dataset to get.

    Returns
    -------
    data : ndarray
        Scalar data.
    coords : list of ndarray
        Cooordinates values along each axis of the data.
    """
    with h5.File(path, "r") as hdf5_file:
        # Get the scalar data
        data = np.array(hdf5_file[dataset_name])
        # Get coordinate information
        coords = [
            np.array(hdf5_file[dataset_name].dims[i][0]) for i in range(np.ndim(data))
        ]
        coords = coords[::-1]

    return data, coords
