import astropy.constants as const
import astropy.units as u
import numpy as np
import scipy.interpolate
import xarray as xr

from .base import ModelOutput
from psipy.io import read_mas_file, get_mas_variables

__all__ = ['MASOutput']


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
              'rho': [u.N / u.cm**3, 1.67e-16 / 1.67e-24],
              't': [u.K, 2.804e7],
              'p': [u.Pa, 3.875717e-2],
              'jr': _junit,
              'jt': _junit,
              'jp': _junit
              }


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

    def get_variables(self):
        return get_mas_variables(self.path)

    def load_file(self, var):
        return read_mas_file(self.path, var)

    def __repr__(self):
        return f'psipy.model.mas.MASOutput("{self.path}")'

    def __str__(self):
        return f"MAS output in directory {self.path}"

    def cell_centered_v(self, extra_phi_coord=False):
        """
        Get the velocity vector at the cell centres.

        Because the locations of the vector component outputs

        Parameters
        ----------
        extra_phi_coord: bool
            If `True`, add an extra phi slice.
        """
        if not set(['vr', 'vt', 'vp']) <= set(self.variables):
            raise RuntimeError('MAS output must have the vr, vt, vp variables loaded')

        # Interpolate new radial coordiantes
        new_rcoord = self['vr'].r_coords
        vt = scipy.interpolate.interp1d(self['vt'].r_coords,
                                        self['vt'].data,
                                        axis=2)(new_rcoord)
        vp = scipy.interpolate.interp1d(self['vp'].r_coords,
                                        self['vp'].data,
                                        axis=2)(new_rcoord)

        # Interpolate new theta coordinates
        new_tcoord = self['vt'].theta_coords
        vr = scipy.interpolate.interp1d(self['vr'].theta_coords,
                                        self['vr'].data,
                                        axis=1)(new_tcoord)
        vp = scipy.interpolate.interp1d(self['vp'].theta_coords,
                                        vp,
                                        axis=1)(new_tcoord)
        # Don't need to interpolate phi coords, but get a copy
        new_pcoord = self['vr'].phi_coords

        if extra_phi_coord:
            dphi = np.mean(np.diff(new_pcoord))
            assert np.allclose(new_pcoord[0] + 2 * np.pi, new_pcoord[-1] + dphi)

            new_pcoord = np.append(new_pcoord, new_pcoord[-1] + dphi)
            vp = np.append(vp, vp[0:1, :, :], axis=0)
            vt = np.append(vt, vt[0:1, :, :], axis=0)
            vr = np.append(vr, vr[0:1, :, :], axis=0)

        return xr.DataArray(np.stack([vp, vt, vr], axis=-1),
                            dims=['phi', 'theta', 'r', 'component'],
                            coords=[new_pcoord, new_tcoord, new_rcoord,
                                    ['vp', 'vt', 'vr']])
