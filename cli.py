"""

    Main module

    :author Robert Kiewisz

"""
import os
import shutil
from time import sleep

import click
import numpy as np
from tifffile import tifffile
from tqdm import tqdm

from slcpy.slcpy import slcpy


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
              type=int,
              help='images pixel size in Angstrom',
              show_default=True)
@click.option('-d', '--circle_size',
              default=250,
              help='size of a circle in Angstrom that would become label shape',
              show_default=True)
def main(dir_path, output, pixel_size, circle_size):
    if os.path.isdir(output):
        os.rename(output, output + r'_old')
        os.mkdir(output)
    else:
        os.mkdir(output)

    for file in tqdm(os.listdir(dir_path)):
        sleep(0.001)

        if file.endswith('.tif'):
            label_mask = slcpy(
                os.path.join(dir_path, file),
                pixel_size,
                circle_size
            )
            shutil.copy(
                os.path.join(dir_path, file),
                os.path.join(output, file)
            )
            tifffile.imwrite(
                os.path.join(output, file[:-3] + r'_mask.tif'),
                np.array(label_mask, 'int8')
            )


if __name__ == '__main__':
    main()
