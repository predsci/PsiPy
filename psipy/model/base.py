import abc
from pathlib import Path

from .variable import Variable


__all__ = ['ModelOutput']


class ModelOutput(abc.ABC):
    """
    An abstract base class to store the output from a single run of a model.

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

        if var in self._units:
            unit = self._units[var][0]
            data = self._data[var] * self._units[var][1]
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
