"""
Sampling data from a 3D model
=============================
"""
###############################################################################
# First, load the required modules.
import datetime

from psipy.model import MASOutput
import astropy.constants as const
import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

from heliopy.data import psp
import heliopy.data.spice as spicedata
import heliopy.spice as spice

###############################################################################
# Load a set of MAS output files.
mas_path = '/Users/dstansby/github/psipy/data/helio'
model = MASOutput(mas_path)
print(model.variables)

###############################################################################
# Load PSP data
starttime = '2018-10-22'
endtime = '2018-11-21'
psp_data = psp.merged_mag_plasma(starttime, endtime)
print(psp_data.columns)

###############################################################################
# Generate PSP trajectory
times = psp_data.index

spicedata.get_kernel('psp')
spicedata.get_kernel('psp_pred')
psp_traj = spice.Trajectory('SPP')
psp_traj.generate_positions(times, 'Sun', 'IAU_SUN')

###############################################################################
# Sample radial velocity
vr_model = model['vr']
vr_sampled = vr_model.sample_at_coords(psp_traj.coords)

###############################################################################
# Plot
fig, ax = plt.subplots()
ax.plot(times, vr_sampled, label='Model')
ax.plot(times, psp_data.quantity('VR'), label='PSP')
ax.legend()
plt.show()
