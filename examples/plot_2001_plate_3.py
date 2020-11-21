"""
Plotting constant longitude slices
==================================
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
phi_idx = 40

fig = plt.figure()
axs = [plt.subplot(1, 3, i + 1, projection='polar') for i in range(3)]

ax = axs[0]
model['vr'].plot_phi_cut(phi_idx, ax=ax, cbar_kwargs=cbar_kwargs)

ax = axs[1]
rho = model['rho']
rho_r2 = rho.radial_normalized(2)
rho_r2.plot_phi_cut(phi_idx, ax=ax, cbar_kwargs=cbar_kwargs)

ax = axs[2]
p = model['p']
p_r3 = p.radial_normalized(3)
p_r3.plot_phi_cut(phi_idx, ax=ax, cbar_kwargs=cbar_kwargs)

# Contour br
for ax in axs:
    model['br'].contour_phi_cut(phi_idx, levels=[0], ax=ax,
                                colors='white', linestyles='--', linewidths=1)

plt.show()
