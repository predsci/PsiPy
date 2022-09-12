import xarray as xr

from psipy.io import pluto


def test_read_pluto_files(pluto_directory):
    # Check that loading a single file works
    data = pluto.read_pluto_files(pluto_directory, "rho")
    assert isinstance(data, xr.Dataset)
