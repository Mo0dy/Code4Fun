from Code4Fun.Utility.Vec2 import *
from Code4Fun.Utility.Transform import *
from Code4Fun.Utility.Renderer import *
import numpy as np
import pygame as pg
import numba as nb
import pygame.surfarray


pg.init()
window_size = 1400, 900
origin = Vec2(np.array(window_size)) / 2
screen = pg.display.set_mode(window_size)
pg.display.set_caption("test")
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms", 50)
t = Transformation()
t.scale(100, -130)
t.trans(origin.x, window_size[1])
t.save()


mb_pressed = False
last_mouse_pos = Vec2(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])

# Variables
points = np.zeros((500000, 2), dtype=np.float32)
dummy = np.zeros(window_size, dtype=np.uint8)

def vec_mouse_pos():
    return Vec2(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])


def zoom(zoom_factor):
    t.trans(-1 * vec_mouse_pos())
    t.scale(zoom_factor, zoom_factor)
    t.trans(vec_mouse_pos())
    reset()


def move_screen():
    global last_mouse_pos
    mouse_pos = Vec2(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
    t.trans(mouse_pos - last_mouse_pos)
    last_mouse_pos = mouse_pos
    reset()


# creates transformation matrix from function parameters and couples it with a probability
def c_func(a, b, c, d, e, f):
    return np.array([[a, b, e],
                    [c, d, f],
                    [0, 0, 1]], dtype=np.float32)


fern = {"mats": np.array([c_func(0, 0, 0, 0.16, 0, 0),
        c_func(0.85, 0.04, -0.04, 0.85, 0, 1.6),
        c_func(0.2, -0.26, 0.23, 0.22, 0, 1.6),
        c_func(-0.15, 0.28, 0.26, 0.24, 0, 0.44)], dtype=np.float32),
        "probs": np.array([0.01, 0.86, 0.93, 1], dtype=np.float32)}


@nb.guvectorize([(nb.float32[:, :, :], nb.float32[:], nb.float32[:], nb.float32[:, :])], '(n,a,a),(n),(b),(c,b)', target='parallel')
def do_steps(matrices, probabilities, p, output):
    for i in range(output.shape[0]):
        # figure out a random number
        rand = np.random.rand()
        index = 0
        while probabilities[index] < rand:
            index += 1

        # matrix operation (we know that [2, 0] and [2, 1] = 0 as well as [2, 2] = 1 so we will write these explicitly
        p[0] = matrices[index][0, 0] * p[0] + matrices[index][0, 1] * p[1] + matrices[index][0, 2]
        p[1] = matrices[index][1, 0] * p[0] + matrices[index][1, 1] * p[1] + matrices[index][1, 2]
        output[i, 0] = p[0]
        output[i, 1] = p[1]


def do_step(trans, p):
    do_steps(trans["mats"], trans["probs"], np.array([0, 0], dtype=np.float32), points)


def reset():
    pass


def update(dt):
    global fern
    if mb_pressed:
        move_screen()


def draw():
    global points, render_arr
    # render_arr[:, :] = (50, 50, 50)
    screen.fill((50, 50, 50))
    color = np.array([255, 255, 255], dtype=np.uint8)
    render_points(t * points, color, pg.surfarray.pixels3d(screen))

    text = font.render(str(clock.get_fps()), True, (100, 100, 100))
    screen.blit(text, (100, 100))

def rotate(amount):
    t.trans(-1 * origin)
    t.rotate(amount)
    t.trans(origin)
    reset()


keydown_func = {
    pg.K_r: reset,
    pg.K_RIGHT: lambda: rotate(0.2),
    pg.K_LEFT: lambda: rotate(-0.2)
}


reset()
do_step(fern, points)

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
        elif e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1:
                mb_pressed = True
                last_mouse_pos = Vec2(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
            elif e.button == 4:
                zoom(2)
            elif e.button == 5:
                zoom(0.5)
        elif e.type == pg.MOUSEBUTTONUP:
            if e.button == 1:
                mb_pressed = False

    update(clock.get_time())
    draw()
    pg.display.flip()
pg.quit()
