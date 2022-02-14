import numpy as np

from psipy.data import sample_data
from psipy.model import MASOutput
from psipy.tracing import FortranTracer


def test_tracer():
    # Simple smoke test of field line tracing
    mas_path = sample_data.mas_sample_data()
    model = MASOutput(mas_path)

    tracer = FortranTracer()

    nseeds = 15
    r0 = 40.
    lat = np.linspace(-np.pi / 5, np.pi / 5, nseeds**2, endpoint=False)
    lon = np.random.rand(nseeds**2) * 2 * np.pi
    r = np.ones(nseeds**2) * r0

    seeds = np.column_stack([lon, lat, r])
    xs = tracer.trace(model, seeds)

    assert isinstance(xs, list)
    assert isinstance(xs[0], np.ndarray)
    assert xs[0].shape == (301, 3)
