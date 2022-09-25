import copy
import textwrap
import warnings
from typing import Optional

import astropy.units as u
import numpy as np
import xarray as xr
from scipy import interpolate

import psipy.visualization as viz
from psipy.util.decorators import add_common_docstring

__all__ = ["Variable"]


# Some docstrings that are used more than once
quad_mesh_link = ":class:`~matplotlib.collections.QuadMesh`"
# TODO: fix this to ':class:`~matplotlib.animation.FuncAnimation`'
animation_link = "animation"

returns_doc = textwrap.indent(
    f"""
{quad_mesh_link} or {animation_link}
    If a timestep is specified, the {quad_mesh_link} of the plot is returned.
    Otherwise an {animation_link} is returned.
""",
    "        ",
)


class Variable:
    """
    A single scalar variable.

    This class primarily contains methods for plotting data. It can be created
    with any `xarray.DataArray` that has ``['theta', 'phi', 'r', 'time']``
    fields.

    Parameters
    ----------
    data : xarray.Dataset
        Variable data.
    name : str
        Variable name.
    unit : astropy.units.Quantity
        Variable unit for the scalar data.
    r_unit : astropy.units.Quantity
        Unit for the radial coordinates.
    """

    def __init__(self, data, name, unit, runit):
        # Convert from xarray Dataset to DataArray
        self._data = data[name]
        # Sort the data once now for any interpolation later
        self._data = self._data.transpose(*["phi", "theta", "r", "time"])
        self._data = self._data.sortby(["phi", "theta", "r", "time"])
        self.name = name
        self._unit = unit
        self._runit = runit

    def __str__(self):
        return textwrap.dedent(
            f"""
        Variable
        --------
        Name: {self.name}
        Grid size: {len(self.phi_coords), len(self.theta_coords), len(self.r_coords)} (phi, theta, r)
        Timesteps: {len(self.time_coords)}
        """
        )

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
        return self._data.coords["r"].values * self._runit

    @r_coords.setter
    def r_coords(self, coords: u.m):
        self._data.coords["r"] = coords.value
        self._runit = coords.unit

    @property
    def theta_coords(self):
        """
        Latitude coordinate values.
        """
        return self._data.coords["theta"].values

    @property
    def phi_coords(self):
        """
        Longitude coordinate values.
        """
        return self._data.coords["phi"].values

    @property
    def time_coords(self):
        """
        Timestep coordinate values.
        """
        return self._data.coords["time"].values

    @property
    def n_timesteps(self):
        """
        Number of timesteps.
        """
        return len(self.time_coords)

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
        norm_factor = (self.r_coords / u.R_sun).to_value(
            u.dimensionless_unscaled
        ) ** radial_exponent
        data = xr.dot(self.data, xr.Variable("r", norm_factor), dims=())
        name = self.name + f" $r^{radial_exponent}$"
        unit = self.unit
        return Variable(xr.Dataset({name: data}), name, unit, self._runit)

    # Methods for radial cuts
    @add_common_docstring(returns_doc=returns_doc)
    def plot_radial_cut(self, r_idx, t_idx=None, ax=None, **kwargs):
        """
        Plot a radial cut.

        Parameters
        ----------
        r_idx : int
            Radial index at which to slice the data.
        t_idx : int, optional
            Time index at which to slice the data. If not given, an anmiation
            will be created across all time indices.
        ax : matplolit.axes.Axes, optional
            axes on which to plot. Defaults to current axes if not specified.
        kwargs :
            Additional keyword arguments are passed to
            `xarray.plot.pcolormesh`.

        Returns
        -------
        {returns_doc}
        """
        r_slice = self.data.isel(r=r_idx)
        time_slice = r_slice.isel(time=t_idx or 0)

        # Setup axes
        ax = viz.setup_radial_ax(ax)
        # Set colorbar string
        kwargs = self._set_cbar_label(kwargs, self.unit.to_string("latex"))
        quad_mesh = time_slice.plot(x="phi", y="theta", ax=ax, **kwargs)
        # Plot formatting
        r = r_slice["r"].values
        ax.set_title(f"{self.name}, r={r:.2f}" + r"$R_{\odot}$")
        viz.format_radial_ax(ax)

        if t_idx is not None or self.n_timesteps == 1:
            return quad_mesh
        else:
            return viz.animate_time(ax, r_slice, quad_mesh)

    def contour_radial_cut(self, r_idx, levels, t_idx=0, ax=None, **kwargs):
        """
        Plot contours on a radial cut.

        Parameters
        ----------
        r_idx : int
            Radial index at which to slice the data.
        levels : list
            List of levels to contour.
        t_idx : int, optional
            Time index at which to slice the data.
        ax : matplolit.axes.Axes, optional
            axes on which to plot. Defaults to current axes if not specified.
        kwargs :
            Additional keyword arguments are passed to `xarray.plot.contour`.
        """
        ax = viz.setup_radial_ax(ax)
        sliced = self.data.isel(r=r_idx, time=t_idx)
        # Need to save a copy of the title to reset it later, since xarray
        # tries to set it's own title that we don't want
        title = ax.get_title()
        xr.plot.contour(sliced, x="phi", y="theta", ax=ax, levels=levels, **kwargs)
        ax.set_title(title)
        viz.format_radial_ax(ax)

    @add_common_docstring(returns_doc=returns_doc)
    def plot_phi_cut(self, phi_idx, t_idx=None, ax=None, **kwargs):
        """
        Plot a phi cut.

        Parameters
        ----------
        phi_idx : int
            Index at which to slice the data.
        t_idx : int, optional
            Time index at which to slice the data. If not given, an anmiation
            will be created across all time indices.
        ax : matplolit.axes.Axes, optional
            axes on which to plot. Defaults to current axes if not specified.
        kwargs :
            Additional keyword arguments are passed to
            `xarray.plot.pcolormesh`.

        Returns
        -------
        {returns_doc}
        """
        phi_slice = self.data.isel(phi=phi_idx)
        time_slice = phi_slice.isel(time=t_idx or 0)

        ax = viz.setup_polar_ax(ax)
        kwargs = self._set_cbar_label(kwargs, self.unit.to_string("latex"))
        # Take slice of data and plot
        quad_mesh = time_slice.plot(x="theta", y="r", ax=ax, **kwargs)
        viz.format_polar_ax(ax)

        phi = np.rad2deg(time_slice["phi"].values)
        ax.set_title(f"{self.name}, " + r"$\phi$= " + f"{phi:.2f}" + r"$^{\circ}$")

        if t_idx is not None or self.n_timesteps == 1:
            return quad_mesh
        else:
            return viz.animate_time(ax, phi_slice, quad_mesh)

    def contour_phi_cut(self, i, levels, t_idx=0, ax=None, **kwargs):
        """
        Plot contours on a phi cut.

        Parameters
        ----------
        i : int
            Index at which to slice the data.
        levels : list
            List of levels to contour.
        t_idx : int, optional
            Time index at which to slice the data.
        ax : matplolit.axes.Axes, optional
            axes on which to plot. Defaults to current axes if not specified.
        kwargs :
            Additional keyword arguments are passed to `xarray.plot.contour`.
        """
        ax = viz.setup_polar_ax(ax)
        sliced = self.data.isel(phi=i, time=t_idx)
        # Need to save a copy of the title to reset it later, since xarray
        # tries to set it's own title that we don't want
        title = ax.get_title()
        xr.plot.contour(sliced, x="theta", y="r", ax=ax, levels=levels, **kwargs)
        viz.format_polar_ax(ax)
        ax.set_title(title)

    @property
    def _equator_theta_idx(self):
        """
        The theta index of the solar equator.
        """
        return (self.data.shape[1] - 1) // 2

    # Methods for equatorial cuts
    @add_common_docstring(returns_doc=returns_doc)
    def plot_equatorial_cut(self, t_idx=None, ax=None, **kwargs):
        """
        Plot an equatorial cut.

        Parameters
        ----------
        ax : matplolit.axes.Axes, optional
            axes on which to plot. Defaults to current axes if not specified.
        t_idx : int, optional
            Time index at which to slice the data. If not given, an anmiation
            will be created across all time indices.
        kwargs :
            Additional keyword arguments are passed to
            `xarray.plot.pcolormesh`.

        Returns
        -------
        {returns_doc}
        """
        theta_slice = self.data.isel(theta=self._equator_theta_idx)
        time_slice = theta_slice.isel(time=t_idx or 0)

        ax = viz.setup_polar_ax(ax)
        kwargs = self._set_cbar_label(kwargs, self.unit.to_string("latex"))
        # Take slice of data and plot
        quad_mesh = time_slice.plot(x="phi", y="r", ax=ax, **kwargs)
        viz.format_equatorial_ax(ax)

        ax.set_title(f"{self.name}, equatorial plane")

        if t_idx is not None or self.n_timesteps == 1:
            return quad_mesh
        else:
            return viz.animate_time(ax, theta_slice, quad_mesh)

    def contour_equatorial_cut(self, levels, t_idx=0, ax=None, **kwargs):
        """
        Plot contours on an equatorial cut.

        Parameters
        ----------
        levels : list
            List of levels to contour.
        ax : matplolit.axes.Axes, optional
            axes on which to plot. Defaults to current axes if not specified.
        t_idx : int, optional
            Time index at which to slice the data.
        kwargs :
            Additional keyword arguments are passed to `xarray.plot.contour`.
        """
        ax = viz.setup_polar_ax(ax)
        sliced = self.data.isel(theta=self._equator_theta_idx, time=t_idx)
        # Need to save a copy of the title to reset it later, since xarray
        # tries to set it's own title that we don't want
        title = ax.get_title()
        xr.plot.contour(sliced, x="phi", y="r", ax=ax, levels=levels, **kwargs)
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
        cbar_kwargs = kwargs.pop("cbar_kwargs", {})
        cbar_kwargs["label"] = cbar_kwargs.pop("label", label)
        kwargs["cbar_kwargs"] = cbar_kwargs
        return kwargs

    @u.quantity_input
    def sample_at_coords(
        self, lon: u.deg, lat: u.deg, r: u.m, t: Optional[np.ndarray] = None
    ) -> u.Quantity:
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
        t : array-like, optional
            Timsteps. If the variable only has a single timstep, this argument
            is not required.

        Returns
        -------
        astropy.units.Quantity
            The sampled data.

        Notes
        -----
        Linear interpolation is used to interpoalte between cells. See the
        docstring of `scipy.interpolate.interpn` for more information.
        """
        if lat.shape != lon.shape:
            raise ValueError(
                f"Shapes of latitude {lat.shape} and longitude {lon.shape} coordinates do not match."
            )
        if r.shape != lon.shape:
            raise ValueError(
                f"Shapes of radial {r.shape} and longitude {lon.shape} coordinates do not match."
            )
        if t is not None and t.shape != lon.shape:
            raise ValueError(
                f"Shapes of time {t.shape} and longitude {lon.shape} coordinates do not match."
            )
        dims = ["phi", "theta", "r", "time"]
        points = [self.data.coords[dim].values for dim in dims]
        values = self.data.values

        # Check that coordinates are increasing
        if not np.all(np.diff(points[1]) >= 0):
            raise RuntimeError("Longitude coordinates are not monotonically increasing")
        if not np.all(np.diff(points[2]) >= 0):
            raise RuntimeError("Latitude coordinates are not monotonically increasing")
        if not np.all(np.diff(points[3]) > 0):
            raise RuntimeError("Radial coordinates are not monotonically increasing")

        # Pad phi points so it's possible to interpolate all the way from
        # 0 to 360 deg
        pcoords = points[0]
        pcoords = np.append(pcoords, pcoords[0] + 2 * np.pi)
        pcoords = np.insert(pcoords, 0, pcoords[-2] - 2 * np.pi)
        points[0] = pcoords

        values = np.append(values, values[0:1, :, :, :], axis=0)
        values = np.insert(values, 0, values[-2:-1, :, :, :], axis=0)

        if len(points[3]) == 1:
            # Only one timestep
            xi = np.column_stack(
                [lon.to_value(u.rad), lat.to_value(u.rad), r.to_value(self._runit)]
            )
            values = values[:, :, :, 0]
            points = points[:-1]
        else:
            xi = np.column_stack(
                [lon.to_value(u.rad), lat.to_value(u.rad), r.to_value(self._runit), t]
            )

        for i, dim in enumerate(dims[:-1]):
            bounds = np.min(points[i]), np.max(points[i])
            coord_bounds = np.min(xi[:, i]), np.max(xi[:, i])
            if not (bounds[0] <= coord_bounds[0] and coord_bounds[1] <= bounds[1]):
                warnings.warn(
                    f"At least one sample coordinate is outside bounds {bounds} in {dim} dimension. Sample coordinate min/max values are {coord_bounds}."
                )

        values_x = interpolate.interpn(
            points, values, xi, bounds_error=False, fill_value=np.nan
        )
        return values_x * self._unit
