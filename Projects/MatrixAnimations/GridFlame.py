from Code4Fun.Utility.Vec2 import *
import numpy as np
import pygame as pg
from scipy.ndimage.filters import convolve


mul_dx = 0.1
mul_dy = 0.15
candle_mul_dx = 0.1
candle_mul_dy = 0.1
random_fac = 0.5

cooldown = 5


con_mat = np.array([[0.08, 0.05, 0.02],
                    [0.48, -1, 0.02],
                    [0.08, 0.05, 0.02]])


def update_ignition_values():
    global ignition_values
    ignition_values = np.reshape(np.random.random_integers(10, 28, ign_dx * 4 * ign_dy), (ign_dx * 2, ign_dy * 2)) * 8


def init(mat_shape, res):
    global heat_mat, resolution, ignition_area, ign_dx, ign_dy, candle_area
    resolution = res
    heat_mat = np.zeros(mat_shape[:2] * resolution, dtype=np.float)
    ign_x = int(heat_mat.shape[0] / 2)
    ign_y = int(heat_mat.shape[1] * 0.8)
    ign_dy = int(heat_mat.shape[1] * mul_dy)
    ign_dx = int(heat_mat.shape[0] * mul_dx)
    ignition_area = np.array([[ign_x - ign_dx, ign_x + ign_dx], [ign_y - ign_dy, ign_y + ign_dy]])

    candle_x = int(mat_shape[0] / 2)
    candle_y = int(mat_shape[1])
    candle_dy = int(mat_shape[1] * candle_mul_dy)
    candle_dx = int(mat_shape[0] * candle_mul_dx)

    candle_area = np.array([[candle_x - candle_dx, candle_x + candle_dx], [candle_y - candle_dy, candle_y]])
    update_ignition_values()


def color_temperature(temp):
    temp = temp * 0.2 + 11
    if temp <= 66:
        r = 255
    else:
        r = temp - 60
        r = 329.698727446 * (r ** -0.1332047592)

    if temp <= 66:
        g = temp
        g = 99.4708025861 * np.log(g) - 161.1195681661
    else:
        g = temp - 60
        g = 288.1221695283 * (g ** -0.0755148492)

    if temp >= 66:
        b = 0
    else:
        b = temp - 10
        b = 138.5177312231 * np.log(b) - 305.0447927307
    return np.clip(np.array([r, g, b], dtype=int), 0, 255)


def color_linear(temp):
    temp *= 2
    if temp < 255:
        return temp, 0, 0
    elif temp < 510:
        return 255, np.clip(510 - temp, 0, 255), 0


def update(content):
    global heat_mat
    # sparking flame:
    if np.random.rand() < random_fac:
        update_ignition_values()
    heat_mat[ignition_area[0][0]: ignition_area[0][1], ignition_area[1][0]: ignition_area[1][1]] = ignition_values
    # diffusion
    heat_mat = heat_mat + convolve(heat_mat, con_mat)
    # cooling
    heat_mat -= cooldown
    heat_mat = np.clip(heat_mat, 0, 1000000)
    for i in range(content.shape[0]):
        for j in range(content.shape[1]):
            content[i, j, 0] = np.sum(heat_mat[i * resolution: (i + 1) * resolution, j * resolution: (j + 1) * resolution]) / resolution ** 2

    for i in range(content.shape[0]):
        for j in range(content.shape[1]):
            content[i, j] = color_linear(content[i, j, 0])

    content[candle_area[0][0]: candle_area[0][1], candle_area[1][0]: candle_area[1][1]] = [200, 200, 10]
