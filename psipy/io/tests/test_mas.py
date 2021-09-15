import pytest
import xarray as xr

from psipy.io import mas
from psipy.model import MASOutput


def test_read_mas_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        mas.read_mas_file(tmp_path, 'rho')

    with pytest.raises(FileNotFoundError):
        mas.get_mas_variables(tmp_path)


def test_read_mas_file(mas_directory):
    # Check that loading a single file works
    data = mas.read_mas_file(mas_directory, 'rho')
    assert isinstance(data, xr.Dataset)
    assert 'rho' in data


def test_save_netcdf(mas_directory):
    # Check that converting to netcdf works
    mas.convert_hdf_to_netcdf(mas_directory, 'rho')
    netcdf_dir = mas_directory / '..' / 'netcdf'

    netcdf_model = MASOutput(netcdf_dir)
    hdf_model = MASOutput(mas_directory)
    assert netcdf_model._data == hdf_model._data
