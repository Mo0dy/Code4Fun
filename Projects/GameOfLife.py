from Code4Fun.Utility.Vec2 import *
import numpy as np
import pygame as pg
import numba as nb
import Code4Fun.Utility.TimeTest as Test
import Code4Fun.Utility.Renderer as rnd

mat_shape = 800, 800

glider = np.array([[0, 1, 0],
                  [0, 0, 1],
                  [1, 1, 1]])

mats = [np.zeros(mat_shape, dtype=np.uint8), np.zeros(mat_shape, dtype=np.uint8)]

curr_mat = 0

def init():
    global mat
    mats[0] = (np.random.rand(mat_shape[0], mat_shape[1]) * 2).astype(np.uint8)


pg.init()
window_size = mat_shape[0], mat_shape[1]
origin = Vec2(np.array(window_size)) / 2
screen = pg.display.set_mode(window_size)
pg.display.set_caption("Matrix Animations")
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms", 20)

size_x = window_size[0] / mat_shape[0]
size_y = window_size[1] / mat_shape[1]


@nb.guvectorize([(nb.uint8[:, :], nb.uint8[:, :])], '(a,b),(a,b)', target='parallel', cache=True)
def do_step(old_m, new_m):
    for i in range(new_m.shape[0] - 2):
        ii = i + 1
        for j in range(new_m.shape[1] - 2):
            jj = j + 1

            con_sum = old_m[i, j] + old_m[i + 1, j] + old_m[i + 2, j] + \
                      old_m[i, j + 1] + old_m[i + 2, j + 1] + \
                      old_m[i, j + 2] + old_m[i + 1, j + 2] + old_m[i + 2, j + 2]

            # live cell
            if old_m[ii, jj]:
                if 3 < con_sum or con_sum < 2:
                    new_m[ii, jj] = 0
                else:
                    new_m[ii, jj] = 1
            # dead cell
            elif con_sum == 3:
                    new_m[ii, jj] = 1
            else:
                new_m[ii, jj] = 0


def reset():
    init()


def clear():
    global content
    content = np.zeros(mat_shape)


def update():
    global curr_mat
    do_step(mats[curr_mat], mats[not curr_mat])
    curr_mat = not curr_mat


def draw():
    screen.fill((50, 50, 50))
    rnd.render_bool_arr(mats[curr_mat], np.array([255, 0, 0], dtype=np.uint8), pg.surfarray.pixels3d(screen))
    fps = font.render("%0.2f" % clock.get_fps(), True, (255, 255, 255))
    screen.blit(fps, (10, 10))
    pg.display.flip()



keydown_func = {
    pg.K_r: reset
}


reset()
loop = True
while loop:
    clock.tick(60)
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
pg.quit()
