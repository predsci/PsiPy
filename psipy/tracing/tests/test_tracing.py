
import astropy.units as u

from psipy.data import sample_data
from psipy.model import MASOutput
from psipy.tracing import FortranTracer


def test_tracer(mas_model):
    # Simple smoke test of field line tracing
    mas_path = sample_data.mas_sample_data()
    model = MASOutput(mas_path)
    bs = model.cell_corner_b()
    # Fake data to be unit vectors pointing in radial direction
    bs.loc[..., 'bp'] = 0
    bs.loc[..., 'bt'] = 0
    bs.loc[..., 'br'] = 1

    def cell_corner_b(self):
        return bs

    model.cell_corner_b = cell_corner_b

    tracer = FortranTracer()

    r = 40
    lat = 0 * u.deg
    lon = 0 * u.deg

    flines = tracer.trace(model, lon=lon, lat=lat, r=r)
    assert len(flines) == 1

    # Check that with auto step size, number of steps is close to number of
    # radial coordinates
    assert len(bs.coords['r']) == 140
    assert flines[0].xyz.shape == (139, 3)

    tracer = FortranTracer(step_size=0.5)
    flines = tracer.trace(model, lon=lon, lat=lat, r=r)
    # Check that changing step size has an effect
    assert flines[0].xyz.shape == (278, 3)
