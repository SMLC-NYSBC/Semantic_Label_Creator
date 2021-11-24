import math

from os.path import join
from typing import Optional

import numpy as np
from tifffile import tifffile


def trim_images(image: np.ndarray,
                trim_size_xy: int,
                trim_size_z: int,
                multi_layer: bool,
                output: str,
                image_counter: int,
                label_mask: Optional[np.ndarray] = None):
    """
    MODULE FOR TRIMMING DATA TO SPECIFIED SIZES

    Args:
        image: corresponding image for the labels
        label_mask: empty label mask or None if image mask is not included
        trim_size_xy: size of trimming in xy dimension
        trim_size_z: size of trimming in z dimension
        multi_layer: single, or unique value for each lines
        output: name of the output directory for saving
        image_counter: number id of image
    """
    idx = image_counter + 1

    if multi_layer:
        nz, ny, nx, nc = label_mask.shape
    elif multi_layer is False and label_mask is not None:
        nz, ny, nx = label_mask.shape
        nc = None
    else:
        nz, ny, nx = image.shape
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

            trim_img = image[nz_start:nz_end,
                             ny_start:ny_end,
                             nx_start:nx_end]

            if label_mask is not None:
                if nc is None:
                    trim_mk = label_mask[nz_start:nz_end,
                                         ny_start:ny_end,
                                         nx_start:nx_end]
                else:
                    trim_mk = label_mask[nz_start:nz_end,
                                         ny_start:ny_end,
                                         nx_start:nx_end,
                                         :]
                if np.all(trim_mk[:, :, :] == 0):
                    idx = idx
                else:
                    # Hard transform between int8 and uint8
                    if np.min(trim_img) < 0:
                        trim_img = trim_img + 128

                    tifffile.imwrite(join(output + r'\mask', mask_name),
                                     np.array(trim_mk, 'int8'))
                    tifffile.imwrite(join(output + r'\imgs', img_name),
                                     np.array(trim_img, 'int8'))
                    idx += 1

    return idx


def trim_to_patches(image: np.ndarray,
                    trim_size_xy: int,
                    trim_size_z: int,
                    multi_layer: bool,
                    output: str,
                    image_counter: int,
                    label_mask: Optional[np.ndarray] = None,
                    stride=25):
    """
    FUNCTION TO TRIMMED IMAGE AND MASKS TO SPECIFIED SIZE

    Output images are saved as tiff with naming shame 1_1_1_25. Where
    number indicate grid position in xyz. Last number indicate stride.

    Args:
        image: Corresponding image for the labels
        label_mask: Empty label mask
        trim_size_xy: Size of trimming in xy dimension
        trim_size_z: Size of trimming in z dimension
        multi_layer: Single, or unique value for each lines
        output: Name of the output directory for saving
        image_counter:
        stride: Trimming step size

    Returns:
        Saved trimmed images as tiff in specified folder
    """
    idx = image_counter

    if multi_layer:
        nz, ny, nx, nc = label_mask.shape
    elif multi_layer is False and label_mask is not None:
        nz, ny, nx = label_mask.shape
        nc = None
    else:
        nz, ny, nx = image.shape
        nc = None

    if trim_size_xy is not None or trim_size_z is not None:
        assert nx >= trim_size_xy, \
            "trim_size_z should be equal or greater then X dimension!"
        assert ny >= trim_size_xy, \
            "trim_size_z should be equal or greater then Y dimension!"
        if nz >= trim_size_z:
            trim_size_z = nz
    else:
        assert stride is not None, \
            "Trim sizes or stride has to be indicated!"
        trim_size_xy = 64
        trim_size_z = 64

    # Calculate number of patches, patch sizes, and stride for xyz
    x, y, z = math.ceil(nx / trim_size_xy), \
              math.ceil(ny / trim_size_xy), \
              math.ceil(nz / trim_size_z)

    x_padding, y_padding, z_padding = (trim_size_xy + ((trim_size_xy - stride) * (x - 1))) - nx, \
                                      (trim_size_xy + ((trim_size_xy - stride) * (y - 1))) - ny, \
                                      (trim_size_z + ((trim_size_z - stride) * (z - 1))) - nz

    # Adapt number of patches for trimming
    if trim_size_xy is not None or trim_size_z is not None:
        while x_padding < 0:
            x += 1
            x_padding += trim_size_xy - stride
        while y_padding < 0:
            y += 1
            y_padding += trim_size_xy - stride
        while z_padding < 0:
            z += 1
            z_padding += trim_size_z - stride

    # Adapt patch size for trimming
    else:
        while x_padding <= 0 or y_padding <= 0:
            trim_size_xy += 1
            x_padding = (trim_size_xy + ((trim_size_xy - stride) * (x - 1))) - nx
            y_padding = (trim_size_xy + ((trim_size_xy - stride) * (y - 1))) - ny

        while z_padding < 0:
            trim_size_z += 1
            z_padding = (trim_size_z + ((trim_size_z - stride) * (z - 1))) - nz

    # Expand image of a patch
    image_padded = np.pad(image,
                          [(0, z_padding), (0, y_padding), (0, x_padding)],
                          mode='constant')

    if label_mask is not None:
        if nc is None:
            mask_padded = np.pad(label_mask,
                                 [(0, z_padding), (0, y_padding), (0, x_padding)],
                                 mode='constant')
        else:
            mask_padded = np.pad(label_mask,
                                 [(0, z_padding), (0, y_padding), (0, x_padding), (0, 0)],
                                 mode='constant')

    # Trim image and mask with stride
    z_start, z_stop = 0 - (trim_size_z - stride), 0

    for i in range(z):
        z_start = z_start + trim_size_z - stride
        z_stop = z_start + trim_size_z
        y_start, y_stop = 0 - (trim_size_xy - stride), 0

        for j in range(y):
            y_start = y_start + trim_size_xy - stride
            y_stop = y_start + trim_size_xy
            x_start, x_stop = 0 - (trim_size_xy - stride), 0

            for k in range(x):
                x_start = x_start + trim_size_xy - stride
                x_stop = x_start + trim_size_xy

                img_name = str("{}_{}_{}_{}_{}.tif".format(idx, k, j, i, stride))
                mask_name = str("{}_{}_{}_{}_{}_mask.tif".format(idx, k, j, i, stride))

                trim_img = image_padded[z_start:z_stop,
                                        y_start:y_stop,
                                        x_start:x_stop]

                if label_mask is not None:
                    if nc is None:
                        trim_mk = mask_padded[z_start:z_stop,
                                              y_start:y_stop,
                                              x_start:x_stop]
                    else:
                        trim_mk = mask_padded[z_start:z_stop,
                                              y_start:y_stop,
                                              x_start:x_stop,
                                              :]
                    tifffile.imwrite(join(output + r'\mask', mask_name),
                                     np.array(trim_mk, 'int8'))

                if label_mask is not None:
                    tifffile.imwrite(join(output + r'\imgs', img_name),
                                     np.array(trim_img, 'int8'))
                else:
                    tifffile.imwrite(join(output, img_name),
                                     np.array(trim_img, 'int8'))
    idx += 1
    return idx
