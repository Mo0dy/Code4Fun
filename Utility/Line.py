import numpy as np
import scipy.linalg as sla
from MyMaths.Vec2 import Vec2
import sys


class Line(object):
    def __init__(self, _p1, _p2):
        self.p1 = _p1
        self.p2 = _p2

    @property
    def dx(self):
        return self.p2.x - self.p1.x

    @property
    def dy(self):
        return self.p2.y - self.p1.y

    @property
    def slope(self):
        if self.dy:
            return self.dx / self.dy
        else:
            return None


def isparallel(l1, l2):
    # two comparisions because there is no abs(None)
    return l1.slope == l2.slope or l1.slope == -1 * l2.slope


def intersect(l1, l2):
    if isparallel(l1, l2):
        sys.stderr.write("intersect: Lines are parallel or colinear")
        sys.stderr.flush()
        return None
    mat = np.array([[l1.p2.y - l1.p1.y, l1.p1.x - l1.p2.x],
                    [l2.p2.y - l2.p1.y, l2.p1.x - l2.p2.x]])

    return Vec2(sla.inv(mat) @ np.array([mat[0, 0] * l1.p1.x + mat[0, 1] * l1.p1.y, mat[1, 0] * l2.p1.x + mat[1, 1] * l2.p1.y]))

