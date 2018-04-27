import numpy as np
from copy import deepcopy


'''Maths functions mostly wrapping numpy
'''


class Vec2(object):
    '''A mathematical vector wrapping numpy
    '''

    def __init__(self, *args):
        if len(args) == 1:
            # arg is a numpy array
            if isinstance(args[0], np.ndarray):
                self.vec = args[0]
            else:
                self.vec = np.array(args[0])
        elif len(args) == 2:
            # args are x and y pos
            self.vec = np.array([args[0], args[1]])
        else:
            self.vec = np.zeros(2)

    def __getitem__(self, item):
        return self.vec[item]

    def __setitem__(self, key, value):
        self.vec[key] = value

    def __mul__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.vec @ other.vec)
        else:
            return Vec2(self.vec * other)

    def __truediv__(self, other):
        return Vec2(self.vec / other)

    def __floordiv__(self, other):
        return Vec2((self.vec / other).astype(int))

    def __rmul__(self, other):
        return self * other

    def __add__(self, other):
        return Vec2(self.vec + other.vec)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.vec - other.vec)
        else:
            return Vec2(self.vec - other)

    # this only works if pointing in the same direction
    def __mod__(self, other):
        pass

    def __abs__(self):
        return np.sqrt(self.vec @ self.vec)

    def __str__(self):
        return str(self.vec)

    def __eq__(self, other):
        return np.all(self.vec == other.vec)

    def __bool__(self):
        return bool(np.any(self.vec))

    def __repr__(self):
        return "<Vec2: [%f | %f]>" % (self.x, self.y)

    def normalized(self):
        length = abs(self)
        if length:
            return self.copy() / length
        else:
            return self.copy()

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, value):
        self[0] = value

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, value):
        self[1] = value

    @property
    def theta(self):
        return np.arctan2(self.x, self.y)

    @theta.setter
    def theta(self, value):
        self.vec = np.array([np.cos(value), np.sin(value)]) * abs(self)

    # some nice additions:
    @property
    def tuple(self):
        return self.x, self.y

    @property
    def tuple_int(self):
        return int(self.x), int(self.y)

    def copy(self):
        return deepcopy(self)

    def zero(self):
        self.vec = np.zeros(2)

    def set_length(self, length):
        self *= length / abs(self)
