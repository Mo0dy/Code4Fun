from Code4Fun.Utility.Vec2 import *
import numpy as np
import pygame as pg
from scipy.ndimage.filters import convolve

mat_shape = np.array([8, 8, 3])
margins = 10
resolution = 2
content = np.zeros(mat_shape)
heat_mat = np.zeros(mat_shape[:2] * resolution, dtype=np.float)

con_mat = np.array([[0.05, 0.2, 0.05],
                    [0.2, -1, 0.2],
                    [0.05, 0.2, 0.05]])

con_mat = np.array([[0.07, 0.2, 0.03],
                    [0.35, -1, 0.05],
                    [0.07, 0.2, 0.03]])

pg.init()
window_size = 800, 800
origin = Vec2(np.array(window_size)) / 2
screen = pg.display.set_mode(window_size)
pg.display.set_caption("test")
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms", 50)
value = np.reshape(np.random.random_integers(2, 25, 9), (3, 3)) * 10


def color_temperature(temp):
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


def reset():
    global heat_mat
    # for i in range(10, 30):
    #     for j in range(10, 20):
    #         heat_mat[i, j] = 255


def clear():
    global content
    content = np.zeros(mat_shape)


def update():
    global heat_mat, value
    # sparking flame:
    if np.random.rand() < 0.1:
        value = np.reshape(np.random.random_integers(2, 25, 9), (3, 3)) * 10
    heat_mat[7:10, 13:16] = value
    # diffusion
    heat_mat = heat_mat + convolve(heat_mat, con_mat)
    # cooling
    heat_mat -= 5
    heat_mat = np.clip(heat_mat, 0, 1000000)
    for i in range(content.shape[0]):
        for j in range(content.shape[1]):
            content[i, j, 0] = np.sum(heat_mat[i * resolution: (i + 1) * resolution, j * resolution: (j + 1) * resolution]) / resolution ** 2

    for i in range(content.shape[0]):
        for j in range(content.shape[1]):
            content[i, j] = color_temperature(content[i, j, 0] * 0.2 + 11)


def draw():
    size_x = window_size[0] / content.shape[0]
    size_y = window_size[1] / content.shape[1]

    for i in range(content.shape[0]):
        for j in range(content.shape[1]):
            pg.draw.rect(screen, content[i, j], (i * size_x + margins, j * size_y + margins, size_x - margins * 2, size_y - margins * 2))


keydown_func = {
    pg.K_r: reset
}


reset()
loop = True
while loop:
    clock.tick()
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False
        elif e.type == pg.KEYDOWN:
            keydown_func[e.key]()

    update()
    screen.fill((50, 50, 50))
    draw()
    pg.display.flip()
pg.quit()
