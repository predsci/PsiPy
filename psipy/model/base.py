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

    def __str__(self):
        return (f'{self.__class__.__name__}\n'
                f'Variables: {self.variables}')

    def __getitem__(self, var):
        if var not in self.variables:
            raise RuntimeError(f'{var} not in list of known variables: '
                               f'{self._variables}')
        if var not in self.loaded_variables:
            self._data[var] = self.load_file(var)

        # Get units
        try:
            unit, factor = self.get_unit(var)
        except Exception as e:
            raise RuntimeError('Do not know what units are for '
                               f'variable "{var}"') from e

        data = self._data[var] * factor
        return Variable(data, var, unit)

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
    def get_unit(self, var):
        """
        Return the units for a variable, and the factor needed to convert
        from the model output to those units.

        Returns
        -------
        unit : `astropy.units.Unit`
        factor : float
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
