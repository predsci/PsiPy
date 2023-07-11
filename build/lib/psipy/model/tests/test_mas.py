import astropy.units as u
import numpy as np
import xarray as xr

from psipy.model import base


def test_mas_model(mas_model):
    # Check that loading a single file works
    assert isinstance(mas_model, base.ModelOutput)
    assert "MAS output in directory" in str(mas_model)
    assert "rho" in str(mas_model)

    rho = mas_model["rho"]
    assert isinstance(rho, base.Variable)
    assert isinstance(rho.data, xr.DataArray)
    assert rho.unit == u.cm**-3
    assert rho.n_timesteps == 1
    assert (
        str(rho)
        == """
Variable
--------
Name: rho
Grid size: (128, 111, 141) (phi, theta, r)
Timesteps: 1
"""
    )


def test_persistance(mas_model):
    # Check that a variable requested twice only makes one copy of the data in
    # memory
    rho1 = mas_model["rho"]
    rho2 = mas_model["rho"]
    # This checks that rho1 and rho2 reference the same underlying data
    assert rho1 is rho2


def test_change_units(mas_model):
    # Check that loading a single file works
    rho = mas_model["rho"]
    assert rho.unit == u.cm**-3
    old_data = rho._data.copy()
    rho.unit = u.m**-3
    assert rho.unit == u.m**-3
    assert np.allclose(rho._data.values, 1e6 * old_data.values)
