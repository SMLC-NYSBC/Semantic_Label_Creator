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
@click.option('-f', '--filter',
              default=6,
              help='Filter size matrix for denoising.',
              show_default=True)
@click.option('-c', '--clean_graph',
              default=True,
              help='Clean graph from neighborhood points.',
              show_default=True)
@click.option('-d', '--down_sampling',
              default=2,
              help='Down-sample point cloud by the factor of...',
              show_default=True)
@click.option('-s', '--save',
              default="numpy",
              help='Save data as numpy .py or .csv.',
              show_default=True
              )
@click.version_option(version=version)
def main(dir_path: str,
         output: str,
         filter: int,
         clean_graph: bool,
         down_sampling: int,
         save: str):
    """
    Main module for composing semantic label from given point cloud

    Args:
        -dir / dir_path: Directory to the folder with image dataset.
        -o / output: Output directory for saving transformed files.
        -f / filter: filter size matrix for denoising
        -c /clean_graph: Clean graph from neighborhood points.
        -s / save: select type of saved data other numpy .npy or .csv
    """

    for file in tqdm(os.listdir(dir_path)):
        sleep(0.001)

        if file.endswith('.tif'):
            coords = slcpy_graph(
                dir_path=os.path.join(dir_path, file),
                filter_img=filter,
                clean_graph=clean_graph,
                down_sampling=down_sampling
            )
            if save == "numpy":
                np.save(os.path.join(output, file[:-4]),
                        coords)
            elif save == "csv":
                np.savetxt(os.path.join(output, str(file[:-4] + ".csv")),
                           coords,
                           delimiter=",")
            elif save == "all":
                np.save(os.path.join(output, file[:-4]),
                        coords)
                np.savetxt(os.path.join(output, str(file[:-4] + ".csv")),
                           coords,
                           delimiter=",")


if __name__ == '__main__':
    main()
