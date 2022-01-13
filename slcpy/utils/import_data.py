import gc
from os import path
from typing import Optional

import cv2
import numpy as np
import open3d as o3d
from skimage import io
from skimage.feature.peak import peak_local_max
from skimage.morphology import skeletonize_3d
from tqdm import tqdm


class ImportDataFromAmira:
    """
    MAIN CLASS TO HANDLE 3D .TIF AND .AM DATA

    Args:
        src_tiff: source of the 3D .tif file
        src_am: source of the spatial graph for corresponding 3D .tif
        mask: If True output semnantic mask
        pixel_size: numeric value of pixel size
    """

    def __init__(self, src_tiff: str,
                 src_am: str,
                 mask: bool,
                 pixel_size=None):
        self.src_tiff = src_tiff
        self.src_am = src_am
        self.pixel_size = pixel_size

        try:
            self.image = io.imread(self.src_tiff)  # Image file [Z x Y x X]
        except RuntimeWarning:
            raise Warning("Directory or input .tiff file is not correct...")

        if not path.isfile(self.src_tiff[:-3] + "am"):
            raise Warning("Missing corresponding .am file...")

        if mask:
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
            word for word in self.spatial_graph if
            word.startswith('EDGE { int NumEdgePoints }')
        ])
        segment_start = "".join((ch if ch in "0123456789" else " ")
                                for ch in segments)
        segment_start = [int(i) for i in segment_start.split()]

        # Find in the line directory that starts with @..
        segment_start = int(self.spatial_graph.index(
            "@" + str(segment_start[0]))) + 1

        # Find line define EDGE ... <- number indicate number of segments
        segments = str([
            word for word in self.spatial_graph if word.startswith('define EDGE')
        ])
        segment_finish = "".join(
            (ch if ch in "0123456789" else " ") for ch in segments)
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
        points_start = "".join((ch if ch in "0123456789" else " ")
                               for ch in points)
        points_start = [int(i) for i in points_start.split()]
        # Find line that start with the directory @.. and select last one
        points_start = int(self.spatial_graph.index(
            "@" + str(points_start[1]))) + 1

        # Find line define POINT ... <- number indicate number of points
        points = str([
            word for word in self.spatial_graph if word.startswith('define POINT')
        ])
        points_finish = "".join(
            (ch if ch in "0123456789" else " ") for ch in points)
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
        """
        This method read the header of ET (.am) file and determines global
        transformation for all coordinates
        """

        et = open(
            self.src_tiff[:-3] + "am",
            "r",
            encoding="iso-8859-1"
        )

        lines_in_et = et.read(50000).split("\n")
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
        """
        If not specified by user, pixel size is searched in .am file

        Estimation is done by an assumption that points can be found on the top
        and the bottom surface
        pixel_size = tomogram physical size[A] / pixel_number in X[px]
        """

        if self.pixel_size is None:
            et = open(self.src_tiff[:-3] + "am",
                      "r",
                      encoding="iso-8859-1")

            lines_in_et = et.read(50000).split("\n")

            physical_size = str([word for word in lines_in_et if
                                 word.startswith('        XLen') or word.startswith(
                                     '        xLen')]).split(" ")

            if 'XLen' in physical_size or 'xLen' in physical_size:
                pixel_size = str([word for word in lines_in_et if
                                  word.startswith('        Nx') or word.startswith(
                                      '        nx')]).split(" ")

                physical_size = float(physical_size[9][:-3])
                pixel_size = float(pixel_size[9][:-3])

                return round(physical_size / pixel_size, 2)
            else:
                transformation_list = str([
                    word for word in lines_in_et if word.startswith('    BoundingBox')
                ]).split(" ")

                physical_size = float(transformation_list[6])
                pixel_size = float(self.image.shape[2])

                size = round(physical_size / pixel_size, 2)
                dim = np.array((23.2, 25.72))
                idx_size = (dim - size).argmin()

                return dim[idx_size]
        else:
            return self.pixel_size

    def get_points(self):
        """Generate table of all points with coordinates in pixel"""
        pixel_size = self.pixel_size_in_et()
        transformation = self.__read_tiff_transformation()
        points_coord = self.__find_points()

        points_coord[0:len(points_coord), 0] = points_coord[0:len(
            points_coord), 0] - transformation[0]
        points_coord[0:len(points_coord), 1] = points_coord[0:len(
            points_coord), 1] - transformation[1]
        points_coord[0:len(points_coord), 2] = points_coord[0:len(
            points_coord), 2] - transformation[2]

        return points_coord / pixel_size


class ImportSemanticMask:
    """
    MAIN MODULE TO LOAD SEMANTIC MASK

    Args:
        src_tiff: source of the 3D .tif file
        filter_small_object: Filter size to remove small object .
        clean_close_point: If True, close point will be removed.
    """

    def __init__(self,
                 src_tiff: Optional[str] = np.ndarray):
        try:
            if isinstance(src_tiff, str):
                self.image = io.imread(src_tiff)
            else:
                self.image = src_tiff
        except RuntimeWarning:
            raise Warning("Directory or input .tiff file is not correct...")

    def image_data(self):
        return self.image

    def find_maximas(self,
                     filter_small_object: Optional[int] = None,
                     down_sampling=True):
        """At each z position find point maxims and store their coordinates"""
        x, y, z = [], [], []

        if filter_small_object is not None:
            denoise_img = np.zeros(self.image.shape, dtype='int16')

            z_iter = tqdm(range(self.image.shape[0]),
                          'Removing small object from prediction...',
                          total=self.image.shape[0],
                          leave=False)
            for i in z_iter:
                slice = self.image[i, :].astype('int16')
                _, thresh = cv2.threshold(src=slice,
                                          thresh=0,
                                          maxval=255,
                                          type=cv2.THRESH_BINARY)
                kernel = np.ones(shape=(filter_small_object, filter_small_object),
                                 dtype=np.int16)
                denoise_img[i, :] = cv2.morphologyEx(src=thresh,
                                                     op=cv2.MORPH_OPEN,
                                                     kernel=kernel)

            denoise_img = abs(denoise_img.astype('int8'))
        else:
            denoise_img = self.image

        del self.image
        gc.collect()

        x, y, z = [], [], []
        sk_image = skeletonize_3d(denoise_img)

        z_iter = tqdm(range(denoise_img.shape[0]),
                      'Building point cloud..',
                      total=denoise_img.shape[0],
                      leave=False)

        """ Compute euclidean transformation for labels and build point cloud """
        for i in z_iter:
            picked_maxima = peak_local_max(sk_image[i, :],
                                           labels=denoise_img[i, :])

            z = np.append(z, np.repeat(i, len(picked_maxima)))
            y = np.append(y, picked_maxima[:, 0])
            x = np.append(x, picked_maxima[:, 1])

        coordinates = np.array((x, y, z)).astype('uint16').T

        """ Down-sampling point cloud by removing closest point """
        if down_sampling:
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(coordinates)
            coordinates_ds = np.asarray(
                pcd.voxel_down_sample(voxel_size=25).points)

            return denoise_img, coordinates, coordinates_ds

        return denoise_img, coordinates
