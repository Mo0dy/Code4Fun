import numpy as np
from Code4Fun.Utility.Vec2 import Vec2
import numba as nb


# matrices used for transformation
def identity_mat():
    return np.identity(3)


def rot_mat(theta):
    return np.array([[np.cos(theta), -np.sin(theta), 0],
                     [np.sin(theta), np.cos(theta), 0],
                     [0, 0, 1]])


def scale_mat(scale_vec):
    return np.array([[scale_vec.x, 0, 0],
                     [0, scale_vec.y, 0],
                     [0, 0, 1]])


def trans_mat(trans_vec):
    return np.array([[1, 0, trans_vec.x],
                     [0, 1, trans_vec.y],
                     [0, 0, 1]])


def transform_vec(vec2, mat):
    # this could be done explcitly
    return (mat @ np.append(vec2.vec, 1))[:2]


def transform_mult_vec(other, mat):
    # this is inefficient
    return np.transpose(mat @ np.transpose(np.c_[other, np.ones(other.shape[0])]))[:, :2]


@nb.guvectorize([(nb.float64[:, :], nb.float64[:, :], nb.float64[:, :])], '(a,b),(c,c)->(a,b)', target='parallel', cache=True)
def transform_numba(vectors, mat, output):
    # vectors shape: (n, 2)
    for i in range(vectors.shape[0]):
        output[i, 0] = mat[0, 0] * vectors[i, 0] + mat[0, 1] * vectors[i, 1] + mat[0, 2]
        output[i, 1] = mat[1, 0] * vectors[i, 0] + mat[1, 1] * vectors[i, 1] + mat[1, 2]


class Transformation(object):
    def __init__(self):
        self.mat = identity_mat()

    def trans(self, *args):
        if len(args) == 1:
            if isinstance(args[0], Vec2):
                self.mat = trans_mat(args[0]) @ self.mat
            else:
                self.mat = trans_mat(Vec2(args[0][0], args[0][1])) @ self.mat
        else:
            self.mat = trans_mat(Vec2(args[0], args[1])) @ self.mat

    def scale(self, *args):
        if len(args) == 1:
            if isinstance(args, Vec2):
                self.mat = scale_mat(args[0]) @ self.mat
            else:
                self.mat = scale_mat(Vec2(args[0], args[0])) @ self.mat
        else:
            self.mat = scale_mat(Vec2(args[0], args[1])) @ self.mat

    def rotate(self, *args):
        if len(args) == 1:
            self.mat = rot_mat(args[0]) @ self.mat
        else:
            self.trans(-1 * args[0])
            self.rotate(args[1])
            self.trans(1 * args[0])

    def zoom(self, point, amount):
        self.trans(-1 * point)
        self.scale(amount)
        self.trans(point)

    def reset(self):
        self.mat = identity_mat()

    def save(self):
        self.saved_mat = self.mat

    def load(self):
        self.mat = self.saved_mat

    def transform(self, other):
        if isinstance(other, Vec2):
            return transform_vec(other, self.mat)
        else:
            return transform_numba(other, self.mat)

    # overloads the multiply operator to transform
    def __mul__(self, other):
        return self.transform(other)





