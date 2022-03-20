import numpy as np
import pyvista as pv
from astropy.coordinates import cartesian_to_spherical
from vtkmodules.vtkCommonCore import vtkCommand
from vtkmodules.vtkRenderingCore import vtkCellPicker

__all__ = ['MASPlotter']


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
        self.pvplotter = pv.Plotter()
        self.mas_output = mas_output
        self.tracer = None

    def add_fline(self, fline, **kwargs):
        spline = pv.Spline(fline.xyz)
        kwargs['pickable'] = kwargs.get('pickable', False)
        self.pvplotter.add_mesh(spline, **kwargs)

    def add_sphere(self, radius, **kwargs):
        """
        Add a sphere at a given radius.

        Returns
        -------
        pyvista.Sphere
        """
        sphere = pv.Sphere(radius=radius,
                           theta_resolution=180,
                           phi_resolution=360)
        self.pvplotter.add_mesh(sphere, **kwargs)
        return sphere

    def show(self, *args, **kwargs):
        return self.pvplotter.show(*args, **kwargs)

    def add_tracing_seed_sphere(self, radius, **kwargs):
        """
        Add a sphere to trace field lines from.

        Returns
        -------
        pyvista.Sphere
        """
        kwargs['pickable'] = True
        self.add_sphere(radius, **kwargs)

        # Setup picking
        cell_picker = vtkCellPicker()
        self.pvplotter.picker = cell_picker
        cell_picker.AddObserver(vtkCommand.EndPickEvent,
                                self._end_pick_event)

        self.pvplotter.enable_trackball_style()
        self.pvplotter.iren.set_picker(cell_picker)

        # Now add text about cell-selection
        show_message = "Press P to pick under the mouse"
        self.pvplotter.add_text(show_message,
                                font_size=18,
                                name='_point_picking_message')

    def _trace_from_seed(self, pos):
        """
        A callback to trace a magnetic field line from the picked point.
        """
        if self.tracer is None:
            from psipy.tracing import FortranTracer
            self.tracer = FortranTracer()

        r, lat, lon = cartesian_to_spherical(*pos)
        flines = self.tracer.trace(self.mas_output, r=r, lat=lat, lon=lon)
        self.add_fline(flines[0])

    def show(self, *args, **kwargs):
        return self.pvplotter.show(*args, **kwargs)

    def _end_pick_event(self, picker, event):
        picked_point = np.array(picker.GetPickPosition())
        self.pvplotter.add_mesh(picked_point,
                                color='pink',
                                point_size=20,
                                name='_picked_point',
                                pickable=False,
                                reset_camera=False)

        self._trace_from_seed(picked_point)
