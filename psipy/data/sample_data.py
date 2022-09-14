"""
Helper functions for downloading sample model output data.
"""
import shutil
from pathlib import Path
from typing import Dict

import pooch

__all__ = ["mas_sample_data", "mas_helio_timesteps"]


file_url = "cr{cr}-medium/hmi_masp_mas_std_0201/{type}/{var}002.hdf"
cache_dir = pooch.os_cache("psipy")


def _get_url(*, type: str, var: str, cr: int = 2210) -> str:
    return file_url.format(cr=cr, type=type, var=var)


registry: Dict[str, None] = {}

# Add consecutive Carrington rotation sample data
for cr in [2210, 2211]:
    registry[_get_url(cr=cr, type="helio", var="vr")] = None


# Add various variables for helio and corona solutions
vars = ["rho", "vr", "br", "bt", "bp"]
for type in ["helio", "corona"]:
    for var in vars:
        registry[_get_url(cr=2210, type=type, var=var)] = None

mas_pooch = pooch.create(
    path=cache_dir,
    base_url="https://www.predsci.com/data/runs/",
    registry=registry,
)

# Add some PLUTO data
pluto_reg: Dict[str, None] = {}
PLUTO_FILES = ["grid.out", "dbl.out", "rho.0000.dbl"]
for file in PLUTO_FILES:
    pluto_reg[file] = None

pluto_pooch = pooch.create(
    path=cache_dir,
    base_url="doi:10.6084/m9.figshare.19401089.v1/",
    registry=pluto_reg,
)


def mas_sample_data(type="helio"):
    """
    Get some MAS data files. These are taken from CR2210, which
    is used for PSP data comparisons in the documentation examples.

    Parameters
    ----------
    type : {'helio', 'corona'}

    Returns
    -------
    pathlib.Path
        Download directory.
    """
    for var in vars:
        path = mas_pooch.fetch(_get_url(cr=2210, type=type, var=var), progressbar=True)
    return Path(path).parent


def mas_helio_timesteps():
    """
    Get two MAS heliospheric data files for two subsequent Carrington
    rotations.

    This is used as sample data for animations - animations are intended to be
    used with output from time dependent simulations, but for ease of
    downloading sample data here we pretend that two Carrington rotations are
    time animations.

    Returns
    -------
    pathlib.Path
        Download directory.
    """
    paths = [
        mas_pooch.fetch(_get_url(cr=cr, type="helio", var="vr"), progressbar=True)
        for cr in [2210, 2211]
    ]
    paths = [Path(p) for p in paths]

    helio_dir = cache_dir / "carrington"
    helio_dir.mkdir(exist_ok=True)
    for i, path in enumerate(paths):
        shutil.copy(path, helio_dir / f"vr00{i+1}.hdf")

    return helio_dir


def pluto_sample_data():
    """
    Get some sample PLUTO data.

    Returns
    -------
    pathlib.Path
        Download directory.
    """
    for file in PLUTO_FILES:
        path = pluto_pooch.fetch(file, progressbar=True)

    return Path(path).parent
