import pytest

from psipy.model import Variable


def test_var_error(mas_model):
    with pytest.raises(RuntimeError, match='not in list of known variables'):
        mas_model['not_a_var']


def test_radial_normalised(mas_model):
    norm = mas_model['rho'].radial_normalized(-2)
    assert isinstance(norm, Variable)
