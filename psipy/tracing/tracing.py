import numpy as np


class FortranTracer:
    r"""
    Tracer using Fortran code.

    Parameters
    ----------
    max_steps: int
        Maximum number of steps each streamline can take before stopping. This
        directly sets the memory allocated to the traced streamlines, so do not
        set it too large.
    step_size : float
        Step size in solar radii.

    Notes
    -----
    Because the stream tracing is done in spherical coordinates, there is a
    singularity at the poles, which means seeds placed directly on the poles
    will not go anywhere.
    """
    def __init__(self, max_steps=200, step_size=0.1):
        try:
            from streamtracer import StreamTracer
        except ModuleNotFoundError as e:
            raise RuntimeError(
                'Using FortranTracer requires the streamtracer module '
                'to be installed.') from e
        # TODO: allow max_steps = 'auto'
        self.max_steps = max_steps
        self.step_size = step_size
        self.tracer = StreamTracer(max_steps, step_size)

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

    def trace(self, mas_output, seeds, t_idx=None):
        """
        Trace field lines.

        Parameters
        ----------
        mas_output : psipy.model.MASOutput
            MAS model output. Must have all three magnetic field components
            available.
        seeds : numpy.ndarray
            Field line seed points. Must be a ``(n, 3)`` shaped array with
            (longitude, latitude, radius) components.
        t_idx : int, optional
            Time slice of the ``mas_output`` to trace through. Doesn't need to
            be specified if only one time step is present.
        """
        vector_grid = self._vector_grid(mas_output, t_idx)
        return self._trace_from_grid(vector_grid, seeds)

    def _trace_from_grid(self, grid, seeds):
        seeds = np.atleast_2d(seeds)
        self.tracer.trace(seeds, grid)
        return self.tracer.xs
