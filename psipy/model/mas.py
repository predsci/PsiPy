from pathlib import Path

from psipy.io import read_mas_files
from psipy.io.mas import _mas_vars

__all__ = ['MASOutput']


class MASOutput:
    """
    The results from a single run of MAS.

    Parameters
    ----------
    path :
        Path to the directry containing the model output files.

    Attributes
    ----------
    TODO: add description of attributes
    """
    def __init__(self, path):
        self.path = Path(path)
        self._data = read_mas_files(self.path)

    def __getattr__(self, attr):
        """
        Get an attribute. This allows one to do e.g. ``masoutput.vr`` to get
        the radial velocity.
        """
        if attr in _mas_vars:
            return self._data[attr]
        return super().__getattr__(attr)
