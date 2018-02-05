from Code4Fun.Utility.Vec2 import *
import numpy as np
import pygame as pg
from scipy.ndimage.filters import convolve
import random


directions = [Vec2(1, 0),
              Vec2(0, 1),
              Vec2(-1, 0),
              Vec2(0, -1)]


dir_index = 0


def turn_right():
    global dir_index
    dir_index = (dir_index + 1) % 4


def turn_left():
    global dir_index
    dir_index = dir_index - 1
    if dir_index < 0:
        dir_index = 3


def flip():
    global mat
    mat[ant.x, ant.y] = not mat[ant.x, ant.y]


def move():
    global ant
    ant += directions[dir_index]

    # out of bounds check and resolution
    if ant.x >= mat.shape[0]:
        ant.x = 0
    elif ant.x < 0:
        ant.x = mat.shape[0] - 1
    elif ant.y >= mat.shape[1]:
        ant.y = 0
    elif ant.y < 0:
        ant.y = mat.shape[1] - 1


def init(mat_shape):
    global mat, ant
    mat = np.zeros((mat_shape[0], mat_shape[1]))
    # mat = (np.random.rand(mat_shape[0], mat_shape[1]) * 2).astype(int)
    ant = Vec2(int(mat_shape[0] / 2), int(mat_shape[1] / 2))


def do_step():
    global mat, ant
    # white square
    if mat[ant.x, ant.y]:
        turn_right()
    else:
        turn_left()
    flip()
    move()


def update(content):
    do_step()
    content[:, :, 0] = mat * 255
    content[:, :, 1] = mat * 255
    content[:, :, 2] = mat * 255

