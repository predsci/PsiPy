"""
Helper functions for downloading sample model output data.
"""
import shutil
from pathlib import Path
from typing import Dict

import pooch

__all__ = ["mas_sample_data", "mas_helio_timesteps"]


file_url = "cr{cr}-{resolution}/hmi_mas{thermo}_mas_std_0201/{sim_type}/{var}002.hdf"
cache_dir = pooch.os_cache("psipy")


def _get_url(
    *,
    sim_type: str,
    var: str,
    cr: int = 2210,
    thermo: str = "poly",
    resolution: str = "medium",
) -> str:
    """
    Get the URL to a MAS dataset with a given
    - simulation type ('corona' or 'helio')
    - simulation variable (e.g. magnetic field, density)
    - carrington rotation
    - thermodynamic model ('poly' or 'thermo')
    - simulation resolution
    """
    if thermo == "poly":
        thermo = "p"
    elif thermo == "thermo":
        thermo = "t"
    else:
        raise ValueError('thermo must be one of ["poly", "thermo"]')
    return file_url.format(
        cr=cr, sim_type=sim_type, var=var, thermo=thermo, resolution=resolution
    )


registry: Dict[str, None] = {}

# Add consecutive Carrington rotation sample data
for cr in [2210, 2211]:
    registry[_get_url(cr=cr, sim_type="helio", var="vr")] = None


# Add various variables for helio and corona solutions
sim_vars = ["rho", "vr", "br", "bt", "bp"]
sim_types = ["helio", "corona"]
for sim_type in sim_types:
    for var in sim_vars:
        registry[_get_url(cr=2210, sim_type=sim_type, var=var)] = None

# Add high res entry
registry[
    _get_url(
        cr=2250,
        sim_type="corona",
        var="rho",
        resolution="high",
        thermo="thermo",
    )
] = None
mas_pooch = pooch.create(
    path=cache_dir,
    base_url="https://www.predsci.com/data/runs/",
    registry=registry,
)

# Add some PLUTO data
pluto_reg: Dict[str, None] = {}
PLUTO_FILES = [
    "grid.out",
    "dbl.out",
    "rho.0000.dbl",
    "Bx1.0000.dbl",
    "Bx2.0000.dbl",
    "Bx3.0000.dbl",
]
for file in PLUTO_FILES:
    pluto_reg[file] = None

pluto_pooch = pooch.create(
    path=cache_dir,
    base_url="doi:10.6084/m9.figshare.19401089.v1/",
    registry=pluto_reg,
)


def mas_sample_data(sim_type="helio"):
    """
    Get some MAS data files. These are taken from CR2210, which
    is used for PSP data comparisons in the documentation examples.

    Parameters
    ----------
    sim_type : {'helio', 'corona'}

    Returns
    -------
    pathlib.Path
        Download directory.
    """
    for var in sim_vars:
        path = mas_pooch.fetch(
            _get_url(cr=2210, sim_type=sim_type, var=var), progressbar=True
        )
    return Path(path).parent


def mas_helio_timesteps() -> Path:
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
        mas_pooch.fetch(_get_url(cr=cr, sim_type="helio", var="vr"), progressbar=True)
        for cr in [2210, 2211]
    ]
    paths = [Path(p) for p in paths]

    helio_dir = cache_dir / "carrington"
    helio_dir.mkdir(exist_ok=True)
    for i, path in enumerate(paths):
        shutil.copy(path, helio_dir / f"vr00{i+1}.hdf")

    return helio_dir


def mas_high_res_thermo() -> Path:
    """
    Get a single MAS high resolution thermodynamic simulation.

    Returns
    -------
    pathlib.Path
        Download directory.
    """
    path = mas_pooch.fetch(
        _get_url(
            cr=2250,
            sim_type="corona",
            var="rho",
            resolution="high",
            thermo="thermo",
        ),
        progressbar=True,
    )
    high_res_dir = cache_dir / "high_res"
    high_res_dir.mkdir(exist_ok=True)
    shutil.copy(path, high_res_dir)

    return high_res_dir


def pluto_sample_data() -> Path:
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
