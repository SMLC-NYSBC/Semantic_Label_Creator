"""

    Module to build a continues segment in given 3D frame

    Module: interpolation_1D
    :param int start: 1D single coordinate to start interpolation
    :param int stop: 1D single coordinate to stop interpolation
    :param int max_len: 1D axis length along which the interpolation will be working

    Module: interpolation_3D
    :param array points: numpy array with points belonging to individual
        segments given by x, y, z coordinates from ImportDataFromAmira class

    Bugfix: fix interpolation_3D for horizontally splayed out segments
        Fixed: in v0.1.8
    :author Robert Kiewisz

"""
import numpy as np


def interpolation_1D(start, stop, max_len):
    points_seq = np.linspace(
        int(start),
        int(stop),
        max_len
    ).round()

    return points_seq


def interpolation_3D(points):
    interpolated = np.zeros(
        (0, 3),
        dtype=int
    )

    for i in range(0, len(points) - 1):
        x = points[i:i + 2, 0]
        y = points[i:i + 2, 1]
        z = points[i:i + 2, 2]

        x_len = abs(x[0] - x[1])
        y_len = abs(y[0] - y[1])
        z_len = abs(z[0] - z[1])
        max_len = max(
            enumerate([x_len, y_len, z_len]),
            key=(lambda k: k[1])
        )

        x_new = interpolation_1D(x[0],
                                 x[1],
                                 int(max_len[1])
                                 )

        y_new = interpolation_1D(y[0],
                                 y[1],
                                 int(max_len[1])
                                 )

        z_new = interpolation_1D(z[0],
                                 z[1],
                                 int(max_len[1])
                                 )

        df = np.zeros((
            int(max_len[1]),
            3
        ))

        df[0:int(max_len[1]), 0] = list(map(int, x_new))
        df[0:int(max_len[1]), 1] = list(map(int, y_new))
        df[0:int(max_len[1]), 2] = list(map(int, z_new))

        interpolated = np.append(interpolated,
                                 df,
                                 axis=0
                                 )

    return interpolated
