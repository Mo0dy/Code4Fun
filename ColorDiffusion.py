from Code4Fun.Utility.Vec2 import *
import numpy as np
import pygame as pg
import pygame.surfarray
import scipy.ndimage
import numba as nb


mat_shape = 500, 500

random_fac = 0.01

cooldown = 0

pg.init()
origin = Vec2(np.array(mat_shape)) / 2
screen = pg.display.set_mode(mat_shape)
pg.display.set_caption("Fire Animation")
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms", 50)


# new_mat = np.zeros(mat_shape, dtype=np.float)
# old_mat = np.zeros(mat_shape, dtype=np.float)
#
# mats = [new_mat, old_mat]
#
# curr_mat = True

orig_mat = np.zeros(mat_shape, dtype=np.float)


con_mat = np.array([[0.05, 0.2, 0.05],
                    [0.2, -1, 0.2],
                    [0.05, 0.2, 0.05]])


def seed():
    x = np.random.randint(0, mat_shape[0] - 11)
    y = np.random.randint(0, mat_shape[1] - 11)
    orig_mat[x: x + 10, y: y + 10] = 100000


@nb.guvectorize([(nb.uint8[:, :, :], nb.float64[:, :])], '(a,b,c),(a,b)', target='parallel', cache=True)
def render(screen_mat, mat):
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            if mat[i, j] < 255:
                screen_mat[i, j, 0] = mat[i, j]
                screen_mat[i, j, 1] = 0
            else:
                screen_mat[i, j, 0] = 255
                screen_mat[i, j, 1] = mat[i, j] - 255

                if screen_mat[i, j, 1] > 255:
                    screen_mat[i, j, 1] = 255


# @nb.guvectorize([(nb.float64[:, :], nb.float64[:, :], nb.float64, nb.float64[:, :])], '(a,b),(a,b),(),(c,d)', target='parallel', cache=True, nopython=True)
# def fast_update(n_mat, o_mat, cool, lap_mat):
#     for i in range(o_mat.shape[0] - 2):
#         ii = i + 1
#         for j in range(o_mat.shape[1] - 2):
#             jj = j + 1
#             my_sum = 0
#             for a in range(3):
#                 for b in range(3):
#                     my_sum += o_mat[i + a, j + b] * lap_mat[a, b]
#             n_mat[ii, jj] += my_sum - cool
#             if n_mat[ii, jj] < 0:
#                 n_mat[ii, jj] = 0

@nb.guvectorize([(nb.float64[:, :], nb.float64, nb.float64[:, :])], '(a,b),(),(c,d)', target='parallel', cache=True, nopython=True)
def fast_update(mat, cool, lap_mat):
    for i in range(orig_mat.shape[0] - 2):
        ii = i + 1
        for j in range(orig_mat.shape[1] - 2):
            jj = j + 1
            my_sum = 0
            for a in range(3):
                for b in range(3):
                    my_sum += orig_mat[i + a, j + b] * lap_mat[a, b]
            mat[ii, jj] += my_sum - cool
            if mat[ii, jj] < 0:
                mat[ii, jj] = 0


iterator = 0
def update():
    global mats, iterator, curr_mat, orig_mat
    # sparking flame:
    if np.random.rand() < random_fac:
        seed()
    # diffusion
    fast_update(heat_mat, cooldown, con_mat)

    if iterator % 20:
        render(pg.surfarray.pixels3d(screen), heat_mat)

    # curr_mat = not curr_mat

    iterator += 1

loop = True
while loop:
    clock.tick(200)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False

    update()
    pg.display.flip()
pg.quit()