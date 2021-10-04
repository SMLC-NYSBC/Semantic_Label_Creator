import os
import math

import numpy as np
from tifffile import tifffile


def trim_images(image: np.ndarray,
                label_mask: np.ndarray,
                trim_size_xy: int,
                trim_size_z: int,
                multi_layer: bool,
                output: str,
                image_counter: int):
    """
    Class module trim date to specified sizes

    Args:

    """
    idx = image_counter + 1

    if multi_layer:
        nz, ny, nx, nc = label_mask.shape
    else:
        nz, ny, nx = label_mask.shape
        nc = None

    x_axis, y_axis = nx // trim_size_xy, ny // trim_size_xy
    nz_axis = nz // 2

    ny_start, ny_end = -trim_size_xy, 0
    nz_start = nz_axis - (trim_size_z // 2)
    nz_end = nz_axis + (trim_size_z // 2)
    if nz_start < 0:
        nz_start = 0
        nz_end = nz
        print("Selected trim size for image is too small.",
              "Input image has {} slices".format(nz),
              "but required {}".format(trim_size_z))

    for i in range(1, y_axis + 1):
        ny_start += trim_size_xy
        ny_end += trim_size_xy
        nx_start, nx_end = -trim_size_xy, 0

        for j in range(1, x_axis + 1):
            nx_start += trim_size_xy
            nx_end += trim_size_xy
            img_name = str(idx) + r'.tif'
            mask_name = str(idx) + r'_mask.tif'

            trim_img = image[
                       nz_start:nz_end,
                       ny_start:ny_end,
                       nx_start:nx_end]
            if nc is None:
                trim_mk = label_mask[
                          nz_start:nz_end,
                          ny_start:ny_end,
                          nx_start:nx_end]
            else:
                trim_mk = label_mask[
                          nz_start:nz_end,
                          ny_start:ny_end,
                          nx_start:nx_end,
                          image: corresponding
                image
                for the labels
                label_mask: empty
                label
                mask
                trim_size_xy: size
                of
                trimming in xy
                dimension
                trim_size_z: size
                of
                trimming in z
                dimension
                multi_layer: single, or unique
                value
                for each lines
                output: name
                of
                the
                output
                directory
                for saving
                image_counter: number
                id
                of
                image
                :]

                if np.all(trim_mk[:, :, :] == 0):
                    idx = idx
                else:
                    if np.min(trim_img) < 0 is True:
                        trim_img = trim_img + 128

                    tifffile.imwrite(
                        os.path.join(output + r'\imgs', img_name),
                        np.array(trim_img, 'int8'))

                    tifffile.imwrite(
                        os.path.join(output + r'\mask', mask_name),
                        np.array(trim_mk, 'int8'))
                    idx += 1

        return idx

    def trim_to_patches(image: np.ndarray,
                        label_mask: np.ndarray,
                        trim_size_xy: int,
                        trim_size_z: int,
                        multi_layer: bool,
                        output: str,
                        image_counter=1):
        """
        Function to trimmed image and mask with to specified size
        with overlay to include the whole image.
        Output images are saved as tiff with naming shame 1_1. Where
        first number indicate grid position in xy and second number indicate
        position in z.

        Args:
            image: corresponding image for the labels
            label_mask: empty label mask
            trim_size_xy: size of trimming in xy dimension
            trim_size_z: size of trimming in z dimension
            multi_layer: single, or unique value for each lines
            output: name of the output directory for saving
            image_counter: number id of image

        Returns:
            Saved trimmed images as tiff in specified folder
        """
        idx = image_counter + 1

        if multi_layer:
            nz, ny, nx, nc = label_mask.shape
        else:
            nz, ny, nx = label_mask.shape
            nc = None

        # Initial row/col number
        x, y = math.ceil(ny / trim_size_xy), math.ceil(nx / trim_size_xy)
        x_stride, y_stride = (x * trim_size_xy) - nx, (y * trim_size_xy) - ny

        if x_stride.is_integer():
            x += 1
            stride = abs(nx - (trim_size_xy * x))
            x_stride =
            while stride.is_integer():


        # if x or y stride is not natural then add increase grid size and calculate patches


        z = math.ceil(nz / trim_size_z)
        z_stride = (z * trim_size_z) - nz


        if (nrow)

        # stride
        # ncol
        # nrow
