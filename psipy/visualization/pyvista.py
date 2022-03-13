import pyvista as pv


class MASPlotter:
    """
    Wrapper for a `pyvista.Plotter`.

    This class provides various convenience methods for plotting various
    structures in ``psipy`` to a 3D pyvista plotter.

    Attributes
    ----------
    plotter : pyvista.Plotter
    """
    def __init__(self, mas_output):
        self.plotter = pv.Plotter()
        self.mas_output = mas_output

    def add_fline(self, fline, **kwargs):
        spline = pv.Spline(fline.xyz)
        self.plotter.add_mesh(spline, **kwargs)

    def add_sphere(self, radius, **kwargs):
        """
        Add a sphere at a given radius.
        """
        sphere = pv.Sphere(radius=radius,
                           theta_resolution=180,
                           phi_resolution=360)
        self.plotter.add_mesh(sphere, **kwargs)

    def show(self, *args, **kwargs):
        return self.plotter.show(*args, **kwargs)
