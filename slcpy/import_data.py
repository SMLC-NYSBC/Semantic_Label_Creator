"""
    Class module to load 3D .tif file
    :param str src_tif: source of the 3D .tif file
    :param str src_am: source of the spatial graph for corresponding 3D .tif
    :param int pixel_size: numeric value of pixel size

    Done: Collect information about input et (image_size, file_name)
    Done: Build empty .tif file for semantic labels
    Done: Load ASCI .am file with 3D coordinates

    :author Robert Kiewisz

"""
from os import path

import numpy as np
from skimage import io


class ImportDataFromAmira:
    def __init__(self, src_tiff, src_am, pixel_size=None):
        self.src_tiff = src_tiff
        self.src_am = src_am
        self.pixel_size = pixel_size

        try:
            self.image = io.imread(self.src_tiff)
        except RuntimeWarning:
            raise Warning("Directory or input .tiff file is not correct...")

        if not path.isfile(self.src_tiff[:-3] + "am"):
            raise Warning("Missing corresponding .am file...")

        self.spatial_graph = open(
            src_am,
            "r",
            encoding="iso-8859-1"
        ).read().split("\n")

    def empty_semantic_label(self):
        return np.zeros(self.image.shape, 'int8')

    def image_data(self):
        return self.image

    def get_segments(self):
        # Find line starting with EDGE { int NumEdgePoints }
        segments = str([
            word for word in self.spatial_graph if word.startswith('EDGE { int NumEdgePoints }')
        ])
        segment_start = "".join((ch if ch in "0123456789" else " ") for ch in segments)
        segment_start = [int(i) for i in segment_start.split()]

        # Find in the line directory that starts with @..
        segment_start = int(self.spatial_graph.index("@" + str(segment_start[0]))) + 1

        # Find line define EDGE ... <- number indicate number of segments
        segments = str([
            word for word in self.spatial_graph if word.startswith('define EDGE')
        ])
        segment_finish = "".join((ch if ch in "0123456789" else " ") for ch in segments)
        segment_finish = [int(i) for i in segment_finish.split()]
        segment_no = int(segment_finish[0])
        segment_finish = segment_start + int(segment_finish[0])

        # Select all lines between @.. (+1) and number of segments
        segments = self.spatial_graph[segment_start:segment_finish]
        segments = [i.split(' ')[0] for i in segments]

        # return an array of number of points belonged to each segment
        df = np.zeros((segment_no, 1), dtype="int")
        df[0:segment_no, 0] = [int(i) for i in segments]

        return df

    def __find_points(self):
        # Find line starting with POINT { float[3] EdgePointCoordinates }
        points = str([
            word for word in self.spatial_graph if word.startswith('POINT { float[3] EdgePointCoordinates }')
        ])
        # Find in the line directory that starts with @..
        points_start = "".join((ch if ch in "0123456789" else " ") for ch in points)
        points_start = [int(i) for i in points_start.split()]
        # Find line that start with the directory @.. and select last one
        points_start = int(self.spatial_graph.index("@" + str(points_start[1]))) + 1

        # Find line define POINT ... <- number indicate number of points
        points = str([
            word for word in self.spatial_graph if word.startswith('define POINT')
        ])
        points_finish = "".join((ch if ch in "0123456789" else " ") for ch in points)
        points_finish = [int(i) for i in points_finish.split()][0]
        points_no = points_finish
        points_finish = points_start + points_finish

        # Select all lines between @.. (-1) and number of points
        points = self.spatial_graph[points_start:points_finish]

        # return an array of all points coordinates in pixel
        df = np.zeros((points_no, 3), dtype="float")
        for j in range(3):
            coord = [i.split(' ')[j] for i in points]
            df[0:points_no, j] = [float(i) for i in coord]

        return df

    def __read_tiff_transformation(self):
        # This method read the header of ET (.am) file and determines global
        # transformation for all coordinates

        et = open(
            self.src_tiff[:-3] + "am",
            "r",
            encoding="iso-8859-1"
        )

        lines_in_et = et.read(10000).split("\n")
        transformation_list = str([
            word for word in lines_in_et if word.startswith('    BoundingBox')
        ]).split(" ")

        trans_x, trans_y, trans_z = (
            float(transformation_list[5]),
            float(transformation_list[7]),
            float(transformation_list[9])
        )
        return trans_x, trans_y, trans_z

    def pixel_size_in_et(self):
        # If not specified by user, pixel size is first searched in .tif file
        # if not found than the pixel size is estimated

        # Estimation is done by an assumption that points can be found on the top
        # and the bottom surface
        # pixel_size = points_dist_in_z[A] / pixel_no[px]

        if self.pixel_size is None:
            pixel_in_z = int(self.image.shape[0] - 1)
            z_coord = self.__find_points()
            min_point_in_z = min(z_coord[0:len(z_coord), 2])
            max_point_in_z = max(z_coord[0:len(z_coord), 2])
            physical_length = abs(max_point_in_z - min_point_in_z)  # in [Angstrom]

            return round(physical_length / pixel_in_z, 2)
        else:
            return self.pixel_size

    def get_points(self):
        # Generate table of all points with coordinates in pixel
        pixel_size = self.pixel_size_in_et()
        transformation = self.__read_tiff_transformation()
        points_coord = self.__find_points()

        points_coord[0:len(points_coord), 0] = points_coord[0:len(points_coord), 0] - transformation[0]
        points_coord[0:len(points_coord), 1] = points_coord[0:len(points_coord), 1] - transformation[1]
        points_coord[0:len(points_coord), 2] = points_coord[0:len(points_coord), 2] - transformation[2]

        return points_coord / pixel_size
