import astropy.constants as const
import astropy.units as u

from .base import ModelOutput
from psipy.io import read_pluto_files, get_pluto_variables

__all__ = ['PLUTOOutput']


class PLUTOOutput(ModelOutput):
    """
    The results from a single run of PLUTO.

    This is a storage object that contains a number of `Variable` objects. It
    is designed to be used like::

        pluto_output = PLUTOOutput('directory')
        br = pluto_output['br']

    Notes
    -----
    Variables are loaded on demand. To see the list of available variables
    use `PLUTOOutput.variables`, and to see the list of already loaded variables
    use `PLUTOOutput.loaded_variables`.
    """
    def get_unit(self, var):
        return u.dimensionless_unscaled, 1

    def get_variables(self):
        return get_pluto_variables(self.path)

    def load_file(self, var):
        return read_pluto_files(self.path, var)
