"""
Plotting radial slices
======================

This example shows how to plot slices of constant radial distance from a MAS model
output.
"""
###############################################################################
# First, load the required modules.
import matplotlib.pyplot as plt

from psipy.data import sample_data
from psipy.model import MASOutput

###############################################################################
# Next, load a set of MAS output files. You will need to change this line to
# point to a folder with MAS files in them.
mas_path = sample_data.mas_sample_data()
model = MASOutput(mas_path)

###############################################################################
# Each MAS model contains a number of variables. The variable names can be
# accessed using the ``.variables`` attribute.
print(model.variables)

###############################################################################
# Set parameters for plotting. The first line will give us a horizontal
# errorbar underneath the plots. The second line is the index to select for the
# radial slice.
cbar_kwargs = {"orientation": "horizontal"}
r_idx = 139


###############################################################################
# Plot the slices
fig, axs = plt.subplots(ncols=3, tight_layout=True)

ax = axs[0]
model["vr"].plot_radial_cut(r_idx, ax=ax, cbar_kwargs=cbar_kwargs)
model["br"].contour_radial_cut(r_idx, levels=[0], ax=ax, colors="white")
ax = axs[1]
model["rho"].plot_radial_cut(r_idx, ax=ax, cbar_kwargs=cbar_kwargs)
model["br"].contour_radial_cut(r_idx, levels=[0], ax=ax, colors="white")
ax = axs[2]
model["br"].plot_radial_cut(r_idx, ax=ax, cbar_kwargs=cbar_kwargs)
model["br"].contour_radial_cut(r_idx, levels=[0], ax=ax, colors="black")

plt.show()
