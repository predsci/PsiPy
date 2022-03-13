from dataclasses import dataclass

import astropy.units as u
import numpy as np
from astropy.coordinates import spherical_to_cartesian

__all__ = ['FieldLines', 'FieldLine']


class FieldLines:
    """
    A container for multiple field lines.
    """
    def __init__(self, xs):
        """
        Parameters
        ----------
        xs : list[numpy.ndarray]
            Field lines. Each array must have lon, lat, r columns in that
            order.
        """
        self.flines = [FieldLine(r=x[:, 2], lat=x[:, 1], lon=x[:, 0])
                       for x in xs]

    def __getitem__(self, i):
        return self.flines[i]

    def __len__(self):
        return len(self.flines)

    def __iter__(self):
        for fline in self.flines:
            yield fline


@dataclass
class FieldLine:
    """
    A single field line.
    """
    r: np.ndarray
    lat: np.ndarray
    lon: np.ndarray

    def __init__(self, *, r, lat, lon):
        self.r = r
        self.lat = lat * u.rad
        self.lon = lon * u.rad

    @property
    def xyz(self):
        """
        Cartesian coordinates as a (n, 3) shaped array.
        """
        return np.array(spherical_to_cartesian(self.r, self.lat, self.lon)).T
