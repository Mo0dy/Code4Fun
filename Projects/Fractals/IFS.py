from Code4Fun.Utility.Vec2 import *
from Code4Fun.Utility.Transform import *
from Code4Fun.Utility.Renderer import *
import Code4Fun.Projects.Fractals.ISFTemplates as tmplt
import numpy as np
import pygame as pg
import numba as nb
import pygame.surfarray
import os


point_amount = int(2e6)
trans = tmplt.barnsleys_fern
autoscale = True


os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 25)
pg.init()
window_size = 800, 800
origin = Vec2(np.array(window_size)) / 2
screen = pg.display.set_mode(window_size)
pg.display.set_caption("test")
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms", 20)
t = Transformation()


mb_pressed = False
last_mouse_pos = Vec2(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])

# Variables
points = np.zeros((point_amount, 2), dtype=np.float32)


def vec_mouse_pos():
    return Vec2(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])


def reset():
    if autoscale:
        min_x = np.min(points[:, 0])
        max_x = np.max(points[:, 0])
        min_y = np.min(points[:, 1])
        max_y = np.max(points[:, 1])

        dx = abs(max_x - min_x)
        dy = abs(min_y - max_y)

        sx = (window_size[0] - 50) / dx
        sy = (window_size[1] - 50) / dy

    t.reset()
    t.scale(sx, -sy)
    t.trans(origin.x - (min_x + max_x) / 2 * sx, window_size[1] + min_y * sy)


def reload():
    do_steps(trans["mats"], trans["probs"], np.array([0, 0], dtype=np.float32), points)


def move_screen():
    global last_mouse_pos
    mouse_pos = Vec2(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
    t.trans(mouse_pos - last_mouse_pos)
    last_mouse_pos = mouse_pos


@nb.guvectorize([(nb.float32[:, :, :], nb.float32[:], nb.float32[:], nb.float32[:, :])], '(n,a,a),(n),(b),(c,b)', target='parallel', cache=True)
def do_steps(matrices, probabilities, start_p, output):
    for i in range(output.shape[0]):
        # figure out a random number
        rand = np.random.rand()
        index = 0
        while probabilities[index] < rand:
            index += 1

        # matrix operation (we know that [2, 0] and [2, 1] = 0 as well as [2, 2] = 1 so we will write these explicitly
        start_p[0] = matrices[index][0, 0] * start_p[0] + matrices[index][0, 1] * start_p[1] + matrices[index][0, 2]
        start_p[1] = matrices[index][1, 0] * start_p[0] + matrices[index][1, 1] * start_p[1] + matrices[index][1, 2]
        output[i, 0] = start_p[0]
        output[i, 1] = start_p[1]


def update(dt):
    global fern
    if mb_pressed:
        move_screen()


def draw():
    global points
    # render_arr[:, :] = (50, 50, 50)
    screen.fill((50, 50, 50))
    color = np.array([255, 255, 255], dtype=np.uint8)
    render_points(t * points, color, pg.surfarray.pixels3d(screen))

    text = font.render(str(clock.get_fps()), True, (100, 50, 50))
    screen.blit(text, (10, 10))


keydown_func = {
    pg.K_r: reset,
    pg.K_l: reload,
    pg.K_RIGHT: lambda: t.rotate(vec_mouse_pos(), 0.2),
    pg.K_LEFT: lambda: t.rotate(vec_mouse_pos(), -0.2)
}


reload()
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
        elif e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1:
                mb_pressed = True
                last_mouse_pos = Vec2(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
            elif e.button == 4:
                t.zoom(vec_mouse_pos(), 2)
            elif e.button == 5:
                t.zoom(vec_mouse_pos(), 0.5)
        elif e.type == pg.MOUSEBUTTONUP:
            if e.button == 1:
                mb_pressed = False

    update(clock.get_time())
    draw()
    pg.display.flip()
pg.quit()
