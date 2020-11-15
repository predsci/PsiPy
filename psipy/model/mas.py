import copy
from pathlib import Path

import astropy.units as u
import numpy as np

from psipy.io import read_mas_files
import psipy.visualization as viz

__all__ = ['MASOutput', 'Variable']


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
              'rho': [u.cm**-3, 1.67e-16 / 1.67e-24],
              't': [u.K, 2.804e7],
              'p': [u.Pa, 3.875717e-2],
              'jr': _junit,
              'jt': _junit,
              'jp': _junit
              }


class MASOutput:
    """
    The results from a single run of MAS.

    This is a storage object that contains a number of `Variable` objects.

    Parameters
    ----------
    path :
        Path to the directry containing the model output files.
    """
    def __init__(self, path):
        self.path = Path(path)
        self._data = read_mas_files(self.path)
        # TODO: add __str__, __repr__

    def __getitem__(self, var):
        if var in _mas_units:
            unit = _mas_units[var][0]
            data = self._data[var] * _mas_units[var][1]
            return Variable(data, var, unit)
        else:
            raise RuntimeError('Do not know what units are for '
                               f'variable "{var}"')

    @property
    def variables(self):
        """
        List of variable names.
        """
        return list(self._data.keys())


class Variable:
    """
    A single scalar variable.

    This class primarily contains methods for plotting data. It can be created
    with any `~xarray.DataArray` that has ``['theta', 'phi', 'r']`` fields.

    Parameters
    ----------
    data : xarray.DataArray
        Variable data.
    name : str
        Variable name.
    unit : astropy.units.Quantity
        Variable unit.
    """
    def __init__(self, data, name, unit):
        self.data = data
        self.name = name
        self._unit = unit

    def __mul__(self, other):
        if not isinstance(other, Variable):
            raise ValueError('Can only multiply a Variable with another Variable')
        data = self.data * other.data
        name = f'{self.name} x {other.name}'
        unit = self.unit * other.unit
        return Variable(data, name, unit)

    @property
    def unit(self):
        """
        Units of the scalar data.
        """
        return self._unit

    def plot_radial_cut(self, i, ax=None, **kwargs):
        """
        Plot a radial cut.

        Parameters
        ----------
        i : int
            Index at which to slice the data.
        ax : matplolit.axes.Axes, optional
            axes on which to plot. Defaults to current axes if not specified.
        kwargs :
            Additional keyword arguments are passed to `xarray.plot.pcolormesh`.
        """
        if ax is None:
            ax = plt.gca()

        self._set_cbar_label(kwargs, str(self.unit))
        # Take slice of data, and plot
        sliced = self.data.isel(r=i)
        sliced.plot(x='phi', y='theta', ax=ax, **kwargs)

        # Plot formatting
        ax.set_aspect('equal')
        r = sliced['r'].values
        ax.set_title(f'{self.name}, r={r:.2f}' + r'$R_{\odot}$')
        ax.set_xlim(0, 2 * np.pi)
        ax.set_ylim(-np.pi / 2, np.pi / 2)
        viz.clear_axes_labels(ax)

        # Tick label formatting
        viz.set_theta_formatters(ax)
        ax.set_xticks(np.deg2rad(np.linspace(0, 360, 7, endpoint=True)))
        ax.set_yticks(np.deg2rad(np.linspace(-90, 90, 7, endpoint=True)))

    def plot_phi_cut(self, i, ax=None, **kwargs):
        """
        Plot a phi cut.

        Parameters
        ----------
        i : int
            Index at which to slice the data.
        ax : matplolit.axes.Axes, optional
            axes on which to plot. Defaults to current axes if not specified.
        kwargs :
            Additional keyword arguments are passed to `xarray.plot.pcolormesh`.
        """
        if ax is None:
            ax = plt.gca()
        if ax.name != 'polar':
            raise ValueError('ax must have a polar projection')

        kwargs = self._set_cbar_label(kwargs, str(self.unit))
        # Take slice of data and plot
        sliced = self.data.isel(phi=i)
        sliced.plot(x='theta', y='r', ax=ax, **kwargs)

        # Plot formatting
        ax.set_rlim(0)
        ax.set_thetalim(-np.pi / 2, np.pi / 2)
        ax.set_aspect('equal')
        phi = np.rad2deg(sliced['phi'].values)
        ax.set_title(f'{self.name}, ' + r'$\phi$= ' + f'{phi:.2f}' + '$^{\circ}$')
        viz.clear_axes_labels(ax)

        # Tick label formatting
        # Set theta ticks
        ax.set_xticks(np.deg2rad(np.linspace(-90, 90, 7, endpoint=True)))

    @staticmethod
    def _set_cbar_label(kwargs, label):
        """
        Set the colobar label with units.
        """
        # Copy kwargs to prevent modifying them inplace
        kwargs = copy.deepcopy(kwargs)
        # Set the colobar label with units
        cbar_kwargs = kwargs.pop('cbar_kwargs', {})
        cbar_kwargs['label'] = cbar_kwargs.pop('label', label)
        kwargs['cbar_kwargs'] = cbar_kwargs
        return kwargs
