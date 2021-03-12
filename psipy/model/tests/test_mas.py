import astropy.units as u
import numpy as np
import pytest
import xarray as xr

from psipy.model import base, mas


def test_mas_model(mas_directory):
    # Check that loading a single file works
    mas_model = mas.MASOutput(mas_directory)
    assert isinstance(mas_model, base.ModelOutput)

    rho = mas_model['rho']
    assert isinstance(rho, base.Variable)
    assert isinstance(rho.data, xr.DataArray)
    assert rho.unit == u.N / u.cm**3


def test_change_units(mas_directory):
    # Check that loading a single file works
    mas_model = mas.MASOutput(mas_directory)
    rho = mas_model['rho']
    assert rho.unit == u.N / u.cm**3
    old_data = rho._data.copy()
    rho.unit = u.N / u.m**3
    assert rho.unit == u.N / u.m**3
    assert np.allclose(rho._data.values, 1e6 * old_data.values)
