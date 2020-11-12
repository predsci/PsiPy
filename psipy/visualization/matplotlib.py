from matplotlib.projections.polar import ThetaFormatter


def clear_axes_labels(ax):
    ax.set_xlabel('')
    ax.set_ylabel('')


def set_theta_formatters(ax):
    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_major_formatter(ThetaFormatter())
        axis.set_minor_formatter(ThetaFormatter())
