"""Main module."""
import argparse

from .slcpy.import_data import *
from .slcpy.build_segment import *
from .slcpy.build_label_mask import *


def main():
    # # For each item in folder...
    # test_img = ImportDataFromAmira(
    #     "./data/Test_ET_Slim.tif",
    #     "./data/Test_ET_Slim.CorrelationLines.am"
    # )
    #
    # label_mask = test_img.empty_semantic_label()
    # segments = test_img.get_segments()
    # points = test_img.get_points().round()
    #
    # for i in range(len(segments)):
    #     start_point = int(sum(segments[0:i]))
    #     stop_point = start_point + int(segments[i])
    #     if i == 0:
    #         start_point = start_point + 1
    #
    #     MT = interpolation_3D(points[start_point:stop_point])
    #
    #     for j in range(len(MT)):
    #         circle_label = build_circle()
    #         label_mask = draw_circle(circle_label,
    #                                  z,
    #                                  label_mask)

    return label_mask


if __name__ == '__main__':
    main()
