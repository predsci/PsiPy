import xarray as xr

from psipy.io.pot3d import _read_pot3d, get_pot3d_variables


def test_read_pot3d(pot3d_directory):
    ds = _read_pot3d(pot3d_directory / "br.hdf")
    assert isinstance(ds, xr.Dataset)


def test_get_var_names(pot3d_directory):
    assert get_pot3d_variables(pot3d_directory) == ["bp", "br", "bt"]
