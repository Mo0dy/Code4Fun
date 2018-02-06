from Code4Fun.Utility.Vec2 import *
import numpy as np
import pygame as pg
from scipy.ndimage.filters import convolve
import numba as nb



mat_shape = 100, 100


con_mat = np.array([[1, 1, 1],
                    [1, 0, 1],
                    [1, 1, 1]], dtype=np.uint8)


glider = np.array([[0, 1, 0],
                  [0, 0, 1],
                  [1, 1, 1]])

mat = np.zeros(mat_shape, dtype=np.uint8)

def init():
    global mat
    mat = (np.random.rand(mat_shape[0], mat_shape[1]) * 2).astype(np.uint8)


pg.init()
window_size = mat_shape[0] * 5, mat_shape[1] * 5
origin = Vec2(np.array(window_size)) / 2
screen = pg.display.set_mode(window_size)
pg.display.set_caption("Matrix Animations")
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms", 20)

size_x = window_size[0] / mat.shape[0]
size_y = window_size[1] / mat.shape[1]


@nb.guvectorize([(nb.uint8[:, :], nb.uint8[:, :])], '(a,b),(c,d)', target='parallel')
def do_step(m, c_m):
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            for a in range()
            # live cell
            if m[i, j]:
                if 3 < n_amount or n_amount < 2:
                    mat[i, j] = 0
            # dead cell
            else:
                if n_amount == 3:
                    m[i, j] = 1


def reset():
    init()


def clear():
    global content
    content = np.zeros(mat_shape)


def update():
    do_step(mat, con_mat)


def draw():
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            pg.draw.rect(screen, (mat[i, j] * 255, 0, 0), (i * size_x, j * size_y, size_x, size_y))
    fps = font.render("%0.2f" % clock.get_fps(), True, (255, 255, 255))
    screen.blit(fps, (10, 10))


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
            try:
                keydown_func[e.key]()
            except:
                pass

    update()
    draw()
    pg.display.flip()
pg.quit()
