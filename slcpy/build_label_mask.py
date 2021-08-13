"""
    Module draw_label to construct shape of a label

    :param int r: radius of a circle in Angstrom
    :param int c: point in 3D indicating center of a circle
    :param array label_mask: array of a mask on which circle is drawn
    :param list segment_color: single list value for naming drawn line in RGB

    :author Robert Kiewisz
"""
from skimage import draw


def draw_label(r, c, label_mask, segment_color):
    assert type(segment_color) == list

    nz, ny, nx, nc = label_mask.shape
    assert len(segment_color) == nc

    x = int(c[0])
    y = int(c[1])
    z = int(c[2])

    if z == nz:
        z = z - 1

    cy, cx = draw.disk((y, x), r, shape=(ny, nx))

    for i in range(nc):
        label_mask[z, cy, cx, i] = segment_color[i]

    return label_mask
