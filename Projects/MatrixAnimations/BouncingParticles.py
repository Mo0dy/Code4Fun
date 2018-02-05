from Code4Fun.Utility.Vec2 import *
import numpy as np
import pygame as pg
from scipy.ndimage.filters import convolve
import random


def random_sign():
    return int(random.random() * 3 - 2)


class Particle(object):
    def __init__(self, min_x, max_x, min_y, max_y):
        self.vel = Vec2(random_sign(), random_sign())
        self.pos = Vec2(np.random.random_integers(min_x, max_x), np.random.random_integers(min_y, max_y))
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y


def init(matrix, amount):
    global particles
    particles = [Particle[0, matrix.shape[0] - 1, 0, matrix.shape[1] - 1] for _ in range(amount)]


def update(content):
    content[:, :, :] = 0
    for p in particles:
        p.update()

    for d in drops:
        d[1] += 1
        if d[1] >= content.shape[1]:
            d[1] = start_height

    for d in drops:
        if d[1] >= 0:
            content[d[0], d[1]] = np.array([0, 71, 186])
        if 0 <= d[1] + 1 < content.shape[1]:
            content[d[0], d[1] + 1] = np.array([0, 71, 186])
    pass


