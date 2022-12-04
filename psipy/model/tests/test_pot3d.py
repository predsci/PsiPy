from psipy.model import ModelOutput, POT3DOutput


def test_pot3d_model(pot3d_directory):
    model = POT3DOutput(pot3d_directory)
    # Check that loading a single file works
    assert isinstance(model, ModelOutput)
    assert "POT3D" in str(model)
    assert model.variables == ["bp", "br", "bt"]
    assert "bp" in str(model)

    '''
    rho = model["bp"]
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
    '''
