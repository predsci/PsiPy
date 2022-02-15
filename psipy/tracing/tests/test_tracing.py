
from psipy.data import sample_data
from psipy.model import MASOutput
from psipy.tracing import FortranTracer


def test_step_size():
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
    lat = 0
    lon = 0

    xs = tracer.trace(model, [lon, lat, r])
    assert len(xs) == 1

    # Check that with auto step size, number of steps is close to number of
    # radial coordinates
    assert len(bs.coords['r']) == 140
    assert xs[0].shape == (141, 3)

    tracer = FortranTracer(step_size=0.5)
    xs = tracer.trace(model, [lon, lat, r])
    # Check that changing step size has an effect
    assert xs[0].shape == (280, 3)
