"""
Sampling data from a 3D model
=============================
"""
###############################################################################
# First, load the required modules.
from psipy.model import MASOutput
import astropy.constants as const
import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

###############################################################################
# Load a set of MAS output files.
mas_path = '/Users/dstansby/github/psipy/data/helio'
model = MASOutput(mas_path)

###############################################################################
# Each MAS model contains a number of variables. The variable names can be
# accessed using the ``.variables`` attribute.
rho = model['rho']
n = 500

for thet in [0, 1]:
    r = 50 * np.ones(n) * const.R_sun
    theta = thet * np.ones(n) * u.deg
    phi = np.linspace(0, 360, n) * u.deg

    sample = rho.sample_at_coords(phi, theta, r)

    plt.plot(phi, sample)
plt.show()
