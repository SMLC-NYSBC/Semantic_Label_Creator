import os

import numpy as np
from tifffile import tifffile


def trim_images(image, label_mask,
                trim_size_xy, trim_size_z, multi_layer,
                output, image_counter):
    """
        Class module trim date to specified sizes

        :param array image: corresponding image for the labels
        :param array label_mask: empty label mask
        :param int trim_size_xy: size of trimming in xy dimension
        :param int trim_size_z: size of trimming in z dimension
        :param bool multi_layer: single, or unique value for each lines
        :param str output: name of the output directory for saving
        :param int image_counter: number id of image

        :author Robert Kiewisz
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
                          :]

            if np.all(trim_mk[:, :, :] == 0):
                idx = idx
            else:
                tifffile.imwrite(
                    os.path.join(output + r'\imgs', img_name),
                    np.array(trim_img, 'int8')
                )

                tifffile.imwrite(
                    os.path.join(output + r'\mask', mask_name),
                    np.array(trim_mk, 'int8')
                )
                idx += 1

    return idx
