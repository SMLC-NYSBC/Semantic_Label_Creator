import numpy as np
from tqdm import tqdm

from slcpy.utils.build_label_mask import draw_label
from slcpy.utils.import_data import ImportDataFromAmira, ImportSemanticMask
from slcpy.utils.interpolation import interpolation_3D
from slcpy.utils.stitch import StitchImages
from slcpy.utils.trim import trim_label_mask


def slcpy_semantic(dir_path: str,
                   mask: bool,
                   pixel_size=None,
                   circle_size=250,
                   multi_layer=False,
                   trim_mask=False):
    """
    MODULE TO LOAD 3D .tif FILES WITH CORRESPONDING .am FILES

    Args:
        dir_path: path direction of the input file *.tif
        mask: If True semantic mask is created
        pixel_size: pixel size in Angstrom
        circle_size: size of a circle the label mask in Angstrom
        multi_layer: single, or unique value for each lines
        trim_mask: If True input data are trimed to the point cloud
    """
    print(" Converting image {}".format(dir_path))
    img = ImportDataFromAmira(
        src_tiff=dir_path,
        src_am=dir_path[:-3] + r"CorrelationLines.am",
        mask=mask,
        pixel_size=pixel_size)
    image = img.image_data()

    if mask:
        label_mask = img.empty_semantic_label()

        if pixel_size is None:
            pixel_size = img.pixel_size_in_et()
            print(" Detected pixel size is {}".format(pixel_size))

        segments = img.get_segments()
        points = img.get_points().round()
        r = round((circle_size / 2) / pixel_size)

        if trim_mask:
            image, label_mask, points = trim_label_mask(points,
                                                        image,
                                                        label_mask)

        if multi_layer:
            label_mask = np.stack((label_mask,) * 3, axis=-1)
            segment_color = [255, 255, 255]
        else:
            segment_color = [1]

        batch_iter = tqdm(range(len(segments)),
                          'Building semantic mask',
                          total=len(segments),
                          leave=False)
        for i in batch_iter:
            start_point = int(sum(segments[0:i]))
            stop_point = start_point + int(segments[i])
            mt = interpolation_3D(points[start_point:stop_point])

            if multi_layer:
                segment_color = list(np.random.choice(range(256), size=3))

            for j in range(len(mt)):
                c = mt[j, :3]
                label_mask = draw_label(r, c, label_mask, segment_color)

        return image, label_mask

    return image


def slcpy_stitch(dir_path: str,
                 mask: bool,
                 prefix=None,
                 dtype='int8'):
    """
    MODULE TO STITCH SEGMENTED IMAGES

    Args:
        dir_path: Path direction of the input file *.tif with semantic masks.
        mask: If True images are treated as Semantic mask not image.
        prefix: Prefix name for the Images.
        dtype: Type of output image.
    """

    stitcher = StitchImages()
    stitch_img = stitcher(dir_path=dir_path,
                          mask=mask,
                          prefix=prefix,
                          dtype=dtype)

    return stitch_img


def slcpy_graph(dir_path: str or np.ndarray,
                filter_img: int,
                down_sampling: bool):
    """
    MODULE TO BUILD POINT CLOUD FROM 3D .tiff FILES

    Args:
        dir_path: Path direction of the input file *.tif with semantic masks.
        filter_img: Remove object that are smaller then given pixel size.
        down_sampling: If True downsampling is perform on build point cloud.
    """

    img = ImportSemanticMask(src_tiff=dir_path)

    return img.find_maximas(filter_small_object=filter_img,
                            down_sampling=down_sampling)
