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
mas_path = '/Users/dstansby/github/psipy/data/helio'
model = MASOutput(mas_path)

###############################################################################
# Each MAS model contains a number of variables. The variable names can be
# accessed using the ``.variables`` attribute.
print(model.variables)

###############################################################################
# Plot a cut of the model at a constant radius.
fig, ax = plt.subplots()
model.rho.plot_radial_cut(0, ax=ax)

###############################################################################
# Plot a cut of the model at a constant longitude.
fig = plt.figure()
ax = plt.subplot(111, projection='polar')
model.rho.plot_phi_cut(75, ax=ax)


###############################################################################
# In the above plot it's hard to see detail at large radial distances, due
# to the :math:`1/r^{2}` decrease in density with distance. We can rescale the data,
# and plot it again.
scaled_rho = model.rho
scaled_rho.data = scaled_rho.data * scaled_rho.data.coords['r']**2
scaled_rho.name = 'rho r$^{2}$'

fig = plt.figure()
ax = plt.subplot(111, projection='polar')
scaled_rho.plot_phi_cut(75, ax=ax)

plt.show()
