"""
Reading and visualising PLUTO runs
==================================
"""
###############################################################################
# First, load the required modules.
import matplotlib.pyplot as plt

from psipy.model import PLUTOOutput

###############################################################################
# Load a set of PLUTO output files.
pluto_path = "/Users/dstansby/github/psipy/data/pluto"
model = PLUTOOutput(pluto_path)

###############################################################################
# Each PLUTO model contains a number of variables. The variable names can be
# accessed using the ``.variables`` attribute.
print(model.variables)

###############################################################################
# Plot a cut of the model at a constant radius
fig, ax = plt.subplots()
model["rho"].plot_radial_cut(0, ax=ax)

###############################################################################
# Plot a cut of the model at a constant longitude.
fig = plt.figure()
ax = plt.subplot(111, projection="polar")
model["rho"].plot_phi_cut(75, ax=ax)

###############################################################################
# Add the current sheet
fig = plt.figure()
ax = plt.subplot(111, projection="polar")
model["rho"].plot_phi_cut(75, ax=ax)
model["Bx1"].contour_phi_cut(75, levels=[0], ax=ax, colors="white")
plt.show()
