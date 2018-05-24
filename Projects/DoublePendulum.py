import numpy as np
from copy import deepcopy
import pygame as pg

size = 800, 800

# constants
g = 9.81 * 70
# g = 0

m1 = 1
m2 = 1
l1 = 100
l2 = 100

theta1 = 1
thetadot1 = 0
theta2 = 0
thetadot2 = 0

pg.init()
screen = pg.display.set_mode(size)
pg.display.set_caption("DoublePendulum(EulerCauchy)")
clock = pg.time.Clock()


# the differential equation describing the double pendulum system
def pen_diff_eq(t1, tdot1, t2, tdot2):
    sin1 = np.sin(t1)
    sin2 = np.sin(t2)
    sin12 = np.sin(t1 - t2)
    cos12 = np.cos(t1 - t2)

    mtot = m1 + m2

    A = mtot * l1
    B = m2 * l2 * cos12
    C = -m2 * l2 * tdot2 ** 2 * sin12 - mtot * g * sin1
    D = l1 / l2 * cos12
    E = (l1 * tdot1 ** 2 * sin12 - g * sin2) / l2

    theta1dotdot = (C - B * E) / (A - B * D)
    theta2dotdot = E - D * theta1dotdot

    return [theta1dotdot, theta2dotdot]


def polar_to_cat_int(theta, length):
    return [int(np.sin(theta) * length), int(-1 * length * np.cos(theta))]


def EulerCauchy(h):
    global theta1, thetadot1, theta2, thetadot2
    thetadotdots = pen_diff_eq(theta1, thetadot1, theta2, thetadot2)

    thetadot1 += thetadotdots[0] * h
    theta1 += thetadot1 * h
    thetadot2 += thetadotdots[1] * h
    theta2 += thetadot2 * h


loop = True
while loop:
    clock.tick()
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False

    EulerCauchy(clock.get_time() / 1000)

    p1 = polar_to_cat_int(theta1, l1)
    p1[0] += 400
    p1[1] += 600

    p2 = polar_to_cat_int(theta2, l2)
    p2[0] += p1[0]
    p2[1] += p1[1]

    screen.fill((50, 50, 50))
    pg.draw.circle(screen, (255, 0, 0), p1, 20)
    pg.draw.circle(screen, (255, 0, 0), p2, 20)

    pg.draw.line(screen, (20, 20, 20), (400, 600), p1, 3)
    pg.draw.line(screen, (20, 20, 20), p2, p1, 3)

    pg.display.flip()

pg.quit()


