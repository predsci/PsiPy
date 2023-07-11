import pytest

from psipy.io import util


def test_HDF4_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        util.HDF4File(tmp_path / "not_a_file.hdf")
