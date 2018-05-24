import pygame as pg
import numpy as np
import random
from Code4Fun.Projects.MatrixAnimations.MatrixLib import *

pg.init()
screen = pg.display.set_mode((800, 800))
matrix = Matrix(10, 10)

matrix[5][3] = [255, 0, 0]

clock = pg.time.Clock()

# normalized vector in direction of gravity (x, y, z)
grav_vec = np.array([0, 0, 1])


def draw():
    dt = clock.get_time()



loop = True
while loop:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False

    clock.tick(60)
    draw()
    pg.display.flip()
