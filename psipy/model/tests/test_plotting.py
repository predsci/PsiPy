"""
Plotting tests. These are currently just smoke tests to check the code runs,
and does not check that the correct plot is produced.
"""
import matplotlib.pyplot as plt


def test_radial_cut(mas_model):
    mas_model["rho"].plot_radial_cut(0)
    plt.close("all")


def test_contour_radial_cut(mas_model):
    mas_model["rho"].contour_radial_cut(0, [200])
    plt.close("all")


def test_phi_cut(mas_model):
    mas_model["rho"].plot_phi_cut(0)
    plt.close("all")


def test_contour_phi_cut(mas_model):
    mas_model["rho"].contour_phi_cut(0, [200])
    plt.close("all")


def test_equatorial_cut(mas_model):
    mas_model["rho"].plot_equatorial_cut()
    plt.close("all")


def test_contour_equatorial_cut(mas_model):
    mas_model["rho"].contour_equatorial_cut([200])
    plt.close("all")
