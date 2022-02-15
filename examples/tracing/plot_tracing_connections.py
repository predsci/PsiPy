"""
Reading and visualising MAS runs
================================
"""
###############################################################################
# First, load the required modules.
import astropy.constants as const
import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

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

nseeds = 5
# Radius
r = np.ones(nseeds**2) * 40
# Some points near the equatorial plane
lat = np.linspace(-10, 10, nseeds**2, endpoint=False) * u.deg
# Choose random longitudes
lon = np.random.rand(nseeds**2) * 360 * u.deg

# Do the tracing!
xs = tracer.trace(model, r=r, lat=lat, lon=lon)

###############################################################################
# xs is a list, with each item containing the field line coordinates.
print(xs[0])

###############################################################################
# To easily visualise the result, here we use Matplotlib. Note that Matplotlib
# is not a 3D renderer, so has several drawbacks (including performance).
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

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
    ax.plot(x, y, z, color=color, linewidth=2)

lim = 60
ax.set_xlim(-60, 60)
ax.set_ylim(-60, 60)
ax.set_zlim(-60, 60)
plt.show()
