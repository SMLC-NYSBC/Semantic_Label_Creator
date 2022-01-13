from os import getcwd, listdir, mkdir, rename
from os.path import isdir, join
from shutil import rmtree

import click
import numpy as np
from tifffile import tifffile
from tqdm import tqdm

from slcpy.main import slcpy_semantic
from slcpy.utils.trim import trim_images, trim_to_patches
from slcpy.version import version


@click.command()
@click.option('-dir', '--dir_path',
              default=join(getcwd(), 'data'),
              help='Directory to the folder which contains *.tif files.',
              show_default=True)
@click.option('-o', '--output',
              default=join(getcwd(), 'data', 'output'),
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
              default=None,
              help='Define size in pixels of output images in xy.',
              show_default=None)
@click.option('-z', '--trim_size_z',
              default=None,
              help='Define size in pixels of output images in z.',
              show_default=True)
@click.option('-f', '--filter_empty_patches',
              default=False,
              help='If True only images containing any data are saved.',
              show_default=True)
@click.option('-s', '--stride',
              default=25,
              help='Overlay size used for trimming images.',
              show_default=True)
@click.version_option(version=version)
def main(dir_path,
         output,
         build_mask,
         pixel_size,
         circle_size,
         multi_classification,
         pretrim_mask,
         trim_size_xy, trim_size_z,
         filter_empty_patches,
         stride):
    """
    MAIN MODULE FOR COMPOSING SEMANTIC LABEL FROM GIVEN POINT CLOUD

    Args:
        dir_path: Directory to the folder with image dataset.
        output: Output directory for saving transformed files.
        build_mask: Define if the semantic mask should be build and saved.
        pixel_size: Pixel size for all images. Note that if images has
            different pixel size set to None to automatically calculate it
            for each image.
        circle_size: Size of drawn circle in Angstrom.
        multi_classification: If True as an output each line is drawn
            with unique label.
        pretrim_mask: If True the image mask will be trimmed before
            building label
            mask. It's helpful for big files to speed up computation.
        trim_size_xy: Final XY dimension of output images.
        time_size_z: Final Z dimension of output images.
        filter_empty_patches: Use whole image for trimming
        stride: stride for patch step size with overlay
    """

    if isdir(output):
        try:
            rename(output, output + '_old')
            mkdir(output)
            mkdir(join(output, 'imgs'))
            mkdir(join(output, 'mask'))

        except Exception:
            print("Folder for the output data already exist... "
                  "Data copied to output_old."
                  "Output folder will be overwrite...")
            rmtree(join(dir_path, 'output_old'))
            rename(output, output + '_old')
            mkdir(output)
            mkdir(join(output, 'imgs'))
            mkdir(join(output, 'mask'))
            pass

    else:
        mkdir(output)
        mkdir(join(output, 'imgs'))
        mkdir(join(output, 'mask'))

    image_counter = 0
    idx = 0

    batch_iter = tqdm(listdir(dir_path),
                      'Building Semantic patch images',
                      total=len(listdir(dir_path)),
                      leave=False)

    for file in batch_iter:
        img_name = file
        mask_name = file[:-4] + '_mask.tif'
        image_counter += 1

        if file.endswith('.tif'):
            if build_mask:
                image, label_mask = slcpy_semantic(
                    join(dir_path, file),
                    mask=build_mask,
                    pixel_size=pixel_size,
                    circle_size=circle_size,
                    multi_layer=multi_classification,
                    trim_mask=pretrim_mask)
            else:
                image = slcpy_semantic(
                    join(dir_path, file),
                    mask=build_mask)
                label_mask = None

            if trim_size_xy is None:
                tifffile.imwrite(join(output, 'imgs', img_name),
                                 np.array(image, 'int8'))

                if build_mask:
                    tifffile.imwrite(join(output, 'mask', mask_name),
                                     np.array(label_mask, 'int8'))
            else:
                if filter_empty_patches:
                    idx = trim_images(image=image,
                                      label_mask=label_mask,
                                      trim_size_xy=trim_size_xy,
                                      trim_size_z=trim_size_z,
                                      multi_layer=multi_classification,
                                      output=output,
                                      image_counter=idx)
                else:
                    idx = trim_to_patches(image=image,
                                          label_mask=label_mask,
                                          trim_size_xy=trim_size_xy,
                                          trim_size_z=trim_size_z,
                                          multi_layer=multi_classification,
                                          image_counter=idx,
                                          output=output,
                                          stride=stride)


if __name__ == '__main__':
    main()
