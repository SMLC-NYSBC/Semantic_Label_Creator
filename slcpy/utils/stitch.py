from os import listdir
from os.path import isfile, join

import numpy as np
from tifffile import tifffile
from tqdm import tqdm


class StitchImages:
    """
    Class object to stitch cut date into one big image. Object recognize images
    with naming 1_1_1_25 where 1 indicate xyz position and 25 indicate stride.

    Args:
        dir_path: Directory where all images are stored. Indicate one directory
            for each dataset, that has to be stitch.
            mask:
            prefix:
    """

    def __init__(self):
        self.idx = 0  # Variable storing number of stitched images
        self.nx, self.ny, self.nz = 0, 0, 0  # Variable used to store xyz image dimension
        self.x, self.y, self.z = 0, 0, 0  # Variable to store number of patches in xyz
        self.stride = 0  # Variable to store step size

    def _find_xyz(self,
                  dir_path: str):
        # Extract information about images in dir_path
        file_list = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]

        self.idx = max(list(map(int, [str.split(f[:-4], "_")[0] for f in file_list])))
        self.x = max(list(map(int, [str.split(f[:-4], "_")[1] for f in file_list])))
        self.y = max(list(map(int, [str.split(f[:-4], "_")[2] for f in file_list])))
        self.z = max(list(map(int, [str.split(f[:-4], "_")[3] for f in file_list])))
        self.stride = max(list(map(int, [str.split(f[:-4], "_")[4] for f in file_list])))

        return file_list

    def _calculate_dim(self,
                       image: np.ndarray):
        self.nz, self.ny, self.nx = image.shape

    def __call__(self,
                 dir_path: str,
                 mask: bool,
                 prefix=None,
                 dtype='int8'):

        file_list = self._find_xyz(dir_path)
        self._calculate_dim(tifffile.imread(join(dir_path, file_list[0])))

        x_dim = self.nx + ((self.nx - self.stride) * self.x)
        y_dim = self.ny + ((self.ny - self.stride) * self.y)
        z_dim = self.nz + ((self.nz - self.stride) * self.z)
        stitched_image = np.zeros((z_dim, y_dim, x_dim), dtype=dtype)

        z_start, z_stop = 0 - (self.nz - self.stride), 0
        img_counter = 0

        if self.z == 0:
            self.z = 1

        batch_iter_z = tqdm(range(self.z),
                            'Stitching images in Z',
                            total=len(range(self.z)),
                            leave=False)

        batch_iter_y = tqdm(range(self.y),
                            'Stitching images in XY',
                            total=len(range(self.y)),
                            leave=False)

        for i in batch_iter_z:
            z_start = z_start + self.nz - self.stride
            z_stop = z_start + self.nz
            y_start, y_stop = 0 - (self.ny - self.stride), 0

            for j in batch_iter_y:
                y_start = y_start + self.ny - self.stride
                y_stop = y_start + self.ny
                x_start, x_stop = 0 - (self.nx - self.stride), 0

                for k in range(self.x):
                    x_start = x_start + self.nx - self.stride
                    x_stop = x_start + self.nx

                    if prefix is not None:
                        img_dir = str(join(dir_path,
                                           "{}_{}_{}_{}_{}_{}.tif".format(self.idx,
                                                                          k, j, i,
                                                                          self.stride,
                                                                          prefix)))
                    else:
                        img_dir = str(join(dir_path,
                                           "{}_{}_{}_{}_{}.tif".format(self.idx,
                                                                       k, j, i,
                                                                       self.stride)))

                    img = tifffile.imread(img_dir)
                    assert img.shape == (self.nz, self.ny, self.nx)
                    if mask:
                        stitched_image[z_start:z_stop, y_start:y_stop, x_start:x_stop] += img
                    else:
                        stitched_image[z_start:z_stop, y_start:y_stop, x_start:x_stop] = img

                    img_counter += 1
        return stitched_image
