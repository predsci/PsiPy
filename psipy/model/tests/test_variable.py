from psipy.model import Variable


def test_radial_normalised(mas_model):
    norm = mas_model['rho'].radial_normalized(-2)
    assert isinstance(norm, Variable)
