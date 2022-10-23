"""
Field lines with pyvista
========================
Visualising traced field lines with pyvista.

pyvista is a Python package that provides a wrapper to the popular VTK library
for 3D visualisation. Unlike Matplotlib this is "true" 3D rendering, and is
much more performant in comparison.
"""
###############################################################################
# First, load the required modules.
import astropy.units as u
import numpy as np

from psipy.data import sample_data
from psipy.model import PLUTOOutput
from psipy.tracing import FortranTracer
from psipy.visualization.pyvista import MASPlotter

###############################################################################
# Load a set of PLUTO output files.
pluto_path = sample_data.pluto_sample_data()
model = PLUTOOutput(pluto_path)

###############################################################################
# To trace field lines, start by creating a tracer. Then we create a set of
# seed points at which the field lines are drawn from.
tracer = FortranTracer()

nseeds = 20
r = np.ones(nseeds**2) * 0.5 * u.au
lat = np.linspace(-45, 45, nseeds**2, endpoint=False) * u.deg
lon = np.random.rand(nseeds**2) * 360 * u.deg

# Do the tracing!
flines = tracer.trace(model, r=r, lat=lat, lon=lon)
print(flines)

###############################################################################
# Visualise the results

plotter = MASPlotter(model)
for fline in flines:
    plotter.add_fline(fline)

# Add a sphere at the inner boundary of the model
plotter.add_sphere(np.min(model["Bx1"].r_coords))
plotter.show()
