import os

import click
import numpy as np
from tifffile import tifffile

from slcpy.main import slcpy_stitch
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
@click.option('-m', '--mask',
              default=False,
              help='Stitching mask or image data.',
              show_default=True)
@click.option('-pf', '--prefix',
              default=None,
              help='Prefix name at the end of the file.',
              show_default=True)
@click.option('-b', '--binary',
              default=None,
              help='Output binary mask.',
              show_default=True)
@click.version_option(version=version)
def main(dir_path: str,
         output: str,
         mask: bool,
         prefix: str,
         binary: bool):
    """
    Main module for stitch individual images into montaged image

    Args:
        -dir / dir_path: Directory to the folder with image dataset.
        -o / output: Output directory for saving transformed files.
        -m / mask: Indicate if stiched images are mask or images.
        -pf / prefix: if not None, indicate additional file prefix.
        -b / binary: If True transform date to binary format.
    """

    stitched_image = slcpy_stitch(dir_path,
                                  mask=mask,
                                  prefix=prefix)
    if binary:
        stitched_image[stitched_image > 0] = 1

    tifffile.imwrite(
        os.path.join(output, 'Stitched_Image.tif'),
        np.array(stitched_image, 'int8')
    )


if __name__ == '__main__':
    main()
