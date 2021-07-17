"""

    Module draw_label to construct shape of a label

    :param int r: radius of a circle in Angstrom
    :param int c: point in 3D indicating center of a circle
    :param array label_mask: array of a mask on which circle is drawn

    :author Robert Kiewisz

"""
from skimage import draw


def draw_label(r, c, label_mask):
    nz, ny, nx = label_mask.shape

    x = int(c[0])
    y = int(c[1])
    z = int(c[2])

    if z == nz:
        z = z - 1

    cy, cx = draw.disk((y, x), r, shape=(ny, nx))
    label_mask[z, cy, cx] = 1

    return label_mask
