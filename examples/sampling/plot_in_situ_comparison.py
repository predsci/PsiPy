"""
Comparing in-situ data to model output
======================================

In this example, we'll see how to compare in-situ data taken by a spacecraft
to equivalent observables in the model along the 1D spacecraft trajectory.

This consists of three steps:
1. Load the spacecraft data
2. Generate the spacecraft trajectory at the in-situ data timestamps
3. Use this trajectory to take samples in the 3D model output

The first two steps are accomplished using ``heliopy.data``
(to get the in-situ data) and ``heliopy.spice`` (to get the trajectory). This
is then fed into `Variable.sample_at_coords` to get the model values, which
we then compare to the in-situ data.
"""
###############################################################################
# First, load the required modules.
import astropy.units as u
import heliopy.data.spice as spicedata
import heliopy.spice as spice
import matplotlib.pyplot as plt
from heliopy.data import psp

from psipy.data import sample_data
from psipy.model import MASOutput

###############################################################################
# Load a set of MAS output files.
mas_path = sample_data.mas_sample_data()
model = MASOutput(mas_path)
print(model.variables)

###############################################################################
# Load PSP data.
#
# Here we load the merged magnetic field and plasma data product, which has
# an hourly data cadence.
starttime = "2018-10-22"
endtime = "2018-11-21"
psp_data = psp.merged_mag_plasma(starttime, endtime)
# Convert the density units to 1/cm**3 so they're the same as the MAS units
psp_data.units["protonDensity"] /= u.N
print(psp_data.columns)

###############################################################################
# Generate the PSP trajectory.
#
# We take the timestamps from the previously loaded data, and use `heliopy.spice`
# to generate the trajectory at these times.
times = psp_data.index

spicedata.get_kernel("psp")
spicedata.get_kernel("psp_pred")
psp_traj = spice.Trajectory("SPP")
psp_traj.generate_positions(times, "Sun", "IAU_SUN")
psp_coords = psp_traj.coords
print(psp_coords)

###############################################################################
# Take a sample of the radial velocity.
#
# Here we start by getting the radial velocity `Variable` from the model, and
# then use the PSP corodinate information to sample it.
vr_model = model["vr"]
vr_sampled = vr_model.sample_at_coords(
    psp_coords.lon, psp_coords.lat, psp_coords.radius
)

###############################################################################
# We can now plot a comparison between the model and in-situ measurements.
fig, ax = plt.subplots()
ax.plot(times, vr_sampled, label="Model")
ax.plot(times, psp_data.quantity("VR"), label="PSP")

ax.set_ylabel(r"$v_{r}$ (km/s)")
ax.legend()
fig.autofmt_xdate()

###############################################################################
# To finish, we'll perform the same comparison, but with a few different
# variables.
fig, axs = plt.subplots(nrows=3, sharex=True)
for ax, mas_name, psp_name in zip(
    axs, ["rho", "vr", "br"], ["protonDensity", "VR", "BR"]
):
    model_var = model[mas_name]
    sampled = model_var.sample_at_coords(
        psp_coords.lon, psp_coords.lat, psp_coords.radius
    )

    in_situ = psp_data.quantity(psp_name)

    # Note that we convert the sampled data to the same units as the PSP data
    ax.plot(times, sampled.to(in_situ.unit), label="Model")
    ax.plot(times, in_situ, label="PSP")

    ax.set_ylabel(str(model_var.unit))
    ax.legend()

fig.autofmt_xdate()

plt.show()
