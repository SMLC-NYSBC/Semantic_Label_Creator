import os
import shutil

import click
import numpy as np
from tifffile import tifffile

from slcpy.main import slcpy_stitch
from slcpy.version import version


@click.command()
@click.option('-dir', '--dir_path',
              default=os.getcwd() + r'\data',
              help='directory to the folder which contains *.tif files.',
              show_default=True)
@click.option('-o', '--output',
              default=os.getcwd() + r'\data' + r'\output',
              help='directory to the folder where results will be saved.',
              show_default=True)
@click.option('-pf', '--prefix',
              default=None,
              help='prefix name at the end of the file.',
              show_default=True)
@click.version_option(version=version)
def main(dir_path: str,
         output: str,
         prefix):
    """
    Main module for stitch individual images into montaged image

    Args:
        -dir / dir_path: Directory to the folder with image dataset.
        -o / output: Output directory for saving transformed files.
    """

    stitched_image = slcpy_stitch(dir_path,
                                  prefix)

    tifffile.imwrite(
        os.path.join(output),
        np.array(stitched_image, 'int8')
    )


if __name__ == '__main__':
    main()
