"""
Tools for reading pluto model outputs.
"""
import glob
from pathlib import Path

import numpy as np
import xarray as xr

__all__ = ["read_pluto_files", "get_pluto_variables", "read_pluto_grid"]


def get_timestep(path):
    """
    Get the timestep from a filename.
    """
    path = Path(path)
    fname = path.stem
    tstep = fname.split(".")[-1]
    return int(tstep)


def read_pluto_files(directory, var):
    """
    Read in a single variable from a set of PLUTO output files.

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
    directory = Path(directory)
    files = glob.glob(str(directory / f"{var}*.dbl"))
    if not len(files):
        raise FileNotFoundError(
            f'Could not find any files for variable "{var}" in '
            f"directory {directory}"
        )
    files.sort()
    all_data = []
    times = []
    for file in files:
        times.append(get_timestep(file))
        data, grid = read_pluto_dbl(file)
        all_data.append(data)

    # Take grid centers as the grid points
    coords = [np.mean(g, axis=1) for g in grid]
    # Convert from co-latitude to latitude
    coords[1] = np.pi / 2 - np.array(coords[1])
    coords = [times] + coords

    dims = ["time", "phi", "theta", "r"]
    return xr.Dataset({var: xr.DataArray(data=all_data, coords=coords, dims=dims)})


def read_pluto_grid(path):
    """
    Read in a single PLUTO grid file.

    Parameters
    ----------
    path :
        Path to the ``grid.out`` file.

    Returns
    -------
    dim1, dim2, dim3 : numpy.ndarray
        Coordinate values along each dimension. These are (n, 2) shaped arrays,
        with the two columns being the minimum and maximum coordinate values
        of a given cell.
    """
    with open(path, "r") as f:
        lines = f.readlines()
    n_header_lines = np.sum([line[0] == "#" for line in lines])
    # Read size of dimensions
    n_dim_1 = int(lines[n_header_lines].split("\n")[0])
    n_dim_2 = int(lines[n_header_lines + n_dim_1 + 1].split("\n")[0])
    n_dim_3 = int(lines[n_header_lines + n_dim_1 + n_dim_2 + 2].split("\n")[0])

    # Read in coordinate values
    dim_1 = np.loadtxt(path, skiprows=n_header_lines + 1, max_rows=n_dim_1)
    dim_2 = np.loadtxt(path, skiprows=n_header_lines + n_dim_1 + 2, max_rows=n_dim_2)
    dim_3 = np.loadtxt(
        path, skiprows=n_header_lines + n_dim_1 + n_dim_2 + 3, max_rows=n_dim_3
    )
    return dim_1[:, 1:], dim_2[:, 1:], dim_3[:, 1:]


def read_pluto_dbl(path):
    """
    Read in a single PLUTO output file.

    Parameters
    ----------
    path :
        Path to the dbl file.

    Returns
    -------
    data : numpy.ndarray
        3D array of data values
    grid : list
        Each item is a (n, 2) shaped array of the min/max limits of the cells
        in each coordinate.

    Notes
    -----
    There must be a ``grid.out`` file present in the same directory as the file
    being read.
    """
    path = Path(path)
    data = np.fromfile(path, np.float64)
    grid = read_pluto_grid(path.parent / "grid.out")

    grid = grid[::-1]
    grid_dims = list(g.shape[0] for g in grid)
    data = data.reshape(grid_dims)

    return data, grid


def get_pluto_variables(directory):
    """
    Return a list of variables present in a given directory.

    Parameters
    ----------
    directory :
        Path to the folder containing the PLUTO data files.

    Returns
    -------
    var_names : list
        List of variable names present in the given directory.
    """
    files = glob.glob(str(Path(directory) / "*.dbl"))
    # Get the variable name from the filename
    # Take anything before the . in the first three characters
    var_names = [Path(f).stem[:3].split(".")[0] for f in files]
    # Only return unique names
    var_names = list(set(var_names))
    if not len(var_names):
        raise FileNotFoundError(f"No variable files found in {directory}")
    var_names.sort()
    return var_names
