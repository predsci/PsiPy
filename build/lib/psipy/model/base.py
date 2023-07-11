import abc
import os
from pathlib import Path
from typing import List, Optional, Tuple

import astropy.units as u
import xarray as xr

from .variable import Variable

__all__ = ["ModelOutput"]


class ModelOutput(abc.ABC):
    r"""
    The results from a single model run.

    This is a storage object that contains a number of `Variable` objects. It
    is not designed to be used directly, but must be sub-classed for different
    models.

    Data is stored in the ``_data`` attribute. This is a mapping of variable
    names to `xarray.DataArray` variables. Each data array must have

    - Four dimensions
    - These dimensions must be labelled ``['r', 'theta', 'phi', 'time']``
    - The phi values must be latitude and *not* co-latitude (ie. must be in
      the range :math:`[-\pi / 2, \pi / 2]`)
    - The theta values must be in the range :math:`[0, 2\pi]`

    Notes
    -----
    Variables are loaded on demand. To see the list of available variables
    use `ModelOutput.variables`, and to see the list of already loaded variables
    use `ModelOutput.loaded_variables`.

    Parameters
    ----------
    path :
        Path to the directory containing the model output files.
    """

    def __init__(self, path: os.PathLike):
        self.path = Path(path)
        # Leave data empty for now, as we want to load on demand
        self._data: dict[str, xr.Dataset] = {}
        self._variables = self.get_variables()
        self._variables.sort()

    def __str__(self):
        return f"{self.__class__.__name__}\n" f"Variables: {self.variables}"

    def __getitem__(self, var: str):
        """
        Get a single variable.
        """
        if var not in self.variables:
            raise RuntimeError(
                f"{var} not in list of known variables: " f"{self._variables}"
            )
        if var in self.loaded_variables:
            # Already loaded
            return self._data[var]

        data = self.load_file(var)

        # Get units
        try:
            unit, factor = self.get_unit(var)
        except Exception as e:
            raise RuntimeError(
                "Do not know what units are for " f'variable "{var}"'
            ) from e
        data *= factor

        runit = self.get_runit()
        # Save a reference on this ModelOutput object
        self._data[var] = Variable(data, var, unit, runit)
        return self._data[var]

    # Abstract methods start here
    #
    # These are methods that must be defined by classes that inherit from this
    # class
    @abc.abstractmethod
    def get_variables(self) -> List[str]:
        """
        Returns
        -------
        list :
            A list of all variable names present in the directory.
        """

    @abc.abstractmethod
    def load_file(self, var):
        """
        Load data for variable *var*.
        """

    @abc.abstractmethod
    def get_unit(self, var) -> Tuple[u.Unit, float]:
        """
        Return the units for a variable, and the factor needed to convert
        from the model output to those units.

        Returns
        -------
        unit : `astropy.units.Unit`
        factor : float
        """

    @abc.abstractmethod
    def get_runit(self) -> u.Unit:
        """
        Return the units for the radial coordinate.
        """

    @abc.abstractmethod
    def cell_corner_b(self, t_idx: Optional[int] = None) -> xr.DataArray:
        """
        Get the magnetic field vector at the cell corners.

        Parameters
        ----------
        t_idx : int, optional
            If more than one timestep is present in the loaded model, a
            timestep index at which to get the vectors must be provided.

        Returns
        -------
        xarray.DataArray

        Notes
        -----
        The phi limits go from 0 to 2pi inclusive, with the vectors at phi=0
        equal to the vectors at phi=2pi.
        """

    # Properties start here
    @property
    def loaded_variables(self) -> List[str]:
        """
        List of loaded variable names.
        """
        return list(self._data.keys())

    @property
    def variables(self) -> List[str]:
        """
        List of all variable names present in the directory.
        """
        return self._variables
