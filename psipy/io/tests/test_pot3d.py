import xarray as xr

from psipy.io.pot3d import _read_pot3d


def test_read_pot3d(pot3d_directory):
    ds = _read_pot3d(pot3d_directory / "br.hdf")
    assert isinstance(ds, xr.Dataset)
