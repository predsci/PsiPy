"""
Field lines with Matplotlib
===========================
Visualising traced field lines with Matplotlib.
"""
###############################################################################
# First, load the required modules.
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
r = np.ones(nseeds**2) * 40 * u.R_sun
# Some points near the equatorial plane
lat = np.linspace(-10, 10, nseeds**2, endpoint=False) * u.deg
# Choose random longitudes
lon = np.random.rand(nseeds**2) * 360 * u.deg

# Do the tracing!
flines = tracer.trace(model, r=r, lat=lat, lon=lon)

###############################################################################
# flines is a list, with each item containing a field line object
print(flines[0])

###############################################################################
# To easily visualise the result, here we use Matplotlib. Note that Matplotlib
# is not a 3D renderer, so has several drawbacks (including performance).
fig = plt.figure()
ax = fig.add_subplot(projection="3d")

br = model["br"]
for fline in flines:
    # Set color with polarity on the inner boundary
    color = (
        br.sample_at_coords(
            np.mod(fline.lon[0], 2 * np.pi * u.rad),
            fline.lat[0],
            fline.r[0] * u.R_sun,
        )
        > 0
    )
    color = {0: "red", 1: "blue"}[int(color)]
    ax.plot(*fline.xyz, color=color, linewidth=2)

lim = 60
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)
ax.set_zlim(-lim, lim)
plt.show()
