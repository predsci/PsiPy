"""
Changing the units of a plot
=============================

This example shows how to change the radial coordiantes. This is helpful if you
want to change the radial coordinates e.g. from solar radii to AU.
"""
###############################################################################
# First, load the required modules.
from psipy.model import MASOutput
from psipy.data import sample_data

import astropy.constants as const
import astropy.units as u
import matplotlib.pyplot as plt

###############################################################################
# Next, load a set of MAS output files. You will need to change this line to
# point to a folder with MAS files in them.
mas_path = sample_data.mas_sample_data()
model = MASOutput(mas_path)

###############################################################################
# Define a conversion factor from solar radii to AU, and apply this to the
# coordinates of a variable
rsun_to_au = float(const.R_sun / const.au)

br = model['br']
print(f'Old coords: {br.r_coords}')
br.r_coords = br.r_coords * rsun_to_au
print(f'New coords: {br.r_coords}')

###############################################################################
# Plot
cbar_kwargs = {'orientation': 'horizontal'}
ax = plt.subplot(projection='polar')
br.plot_equatorial_cut(ax=ax, cbar_kwargs=cbar_kwargs)

plt.show()
