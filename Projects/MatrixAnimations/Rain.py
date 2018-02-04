from Code4Fun.Utility.Vec2 import *
import numpy as np
import pygame as pg
from scipy.ndimage.filters import convolve



def init(mat_shape, density):
    global drops, start_height
    start_height = mat_shape[1] * -100
    drops = [[np.random.random_integers(0, mat_shape[0] - 1), np.random.random_integers(mat_shape[1] * -99, 0)] for i in range(int(density * mat_shape[0] * mat_shape[1]))]


def update(content):
    content[:, :, :] = 0
    for d in drops:
        d[1] += 1
        if d[1] >= content.shape[1]:
            d[1] = start_height

    for d in drops:
        if d[1] >= 0:
            content[d[0], d[1]] = np.array([0, 71, 186])
        if 0 <= d[1] + 1 < content.shape[1]:
            content[d[0], d[1] + 1] = np.array([0, 71, 186])
