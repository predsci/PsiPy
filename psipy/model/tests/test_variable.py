import astropy.constants as const
import astropy.units as u
import pytest

from psipy.model import Variable


def test_var_error(mas_model):
    with pytest.raises(RuntimeError, match='not in list of known variables'):
        mas_model['not_a_var']


def test_radial_normalised(mas_model):
    norm = mas_model['rho'].radial_normalized(-2)
    assert isinstance(norm, Variable)


# Check different shaped input, including lon/lat points that go up/down in
# value
@pytest.mark.parametrize(
    'lon, lat, r',
    [(1*u.deg, 1*u.deg, 30*const.R_sun),
     ([1, 2] * u.deg, [1, 2] * u.deg, [30, 31] * const.R_sun),
     ([1, 0] * u.deg, [1, 0] * u.deg, [30, 31] * const.R_sun),
     ])
def test_sample_at_coords(mas_model, lon, lat, r):
    # Check scalar coords
    rho = mas_model['rho'].sample_at_coords(lon=lon, lat=lat, r=r)
    assert rho.unit == mas_model['rho'].unit
    assert u.allclose(rho[0], [447.02795493] * u.cm**-3)
