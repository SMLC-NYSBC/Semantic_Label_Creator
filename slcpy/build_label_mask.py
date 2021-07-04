"""

    Module to construct shape of a label

    :param int radius: radius or a circle in nm
    :param int pixel_size: size of a pixel

    :author Robert Kiewisz

"""
import numpy as np


def build_circle_v2(radius, pixel_size):
    dim = round(radius / pixel_size)
    circle = np.zeros((dim, dim))
    x0, y0 = (round((dim / 2)), round((dim / 2)))

    for x in range(dim):
        dx = int(x0 - x)
        for y in range(dim):
            dy = int(y0 - y)
            distance_squared = dx*dx + dy*dy

            if distance_squared <= dim:
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
