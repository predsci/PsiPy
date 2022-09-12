"""
Animating plots
===============
How to make animated plots.

If multiple timesteps are loaded, then it is possible to make an animation with
any of the plotting methods associated with a `Variable` object.
"""
###############################################################################
# First, load the required modules.
from psipy.data import sample_data
from psipy.model import MASOutput

###############################################################################
# Next, load a set of MAS output files. Here we just download two succesive
# Carrington rotations, but you can change this line to point to any directory
# that has data files spanning multiple timesteps of a simulation.
mas_path = sample_data.mas_helio_timesteps()
model = MASOutput(mas_path)

###############################################################################
# Get a variable from the model output. We can also inspect the variable to see
# how many timesteps it has.
vr = model["vr"]
print(f"Number of timesteps: {vr.n_timesteps}")


###############################################################################
# We can now create an animation. In this example we plot a radial cut at the
# outer boundary of the model (i.e. a radial index of ``-1``).
animation = vr.plot_radial_cut(r_idx=-1)

###############################################################################
# Note that ``animation`` is a `matplotlib.animation.Animation` object. To save
# the animation to disk you can use the
# :meth:`~matplotlib.animation.Animation.save` method, e.g.:
# ``animation.save('mymovie.mp4')``
