import copy
import numpy as np
import xarray as xr

import psipy.visualization as viz


__all__ = ['Variable']


class Variable:
    """
    A single scalar variable.

    This class primarily contains methods for plotting data. It can be created
    with any `xarray.DataArray` that has ``['theta', 'phi', 'r']`` fields.

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
        self._data = data
        self.name = name
        self._unit = unit

    @property
    def data(self):
        """
        DataFrame with the data.
        """
        return self._data

    @property
    def unit(self):
        """
        Units of the scalar data.
        """
        return self._unit

    def radial_normalized(self, radial_exponent):
        """
        Return a radially normalised copy of this variable.

        Returns var**gamma, where gamma is the given exponent.

        Parameters
        ----------
        radial_exponent : float

        Returns
        -------
        Variable
        """
        r = self.data.coords['r']
        rsun_au = float(u.AU / const.R_sun)
        data = self.data * (r * rsun_au)**radial_exponent
        units = self.unit * (u.AU)**radial_exponent
        name = self.name + f' $r^{radial_exponent}$'
        return Variable(data, name, units)

    # Methods for radial cuts
    @staticmethod
    def _setup_radial_ax(ax):
        if ax is None:
            ax = plt.gca()
        return ax

    @staticmethod
    def _format_radial_ax(ax):
        # Plot formatting
        ax.set_aspect('equal')
        ax.set_xlim(0, 2 * np.pi)
        ax.set_ylim(-np.pi / 2, np.pi / 2)
        viz.clear_axes_labels(ax)

        # Tick label formatting
        viz.set_theta_formatters(ax)
        ax.set_xticks(np.deg2rad(np.linspace(0, 360, 7, endpoint=True)))
        ax.set_yticks(np.deg2rad(np.linspace(-90, 90, 7, endpoint=True)))

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
        ax = self._setup_radial_ax(ax)

        kwargs = self._set_cbar_label(kwargs, self.unit.to_string('latex'))
        # Take slice of data, and plot
        sliced = self.data.isel(r=i)
        sliced.plot(x='phi', y='theta', ax=ax, **kwargs)

        # Plot formatting
        r = sliced['r'].values
        ax.set_title(f'{self.name}, r={r:.2f}' + r'$R_{\odot}$')
        self._format_radial_ax(ax)

    def contour_radial_cut(self, i, levels, ax=None, **kwargs):
        """
        Plot contours on a radial cut.

        Parameters
        ----------
        i : int
            Index at which to slice the data.
        levels : list
            List of levels to contour.
        ax : matplolit.axes.Axes, optional
            axes on which to plot. Defaults to current axes if not specified.
        kwargs :
            Additional keyword arguments are passed to `xarray.plot.contour`.
        """
        ax = self._setup_radial_ax(ax)
        sliced = self.data.isel(r=i)
        # Need to save a copy of the title to reset it later, since xarray
        # tries to set it's own title that we don't want
        title = ax.get_title()
        xr.plot.contour(sliced, x='phi', y='theta', ax=ax,
                        levels=levels, **kwargs)
        # self._format_polar_ax(ax, sliced)
        ax.set_title(title)
        self._format_radial_ax(ax)

    def _format_polar_ax(self, ax, data):
        # Plot formatting
        ax.set_rlim(0)
        ax.set_thetalim(-np.pi / 2, np.pi / 2)
        viz.clear_axes_labels(ax)

        # Tick label formatting
        # Set theta ticks
        ax.set_xticks([])

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
        ax = viz.setup_polar_ax(ax)

        kwargs = self._set_cbar_label(kwargs, self.unit.to_string('latex'))
        # Take slice of data and plot
        sliced = self.data.isel(phi=i)
        sliced.plot(x='theta', y='r', ax=ax, **kwargs)
        self._format_polar_ax(ax, sliced)
        phi = np.rad2deg(sliced['phi'].values)
        ax.set_title(f'{self.name}, ' + r'$\phi$= ' + f'{phi:.2f}' + '$^{\circ}$')

    def contour_phi_cut(self, i, levels, ax=None, **kwargs):
        """
        Plot contours on a phi cut.

        Parameters
        ----------
        i : int
            Index at which to slice the data.
        levels : list
            List of levels to contour.
        ax : matplolit.axes.Axes, optional
            axes on which to plot. Defaults to current axes if not specified.
        kwargs :
            Additional keyword arguments are passed to `xarray.plot.contour`.
        """
        ax = viz.setup_polar_ax(ax)
        sliced = self.data.isel(phi=i)
        # Need to save a copy of the title to reset it later, since xarray
        # tries to set it's own title that we don't want
        title = ax.get_title()
        xr.plot.contour(sliced, x='theta', y='r', ax=ax,
                        levels=levels, **kwargs)
        self._format_polar_ax(ax, sliced)
        ax.set_title(title)

    @property
    def _equator_theta_idx(self):
        """
        The theta index of the solar equator.
        """
        return (self.data.shape[1] - 1) // 2

    # Methods for equatorial cuts
    def plot_equatorial_cut(self, ax=None, **kwargs):
        """
        Plot an equatorial cut.

        Parameters
        ----------
        ax : matplolit.axes.Axes, optional
            axes on which to plot. Defaults to current axes if not specified.
        kwargs :
            Additional keyword arguments are passed to `xarray.plot.pcolormesh`.
        """
        ax = viz.setup_polar_ax(ax)
        kwargs = self._set_cbar_label(kwargs, self.unit.to_string('latex'))
        # Get data slice
        sliced = self.data.isel(theta=self._equator_theta_idx)
        # Plot
        sliced.plot(x='phi', y='r', ax=ax, **kwargs)
        # Plot formatting
        viz.format_equatorial_ax(ax)
        theta = np.rad2deg(sliced['theta'].values)
        ax.set_title(f'{self.name}, equatorial plane')

    def contour_equatorial_cut(self, levels, ax=None, **kwargs):
        """
        Plot contours on an equatorial cut.

        Parameters
        ----------
        levels : list
            List of levels to contour.
        ax : matplolit.axes.Axes, optional
            axes on which to plot. Defaults to current axes if not specified.
        kwargs :
            Additional keyword arguments are passed to `xarray.plot.contour`.
        """
        ax = viz.setup_polar_ax(ax)
        sliced = self.data.isel(theta=self._equator_theta_idx)
        # Need to save a copy of the title to reset it later, since xarray
        # tries to set it's own title that we don't want
        title = ax.get_title()
        xarray.plot.contour(sliced, x='phi', y='r', ax=ax,
                            levels=levels, **kwargs)
        viz.format_equatorial_ax(ax)
        ax.set_title(title)

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
