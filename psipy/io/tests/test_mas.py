import pytest
import xarray as xr

from psipy.io import mas


def test_read_mas_file(mas_directory):
    # Check that loading a single file works
    data = mas.read_mas_file(mas_directory, 'rho')
    assert isinstance(data, xr.DataArray)
