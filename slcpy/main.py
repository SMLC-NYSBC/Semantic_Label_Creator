from time import sleep

import numpy as np
from tqdm import tqdm

from slcpy.build_label_mask import draw_label
from slcpy.import_data import ImportDataFromAmira
from slcpy.interpolation import interpolation_3D


def trim_label_mask(points, image, label_mask):
    """
        Module to load 3D .tif file
        :param str points: 3D coordinates of pitons
        :param array image: corresponding image for the labels
        :param array label_mask: empty label mask

        :author Robert Kiewisz
    """
    max_x, min_x = max(points[:, 0]), min(points[:, 0])
    max_y, min_y = max(points[:, 1]), min(points[:, 1])
    max_z, min_z = max(points[:, 2]), min(points[:, 2])

    image_trim = image[
                 int(min_z):int(max_z),
                 int(min_y):int(max_y),
                 int(min_x):int(max_x)
                 ]
    label_mask_trim = label_mask[
                      int(min_z):int(max_z),
                      int(min_y):int(max_y),
                      int(min_x):int(max_x)
                      ]

    points[:, 0] = points[:, 0] - min_x
    points[:, 1] = points[:, 1] - min_y
    points[:, 2] = points[:, 2] - min_z

    return image_trim, label_mask_trim, points


def slcpy(dir_path,
          pixel_size=None, circle_size=125,
          multi_layer=False, trim_mask=True):
    """
        Class module to load 3D .tif file
        :param str dir_path: path direction of the input file *.tif
        :param str pixel_size: pixel size in Angstrom
        :param int circle_size: size of a circle the label mask in Angstrom
        :param bool trim_mask: True/False statement for trimming input data
        :param bool multi_layer: single, or unique value for each lines

        :author Robert Kiewisz
    """

    img = ImportDataFromAmira(
        dir_path,
        dir_path[:-3] + r"CorrelationLines.am",
        pixel_size
    )
    label_mask = img.empty_semantic_label()
    image = img.image_data()

    if pixel_size is None:
        pixel_size = img.pixel_size_in_et().astype("int8")

    segments = img.get_segments()
    points = img.get_points().round()
    r = round((circle_size / 2) / pixel_size)

    if trim_mask:
        image, label_mask, points = trim_label_mask(
            points,
            image,
            label_mask
        )

    if multi_layer:
        label_mask = np.stack((label_mask,) * 3, axis=-1)
        segment_color = [255, 255, 255]
    else:
        segment_color = [1]

    for i in tqdm(range(len(segments))):
        sleep(0.001)

        start_point = int(sum(segments[0:i]))
        stop_point = start_point + int(segments[i])
        mt = interpolation_3D(points[start_point:stop_point])

        if multi_layer:
            segment_color = list(np.random.choice(range(256), size=3))

        for j in range(len(mt)):
            c = mt[j, :3]
            label_mask = draw_label(r, c, label_mask, segment_color)

    return image, label_mask
