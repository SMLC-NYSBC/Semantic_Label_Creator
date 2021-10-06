import os
import shutil
from time import sleep

import click
import numpy as np
from tifffile import tifffile
from tqdm import tqdm

from slcpy.main import slcpy_semantic
from slcpy.utils.trim import trim_images, trim_to_patches
from slcpy.version import version


@click.command()
@click.option('-dir', '--dir_path',
              default=os.getcwd() + r'\data',
              help='directory to the folder which contains *.tif files',
              show_default=True)
@click.option('-o', '--output',
              default=os.getcwd() + r'\data' + r'\output',
              help='directory to the folder where results will be saved',
              show_default=True)
@click.option('-px', '--pixel_size',
              default=None,
              type=float,
              help='images pixel size in Angstrom',
              show_default=True)
@click.option('-d', '--circle_size',
              default=250,
              help='size of a circle in Angstrom for label shape',
              show_default=True)
@click.option('-l', '--multi_layer',
              default=False,
              help='specified if lines should have independent labeling',
              show_default=True)
@click.option('-t', '--trim_mask',
              default=True,
              help='define if the input image has to be trim to fit labels.',
              show_default=True)
@click.option('-xy', '--trim_size_xy',
              default=None,
              type=int,
              help='define size in pixels of output images in xy.',
              show_default=None)
@click.option('-z', '--trim_size_z',
              default=64,
              help='define size in pixels of output images in z.',
              show_default=True)
@click.option('-a', '--trim_all',
              default=False,
              help='if True the whole image is used for trimming',
              show_default=True)
@click.option('-s', '--stride',
              default=25,
              help='overlay size used for trimming images',
              show_default=True)
@click.version_option(version=version)
def main(dir_path, output,
         pixel_size, circle_size,
         multi_layer,
         trim_mask, trim_size_xy, trim_size_z,
         trim_all, stride):
    """
    Main module for composing semantic label from given point cloud

    Args:
        -dir / dir_path: Directory to the folder with image dataset.
        -o / output: Output directory for saving transformed files.
        -px / pixel_size: Pixel size for all images. Note that if images has different
            pixel size set to None to automatically calculate it for each image.
       -d / circle_size: Size of drawn circle in Angstrom.
       -l / multi_layer: If True as an output each line is drawn with unique label.
       -t / trim_mask: If True the image mask will be trimmed before building label
            mask. It's helpful for big files to speed up computation.
       -xy / trim_size_xy: Final XY dimension of output images.
       -z / time_size_z: Final Z dimension of output images.
       -a / trim_all: Use whole image for trimming
       -s / stride: stride for patch step size with overlay
    """

    if os.path.isdir(output):
        try:
            os.rename(output, dir_path + r'\output_old')
            os.mkdir(output)
            os.mkdir(output + r'\imgs')
            os.mkdir(output + r'\mask')

        except Exception:
            print("Folder for the output data already exist... "
                  "Data copied to output_old."
                  "Output folder will be overwrite...")
            shutil.rmtree(dir_path + r'\output_old')
            os.rename(output, dir_path + r'\output_old')
            os.mkdir(output)
            os.mkdir(output + r'\imgs')
            os.mkdir(output + r'\mask')
            pass

    else:
        os.mkdir(output)
        os.mkdir(output + r'\imgs')
        os.mkdir(output + r'\mask')

    image_counter = 0
    idx = 0
    for file in tqdm(os.listdir(dir_path)):
        sleep(0.001)
        img_name = str(image_counter) + r'.tif'
        mask_name = str(image_counter) + r'_mask.tif'
        image_counter += 1

        if file.endswith('.tif'):
            image, label_mask = slcpy_semantic(
                os.path.join(dir_path, file),
                pixel_size,
                circle_size,
                multi_layer,
                trim_mask
            )

            if trim_size_xy is None:
                tifffile.imwrite(
                    os.path.join(output + r'\imgs', img_name),
                    np.array(image, 'int8')
                )

                tifffile.imwrite(
                    os.path.join(output + r'\mask', mask_name),
                    np.array(label_mask, 'int8')
                )
            else:
                if not trim_all:
                    idx = trim_images(image, label_mask,
                                      trim_size_xy, trim_size_z, multi_layer,
                                      output, idx)
                else:
                    idx = trim_to_patches(image, label_mask,
                                          trim_size_xy, trim_size_z, multi_layer,
                                          output, stride)


if __name__ == '__main__':
    main()