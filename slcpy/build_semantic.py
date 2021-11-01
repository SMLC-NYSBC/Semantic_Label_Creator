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
              help='Directory to the folder which contains *.tif files.',
              show_default=True)
@click.option('-o', '--output',
              default=os.getcwd() + r'\data' + r'\output',
              help='Directory to the folder where results will be saved.',
              show_default=True)
@click.option('-m', '--build_mask',
              default=True,
              help='Indicate if mask is included.',
              show_default=True)
@click.option('-px', '--pixel_size',
              default=None,
              type=float,
              help='Images pixel size in Angstrom. If None pixel size '
                   'is calculated from image metadata.',
              show_default=True)
@click.option('-d', '--circle_size',
              default=250,
              help='Size of a circle in Angstrom for label shape.',
              show_default=True)
@click.option('-l', '--multi_classification',
              default=False,
              help='Specified if lines should have independent labeling.',
              show_default=True)
@click.option('-t', '--pretrim_mask',
              default=True,
              help='Define if the input image has to be trim to fit labels.',
              show_default=True)
@click.option('-xy', '--trim_size_xy',
              default=64,
              help='Define size in pixels of output images in xy.',
              show_default=None)
@click.option('-z', '--trim_size_z',
              default=64,
              help='Define size in pixels of output images in z.',
              show_default=True)
@click.option('-a', '--filter_empty_patches',
              default=False,
              help='If True only images containing any data are saved.',
              show_default=True)
@click.option('-s', '--stride',
              default=25,
              help='Overlay size used for trimming images.',
              show_default=True)
@click.version_option(version=version)
def main(dir_path, output,
         build_mask,
         pixel_size,
         circle_size,
         multi_classification,
         pretrim_mask,
         trim_size_xy, trim_size_z,
         filter_empty_patches,
         stride):
    """
    Main module for composing semantic label from given point cloud

    Args:
        -dir / dir_path: Directory to the folder with image dataset.
        -o / output: Output directory for saving transformed files.
        -m / build_mask: Define if the semantic mask should be build and saved.
        -px / pixel_size: Pixel size for all images. Note that if images has
            different pixel size set to None to automatically calculate it
            for each image.
       -d / circle_size: Size of drawn circle in Angstrom.
       -l / multi_classification: If True as an output each line is drawn
            with unique label.
       -t / pretrim_mask: If True the image mask will be trimmed before
            building label
            mask. It's helpful for big files to speed up computation.
       -xy / trim_size_xy: Final XY dimension of output images.
       -z / time_size_z: Final Z dimension of output images.
       -a / filter_empty_patches: Use whole image for trimming
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

    batch_iter = tqdm(os.listdir(dir_path),
                      'Building Semantic patch images',
                      total=len(os.listdir(dir_path)),
                      leave=False)

    for file in batch_iter:
        sleep(0.001)
        img_name = str(image_counter) + r'.tif'
        mask_name = str(image_counter) + r'_mask.tif'
        image_counter += 1

        if file.endswith('.tif'):
            if build_mask:
                image, label_mask = slcpy_semantic(
                    os.path.join(dir_path, file),
                    mask=build_mask,
                    pixel_size=pixel_size,
                    circle_size=circle_size,
                    multi_layer=multi_classification,
                    trim_mask=pretrim_mask)
            else:
                image = slcpy_semantic(
                    os.path.join(dir_path, file),
                    mask=build_mask)
                label_mask = None

            if trim_size_xy is None:
                tifffile.imwrite(
                    os.path.join(output + r'\imgs', img_name),
                    np.array(image, 'int8')
                )

                if build_mask:
                    tifffile.imwrite(
                        os.path.join(output + r'\mask', mask_name),
                        np.array(label_mask, 'int8')
                    )
            else:

                if not filter_empty_patches:
                    idx = trim_images(image, label_mask,
                                      trim_size_xy, trim_size_z,
                                      multi_classification,
                                      output, idx)
                else:
                    idx = trim_to_patches(image, label_mask,
                                          trim_size_xy, trim_size_z,
                                          multi_classification,
                                          output, stride)


if __name__ == '__main__':
    main()
