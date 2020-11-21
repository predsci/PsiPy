"""
Plotting equatorial slices
==========================
"""
###############################################################################
# First, load the required modules.
from psipy.model import MASOutput
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

###############################################################################
# Load a set of MAS output files.
mas_path = '/Users/dstansby/github/psipy/data/helio'
model = MASOutput(mas_path)

###############################################################################
# Each MAS model contains a number of variables. The variable names can be
# accessed using the ``.variables`` attribute.
print(model.variables)

###############################################################################
# Plot the data layout
cbar_kwargs = {'orientation': 'horizontal'}

ax = plt.subplot(projection='polar')
model['vr'].plot_equatorial_cut(ax=ax, cbar_kwargs=cbar_kwargs)

plt.show()
