Field line tracing
==================

The `streamtracer` library is used to trace magnetic field lines through
models. Note that this must be installed prior to use (pip install streamtracer).
In spherical coordinates the streamline equations are:

.. math:: \frac{dr}{ds} = \hat{B}_{r}
.. math:: \frac{d\theta}{ds} = \frac{\hat{B}_{\theta}}{r}
.. math:: \frac{d\phi}{ds} = \frac{\hat{B}_{\phi}}{r\cos(\theta)}

Tracing magnetic field lines uses the :class:`~psipy.tracing.FortranTracer` class.
From a set of seed points with specified radius, longitude, latitude, the tracer
is called to trace field lines from these points:

.. code-block:: python

  import astropy.units as u
  import numpy as np
  from psipy.tracing import FortranTracer
  tracer = FortranTracer()

  # Radius
  r = [40, 45]
  lat = [0, 10] * u.deg
  lon = [0, np.pi / 4] * u.rad
  flines = tracer.trace(model, r=r, lat=lat, lon=lon)

where ``model`` is a `MASOutput` which must have all three components of the
magnetic field available.

The tracer has two configurable options:

- ``max_steps`` is the maximum number of steps that an individual field line
  can have. This is set to ``'auto'`` by default, which will allocate four
  times the steps needed to travel radially from the inner to the outer
  boundary of the model.
- ``step_size`` is the size of individual steps along the field line, as a
  multiple of the radial cell size. This is set to ``1`` by default.

For a full example see :ref:`sphx_glr_auto_examples_tracing_tracing_pyvista.py`.

``flines`` is a :class:`~psipy.tracing.FieldLines` object, that stores a
series of field lines. Each field line can be accessed by indexing the
:class:`~psipy.tracing.FieldLines` with an integer.

Saving and loading
------------------
Field lines can be saved using :meth:`~psipy.tracing.FieldLines.save` and
:meth:`~psipy.tracing.FieldLines.load`. The field lines are saved to a
``.npz`` file using `numpy.savez_compressed`.

Visualising
-----------
Although it is possible to plot field lines in 3D using Matplotlib, this is
not recommended as performance is poor and Matplotlib is not a true 3D
rendering library.

Instead the `pyvista` library can be used to visualise in 3D. This is a
Python wrapper around the popular Visualisation Toolkit (VTK).

To start we we need to create a plotting window, called a 'plotter':

.. code-block:: python

  from psipy.visualization.pyvista import MASPlotter

  plotter = MASPlotter(model)

Once we have a plotter, we can add field lines to it. In this example
we'll colour the field lines by their polarity near the inner boundary of the
model:

.. code-block:: python

  for fline in flines:
    # Set color with polarity near the inner boundary
    color = br.sample_at_coords(np.mod(fline.lon[1], 2 * np.pi * u.rad),
                                fline.lat[1],
                                fline.r[1] * u.R_sun) > 0
    color = {0: 'red', 1: 'blue'}[int(color)]
    # Add field line to the plotter
    plotter.add_fline(fline, color=color)

Finally, to show the plotting window we call:

.. code-block:: python

  plotter.show()

This will open an interactive window where you can change the view with the
mouse.
