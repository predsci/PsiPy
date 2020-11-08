"""
Reading and visualising MAS runs
================================
"""
###############################################################################
# First, load the required modules.
from psipy.model import MASOutput
import matplotlib.pyplot as plt

###############################################################################
# Load a set of MAS output files.
mas_path = '../data/helio'
model = MASOutput(mas_path)

###############################################################################
# Plot a cut of the model at a constant theta value.
fig = plt.figure()
ax = plt.subplot(111, projection='polar')
model.rho.plot_theta_cut(75, ax=ax)

###############################################################################
# Plot a cut of the model at a constant radius value.
fig, ax = plt.subplots()
model.rho.plot_radial_cut(0, ax=ax)
plt.show()
