import astropy.units as u
import xarray as xr

from psipy.model import base


def test_pluto_model(pluto_model):
    # Check that loading a single file works
    assert isinstance(pluto_model, base.ModelOutput)
    assert "PLUTOOutput" in str(pluto_model)
    assert pluto_model.variables == ["rho"]
    assert "rho" in str(pluto_model)

    rho = pluto_model["rho"]
    assert isinstance(rho, base.Variable)
    assert isinstance(rho.data, xr.DataArray)
    assert rho.unit == u.dimensionless_unscaled
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
