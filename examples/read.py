from psipy.model import MASOutput
import matplotlib.pyplot as plt

mas_path = 'data/corona'
model = MASOutput(mas_path)

fig, ax = plt.subplots()
model.vr.plot_radial_cut(-1, ax=ax)
plt.show()
