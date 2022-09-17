import astropy.units as u
import numpy as np
import pytest

from psipy.model import Variable


def test_var_error(mas_model):
    with pytest.raises(RuntimeError, match="not in list of known variables"):
        mas_model["not_a_var"]


def test_radial_normalised(mas_model):
    norm = mas_model["rho"].radial_normalized(-2)
    assert isinstance(norm, Variable)


# Check different shaped input, including lon/lat points that go up/down in
# value
@pytest.mark.parametrize(
    "lon, lat, r",
    [
        (1 * u.deg, 1 * u.deg, 30 * u.R_sun),
        ([1, 2] * u.deg, [1, 2] * u.deg, [30, 31] * u.R_sun),
        ([1, 0] * u.deg, [1, 0] * u.deg, [30, 31] * u.R_sun),
    ],
)
def test_sample_at_coords_mas(mas_model, lon, lat, r):
    # Check scalar coords
    rho = mas_model["rho"].sample_at_coords(lon=lon, lat=lat, r=r)
    assert rho.unit == mas_model["rho"].unit
    assert u.allclose(rho[0], [447.02795493] * u.cm**-3)


@pytest.mark.parametrize(
    "lon, lat, r",
    [
        (1 * u.deg, 1 * u.deg, 1 * u.AU),
        ([1, 2] * u.deg, [1, 2] * u.deg, [1, 1.01] * u.AU),
        ([1, 0] * u.deg, [1, 0] * u.deg, [1, 1.01] * u.AU),
    ],
)
def test_sample_at_coords_pluto(pluto_model, lon, lat, r):
    # Check scalar coords
    rho = pluto_model["rho"].sample_at_coords(lon=lon, lat=lat, r=r)
    assert rho.unit == pluto_model["rho"].unit
    assert u.allclose(rho[0], [13.50442343])


def test_sample_out_of_bounds(pluto_model):
    lon = [0, 0, 0] * u.deg
    lat = [0, 0, 0] * u.deg
    rho = pluto_model["rho"]
    # Check point below bounds, in bounds, above bounds
    r = [0, 0.5, 2] * u.AU
    assert r[0] < rho.r_coords[0]
    assert rho.r_coords[0] < r[1] < rho.r_coords[-1]
    assert rho.r_coords[-1] < r[2]
    # Check scalar coords
    with pytest.warns(UserWarning, match="outside bounds"):
        samples = rho.sample_at_coords(lon=lon, lat=lat, r=r)
    assert np.isnan(samples[0])
    assert not np.isnan(samples[1])
    assert np.isnan(samples[2])
