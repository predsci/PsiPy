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
  from psipy.tracing import FortranTracer
  tracer = FortranTracer()

  # Radius
  r = [40, 45]
  lat = [0, 10] * u.deg
  lon = [0, np.pi / 4] * u.rad
  xs = tracer.trace(model, r=r, lat=lat, lon=lon)

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
