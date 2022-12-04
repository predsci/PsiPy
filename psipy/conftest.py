"""
This file includes global test configuration.

In particular, it defines the location where test data is available.
"""
from pathlib import Path

import pytest
from pytest_cases import fixture, fixture_union

from psipy.data import sample_data
from psipy.model import mas, pluto

test_data_dir = (Path(__file__) / ".." / ".." / "data").resolve()


def get_mas_directory(filetype: str) -> Path:
    if filetype == "mas_helio":
        # Check for and download data if not present
        mas_directory = sample_data.mas_sample_data(sim_type="helio")
    elif filetype == "mas_high_res_thermo":
        mas_directory = sample_data.mas_high_res_thermo()
    else:
        # Directories with MAS outputs
        mas_directory = test_data_dir / filetype

    if not mas_directory.exists():
        pytest.xfail(f"Could not find MAS data directory at {mas_directory}")

    return mas_directory


def get_pluto_directory() -> Path:
    directory = sample_data.pluto_sample_data()
    if not directory.exists():
        pytest.xfail(f"Could not find PLUTO data directory at {directory}")
    return directory


@fixture(scope="module")
def pluto_directory():
    return get_pluto_directory()


@fixture(scope="module")
@pytest.mark.parametrize("filetype", ["mas_helio", "mas_hdf5", "mas_high_res_thermo"])
def mas_directory(filetype: str) -> Path:
    return get_mas_directory(filetype)


@fixture(scope="module")
@pytest.mark.parametrize("filetype", ["mas_helio", "mas_hdf5"])
def mas_model(filetype: str) -> mas.MASOutput:
    return mas.MASOutput(get_mas_directory(filetype))


@fixture(scope="module")
@pytest.mark.parametrize("filetype", ["mas_helio", "mas_hdf5", "mas_high_res_thermo"])
def all_mas_models(filetype: str) -> mas.MASOutput:
    """
    Same as mas_model above, but also includes a high resolution model
    with only 'rho' loaded.
    """
    return mas.MASOutput(get_mas_directory(filetype))


@fixture(scope="module")
def pluto_model():
    directory = sample_data.pluto_sample_data()
    if not directory.exists():
        pytest.xfail(f"Could not find PLUTO data directory at {directory}")

    return pluto.PLUTOOutput(get_pluto_directory())


fixture_union("model", [mas_model, pluto_model])


@fixture(scope="module")
def pot3d_directory() -> Path:
    return sample_data.pot3d_sample_data()
