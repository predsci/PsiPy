"""
Sampling data from a 3D model
=============================

In this example we'll see how to sample a 3D model output at arbitrary points
within the model domain.
"""
###############################################################################
# First, load the required modules.
from psipy.model import MASOutput
import astropy.constants as const
import astropy.units as u

import matplotlib.pyplot as plt
import numpy as np

###############################################################################
# Load a set of MAS output files, and get the number density variable from the
# model run.
mas_path = '/Users/dstansby/github/psipy/data/helio'
model = MASOutput(mas_path)
rho = model['rho']

###############################################################################
# Choose a set of 1D points to interpolate the model output at.
#
# Here we keep a constant radius, and a set of longitudes that go all the way
# from 0 to 360 degrees. Then we choose two different, but close latitude
# values, and plot the results.
#
# As expected, the values at 0 and 360 degrees are the same, and the profiles
# are similar, but different, due to the small difference in latitude.
fig, ax = plt.subplots()

npoints = 1000
r = 50 * np.ones(npoints) * const.R_sun
lon = np.linspace(0, 360, npoints) * u.deg

for latitude in [0, 1] * u.deg:
    lat = latitude * np.ones(npoints)
    samples = rho.sample_at_coords(lon, lat, r)

    ax.plot(lon, samples, label='lat = ' + str(latitude))

ax.legend()
ax.set_xlim(0, 360)
ax.set_ylim(bottom=0)
ax.set_xlabel('Longitude (deg)')
ax.set_ylabel(r'$\rho$ (cm$^{-3}$)')
ax.set_xticks([0, 90, 180, 270, 360])
plt.show()
