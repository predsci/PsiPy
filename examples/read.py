from psipy.model import MASOutput
import matplotlib.pyplot as plt

mas_path = 'data/corona'
model = MASOutput(mas_path)

ax = plt.subplot(111, projection='polar')
model.vr.plot_phi_cut(75, ax=ax)
plt.show()
