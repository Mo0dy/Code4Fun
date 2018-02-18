from Code4Fun.Utility.Vec2 import *
import numpy as np
import pygame as pg
import pygame.surfarray
import scipy.ndimage
import numba as nb


mat_shape = 350, 500


mul_dx = 0.05
mul_dy = 0.03
random_fac = 0.05
start_y_mul = 0.9

cooldown = 0.5


pg.init()
origin = Vec2(np.array(mat_shape)) / 2
screen = pg.display.set_mode(mat_shape)
pg.display.set_caption("Fire Animation")
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms", 50)


heat_mat = np.zeros(mat_shape, dtype=np.float)
res = 6
ign_x = int(heat_mat.shape[0] / 2)
ign_y = int(heat_mat.shape[1] * start_y_mul)
ign_dy = int(heat_mat.shape[1] * mul_dy / 5) * 5
ign_dx = int(heat_mat.shape[0] * mul_dx / 5) * 5
ignition_area = np.array([[ign_x - ign_dx, ign_x + ign_dx], [ign_y - ign_dy, ign_y + ign_dy]])


def update_ignition_values():
    global ignition_values
    # ignition_values = np.reshape(np.random.random_integers(50, 60, ign_dx * 4 * ign_dy), (ign_dx * 2, ign_dy * 2)) * 8
    ignition_values = np.reshape(np.random.random_integers(50, 60, int(ign_dx * ign_dy * 4 / res ** 2)), (int(ign_dx * 2 / res), int(ign_dy * 2 / res))) * 8
    ignition_values = scipy.ndimage.zoom(ignition_values, res, order=0)


update_ignition_values()
heat_mat[ignition_area[0][0]: ignition_area[0][1], ignition_area[1][0]: ignition_area[1][1]] = ignition_values


con_mat = np.array([[0.02, 0.15, 0.12],
                    [0.02, -1, 0.4],
                    [0.02, 0.15, 0.12]])


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


@nb.guvectorize([(nb.float64[:, :], nb.float64, nb.float64[:, :])], '(a,b),(),(c,d)', target='parallel', cache=True)
def fast_update(mat, cool, lap_mat):
    for i in range(heat_mat.shape[0] - 2):
        ii = i + 1
        for j in range(heat_mat.shape[1] - 2):
            jj = j + 1
            my_sum = 0
            for a in range(3):
                for b in range(3):
                    my_sum += heat_mat[i + a, j + b] * lap_mat[a, b]
            mat[ii, jj] += my_sum - cool
            if mat[ii, jj] < 0:
                mat[ii, jj] = 0


iterator = 0
def update():
    global heat_mat, iterator
    # sparking flame:
    if np.random.rand() < random_fac:
        update_ignition_values()
    heat_mat[ignition_area[0][0]: ignition_area[0][1], ignition_area[1][0]: ignition_area[1][1]] = ignition_values
    # diffusion
    fast_update(heat_mat, cooldown, con_mat)

    if iterator % 20:
        render(pg.surfarray.pixels3d(screen), heat_mat)
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