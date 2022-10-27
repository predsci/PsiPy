import astropy.units as u
import numpy as np

from psipy.data import sample_data
from psipy.model import MASOutput, PLUTOOutput
from psipy.tracing import FieldLines, FortranTracer


def test_tracer(model):
    # Simple smoke test of field line tracing
    bs = model.cell_corner_b()
    # Fake data to be unit vectors pointing in radial direction
    bs.loc[..., "bp"] = 0
    bs.loc[..., "bt"] = 0
    bs.loc[..., "br"] = 1

    def cell_corner_b(self):
        return bs

    model.cell_corner_b = cell_corner_b

    tracer = FortranTracer()

    r = 40 * u.R_sun
    lat = 0 * u.deg
    lon = 0 * u.deg

    flines = tracer.trace(model, lon=lon, lat=lat, r=r)
    assert len(flines) == 1

    # Check that with auto step size, number of steps is close to number of
    # radial coordinates
    if isinstance(model, MASOutput):
        assert len(bs.coords["r"]) == 140
        assert flines[0].xyz.shape == (139, 3)
    elif isinstance(model, PLUTOOutput):
        assert len(bs.coords["r"]) == 141
        assert flines[0].xyz.shape == (139, 3)

    tracer = FortranTracer(step_size=0.5)
    flines = tracer.trace(model, lon=lon, lat=lat, r=r)
    # Check that changing step size has an effect
    assert flines[0].xyz.shape == (278, 3)


def test_fline_io(model, tmpdir):
    # Test saving and loading field lines
    tracer = FortranTracer()

    r = 40 * u.R_sun
    lat = 0 * u.deg
    lon = 0 * u.deg

    flines = tracer.trace(model, lon=lon, lat=lat, r=r)
    fline_0 = flines[0]
    flines.save(tmpdir / "flines.npz")
    del flines

    loaded_flines = FieldLines.load(tmpdir / "flines.npz")
    fline_1 = loaded_flines[0]

    np.testing.assert_allclose(fline_0.r, fline_1.r)
    np.testing.assert_allclose(fline_0.lon, fline_1.lon)
    np.testing.assert_allclose(fline_0.lat, fline_1.lat)
