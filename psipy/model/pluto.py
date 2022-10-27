import astropy.units as u
import numpy as np
import xarray as xr

from psipy.io import get_pluto_variables, read_pluto_files
from .base import ModelOutput

__all__ = ["PLUTOOutput"]


class PLUTOOutput(ModelOutput):
    """
    The results from a single run of PLUTO.

    This is a storage object that contains a number of `Variable` objects. It
    is designed to be used like::

        pluto_output = PLUTOOutput('directory')
        br = pluto_output['br']

    Notes
    -----
    Variables are loaded on demand. To see the list of available variables
    use `PLUTOOutput.variables`, and to see the list of already loaded variables
    use `PLUTOOutput.loaded_variables`.
    """

    def get_unit(self, var):
        return u.dimensionless_unscaled, 1

    def get_runit(self):
        return u.AU

    def get_variables(self):
        return get_pluto_variables(self.path)

    def load_file(self, var):
        return read_pluto_files(self.path, var)

    def cell_corner_b(self, t_idx: int = None) -> xr.DataArray:
        if not set(["Bx1", "Bx2", "Bx3"]) <= set(self.variables):
            raise RuntimeError(
                "PLUTO output must have the BX1, Bx2, Bx3 variables loaded"
            )

        r_coords = self["Bx1"].r_coords
        t_coords = self["Bx1"].theta_coords
        p_coords = self["Bx1"].phi_coords

        br = self["Bx1"].data.isel(time=t_idx or 0)
        bt = self["Bx2"].data.isel(time=t_idx or 0)
        bp = self["Bx3"].data.isel(time=t_idx or 0)

        # Add an extra layer of cells around phi=2pi for the tracer
        br = np.concatenate((br, br[0:1, :, :]), axis=0)
        bt = np.concatenate((bt, bt[0:1, :, :]), axis=0)
        bp = np.concatenate((bp, bp[0:1, :, :]), axis=0)
        new_pcoords = np.append(p_coords, p_coords[0:1] + 2 * np.pi)

        return xr.DataArray(
            np.stack([bp, bt, br], axis=-1),
            dims=["phi", "theta", "r", "component"],
            coords=[new_pcoords, t_coords, r_coords, ["bp", "bt", "br"]],
        )
