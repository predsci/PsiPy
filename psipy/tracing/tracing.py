import numpy as np


class FortranTracer:
    r"""
    Tracer using Fortran code.

    Parameters
    ----------
    max_steps: int
        Maximum number of steps each streamline can take before stopping.
    step_size : float
        Step size as a fraction of cell size at the equator.

    Notes
    -----
    Because the stream tracing is done in spherical coordinates, there is a
    singularity at the poles (ie. :math:`s = \pm 1`), which means seeds placed
    directly on the poles will not go anywhere.
    """
    def __init__(self, max_steps=1000, step_size=0.01):
        try:
            from streamtracer import StreamTracer
        except ModuleNotFoundError as e:
            raise RuntimeError(
                'Using FortranTracer requires the streamtracer module, '
                'but streamtracer could not be loaded') from e
        self.max_steps = max_steps
        self.step_size = step_size
        self.tracer = StreamTracer(max_steps, step_size)

    @staticmethod
    def vector_grid(mas_output, var):
        """
        Create a `streamtracer.VectorGrid` object.
        """
        from streamtracer import VectorGrid

        vs = mas_output.cell_centered_b(extra_phi_coord=True)
        # Correct phi component for distortion
        vs.loc[..., f'{var}p'] /= np.cos(vs.coords['theta'])
        vs.loc[..., f'{var}t'] /= vs.coords['r']
        vs.loc[..., f'{var}p'] /= vs.coords['r']

        grid_spacing = [np.mean(np.diff(vs.coords[comp])) for comp in ['phi', 'theta', 'r']]
        # Cyclic only in the phi direction
        # (theta direction becomes singular at the poles so it is not cyclic)
        cyclic = [True, False, False]
        origin_coord = [np.min(vs.coords['phi']), np.min(vs.coords['theta']), np.min(vs.coords['r'])]
        vector_grid = VectorGrid(vs.data, grid_spacing, cyclic=cyclic,
                                 origin_coord=origin_coord)
        return vector_grid

    def trace(self, seeds, mas_output, var):
        seeds = np.atleast_2d(seeds)

        # Get a grid
        vector_grid = self.vector_grid(mas_output, var)

        # Do the tracing
        self.tracer.trace(seeds, vector_grid)
        return self.tracer.xs
