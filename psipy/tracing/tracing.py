import astropy.units as u
import numpy as np


class FortranTracer:
    r"""
    Tracer using Fortran code.

    Parameters
    ----------
    max_steps: 'auto', int
        Maximum number of steps each streamline can take before stopping. This
        directly sets the memory allocated to the traced streamlines, so do not
        set it too large. If set to ``'auto'`` (the default),
    step_size : float
        Step size as a fraction of the smallest radial grid spacing.

    Notes
    -----
    Because the stream tracing is done in spherical coordinates, there is a
    singularity at the poles, which means seeds placed directly on the poles
    will not go anywhere.
    """
    def __init__(self, max_steps='auto', step_size=1):
        try:
            import streamtracer  # NoQA
        except ModuleNotFoundError as e:
            raise RuntimeError(
                'Using FortranTracer requires the streamtracer module, '
                'but streamtracer could not be loaded') from e
        self.max_steps = max_steps
        self.step_size = step_size
        self.max_steps = max_steps
        max_steps = 1 if max_steps == 'auto' else max_steps
        # We have to set max_steps and step_size here to create a tracer,

    def _vector_grid(self, mas_output, t_idx):
        """
        Create a `streamtracer.VectorGrid` object from a MAS output.
        """
        bs = mas_output.cell_corner_b(t_idx)
        return self._vector_grid_from_bs(bs)

    def _vector_grid_from_bs(self, bs):
        """
        Create a `streamtracer.VectorGrid` object from a magnetic field array.
        """
        from streamtracer import VectorGrid

        # Account for tracing in spherical coordinates
        bs.loc[..., 'bp'] /= np.cos(bs.coords['theta'])
        bs.loc[..., 'bp'] /= bs.coords['r']
        bs.loc[..., 'bt'] /= bs.coords['r']

        grid_spacing = self._get_spacing(bs.coords)
        # cyclic only in the phi direction
        cyclic = [True, False, False]
        origin_coord = np.array([bs.coords['phi'][0].values,
                                 bs.coords['theta'][0].values,
                                 bs.coords['r'][0].values])
        vector_grid = VectorGrid(bs.data, grid_spacing, cyclic=cyclic,
                                 origin_coord=origin_coord)
        return vector_grid

    @staticmethod
    def _get_spacing(coords):
        """
        Returns
        -------
        spacing : list
            Spacing in [phi, theta, r].

        Raises
        ------
        ValueError
            If any one of the coordinates are not regularly spaced.
        """
        spacing = []
        for coord in ['phi', 'theta', 'r']:
            all_spacing = np.diff(coords[coord])
            if not np.allclose(all_spacing, all_spacing[0], rtol=1e-5, atol=0):
                raise ValueError('Tracer currently only works with '
                                 f'regularly spaced grid in {coord}.')
            spacing.append(np.mean(all_spacing))

        return spacing

    @u.quantity_input
    def trace(self, mas_output, *, r, lat: u.rad, lon: u.rad, t_idx=None):
        """
        Trace field lines.

        Parameters
        ----------
        mas_output : psipy.model.MASOutput
            MAS model output. Must have all three magnetic field components
            available.
        r : numpy.ndarray
            Radial seed coordinates. These are interpreted in units equivalent
            to the ``mas_output`` radial units.
        lat : astropy.units.Quantity
            Latitude seed points. Must be same shape as ``r``.
        lon : astropy.units.Quantity
            Longitude seed points. Must be same shape as ``r``.
        t_idx : int, optional
            Time slice of the ``mas_output`` to trace through. Doesn't need to
            be specified if only one time step is present.
        """
        lat = lat.to_value(u.rad)
        lon = lon.to_value(u.rad)
        seeds = np.stack([lon, lat, r], axis=-1)
        vector_grid = self._vector_grid(mas_output, t_idx)
        return self._trace_from_grid(vector_grid, seeds)

    def _trace_from_grid(self, grid, seeds):
        from streamtracer import StreamTracer
        seeds = np.atleast_2d(seeds)
        if self.max_steps == 'auto':
            max_steps = int(4 * len(grid.zcoords) / self.step_size)
        else:
            max_steps = self.max_steps

        # Normalize step size to radial cell size
        step_size = grid.grid_spacing[2] * self.step_size
        self.tracer = StreamTracer(max_steps, step_size)
        self.tracer.trace(seeds, grid)
        return self.tracer.xs
