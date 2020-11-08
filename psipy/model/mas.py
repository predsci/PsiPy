from pathlib import Path

import numpy as np

from psipy.io import read_mas_files
from psipy.io.mas import _mas_vars

__all__ = ['MASOutput', 'Variable']


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
    """
    def __init__(self, data, name):
        self.data = data
        self.name = name

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

        # Take slice of data, and plot
        sliced = self.data.isel(r=i)
        sliced.plot(x='phi', y='theta', ax=ax, **kwargs)

        # Plot formatting
        ax.set_aspect('equal')
        r = sliced['r'].values
        ax.set_title(f'{self.name}, r={r:.2f}' + r'$R_{\odot}$')
        ax.set_xlim(0, 2 * np.pi)
        ax.set_ylim(-np.pi / 2, np.pi / 2)

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

        sliced = self.data.isel(phi=i)
        sliced.plot(x='theta', y='r', ax=ax, **kwargs)

        # Plot formatting
        ax.set_rlim(0)
        ax.set_thetalim(-np.pi / 2, np.pi / 2)
        ax.set_aspect('equal')
        phi = np.rad2deg(sliced['phi'].values)
        ax.set_title(f'{self.name}, ' + r'$\phi$= ' + f'{phi:.2f}' + '$^{\circ}$')


class MASOutput:
    """
    The results from a single run of MAS.

    This is a storage object that contains a number of `Variable` objects.

    Parameters
    ----------
    path :
        Path to the directry containing the model output files.

    Attributes
    ----------
    TODO: add description of attributes
    """
    def __init__(self, path):
        self.path = Path(path)
        self._data = read_mas_files(self.path)

        # TODO: set following attributes:
        # - Carrington rotation
        # - Type of model (heliospheric/coronal)
        # - Type of solution (thermodynamic/Alfvén wave)

    def __getattr__(self, attr):
        """
        Get an attribute. This allows one to do e.g. ``masoutput.vr`` to get
        the radial velocity variable.
        """
        if attr in _mas_vars:
            return Variable(self._data[attr], attr)
        else:
            raise AttributeError(f'attribute {attr} not present in {_mas_vars}')
