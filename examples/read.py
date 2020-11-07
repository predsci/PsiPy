from psipy.model import MASOutput
import matplotlib.pyplot as plt

mas_path = 'data/corona'
model = MASOutput(mas_path)
vr = model.vr
print(model.vr)

vr_slice = vr.isel(r=-1)
print(vr_slice)

fig, ax = plt.subplots()
vr_slice.plot(x='phi', y='theta', ax=ax)
ax.set_aspect('equal')
plt.show()
