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

    try:
        nz, ny, nx, nc = label_mask.shape
    except Exception:
        nz, ny, nx = label_mask.shape
        nc = 1

    assert len(segment_color) == nc

    x = int(c[0])
    y = int(c[1])
    z = int(c[2])

    if z == nz:
        z = z - 1

    cy, cx = draw.disk((y, x), r, shape=(ny, nx))

    if nc > 1:
        for i in range(nc):
            label_mask[z, cy, cx, i] = segment_color[i]
    else:
        label_mask[z, cy, cx] = segment_color

    return label_mask
