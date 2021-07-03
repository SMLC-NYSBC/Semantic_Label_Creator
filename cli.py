"""
    Main module

    :author Robert Kiewisz
"""
import os
import click
import numpy as np

from tifffile import tifffile
from slcpy.slcpy import slcpy

from time import sleep
from tqdm import tqdm

@click.command()
@click.option('--dir_path',
              default=os.getcwd() + r'\data',
              help='directory to the folder which contains *.tif files')
@click.option('--output',
              default=os.getcwd() + r'\data' + r'\output',
              help='directory to the folder where results will be saved')
@click.option('--pixel_size',
              default=None,
              help='images pixel size')
@click.option('--circle_size',
              default=250,
              help='images pixel size')
def main(dir_path, output, pixel_size, circle_size):
    global label_mask
    if not os.path.isdir(os.getcwd() + r'\data' + r'\output'):
        os.mkdir(output)

    for file in tqdm(os.listdir(dir_path)):
        sleep(0.001)

        if file.endswith('.tif'):

            label_mask = slcpy(
                os.path.join(dir_path, file),
                pixel_size,
                circle_size
            )
            os.rename(
                os.path.join(dir_path, file),
                os.path.join(output, file)
            )
            tifffile.imwrite(
                os.path.join(output, file),
                np.array(label_mask, 'int8')
            )


if __name__ == '__main__':
    main()
