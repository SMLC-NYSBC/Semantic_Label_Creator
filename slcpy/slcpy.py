"""
    Class module to load 3D .tif file
    :param str dir_path: path direction of the input file *.tif
    :param str pixel_size: pixel size in nm
    :param int circle_size: size of a circle that is drawn to the label mask in nm

    :author Robert Kiewisz

"""
from time import sleep

from tqdm import tqdm

from slcpy.build_label_mask import *
from slcpy.build_segment import *
from slcpy.import_data import *


def slcpy(dir_path, pixel_size=None, circle_size=125):
    img = ImportDataFromAmira(
        dir_path,
        dir_path[:-3] + r"CorrelationLines.am",
        pixel_size
    )

    if pixel_size is None:
        pixel_size = img.pixel_size_in_et()

    label_mask = img.empty_semantic_label()
    segments = img.get_segments()
    points = img.get_points().round()
    circle_shape = build_circle_v2(circle_size, pixel_size)

    for i in tqdm(range(len(segments))):
        sleep(0.001)

        start_point = int(sum(segments[0:i]))
        stop_point = start_point + int(segments[i])
        MT = interpolation_3D(points[start_point:stop_point])

        for j in range(len(MT)):
            if len(label_mask) != int(MT[j, 2]):
                circle_dim = (len(circle_shape) - 1) / 2

                x0, x1 = (int(MT[j, 0] - circle_dim - 1), int(MT[j, 0] + circle_dim))
                y0, y1 = (int(MT[j, 1] - circle_dim - 1), int(MT[j, 1] + circle_dim))

                if label_mask[int(MT[j, 2]), y0:y1, x0:x1].shape == circle_shape.shape:
                    label_mask[int(MT[j, 2]), y0:y1, x0:x1] = circle_shape

    return label_mask
