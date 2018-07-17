from Code4Fun.Utility.Vec2 import *
import numpy as np
import pygame as pg
import pygame.surfarray
import scipy.ndimage
import numba as nb


mat_shape = 301, 501

nx = mat_shape[0]
ny = mat_shape[1]

mul_dx = 0.8
random_fac = 0.05
res = 15

scale = 1

pg.init()
# screen = pg.display.set_mode([m * scale for m in mat_shape])
screen = pg.display.set_mode((nx * scale, ny * scale))
pg.display.set_caption("Fire Animation")
clock = pg.time.Clock()
clock.tick()
font = pg.font.SysFont("comicsansms", 50)


mat_1 = np.zeros(mat_shape, dtype=np.float64)
mat_2 = np.zeros(mat_shape, dtype=np.float64)

curr_mat = False

D = 0.2
E = -15

dx = 1 / mat_shape[0]
dy = 1 / mat_shape[1]

mat_1[100:200, -1] = 500
mat_2[100:200, -1] = 500

ign_dx = int(mat_1.shape[0] * mul_dx / res)

cooling = 0.1


@nb.guvectorize([(nb.uint8[:, :, :], nb.float64[:, :])], '(a,b,c),(a,b)', target='parallel', cache=True)
def render(screen_mat, mat):
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            if mat[i, j] < 255:
                screen_mat[i, j, 0] = mat[i, j]
                # screen_mat[i, j, 0] = 0
                screen_mat[i, j, 1] = 0
            else:
                screen_mat[i, j, 0] = 255
                screen_mat[i, j, 1] = mat[i, j] - 255

                if screen_mat[i, j, 1] > 255:
                    screen_mat[i, j, 1] = 255


@nb.guvectorize([(nb.uint8[:, :, :], nb.float64[:, :], nb.int8)], '(a,b,c),(e,f),()', target='parallel', cache=True)
def render_scale(screen_mat, mat, s):
    color = np.array([0, 0])
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            if mat[i, j] < 255:
                color[0] = mat[i, j]
                color[1] = 0
            else:
                color[0] = 255
                color[1] = mat[i, j] - 255

                if color[1] > 255:
                    color[1] = 255
            for a in range(s):
                for b in range(s):
                    screen_mat[i * s + a, j * s + b, 0] = color[0]
                    screen_mat[i * s + a, j * s + b, 1] = color[1]


@nb.guvectorize([(nb.float64[:, :], nb.float64[:, :])], '(a,b),(a,b)', target='parallel', cache=True, nopython=True)
def fast_update(mat, o_mat):
    c = ny / nx
    csqr = c ** 2
    for ii in range(o_mat.shape[0] - 2):
        i = ii + 1
        for jj in range(o_mat.shape[1] - 2):
            j = jj + 1
            # mat[i, j] = o_mat[i, j] + (D * ((o_mat[i - 1, j] - 2 * o_mat[i, j] + o_mat[i + 1, j]) / dx ** 2 + (o_mat[i, j - 1] - 2 * o_mat[i, j] + o_mat[i, j + 1]) / dy ** 2) - \
            #     E * ((o_mat[i, j + 1] - o_mat[i, j -1]) / dy)) * 0.000002

            mat[i, j] = o_mat[i, j] + nx * (D * nx * ((o_mat[i - 1, j] - 2 * o_mat[i, j] + o_mat[i + 1, j]) + (o_mat[i, j - 1] - 2 * o_mat[i, j] + o_mat[i, j + 1]) / csqr) - \
                E * ((o_mat[i, j + 1] - o_mat[i, j -1]) * c)) * 0.00001

    # neumann randbedingungen adiabat:
    # for jj in range(mat.shape[1] - 2):
    #     j = jj + 1
    #     mat[0, j] = o_mat[1, j]
    #     mat[-1, j] = o_mat[-2, j]


iterator = 0
def update():
    global mat_1, mat_2, curr_mat, iterator

    # sparking flame:
    if np.random.rand() < random_fac:
        # dirichtle randbedingung (does not get updates)
        ignition_values = np.random.random_integers(150, 500, ign_dx)
        ignition_values = scipy.ndimage.zoom(ignition_values, res, order=0)

        start = int((nx - ignition_values.shape[0]) / 2)

        mat_1[start:start+ignition_values.shape[0], -1] = ignition_values
        mat_2[start:start+ignition_values.shape[0], -1] = ignition_values

        # mat_1[:, -1] = 0
        # mat_2[:, -1] = 0
        # for i in range(7):
        #     start = np.random.random_integers(50, mat_1.shape[0] - 100)
        #     end = start + 30
        #
        #     mat_1[start:end, -1] = 500
        #     mat_2[start:end, -1] = 500
    # diffusion
    if curr_mat:
        fast_update(mat_1, mat_2)
        cpy = mat_1[:, -1].copy()
        mat_1 -= cooling
        mat_1[mat_1 < 0] = 0
        mat_1[:, -1] = cpy
    else:
        fast_update(mat_2, mat_1)
        cpy = mat_1[:, -1].copy()
        mat_2 -= cooling
        mat_2[mat_2 < 0] = 0
        mat_2[:, -1] = cpy

    curr_mat = not curr_mat

    if not iterator % 40:
        if scale > 1:
            render_scale(pg.surfarray.pixels3d(screen), mat_1, scale)
        else:
            render(pg.surfarray.pixels3d(screen), mat_1)
        # for i in range(mat_shape[0]):
        #     for j in range(mat_shape[1]):
        #         if mat_1[i, j] < 255:
        #             color = [mat_1[i, j], 0, 0]
        #         else:
        #             color = [255, mat_1[i, j] - 255, 0]
        #             if color[1] > 255:
        #                 color[1] = 255
        #         pg.draw.rect(screen, color, (i * scale, j * scale, scale, scale))
    iterator += 1

loop = True
while loop:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False

    update()
    pg.display.flip()
pg.quit()