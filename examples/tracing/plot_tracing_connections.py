"""
Reading and visualising MAS runs
================================
"""
###############################################################################
# First, load the required modules.
import astropy.constants as const
import astropy.units as u
from astropy.coordinates import spherical_to_cartesian
import numpy as np
from psipy.model import MASOutput
from psipy.data import sample_data
from psipy.tracing import FortranTracer

import matplotlib.pyplot as plt

###############################################################################
# Load a set of MAS output files.
mas_path = sample_data.mas_helio()
model = MASOutput(mas_path)
tracer = FortranTracer(step_size=0.1)

nseeds = 15
r0 = 40.
lat = np.linspace(-np.pi / 5, np.pi / 5, nseeds**2, endpoint=False)
lon = np.random.rand(nseeds**2) * 2 * np.pi
r = np.ones(nseeds**2) * r0

seeds = np.column_stack([lon, lat, r])
xs = tracer.trace(seeds, model, 'b')

import pyvista as pv
p = pv.Plotter()
br = model['br']
for line in xs:
    color = br.sample_at_coords(np.mod(line[2, 0], 2 * np.pi) * u.rad,
                                    line[2, 1] * u.rad,
                                    line[2, 2] * const.R_sun) > 0
    x = line[:, 2] * np.cos(line[:, 1]) * np.cos(line[:, 0])
    y = line[:, 2] * np.cos(line[:, 1]) * np.sin(line[:, 0])
    z = line[:, 2] * np.sin(line[:, 1])
    color = {0: 'red', 1: 'blue'}[int(color)]
    p.add_lines(np.column_stack([x, y, z]), color=color, width=3)

p.show()
