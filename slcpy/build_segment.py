"""

    Module to build a continues segment in given 3D frame

    Module: interpolation_1D
    :param int start: 1D single coordinate to start interpolation
    :param int stop: 1D single coordinate to stop interpolation
    :param int max_len: 1D axis length along which the interpolation will be working

    Module: interpolation_3D
    :param array points: numpy array with points belonging to individual
        segments given by x, y, z coordinates from ImportDataFromAmira class

    :author Robert Kiewisz

"""
import numpy as np


# Interpolate 1D axis
def interpolation_1D(start, stop, max_len):
    points_seq = np.linspace(
        int(start), int(stop),
        max_len
    ).round()

    return points_seq


# An interpolation method to calculated continuity between set of points
def interpolation_3D(points):
    interpolated = np.zeros(
        (int(max(points[0:len(points), 2]) - min(points[0:len(points), 2])), 3),
        dtype=int
    )
    # Interpolate Z axis
    interpolated[0:len(interpolated), 2] = np.linspace(
        int(min(points[0:len(points), 2])), int(max(points[0:len(points), 2])),
        len(interpolated)
    ).round()

    len_counter = 0
    for i in range(len(points) - 1):
        if len_counter == 0:
            max_len = abs(int(points[i, 2]) - int(points[i + 1, 2])) + 1
        else:
            max_len = abs(int(points[i, 2] + 1) - int(points[i + 1, 2])) + 1

        if i == int(len(points) - 2):
            max_len = max_len - 1
        len_of_seq = len_counter + max_len

        # Interpolate X, Y, Z axis
        points_seq_x = interpolation_1D(
            points[i, 0],
            points[i + 1, 0],
            max_len
        )
        points_seq_y = interpolation_1D(
            points[i, 1],
            points[i + 1, 1],
            max_len
        )

        interpolated[len_counter:len_of_seq, 0] = points_seq_x
        interpolated[len_counter:len_of_seq, 1] = points_seq_y

        len_counter = len_counter + max_len

    return interpolated
