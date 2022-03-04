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
import pyvista as pv
from astropy.coordinates import spherical_to_cartesian

from psipy.data import sample_data
from psipy.model import MASOutput
from psipy.tracing import FortranTracer

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
xs = tracer.trace(model, r=r, lat=lat, lon=lon)

###############################################################################
# To visualise the result we use the pyvista library, which is a Python
# wrappper around VTK.

plotter = pv.Plotter()
br = model['br']
for line in xs:
    # Set color with polarity on the inner boundary
    color = br.sample_at_coords(np.mod(line[2, 0], 2 * np.pi) * u.rad,
                                line[2, 1] * u.rad,
                                line[2, 2] * const.R_sun) > 0
    x = line[:, 2] * np.cos(line[:, 1]) * np.cos(line[:, 0])
    y = line[:, 2] * np.cos(line[:, 1]) * np.sin(line[:, 0])
    z = line[:, 2] * np.sin(line[:, 1])
    color = {0: 'red', 1: 'blue'}[int(color)]

    xyz = spherical_to_cartesian(line[:, 2],
                                 line[:, 1] * u.rad,
                                 line[:, 0] * u.rad)
    spline = pv.Spline(np.array(xyz).T)
    plotter.add_mesh(spline, color=color)

plotter.show()
