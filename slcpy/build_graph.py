import os
from time import sleep

import click
import numpy as np
from tqdm import tqdm

from slcpy.main import slcpy_graph
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
@click.option('-s', '--save',
              default="numpy",
              help='Save data as numpy .py or .csv.',
              show_default=True
              )
@click.version_option(version=version)
def main(dir_path: str,
         output: str,
         save: str):
    """
    Main module for composing semantic label from given point cloud

    Args:
        -dir / dir_path: Directory to the folder with image dataset.
        -o / output: Output directory for saving transformed files.
        -s / save: select type of saved data other numpy .py or .csv
    """

    for file in tqdm(os.listdir(dir_path)):
        sleep(0.001)

        if file.endswith('.tif'):
            coords = slcpy_graph(
                os.path.join(dir_path, file)
            )
            if save == "numpy":
                np.save(os.path.join(output, file[:-4]),
                        coords)
            elif save == "csv":
                np.savetxt(os.path.join(output, str(file[:-4] + ".csv")),
                           coords,
                           delimiter=",")


if __name__ == '__main__':
    main()
