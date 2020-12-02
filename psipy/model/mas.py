import astropy.constants as const
import astropy.units as u

from .base import ModelOutput
from psipy.io import read_mas_file, get_mas_variables

__all__ = ['MASOutput']


# A mapping from unit names to their units, and factors the data needs to be
# multiplied to get them into these units.
_vunit = [u.km / u.s, 481.37]
_bunit = [u.G, 2.205]
_junit = [u.A / u.m**2, 2.267e4]
_mas_units = {'vr': _vunit,
              'vt': _vunit,
              'vp': _vunit,
              'va': _vunit,
              'br': _bunit,
              'bt': _bunit,
              'bp': _bunit,
              'bmag': _bunit,
              'rho': [u.N / u.cm**3, 1.67e-16 / 1.67e-24],
              't': [u.K, 2.804e7],
              'p': [u.Pa, 3.875717e-2],
              'jr': _junit,
              'jt': _junit,
              'jp': _junit
              }


class MASOutput(ModelOutput):
    """
    The results from a single run of MAS.

    This is a storage object that contains a number of `Variable` objects. It
    is designed to be used like::

        mas_output = MASOutput('directory')
        br = mas_output['br']

    Notes
    -----
    Variables are loaded on demand. To see the list of available variables
    use `MASOutput.variables`, and to see the list of already loaded variables
    use `MASOutput.loaded_variables`.
    """
    def get_unit(self, var):
        return _mas_units[var]

    def get_variables(self):
        return get_mas_variables(self.path)

    def load_file(self, var):
        return read_mas_file(self.path, var)

    def __repr__(self):
        return f'psipy.model.mas.MASOutput("{self.path}")'

    def __str__(self):
        return f"MAS output in directory {self.path}"
