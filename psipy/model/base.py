import abc
from pathlib import Path

from .variable import Variable


__all__ = ['ModelOutput']


class ModelOutput(abc.ABC):
    """
    The results from a single model run.

    This is a storage object that contains a number of `Variable` objects. It
    is not designed to be used directly, but must be sub-classed for different
    models.

    Notes
    -----
    Variables are loaded on demand. To see the list of available variables
    use `ModelOutput.variables`, and to see the list of already loaded variables
    use `ModelOutput.loaded_variables`.

    Parameters
    ----------
    path :
        Path to the directry containing the model output files.
    """
    def __init__(self, path):
        self.path = Path(path)
        # Leave data empty for now, as we want to load on demand
        self._data = {}
        self._variables = self.get_variables()

    def __getitem__(self, var):
        if var not in self.variables:
            raise RuntimeError(f'{var} not in list of known variables: '
                               f'{self._variables}')
        if var not in self.loaded_variables:
            self._data[var] = self.load_file(var)

        units = self.get_units()
        if var in units:
            unit = units[var][0]
            data = self._data[var] * units[var][1]
            return Variable(data, var, unit)
        else:
            raise RuntimeError('Do not know what units are for '
                               f'variable "{var}"')

    @abc.abstractmethod
    def get_variables(self):
        """
        Returns
        -------
        list :
            A list of all variable names present in the directory.
        """
        pass

    @abc.abstractmethod
    def load_file(self, var):
        """
        Load data for variable *var*.
        """
        pass

    @abc.abstractmethod
    def get_units(self):
        """
        Return a mapping from variable names to astropy units, and the
        conversion factor needed to go from the model output to those units.

        Returns
        -------
        list[`astropy.units.Unit`, float]
        """
        pass

    @property
    def loaded_variables(self):
        """
        List of loaded variable names.
        """
        return list(self._data.keys())

    @property
    def variables(self):
        """
        List of all variable names present in the directory.
        """
        return self._variables
