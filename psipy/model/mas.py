from pathlib import Path

from psipy.io import read_mas_files

__all__ = ['MASOutput']


class MASOutput:
    def __init__(self, path):
        self.path = Path(path)
        self._data = read_mas_files(self.path)
