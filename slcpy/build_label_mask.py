"""

    Module draw_label to construct shape of a label

    :param int r: radius of a circle in Angstrom
    :param int c0: first point for interpolation
    :param int c1: second point for interpolation
    :param array label_mask: array of a mask on which circle is drawn

    :author Robert Kiewisz

"""
import numpy as np
from numpy.linalg import norm
import skimage.draw


def vector_angle(v, u):
    return np.arccos(norm(np.dot(v, u)) / (norm(v) + norm(u)))


def draw_label(r, c0, c1, label_mask):
    c = c1 - c0

    x, y, z = np.eye(3)

    minor_axis = r
    major_axis = r

    alpha = vector_angle(x, c0 + c)

    nz, ny, nx = label_mask.shape

    for i in range(int(c0[2]), int(c1[2])):
        lam = - (c0[2] - i) / c[2]
        p = c0 + c * lam
        y, x = skimage.draw.ellipse(p[1], p[0], major_axis, minor_axis, shape=(ny, nx), rotation=alpha)
        label_mask[i, y, x] = 1

    return label_mask


def build_circle_v2(diameter, pixel_size):
    # Module to construct shape of a label
    #
    # :param int diameter: radius or a circle in Angstrom
    # :param int pixel_size: size of a pixel

    dim = round(diameter / pixel_size)
    if dim % 2 == 0:
        dim = dim + 1

    circle = np.zeros((dim, dim))
    x0, y0 = (round(int(len(circle) / 2)), round(int(len(circle) / 2)))

    for x in range(dim):
        dx = int(x - x0)
        for y in range(dim):
            dy = int(y - y0)
            distance_squared = (dx * dx + dy * dy) ** .5
            if distance_squared <= dim / 2:
                circle[x, y] = 1

    return circle

# Module: build_circle
# P = {(x, y:(x - x0) ^ 2 + (y - y0) ^ 2 <= r ^ 2}
#
# :param int x0, y0: center or a circle in pixel
# :param int circle_size: diameter of a circle
# :param int pixel_size: size of a pixel

# def build_circle(x0, y0, circle_size, pixel_size, img_size)
#     radius_squared = circle_size / pixel_size
#     circle = np.zeros((0, 2))
#
#     for x in range(img_size):
#         for y in range(img_size):
#             dx = x - x0
#             dy = y - y0
#             distance_squared = dx * dx + dy * dy
#
#             if distance_squared <= radius_squared:
#                 circle = np.append(circle,
#                                    np.array((x, y)).reshape((1, 2)),
#                                    axis=0
#                                    )
#     return circle


# Module: draw_circle
# :param array circle: output from build_circle() method
# :param int z: Z dimension on which circle should be drawn
# :param array label_mask: array to which circle should be added
#
# def draw_circle(circle, z, label_mask):
#     for i in range(len(circle)):
#         x = int(circle[i, 0])
#         y = int(circle[i, 1])
#
#         if label_mask[z, x, y] != 1:
#             label_mask[z, x, y] = 1
#
#     return label_mask
