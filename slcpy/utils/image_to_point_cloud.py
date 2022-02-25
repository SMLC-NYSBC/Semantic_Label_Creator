import gc
from typing import Optional

import numpy as np
from tqdm import tqdm
import tifffile.tifffile as tifffile
import cv2
from skimage.morphology import skeletonize_3d

class BuildPointCloud:
    """
    MAIN MODULE TO LOAD SEMANTIC MASK

    Args:
        src_tiff: source of the 3D .tif file in [Z x Y x X]
        filter_small_object: Filter size to remove small object .
        clean_close_point: If True, close point will be removed.
    """

    def __init__(self,
                 src_tiff: Optional[str] = np.ndarray):
        try:
            if isinstance(src_tiff, str):
                self.image = tifffile.imread(src_tiff)
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
                pcd.voxel_down_sample(voxel_size=12).points)

            return denoise_img, coordinates, coordinates_ds

        return denoise_img, coordinates
