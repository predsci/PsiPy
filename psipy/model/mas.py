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

    def plot_radial_cut(self, i, ax=None):
        """
        Parameters
        ----------
        i : int
            Index at which to slice the data.
        ax : matplolit.axes.Axes, optional
            axes on which to plot. Defaults to current axes if not specified.
        """
        sliced = self.data.isel(r=-1)

        if ax is None:
            ax = plt.gca()

        sliced.plot(x='phi', y='theta', ax=ax)
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

    def __getattr__(self, attr):
        """
        Get an attribute. This allows one to do e.g. ``masoutput.vr`` to get
        the radial velocity variable.
        """
        if attr in _mas_vars:
            return Variable(self._data[attr], attr)
        return super().__getattr__(attr)
