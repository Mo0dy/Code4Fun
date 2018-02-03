import pygame as pg
import time
from Code4Fun.Projects.WalkingSim.WalkingClasses import *
import random
import numpy as np

from Code4Fun.Utility.Vec2 import *


size = [1200, 600]
BACKGROUND_COLOR = (206, 195, 163)
NODE_COLOR = (206, 59, 22)
LINE_COLOR = (58, 46, 43)

GROUND_HEIGHT = 500
GROUND_THICKNESS = 10
GROUND_TENTION = 1e5

DAMPING_COEFF = 1e7

g = Vec2(0, 9.81 * 50)

pg.init()
screen = pg.display.set_mode(size)


def random_node():
    return Node((np.random.random_integers(300, 800), np.random.random_integers(50, 400)))


# nodes = [Node((random.random() * size[0], random.random() * size[0] / 2 - GROUND_HEIGHT)) for i in range(10)]
nodes = []
def initialize():
    global nodesma
    nodes = [random_node(), random_node(), random_node()]
    apply_connection(nodes[0], nodes[1], abs(nodes[0].pos - nodes[1].pos))
    apply_connection(nodes[0], nodes[2], abs(nodes[0].pos - nodes[2].pos))
    apply_connection(nodes[1], nodes[2], abs(nodes[1].pos - nodes[2].pos))

    # nodes = [Node((500, 200))]
    # for i in range(2 * 6):
    #     nodes.append(Node((500 + np.cos(i * 0.5) * 100, 200 + np.sin(i * 0.5) * 100)))
    # apply_connection(nodes[0], nodes[1], abs(nodes[0].pos - nodes[1].pos))
    # for i in range(len(nodes) - 2):
    #     j = i + 2
    #     apply_connection(nodes[0], nodes[j], abs(nodes[0].pos - nodes[j].pos))
    #     apply_connection(nodes[j - 1], nodes[j], abs(nodes[j - 1].pos - nodes[j].pos))
    #     apply_connection(nodes[1], nodes[-1], abs(nodes[1].pos - nodes[-1].pos))



def add_gravity():
    for n in nodes:
        n.add_force(g * n.mass)


def floor_collition():
    for n in nodes:
        pen_depth = n.pos.y - GROUND_HEIGHT
        if pen_depth > 0:
            n.add_force(Vec2(0, -pen_depth * GROUND_TENTION - n.vel.y * DAMPENING_COEFF))  # - n.vel * DAMPING_COEFF)


def draw():
    screen.fill(BACKGROUND_COLOR)

    # draw ground
    pg.draw.line(screen, LINE_COLOR, (0, GROUND_HEIGHT + GROUND_THICKNESS), (size[0], GROUND_HEIGHT + GROUND_THICKNESS), GROUND_THICKNESS)
    for n in nodes:
        n.draw(screen)

    pg.display.flip()


initialize()
last_time = time.time()
loop = True
while loop:
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time

    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False
        if e.type == pg.KEYDOWN:
            initialize()

    add_gravity()
    floor_collition()
    for n in nodes:
        n.push_forces()
    for n in nodes:
        n.update(dt)

    draw()



