"""
Plotting tests. These are currently just smoke tests to check the code runs,
and does not check that the correct plot is produced.
"""


def test_radial_cut(mas_model):
    mas_model['rho'].plot_radial_cut(0)


def test_contour_radial_cut(mas_model):
    mas_model['rho'].contour_radial_cut(0, [200])
