from Code4Fun.Utility.Vec2 import *
import numpy as np
import pygame as pg

background_color = 50, 50, 50
window_size = 800, 800
margin = 100


pg.init()
origin = Vec2(np.array(window_size)) / 2
screen = pg.display.set_mode(window_size)
pg.display.set_caption("test")
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms", 10)
# the index of the selected point
selection = -1

render_info = True


def bezier_curve(p0, p1, p2, amount):
    t = np.linspace(0, 1, amount)

    points_x = (1 - t) * ((1 - t) * p0[0] + t * p1[0]) + t * ((1 - t) * p1[0] + t * p2[0])
    points_y = (1 - t) * ((1 - t) * p0[1] + t * p1[1]) + t * ((1 - t) * p1[1] + t * p2[1])
    return np.stack((points_x, points_y), axis=1)


def calc_b_spline():
    global curve_p, b_spline
    curve_p = [points[0]]
    for i in range(1, len(points) - 2):
        half_p = (points[i] + points[i + 1]) / 2
        curve_p.append(points[i])
        curve_p.append(half_p)
    curve_p.append(points[-2])
    curve_p.append(points[-1])

    index = 0
    while index < len(curve_p) - 2:
        c = bezier_curve(curve_p[index], curve_p[index + 1], curve_p[index + 2], 100)
        if index == 0:
            b_spline = c
        else:
            b_spline = np.concatenate((b_spline, c), axis=0)
        index += 2


def random_point():
    point = np.random.rand(2)
    point[0] = point[0] * (window_size[0] - 2 * margin) + margin
    point[1] = point[1] * (window_size[1] - 2 * margin) + margin
    return point


def reset():
    global curve, points
    points = [random_point() for _ in range(3)]
    curve = bezier_curve(points[0], points[1], points[2], 100)


def move_selected():
    global points
    if selection >= 0:
        points[selection] = np.array(pg.mouse.get_pos())


def update():
    global curve
    move_selected()
    calc_b_spline()


def draw():
    if render_info:
        pg.draw.lines(screen, (100, 100, 100), False, curve_p, 1)
    pg.draw.lines(screen, (255, 255, 255), False, b_spline, 1)

    if render_info:
        for p in points:
            pg.draw.circle(screen, (230, 80, 20), p.astype(int), 5)

        for p in curve_p:
            pg.draw.circle(screen, (20, 230, 20), p.astype(int), 3)

    text = font.render("%0.2f" % clock.get_fps(), True, (255, 255, 255))
    screen.blit(text, (10, 10))


def toggle_info():
    global render_info
    render_info = not render_info


keydown_func = {
    pg.K_r: reset,
    pg.K_i: toggle_info,
}


def create_point():
    points.append(np.array(pg.mouse.get_pos()))


def select():
    global selection
    mouse_pos = pg.mouse.get_pos()
    selected = False
    for i in range(len(points)):
        d_x = mouse_pos[0] - points[i][0]
        d_y = mouse_pos[1] - points[i][1]
        dist = np.sqrt(d_x ** 2 + d_y ** 2)
        if dist < 50:
            selection = i
            selected = True
            break
    if not selected:
        create_point()


mouse_pressed = False


reset()
loop = True
while loop:
    clock.tick(30)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False
        elif e.type == pg.KEYDOWN:
            try:
                keydown_func[e.key]()
            except:
                pass
        elif e.type == pg.MOUSEBUTTONDOWN:
            select()
            mouse_pressed = True
        elif e.type == pg.MOUSEBUTTONUP:
            mouse_pressed = True
            selection = -1

    update()
    screen.fill(background_color)
    draw()
    pg.display.flip()
pg.quit()
