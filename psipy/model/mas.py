import astropy.units as u
import numpy as np
import scipy.interpolate
import xarray as xr

from psipy.io import get_mas_variables, read_mas_file
from .base import ModelOutput

__all__ = ["MASOutput"]


# A mapping from unit names to their units, and factors the data needs to be
# multiplied to get them into these units.
_vunit = [u.km / u.s, 481.37]
_bunit = [u.G, 2.205]
_junit = [u.A / u.m**2, 2.267e4]
_mas_units = {
    "vr": _vunit,
    "vt": _vunit,
    "vp": _vunit,
    "va": _vunit,
    "br": _bunit,
    "bt": _bunit,
    "bp": _bunit,
    "bmag": _bunit,
    "rho": [u.cm**-3, 1.67e-16 / 1.67e-24],
    "t": [u.K, 2.804e7],
    "p": [u.Pa, 3.875717e-2],
    "jr": _junit,
    "jt": _junit,
    "jp": _junit,
}
_2pi = 2 * np.pi


class MASOutput(ModelOutput):
    """
    The results from a single run of MAS.

    This is a storage object that contains a number of `Variable` objects. It
    is designed to be used like::

        mas_output = MASOutput('directory')
        br = mas_output['br']

    Notes
    -----
    Variables are loaded on demand. To see the list of available variables
    use `MASOutput.variables`, and to see the list of already loaded variables
    use `MASOutput.loaded_variables`.
    """

    def get_unit(self, var):
        return _mas_units[var]

    def get_runit(self):
        return u.R_sun

    def get_variables(self):
        return get_mas_variables(self.path)

    def load_file(self, var):
        return read_mas_file(self.path, var)

    def __repr__(self):
        return f'psipy.model.mas.MASOutput("{self.path}")'

    def __str__(self):
        return f"MAS output in directory {self.path}\n" + super().__str__()

    def cell_corner_b(self, t_idx=None):
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
        if not set(["br", "bt", "bp"]) <= set(self.variables):
            raise RuntimeError("MAS output must have the br, bt, bp variables loaded")

        # Interpolate radial coordinate
        new_rcoord = self["bt"].r_coords
        br = scipy.interpolate.interp1d(
            self["br"].r_coords,
            self["br"].data.isel(time=t_idx or 0),
            axis=2,
            fill_value="extrapolate",
        )(new_rcoord)

        # Interpolate theta coordinate
        new_tcoord = self["bp"].theta_coords
        bt = scipy.interpolate.interp1d(
            self["bt"].theta_coords,
            self["bt"].data.isel(time=t_idx or 0),
            axis=1,
            fill_value="extrapolate",
        )(new_tcoord)

        # Interoplate phi coordinate
        new_pcoord = self["br"].phi_coords
        bp = scipy.interpolate.interp1d(
            self["bp"].phi_coords,
            self["bp"].data.isel(time=t_idx or 0),
            axis=0,
            fill_value="extrapolate",
        )(new_pcoord)
        # Calculate edge/cyclic phi value
        old_pcoord = self["bp"].phi_coords
        edge_pcoord = [old_pcoord[-1], old_pcoord[0] + _2pi]
        edge_data = self["bp"].data.isel(time=t_idx or 0)
        edge_data = np.stack([edge_data[-1, :, :], edge_data[0, :, :]], axis=0)
        bp_edge = scipy.interpolate.interp1d(edge_pcoord, edge_data, axis=0)(_2pi)
        bp_edge = bp_edge.reshape((1, *bp_edge.shape))

        # Add an extra layer of cells at phi=2pi for the tracer
        br = np.concatenate((br, br[0:1]), axis=0)
        bt = np.concatenate((bt, bt[0:1]), axis=0)
        bp = np.concatenate((bp_edge, bp[1:, :, :], bp_edge), axis=0)
        new_pcoord = np.append(new_pcoord, _2pi)

        return xr.DataArray(
            np.stack([bp, bt, br], axis=-1),
            dims=["phi", "theta", "r", "component"],
            coords=[new_pcoord, new_tcoord, new_rcoord, ["bp", "bt", "br"]],
        )

    def cell_centered_v(self, extra_phi_coord=False):
        """
        Get the velocity vector at the cell centres.

        Because the locations of the vector component outputs

        Parameters
        ----------
        extra_phi_coord: bool
            If `True`, add an extra phi slice.
        """
        if not set(["vr", "vt", "vp"]) <= set(self.variables):
            raise RuntimeError("MAS output must have the vr, vt, vp variables loaded")

        # Interpolate new radial coordiantes
        new_rcoord = self["vr"].r_coords
        vt = scipy.interpolate.interp1d(self["vt"].r_coords, self["vt"].data, axis=2)(
            new_rcoord
        )
        vp = scipy.interpolate.interp1d(self["vp"].r_coords, self["vp"].data, axis=2)(
            new_rcoord
        )

        # Interpolate new theta coordinates
        new_tcoord = self["vt"].theta_coords
        vr = scipy.interpolate.interp1d(
            self["vr"].theta_coords, self["vr"].data, axis=1
        )(new_tcoord)
        vp = scipy.interpolate.interp1d(self["vp"].theta_coords, vp, axis=1)(new_tcoord)
        # Don't need to interpolate phi coords, but get a copy
        new_pcoord = self["vr"].phi_coords

        if extra_phi_coord:
            dphi = np.mean(np.diff(new_pcoord))
            assert np.allclose(new_pcoord[0] + 2 * np.pi, new_pcoord[-1] + dphi)

            new_pcoord = np.append(new_pcoord, new_pcoord[-1] + dphi)
            vp = np.append(vp, vp[0:1, :, :], axis=0)
            vt = np.append(vt, vt[0:1, :, :], axis=0)
            vr = np.append(vr, vr[0:1, :, :], axis=0)

        return xr.DataArray(
            np.stack([vp, vt, vr], axis=-1),
            dims=["phi", "theta", "r", "component"],
            coords=[new_pcoord, new_tcoord, new_rcoord, ["vp", "vt", "vr"]],
        )
