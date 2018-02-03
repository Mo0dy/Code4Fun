from Code4Fun.Utility.Vec2 import Vec2
import pygame as pg
import numpy as np
from random import random

# Period
T = 100000
size = Vec2(800, 800)
origin = size / 2

circleAmount = 10

pg.init()
screen = pg.display.set_mode(size.tuple_int)
pg.display.set_caption("Fractal Spirograph")


def createFractal():
    global line
    lengths = np.array([300 / (i + 1) ** 3 for i in range(circleAmount)])
    amount = int(random() * 9) + 2
    thetadots = np.array([-np.pi * 2 * amount ** (i + 1) / T if i % 2 else np.pi * 2 * amount ** (i + 1) / T for i in range(circleAmount)])
    angles = np.outer(np.arange(0, T), thetadots)
    angles -= np.pi / 2
    line = np.column_stack(((np.cos(angles)[:] @ lengths) + origin.x, (np.sin(angles)[:] @ lengths) + origin.y))

    screen.fill((45, 34, 27))
    pg.draw.lines(screen, (237, 42, 42), False, line.astype(int))
    pg.display.flip()

createFractal()
loop = True
while loop:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False
        elif e.type == pg.KEYDOWN:
            createFractal()

pg.quit()



