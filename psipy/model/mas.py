from pathlib import Path

from psipy.io import read_mas_files

__all__ = ['MASOutput']


class MASOutput:
    """
    The results from a single run of MAS.

    Parameters
    ----------
    path :
        Path to the directry containing the model output files.
    """
    def __init__(self, path):
        self.path = Path(path)
        self._data = read_mas_files(self.path)

    @property
    def vr(self):
        """
        Radial velocity.
        """
        return self._data['vr']

    @property
    def vt(self):
        """
        Transverse velocity.
        """
        return self._data['vt']

    @property
    def vn(self):
        """
        Normal velocity.
        """
        return self._data['vn']
