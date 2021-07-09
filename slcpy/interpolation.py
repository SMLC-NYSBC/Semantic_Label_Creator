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

    :author Robert Kiewisz

"""
import numpy as np


# Interpolate 1D axis
def interpolation_1D(start, stop, max_len):
    points_seq = np.linspace(
        int(start),
        int(stop),
        max_len
    ).round()

    return points_seq


# An interpolation method to calculated continuity between set of points
def interpolation_3D(points):
    interpolated = np.zeros(
        (0, 3),
        dtype=int
    )

    for i in range(len(points)):
        if i == len(points)-1 or points[i + 1, 2] in (points[i, 2], int(points[i, 2] + 1)):
            interpolated = np.append(interpolated,
                                     points[i:i + 1, :3],
                                     axis=0
                                     )
        else:
            max_len = int(abs(points[i, 2] - points[i+1, 2]) + 1)
            df = np.zeros((
                max_len,
                3
            ))

            x = interpolation_1D(points[i, 0],
                                 points[i + 1, 0],
                                 max_len
                                 )
            y = interpolation_1D(points[i, 1],
                                 points[i + 1, 1],
                                 max_len
                                 )
            z = interpolation_1D(points[i, 2],
                                 points[i + 1, 2],
                                 max_len
                                 )

            df[0:max_len, 0] = x
            df[0:max_len, 1] = y
            df[0:max_len, 2] = z
            interpolated = np.append(interpolated,
                                     df,
                                     axis=0
                                     )

    return interpolated
