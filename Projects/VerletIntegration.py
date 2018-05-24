import numpy as np
import pygame as pg
from Code4Fun.Utility.Vec2 import *
import numba as nb


x_margin = 500
y_margin = 100
damping = 0.999
floor_damping = 0.3
gravity = 400
floor_height = 550
con_amount = 400
point_size = 5

force_point = 8

cloth_rows = 16
cloth_columns = 16
points_amount = cloth_rows * cloth_columns

line_color = (100, 100, 100)
node_color = (0, 204, 6)
background_color = (50, 50, 50)

size = 1200, 600
pg.init()
screen = pg.display.set_mode(size)
pg.display.set_caption("testing Verlet integration")
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms", 10)


def cloth_init():
    global points, old_points, constraints, con_lengths

    d_row = (size[0] - 2 * x_margin) / (cloth_rows - 1)
    d_col = (size[1] - 2 * y_margin) / (cloth_columns - 1)

    points = []
    for i in range(cloth_rows):
        for j in range(cloth_columns):
            points.append([i * d_row + x_margin, j * d_col + y_margin])

    points = np.array(points)
    print(points.shape[0])

    old_points = points

    constraints = []

    for i in range(cloth_rows):
        for j in range(cloth_columns - 1):
            constraints.append([i * cloth_columns + j, i * cloth_columns + j + 1])

    for i in range(cloth_rows - 1):
        for j in range(cloth_columns):
            constraints.append([i * cloth_columns + j, (i + 1) * cloth_columns + j])

    for i in range(cloth_rows - 1):
        constraints.append([cloth_rows + i + 1, i])

    for i in range(1, cloth_rows):
        constraints.append([cloth_rows + i - 1, i])

    constraints = np.array(constraints, dtype=np.uint8)

    con_lengths = np.zeros(constraints.shape[0])
    for i in range(constraints.shape[0]):
        p1 = points[constraints[i, 0]]
        p2 = points[constraints[i, 1]]
        delta = p1 - p2
        dist = np.sqrt(np.sum(delta @ delta))
        con_lengths[i] = dist


def init():
    cloth_init()


@nb.guvectorize([(nb.uint8[:, :], nb.float64[:], nb.float64[:, :])], '(a,b),(a),(c,b)', target='parallel', cache=True)
def resolve_constraints(con, con_l, p):
    for i in nb.prange(con.shape[0]):
        delta_x = p[con[i, 0], 0] - p[con[i, 1], 0]
        delta_y = p[con[i, 0], 1] - p[con[i, 1], 1]

        dist = np.sqrt(delta_x ** 2 + delta_y ** 2)
        if dist > 0:
            scale = (con_l[i] - dist) / dist / 2
        else:
            scale = 0
        p[con[i, 0], 0] += scale * delta_x
        p[con[i, 0], 1] += scale * delta_y
        p[con[i, 1], 0] -= scale * delta_x
        p[con[i, 1], 1] -= scale * delta_y


def update(dt):
    global points, old_points
    acceleration = np.stack((np.zeros(points_amount), np.ones(points_amount) * gravity), axis=1)

    if mouse_pressed:
        acceleration[force_point] = (pg.mouse.get_pos() - points[force_point]) * 500
    vel = points - old_points

    old_points = points.copy()
    points += vel * damping + acceleration * dt ** 2

    # resolve floor collision:
    floor_points = points[:, 1] > floor_height
    points[floor_points, 1] = floor_height
    old_points[floor_points, 1] = points[floor_points, 1] + vel[floor_points, 1] * 0.9
    points[floor_points, 0] -= vel[floor_points, 0] * floor_damping

    # resolve walls
    oob_right = points[:, 0] > size[0]
    points[oob_right, 0] = size[0]
    old_points[oob_right, 0] = points[oob_right, 0] + vel[oob_right, 0]

    oob_left = points[:, 0] < 0
    points[oob_left, 0] = 0
    old_points[oob_left, 0] = points[oob_left, 0] + vel[oob_left, 0]

    # resolving constraints
    for _ in range(10):
        resolve_constraints(constraints, con_lengths, points)


def draw():
    screen.fill(background_color)

    if mouse_pressed:
        pg.draw.line(screen, (107, 109, 50), (int(points[force_point, 0]), int(points[force_point, 1])), pg.mouse.get_pos(), 3)

    for c in constraints:
        p1 = points[c[0]]
        p2 = points[c[1]]
        pg.draw.line(screen, line_color, (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1])), 3)

    for p in points:
        pg.draw.circle(screen, node_color, (int(p[0]), int(p[1])), point_size)

    pg.draw.line(screen, line_color, (0, floor_height + 10), (size[0], floor_height + 10), 10)

    fps = font.render("%0.2f" % clock.get_fps(), True, (200, 100, 100))
    screen.blit(fps, (10, 10))
    pg.display.flip()


def my_quit():
    global loop
    loop = False


keydown_func = {
    pg.K_ESCAPE: my_quit,
    pg.K_r: init,
}


mouse_pressed = False
init()
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
            mouse_pressed = True
        elif e.type == pg.MOUSEBUTTONUP:
            mouse_pressed = False

    update(clock.get_time() / 1000)
    draw()

pg.quit()
