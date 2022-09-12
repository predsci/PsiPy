"""
This file includes global test configuration.

In particular, it defines the location where test data is available.
"""
from pathlib import Path

import pytest

from psipy.data import sample_data
from psipy.model import mas, pluto

test_data_dir = (Path(__file__) / ".." / ".." / "data").resolve()


@pytest.fixture(scope="module", params=["mas_helio", "mas_hdf5"])
def mas_directory(request):
    if request.param == "mas_helio":
        # Check for and download data if not present
        directory = sample_data.mas_sample_data(type="helio")
    else:
        # Directories with MAS outputs
        directory = test_data_dir / request.param
    if not directory.exists():
        pytest.xfail(f"Could not find MAS data directory at {directory}")

    return directory


@pytest.fixture(scope="module")
def mas_model(mas_directory):
    return mas.MASOutput(mas_directory)


@pytest.fixture(scope="module")
def pluto_directory():
    directory = sample_data.pluto_sample_data()
    if not directory.exists():
        pytest.xfail(f"Could not find PLUTO data directory at {directory}")

    return directory


@pytest.fixture(scope="module")
def pluto_model(pluto_directory):
    return pluto.PLUTOOutput(pluto_directory)
