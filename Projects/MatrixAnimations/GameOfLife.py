from Code4Fun.Utility.Vec2 import *
import numpy as np
import pygame as pg
from scipy.ndimage.filters import convolve
import random


con_mat = [[1, 1, 1],
           [1, 0, 1],
           [1, 1, 1]]


glider = np.array([[0, 1, 0],
                  [0, 0, 1],
                  [1, 1, 1]])


def init(mat_shape):
    global mat
    # mat = np.zeros((mat_shape[0], mat_shape[1]))
    mat = (np.random.rand(mat_shape[0], mat_shape[1]) * 2).astype(int)


def do_step():
    global mat
    neighbour_amounts = convolve(mat, con_mat)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            n_amount = neighbour_amounts[i, j]
            # live cell
            if mat[i, j]:
                if 3 < n_amount or n_amount < 2:
                    mat[i, j] = 0
            # dead cell
            else:
                if n_amount == 3:
                    mat[i, j] = 1


def update(content):
    do_step()
    content[:, :, 0] = mat * 255
    content[:, :, 1] = mat * 255
    content[:, :, 2] = mat * 255

