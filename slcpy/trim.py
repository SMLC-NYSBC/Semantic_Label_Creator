"""
    Class module trim date to specified sizes

    :param array image: corresponding image for the labels
    :param array label_mask: empty label mask
    :param int trim_size: size of trimming
    :param bool multi_layer: single, or unique value for each lines
    :param str file: name of the image file for saving
    :param str output: name of the output directory for saving

    :author Robert Kiewisz
"""
import os

import numpy as np
from tifffile import tifffile


def trim_images(image, label_mask, trim_size, multi_layer, file, output):
    if multi_layer:
        nz, ny, nx, nc = label_mask.shape
    else:
        nz, ny, nx = label_mask.shape
        nc = None

    x_axis, y_axis = nx // trim_size, ny // trim_size
    idx = 1

    ny_start, ny_end = -trim_size, 0
    for i in range(1, y_axis + 1):
        ny_start += trim_size
        ny_end += trim_size
        nx_start, nx_end = -trim_size, 0

        for j in range(1, x_axis + 1):
            nx_start += trim_size
            nx_end += trim_size

            trim_img = image[:, ny_start:ny_end, nx_start:nx_end]
            if nc is None:
                trim_mk = label_mask[:, ny_start:ny_end, nx_start:nx_end]
            else:
                trim_mk = label_mask[:, ny_start:ny_end, nx_start:nx_end, :]

            if np.all(trim_mk[:, :, :, 1] == 0):
                idx = idx
            else:
                tifffile.imwrite(
                    os.path.join(output, file[:-4] + "_" + str(idx) + r'.tif'),
                    np.array(trim_img, 'int8')
                )

                tifffile.imwrite(
                    os.path.join(output, file[:-4] + "_" + str(idx) + r'_mask.tif'),
                    np.array(trim_mk, 'int8')
                )
                idx += 1
