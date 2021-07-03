"""
    Class module to load 3D .tif file
    :param str path_dir: path direction of the input file *.tif
    :param str pixel_size: pixel size in nm
    :param int circle_size: size of a circle that is drawn to the label mask in nm

    :author Robert Kiewisz

"""
from slcpy.build_label_mask import *
from slcpy.build_segment import *
from slcpy.import_data import *

from time import sleep
from tqdm import tqdm


def slcpy(path_dir, pixel_size=None, circle_size=250):
    img = ImportDataFromAmira(
        path_dir,
        path_dir[:-3] + r"CorrelationLines.am",
        pixel_size
    )

    if pixel_size is None:
        pixel_size = img.pixel_size_in_et()

    label_mask = img.empty_semantic_label()
    segments = img.get_segments()
    points = img.get_points().round()

    for i in tqdm(range(len(segments))):
        sleep(0.001)

        start_point = int(sum(segments[0:i]))
        stop_point = start_point + int(segments[i])
        MT = interpolation_3D(points[start_point:stop_point])

        for j in range(len(MT)):
            if len(label_mask) != int(MT[j, 2]):
                label_mask = draw_circle(build_circle(int(MT[j, 0]),
                                                      int(MT[j, 1]),
                                                      circle_size,
                                                      pixel_size,
                                                      len(label_mask[0,])
                                                      ),
                                         int(MT[j, 2]),
                                         label_mask
                                         )

    return label_mask
