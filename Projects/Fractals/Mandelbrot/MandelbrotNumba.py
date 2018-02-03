import numpy as np
import pygame as pg
from TopLevel.Vec2 import Vec2
from copy import deepcopy
from numba import jit, vectorize, guvectorize, float64, complex64, int32, float32, int64
import time
import scipy.misc

# size = Vec2(1400, 1000)
size = Vec2(1120, 800)
man_min = Vec2(-2.5, -1.25)
man_max = Vec2(1, 1.25)
# x_size = 3000
# size = Vec2(int(x_size / 3.5 * 2.5), x_size)

origin = size / 2
iterations = 150
draw_guidlines = False

pg.init()
screen = pg.display.set_mode(size.tuple_int)
pg.display.set_caption("Mandelbrot Numba")
font = pg.font.SysFont("comicsansms", 50)
text = font.render(" ", True, (100, 50, 50))
mandelbrot_screen = np.empty((size.x, size.y))

# screen.fill((255, 255, 255))

iterator = 0
def init():
    global iterator
    global mandelbrot_values
    global indices
    global text
    global mandelbrot_screen

    start_time = time.time()
    mandelbrot_screen = julia_set(man_min.x, man_max.x, man_min.y, man_max.y, size.x, size.y, iterations)
    pg.surfarray.pixels2d(screen)[:, :] = mandelbrot_screen
    text_time = font.render("time: %0.4f" % (time.time() - start_time), True, (100, 50, 50))
    text_iterations = font.render("iter: %d" % iterations, True, (100, 50, 50))
    screen.blit(text_time, (20, 20))
    screen.blit(text_iterations, (20, 80))
    pg.display.flip()


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


@guvectorize([(complex64[:], int32, int32[:])], '(n),()->(n)', target='cuda')
def mandelbrot_numpy(c, maxit, output):
    maxiter = maxit
    step_size = 255 / maxiter
    for i in range(c.shape[0]):
        single_c = c[i]
        nreal = 0
        real = 0
        imag = 0
        iterations_done = 0
        for n in range(maxiter):
            nreal = real * real - imag * imag + single_c.real
            imag = 2 * real * imag + single_c.imag
            real = nreal;
            if real * real + imag * imag > 4.0:
                iterations_done = n
                break
        output[i] = iterations_done * step_size


def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, maxiter):
    r1 = np.linspace(xmin, xmax, width, dtype=np.float32)
    r2 = np.linspace(ymin, ymax, height, dtype=np.float32)
    c = r1 + r2[:, None] * 1j
    n3 = mandelbrot_numpy(c, maxiter)
    return n3.T


@guvectorize([(complex64[:], complex64, int32, int32[:])], '(n),(),()->(n)', target='cuda')
def julia_numpy(c, pos, maxit, output):
    maxiter = maxit
    step_size = 255 / maxiter
    for i in range(c.shape[0]):
        single_c = pos
        nreal = 0
        real = c[i].real
        imag = c[i].imag
        iterations_done = 0
        for n in range(maxiter):
            nreal = real * real - imag * imag + single_c.real
            imag = 2 * real * imag + single_c.imag
            real = nreal;
            if real * real + imag * imag > 4.0:
                iterations_done = n
                break
        output[i] = iterations_done * step_size


def julia_set(xmin, xmax, ymin, ymax, width, height, maxiter):
    r1 = np.linspace(xmin, xmax, width, dtype=np.float32)
    r2 = np.linspace(ymin, ymax, height, dtype=np.float32)
    c = r1 + r2[:, None] * 1j
    n3 = julia_numpy(c, -0.70176 -0.3842 * 1j, maxiter)
    return n3.T


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
                iterations = int(iterations / 2)
                init()
            elif e.key == pg.K_SPACE:
                reset()
            elif e.key == pg.K_DOWN:
                zoom_out()
            elif e.key == pg.K_UP:
                zoom_in()
            elif e.key == pg.K_c:
                draw_guidlines = not draw_guidlines

pg.quit()






