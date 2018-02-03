import numpy as np
import pygame as pg
# from MyMaths.Vec2 import Vec2
from TopLevel.Vec2 import Vec2
from copy import deepcopy

# size = Vec2(1400, 1000)
size = Vec2(1120, 800)
man_min = Vec2(-2.5, -1.25)
man_max = Vec2(1, 1.25)

origin = size / 2
iterations = 80
stepsize = 255 / iterations

draw_guidlines = False

pg.init()
screen = pg.display.set_mode(size.tuple_int)
pg.display.set_caption("Mandelbrot FTW")

screen.fill((255, 255, 255))

font = pg.font.SysFont("comicsansms", 50)

a, b = np.meshgrid(np.linspace(man_min.y, man_max.y, size.y) * 1j, np.linspace(man_min.x, man_max.y, size.x))
indices = a + b
mandelbrot_values = np.zeros(indices.shape)
mandelbrot_screen = deepcopy(pg.surfarray.pixels2d(screen))


iterator = 0
def init():
    global iterator
    global mandelbrot_values
    global indices

    iterator = 0
    a, b = np.meshgrid(np.linspace(man_min.y, man_max.y, size.y) * 1j, np.linspace(man_min.x, man_max.x, size.x))
    indices = a + b
    mandelbrot_values = np.zeros(indices.shape)


def zoom(zoom_factor):
    global man_min
    global man_max
    center = (man_min + man_max) / 2
    min_rel = man_min - center
    max_rel = man_max - center
    min_rel *= zoom_factor
    max_rel *= zoom_factor
    man_min = center + min_rel
    man_max = center + max_rel


def zoom_in():
    zoom(0.5)
    init()


def zoom_out():
    zoom(1.5)
    init()


def center_on_mouse():
    global man_min
    global man_max
    global stepsize

    stepsize = 255 / iterations

    # change center pos
    d_m = Vec2(size.x / 2 - pg.mouse.get_pos()[0], size.y / 2 - pg.mouse.get_pos()[1])
    delta = Vec2(d_m.x / size.x * (man_max.x - man_min.x), d_m.y / size.y * (man_max.y - man_min.y))

    man_min -= delta
    man_max -= delta
    init()


def reset():
    global man_min
    global man_max

    man_min = Vec2(-2.5, -1.25)
    man_max = Vec2(1, 1.25)
    init()


loop = True
while loop:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False
        elif e.type == pg.MOUSEBUTTONDOWN:
            center_on_mouse()
        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_RIGHT:
                iterations *= 2
                init()
            elif e.key == pg.K_LEFT:
                iterations /= 2
                init()
            elif e.key == pg.K_SPACE:
                reset()
            elif e.key == pg.K_DOWN:
                zoom_out()
            elif e.key == pg.K_UP:
                zoom_in()
            elif e.key == pg.K_c:
                draw_guidlines = not draw_guidlines

    if iterator < iterations:
        mandelbrot_values = np.square(mandelbrot_values) + indices
        mandelbrot_screen[np.absolute(mandelbrot_values) < 4] = iterator * stepsize

        screen.fill((255, 255, 255))
        text = font.render("Iter: " + str(iterator), True, (50, 50, 100))
        pg.surfarray.pixels2d(screen)[:, :] = mandelbrot_screen[:, :]
        screen.blit(text, (10, size.y - 70))
        if draw_guidlines:
            pg.draw.line(screen, (80, 80, 80), (origin.x, 0), (origin.x, size.y))
            pg.draw.line(screen, (80, 80, 80), (0, origin.y), (size.x, origin.y))
            pg.draw.line(screen, (120, 80, 80), (pg.mouse.get_pos()[0] - 100, pg.mouse.get_pos()[1]), (pg.mouse.get_pos()[0] + 100, pg.mouse.get_pos()[1]))
            pg.draw.line(screen, (120, 80, 80), (pg.mouse.get_pos()[0], pg.mouse.get_pos()[1] - 100), (pg.mouse.get_pos()[0], pg.mouse.get_pos()[1] + 100))
        pg.display.flip()
        iterator += 1
pg.quit()






