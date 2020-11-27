import abc
from pathlib import Path


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

    @abc.abstractmethod
    def get_variables(self):
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
