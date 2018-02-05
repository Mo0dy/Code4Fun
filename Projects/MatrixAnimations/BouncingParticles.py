from Code4Fun.Utility.Vec2 import *
import numpy as np
import pygame as pg
from scipy.ndimage.filters import convolve
import random


def random_sign():
    return int(random.random() * 2) * 2 - 1


class Particle(object):
    def __init__(self, min_x, max_x, min_y, max_y):
        self.vel = Vec2(random_sign(), random_sign())
        self.pos = Vec2(np.random.random_integers(min_x, max_x), np.random.random_integers(min_y, max_y))
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def update(self):
        new_pos = self.pos + self.vel

        if self.min_x > new_pos.x or new_pos.x > self.max_x:
            self.vel.x *= -1
        if self.min_y > new_pos.y or new_pos.y > self.max_y:
            self.vel.y *= -1
        self.pos += self.vel


def init(mat_shape, amount):
    global particles
    particles = [Particle(0, mat_shape[0] - 1, 0, mat_shape[1] - 1) for _ in range(amount)]


def update(content):
    content[:, :, :] = 0
    for p in particles:
        p.update()
        content[p.pos.x, p.pos.y] = np.array([255, 255, 255], dtype=np.uint8)

