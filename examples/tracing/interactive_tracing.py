"""
Manual field line seeds
=======================
How to interactively choose field line seed points using the mouse.
"""
###############################################################################
# First, load the required modules.

from psipy.data import sample_data
from psipy.model import MASOutput
from psipy.visualization.pyvista import MASPlotter

###############################################################################
# Load a set of MAS output files.
mas_path = sample_data.mas_sample_data()
model = MASOutput(mas_path)

###############################################################################
# To visualise the result create a pyvista plotter window. To interactively
# trace field lines, we then create a sphere to trace the field lines from.
#
# Once the window pops up, you can place your mouse over somewhere on the
# sphere and click "p" to trace a field line from that point.
#
# Note that we've used the second r coordinate in the model to trace the
# field lines from. Choosing the first coordinate (the inner boundary of the
# model) will lead to surprising edge effects.

plotter = MASPlotter(model)
plotter.add_tracing_seed_sphere(model["br"].r_coords[1])
plotter.show()
