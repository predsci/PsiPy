import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.projections.polar import ThetaFormatter


def clear_axes_labels(ax):
    """
    Remove labels from both x and y axes.
    """
    ax.set_xlabel("")
    ax.set_ylabel("")


def set_theta_formatters(ax):
    """
    Set both x and y axes to have theta formatters (ie. degrees)
    """
    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_major_formatter(ThetaFormatter())
        axis.set_minor_formatter(ThetaFormatter())


def setup_radial_ax(ax):
    if ax is None:
        ax = plt.gca()
    return ax


def format_radial_ax(ax):
    ax.set_aspect("equal")
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(-np.pi / 2, np.pi / 2)
    clear_axes_labels(ax)

    # Tick label formatting
    set_theta_formatters(ax)
    ax.set_xticks(np.deg2rad(np.linspace(0, 360, 7, endpoint=True)))
    ax.set_yticks(np.deg2rad(np.linspace(-90, 90, 7, endpoint=True)))


def setup_polar_ax(ax):
    if ax is None:
        ax = plt.subplot(projection="polar")
    elif ax.name != "polar":
        raise ValueError("ax must have a polar projection")
    return ax


def format_polar_ax(ax):
    # Plot formatting
    ax.set_rlim(0)
    ax.set_thetalim(-np.pi / 2, np.pi / 2)
    clear_axes_labels(ax)

    # Tick label formatting
    # Set theta ticks
    ax.set_xticks([])


def format_equatorial_ax(ax):
    # Plot formatting
    ax.set_rlim(0)
    ax.set_thetalim(0, 2 * np.pi)
    clear_axes_labels(ax)

    # Tick label formatting
    # Remove theta ticks
    ax.set_xticks([])


def animate_time(ax, slice, quad_mesh):
    """
    Animate *slice* over the *time* dimension.
    """
    n_timesteps = len(slice.coords["time"])

    def animate(frame_number):
        time_slice = slice.isel(time=frame_number)
        quad_mesh.set_array(time_slice.data.T)
        return quad_mesh

    return FuncAnimation(ax.figure, animate, frames=n_timesteps)
