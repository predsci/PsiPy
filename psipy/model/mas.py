from pathlib import Path

from psipy.io import read_mas_files
from psipy.io.mas import _mas_vars

__all__ = ['MASOutput']


class Variable:
    """
    A single scalar variable.

    This class contains methods for plotting data.

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
        sliced = self.data.isel(r=i)

        if ax is None:
            ax = plt.gca()

        sliced.plot(x='phi', y='theta', ax=ax, **kwargs)
        ax.set_aspect('equal')

    def plot_phi_cut(self, i, ax=None, **kwargs):
        """
        Plot a theta cut.

        Parameters
        ----------
        i : int
            Index at which to slice the data.
        ax : matplolit.axes.Axes, optional
            axes on which to plot. Defaults to current axes if not specified.
        kwargs :
            Additional keyword arguments are passed to `xarray.plot.pcolormesh`.
        """
        sliced = self.data.isel(phi=i)

        if ax is None:
            ax = plt.gca()
        if ax.name != 'polar':
            raise ValueError('ax must have a polar projection')

        sliced.plot(x='theta', y='r', ax=ax, **kwargs)

        ax.set_rlim(0)
        ax.set_aspect('equal')


class MASOutput:
    """
    The results from a single run of MAS.

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
