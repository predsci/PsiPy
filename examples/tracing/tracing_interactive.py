"""
Field lines with pyvista
========================
Visualising traced field lines with pyvista.
"""
###############################################################################
# First, load the required modules.
import astropy.constants as const
import astropy.units as u
import numpy as np

from psipy.data import sample_data
from psipy.model import MASOutput
from psipy.tracing import FortranTracer
from psipy.visualization.pyvista import MASPlotter

###############################################################################
# Load a set of MAS output files.
mas_path = sample_data.mas_sample_data()
model = MASOutput(mas_path)

###############################################################################
# To trace field lines, start by creating a tracer. Then we create a set of
# seed points at which the field lines are drawn from.
tracer = FortranTracer()

nseeds = 20
# Radius
r = np.ones(nseeds**2) * 40
# Some points near the equatorial plane
lat = np.linspace(-45, 45, nseeds**2, endpoint=False) * u.deg
# Choose random longitudes
lon = np.random.rand(nseeds**2) * 360 * u.deg

# Do the tracing!
flines = tracer.trace(model, r=r, lat=lat, lon=lon)

###############################################################################
# To visualise the result we use the pyvista library, which is a Python
# wrappper around VTK.

plotter = MASPlotter()
br = model['br']
for fline in flines:
    # Set color with polarity on the inner boundary
    color = br.sample_at_coords(np.mod(fline.lon[0], 2 * np.pi * u.rad),
                                fline.lat[0],
                                fline.r[0] * const.R_sun) > 0
    color = {0: 'red', 1: 'blue'}[int(color)]
    plotter.add_fline(fline, color=color)

plotter.show()
