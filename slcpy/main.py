"""

    Class module to load 3D .tif file
    :param str dir_path: path direction of the input file *.tif
    :param str pixel_size: pixel size in Angstrom
    :param int circle_size: size of a circle that is drawn to the label mask in Angstrom

    :author Robert Kiewisz

"""
from time import sleep

from tqdm import tqdm

from slcpy.build_label_mask import draw_label
from slcpy.build_segment import interpolation_3D
from slcpy.import_data import ImportDataFromAmira


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
    # circle_shape = build_circle_v2(circle_size, pixel_size)
    r = round((circle_size / 2) / pixel_size)

    for i in tqdm(range(len(segments))):
        sleep(0.001)

        start_point = int(sum(segments[0:i]))
        stop_point = start_point + int(segments[i])
        MT = interpolation_3D(points[start_point:stop_point])

        for j in range(len(MT)-1):
            c0 = MT[j, :3]
            c1 = MT[j+1, :3]
            label_mask = draw_label(r, c0, c1, label_mask)

    return label_mask
