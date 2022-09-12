from psipy.data import sample_data
from psipy.model import MASOutput


def test_helio_timestamps():
    # Check that helio sample data has > 1 timesteps
    mas_path = sample_data.mas_helio_timesteps()
    model = MASOutput(mas_path)
    vr = model["vr"]
    assert vr.n_timesteps > 1
