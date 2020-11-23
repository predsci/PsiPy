"""
Plotting radial slices
======================

This example shows how to plot slices of constant radial distance from a MAS model
output.
"""
###############################################################################
# First, load the required modules.
from psipy.model import MASOutput
import matplotlib.pyplot as plt

###############################################################################
# Next, load a set of MAS output files. You will need to change this line to
# point to a folder with MAS files in them.
mas_path = '/Users/dstansby/github/psipy/data/helio'
model = MASOutput(mas_path)

###############################################################################
# Each MAS model contains a number of variables. The variable names can be
# accessed using the ``.variables`` attribute.
print(model.variables)

###############################################################################
# Set parameters for plotting. The first line will give us a horizontal
# errorbar underneath the plots. The second line is the index to select for the
# radial slice.
cbar_kwargs = {'orientation': 'horizontal'}
r_idx = 139


###############################################################################
# Plot the slices
fig, axs = plt.subplots(nrows=2, ncols=3)

ax = axs[0, 0]
model['vr'].plot_radial_cut(r_idx, ax=ax, cbar_kwargs=cbar_kwargs)
model['br'].contour_radial_cut(r_idx, levels=[0], ax=ax, colors='white')
ax = axs[0, 1]
model['vp'].plot_radial_cut(r_idx, ax=ax, cbar_kwargs=cbar_kwargs)
model['br'].contour_radial_cut(r_idx, levels=[0], ax=ax, colors='black')
ax = axs[0, 2]
model['vt'].plot_radial_cut(r_idx, ax=ax, cbar_kwargs=cbar_kwargs)
model['br'].contour_radial_cut(r_idx, levels=[0], ax=ax, colors='black')

ax = axs[1, 0]
model['rho'].plot_radial_cut(r_idx, ax=ax, cbar_kwargs=cbar_kwargs)
model['br'].contour_radial_cut(r_idx, levels=[0], ax=ax, colors='white')
ax = axs[1, 1]
model['p'].plot_radial_cut(r_idx, ax=ax, cbar_kwargs=cbar_kwargs)
model['br'].contour_radial_cut(r_idx, levels=[0], ax=ax, colors='white')

plt.show()
