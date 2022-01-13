from os import getcwd, listdir
from os.path import join

import click
import numpy as np
from tifffile import tifffile
from tqdm import tqdm

from slcpy.main import slcpy_graph
from slcpy.version import version


@click.command()
@click.option('-dir', '--dir_path',
              default=join(getcwd() + 'data'),
              help='Directory to the folder which contains *.tif files.',
              show_default=True)
@click.option('-o', '--output',
              default=join(getcwd(), 'data', 'output'),
              help='Directory to the folder where results will be saved.',
              show_default=True)
@click.option('-f', '--filter',
              default=6,
              help='Filter size matrix for denoising.',
              show_default=True)
@click.option('-d', '--down_sampling',
              default=0,
              help='Down-sample point cloud by the factor of...',
              show_default=True)
@click.option('-s', '--save',
              default="all",
              type=click.Choice(['all', 'csv', 'numpy'], case_sensitive=True),
              help='Save data as numpy .py or .csv.',
              show_default=True)
@click.version_option(version=version)
def main(dir_path: str,
         output: str,
         filter: int,
         save: str,
         down_sampling: bool):
    """
    MAIN MODULE FOR EXTRACTING POINT CLOUD FROM SEMANTIC LABEL

    Args:
        dir_path: Directory to the folder with image dataset.
        output: Output directory for saving transformed files.
        filter: filter size matrix for denoising
        clean_graph: Clean graph from neighborhood points.
        save: select type of saved data other numpy .npy or .csv
    """

    for file in tqdm(listdir(dir_path)):
        if file.endswith('.tif'):
            if down_sampling:
                img, coords_HD, coords_LD = slcpy_graph(dir_path=join(dir_path, file),
                                                        filter_img=filter,
                                                        down_sampling=down_sampling)
            else:
                img, coords_HD = slcpy_graph(dir_path=join(dir_path, file),
                                             filter_img=filter,
                                             down_sampling=down_sampling)

            if save == "numpy":
                np.save(join(output, file[:-4] + '_HD'),
                        coords_HD)
                if down_sampling:
                    np.save(join(output, file[:-4] + '_LD'),
                            coords_LD)
            elif save == "csv":
                np.savetxt(join(output, str(file[:-4] + '_HD' + ".csv")),
                           coords_HD,
                           delimiter=",")
                if down_sampling:
                    np.savetxt(join(output, str(file[:-4] + '_LD' + ".csv")),
                               coords_LD,
                               delimiter=",")
            elif save == "all":
                tifffile.imwrite(join(output, file[:-4] + '_denoise.tif'),
                                 np.array(img, 'int8'))
                np.save(join(output, file[:-4]),
                        coords_HD)
                np.savetxt(join(output, str(file[:-4] + ".csv")),
                           coords_HD,
                           delimiter=",")

                if down_sampling:
                    np.save(join(output, file[:-4] + '_LD'),
                            coords_LD)
                    np.savetxt(join(output, str(file[:-4] + + '_LD' + ".csv")),
                               coords_LD,
                               delimiter=",")


if __name__ == '__main__':
    main()
