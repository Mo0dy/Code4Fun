import numba as nb
import numpy as np


@nb.guvectorize([(nb.float64[:, :], nb.float64, nb.float64, nb.float64, nb.float64, nb.float64[:, :])], '(a,b),(),(),(),()->(a,b)', target='parallel')
def clip(p, x_min, x_max, y_min, y_max, output):
    for i in range(p.shape[0]):
        if p[i, 0] < x_min:
            output[i, 0] = x_min
        elif p[i, 0] > x_max:
            output[i, 0] = x_max
        else:
            output[i, 0] = p[i, 0]

        if p[i, 1] < y_min:
            output[i, 1] = y_min
        elif p[i, 1] > y_max:
            output[i, 1] = y_max
        else:
            output[i, 1] = p[i, 1]


@nb.guvectorize([(nb.float64[:, :], nb.uint8[:], nb.uint8[:, :, :])], '(a,b),(e),(c,d,e)', target='parallel')
def render_points(points, color, output):
    for i in range(points.shape[0]):
        i1 = nb.int32(points[i, 0])
        i2 = nb.int32(points[i, 1])
        output[i1, i2, 0] = color[0]
        output[i1, i2, 1] = color[1]
        output[i1, i2, 2] = color[2]
