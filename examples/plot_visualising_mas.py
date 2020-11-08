"""
Reading and visualising MAS runs
================================
"""

from psipy.model import MASOutput
import matplotlib.pyplot as plt

mas_path = '../data/helio'
model = MASOutput(mas_path)

ax = plt.subplot(111, projection='polar')
model.rho.plot_phi_cut(75, ax=ax)

fig, ax = plt.subplots()
model.rho.plot_radial_cut(0, ax=ax)
plt.show()
