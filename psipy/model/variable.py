import copy
import textwrap

import astropy.constants as const
import astropy.units as u
import numpy as np
from scipy import interpolate
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
        # Sort the data once now for any interpolation later
        self._data = self._data.sortby(['phi', 'theta', 'r'])
        self.name = name
        self._unit = unit

    def __str__(self):
        return textwrap.dedent(f'''
        Variable
        --------
        Name: {self.name}
        Grid size: {self._data.shape} (phi, theta, r)
        ''')

    @property
    def data(self):
        """
        `xarray.DataArray` with the data.
        """
        return self._data

    @property
    def unit(self):
        """
        Units of the scalar data.
        """
        return self._unit

    @unit.setter
    def unit(self, new_unit):
        # This line will error if untis aren't compatible
        conversion = float(1 * self._unit / new_unit)
        self._data *= conversion
        self._unit = new_unit

    @property
    def r_coords(self):
        """
        Radial coordinate values.
        """
        return self._data.coords['r'].values

    @property
    def theta_coords(self):
        """
        Latitude coordinate values.
        """
        return self._data.coords['theta'].values

    @property
    def phi_coords(self):
        """
        Longitude coordinate values.
        """
        return self._data.coords['phi'].values

    def radial_normalized(self, radial_exponent):
        r"""
        Return a radially normalised copy of this variable.

        Multiplies the variable by :math:`(r / r_{\odot})^{\gamma}`,
        where :math:`\gamma` = ``radial_exponent`` is the given exponent.

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
        ax.set_title(title)
        self._format_radial_ax(ax)

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
        viz.format_polar_ax(ax)
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
        viz.format_polar_ax(ax)
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

    @u.quantity_input
    def sample_at_coords(self, lon, lat, r):
        """
        Sample this variable along a 1D trajectory of coordinates.

        Parameters
        ----------
        lon : astropy.units.Quantity
            Longitudes.
        lat : astropy.units.Quantity
            Latitudes.
        r : astropy.units.Quantity
            Radial distances.

        Returns
        -------
        astropy.units.Quantity
            The sampled data.

        Notes
        -----
        Linear interpolation is used to interpoalte between cells. See the
        docstring of `scipy.interpolate.interpn` for more information.
        """
        points = [self.data.coords[dim].values for dim in ['phi', 'theta', 'r']]
        values = self.data.values
        # Check that coordinates are increasing
        if not np.all(np.diff(points[0]) >= 0):
            raise RuntimeError('Longitude coordinates are not monotonically increasing')
        if not np.all(np.diff(points[1]) >= 0):
            raise RuntimeError('Latitude coordinates are not monotonically increasing')
        if not np.all(np.diff(points[2]) > 0):
            raise RuntimeError('Radial coordinates are not monotonically increasing')

        # Pad phi points so it's possible to interpolate all the way from
        # 0 to 360 deg
        points[0] = np.append(points[0], points[0][0] + 2 * np.pi)
        values = np.append(values, values[0:1, ...], axis=0)

        xi = np.column_stack([lon.to_value(u.rad),
                              lat.to_value(u.rad),
                              r.to_value(const.R_sun)])

        values_x = interpolate.interpn(points, values, xi)
        return values_x * self._unit
