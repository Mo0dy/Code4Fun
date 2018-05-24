import numpy as np
import pygame as pg
from Code4Fun.Utility.Vec2 import Vec2
from numba import guvectorize, complex64, int32
from PIL import Image


# size = Vec2(1400, 1000)
# size = Vec2(1120, 400)
size = Vec2(1680, 600)
man_min = Vec2(-2.5, -1.25)
man_max = Vec2(1, 1.25)

jul_min = Vec2(-1.75, -1.25)
jul_max = Vec2(1.75, 1.25)

julia_size = Vec2(int(size.x / 2), size.y)
man_size = Vec2(int(size.x / 2), size.y)

# x_size = 3000
# size = Vec2(int(x_size / 3.5 * 2.5), x_size)

origin = size / 2
iterations = 150
julia_iterations = 150
draw_guidlines = False
draw_min_mandel = True
lock_julia = False
julia_pos = 0 + 0j


pg.init()
screen = pg.display.set_mode(size.tuple_int)
pg.display.set_caption("Mandelbrot Numba")
font = pg.font.SysFont("comicsansms", 50)
text = font.render(" ", True, (100, 50, 50))
mandelbrot_screen = np.empty((man_size.x, man_size.y))
julia_screen = np.empty((julia_size.x, julia_size.y))

iterator = 0


def save_image():
    Image.fromarray(pg.surfarray.pixels3d(screen)).save("julia_set.png")


def init():
    global iterator
    global mandelbrot_values
    global indices
    global text
    global mandelbrot_screen

    mandelbrot_screen = mandelbrot_set(man_min.x, man_max.x, man_min.y, man_max.y, man_size.x, man_size.y, iterations)
    pg.surfarray.pixels2d(screen)[0:man_size.x, :] = mandelbrot_screen
    update_julia()


def update_julia():
    global julia_screen, julia_pos
    if not lock_julia:
        julia_pos = mouse_to_complex()
    julia_screen = julia_set(jul_min.x, jul_max.x, jul_min.y, jul_max.y, julia_size.x, julia_size.y, julia_iterations, julia_pos)
    pg.surfarray.pixels2d(screen)[man_size.x: man_size.x + julia_size.x, :] = julia_screen

    if draw_min_mandel:
        mini_mandel()

    pg.display.flip()


def mini_mandel():
    mini_mandel_min, mini_mandel_max = mini_mandel_pos()
    mini_mandel = mandelbrot_set(mini_mandel_min.x, mini_mandel_max.x, mini_mandel_min.y, mini_mandel_max.y, 175, 125, iterations * 3)
    mini_max = np.max(mini_mandel)
    if mini_max < 255:
        mini_mandel = mini_mandel / mini_max * 255
    pg.surfarray.pixels2d(screen)[10: 185, 10: 135] = mini_mandel
    pg.draw.line(screen, (100, 80, 50), (int(175 / 2) + 10, 10), (int(175 / 2) + 10, 135))
    pg.draw.line(screen, (100, 80, 50), (10, int(125 / 2) + 10), (185, int(125 / 2) + 10))
    pg.draw.line(screen, (100, 50, 50), (10, 10), (10, 135), 2)
    pg.draw.line(screen, (100, 50, 50), (185, 10), (185, 135), 2)
    pg.draw.line(screen, (100, 50, 50), (10, 135), (185, 135), 2)
    pg.draw.line(screen, (100, 50, 50), (10, 10), (185, 10), 2)


def mouse_to_complex():
    mpos = pg.mouse.get_pos()
    m_x = mpos[0]
    m_y = mpos[1]

    real = m_x / man_size.x * (man_max.x - man_min.x) + man_min.x
    imag = m_y / man_size.y * (man_max.y - man_min.y) + man_min.y
    return real + imag * 1j


def mini_mandel_pos():
    m_pos = mouse_to_complex()
    m_vec = Vec2(m_pos.real, m_pos.imag)
    delta = (man_min - man_max) / 20
    return m_vec + delta, m_vec - delta


def zoom(zoom_factor, **kwargs):
    global man_min, man_max

    if "pos" in kwargs:
        center = Vec2(kwargs["pos"].real, kwargs["pos"].imag)
    else:
        center = (man_min + man_max) / 2
    min_rel = man_min - center
    max_rel = man_max - center
    min_rel *= zoom_factor
    max_rel *= zoom_factor
    man_min = center + min_rel
    man_max = center + max_rel
    init()


def zoom_julia(zoom_factor):
    global jul_min, jul_max
    center = (jul_min + jul_max) / 2
    min_rel = jul_min - center
    max_rel = jul_max - center
    min_rel *= zoom_factor
    max_rel *= zoom_factor
    jul_min = center + min_rel
    jul_max = center + max_rel
    update_julia()


def zoom_in():
    zoom(0.5)


def zoom_out():
    zoom(1.5)


def center_on(pos):
    global man_min, man_max, stepsize

    d_m = Vec2(man_size.x / 2 - pos[0], man_size.y / 2 - pos[1])
    delta = Vec2(d_m.x / man_size.x * (man_max.x - man_min.x), d_m.y / man_size.y * (man_max.y - man_min.y))

    man_min -= delta
    man_max -= delta
    init()


def center_on_mouse():
    center_on(pg.mouse.get_pos())


def reset():
    global man_min, man_max, jul_min, jul_max
    man_min = Vec2(-2.5, -1.25)
    man_max = Vec2(1, 1.25)
    jul_min = Vec2(-1.75, -1.25)
    jul_max = Vec2(1.75, 1.25)
    init()


@guvectorize([(complex64[:], int32, int32[:])], '(n),()->(n)', target='parallel')
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


@guvectorize([(complex64[:], complex64, int32, int32[:])], '(n),(),()->(n)', target='parallel')
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


def julia_set(xmin, xmax, ymin, ymax, width, height, maxiter, pos):
    r1 = np.linspace(xmin, xmax, width, dtype=np.float32)
    r2 = np.linspace(ymin, ymax, height, dtype=np.float32)
    c = r1 + r2[:, None] * 1j
    n3 = julia_numpy(c, pos, maxiter)
    return n3.T


def offset_julia(offset):
    global jul_min, jul_max
    x_tot = jul_max.x - jul_min.x
    y_tot = jul_max.y - jul_min.y

    offset.x *= x_tot
    offset.y *= y_tot

    jul_min += offset
    jul_max += offset
    update_julia()


init()
loop = True
while loop:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False
        elif e.type == pg.MOUSEBUTTONDOWN:
            # leftklick
            if e.button == 1:
                zoom_julia(0.5)
                update_julia()
            # middle mouse button
            if e.button == 2:
                center_on_mouse()
            # rightklick
            elif e.button == 3:
                zoom_julia(1.5)
                update_julia()
            # scroll_up
            elif e.button == 4:
                zoom(0.5, pos=mouse_to_complex())
            # scroll_up
            elif e.button == 5:
                zoom(1.5, pos=mouse_to_complex())
            elif e.button == 6:
                iterations = int(iterations / 2)
                init()
            elif e.button == 7:
                iterations *= 2
                init()
        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_RIGHT:
                offset_julia(Vec2(0.1, 0))
            elif e.key == pg.K_LEFT:
                offset_julia(Vec2(-0.1, 0))
            elif e.key == pg.K_SPACE:
                reset()
            elif e.key == pg.K_DOWN:
                offset_julia(Vec2(0, 0.1))
            elif e.key == pg.K_UP:
                offset_julia(Vec2(0, -0.1))

            elif e.key == pg.K_c:
                draw_guidlines = not draw_guidlines
            elif e.key == pg.K_KP_PLUS:
                zoom_julia(0.5)
                update_julia()
            elif e.key == pg.K_KP_MINUS:
                zoom_julia(1.5)
                update_julia()
            elif e.key == pg.K_m:
                draw_min_mandel = not draw_min_mandel
                init()
            elif e.key == pg.K_p:
                lock_julia = not lock_julia
            elif e.key == pg.K_o:
                julia_iterations *= 2
                update_julia()
            elif e.key == pg.K_l:
                julia_iterations = int(julia_iterations / 2)
                update_julia()
            elif e.key == pg.K_s:
                save_image()
        elif e.type == pg.MOUSEMOTION:
            update_julia()

pg.quit()






