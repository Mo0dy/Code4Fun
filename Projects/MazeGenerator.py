import numpy as np
import pygame as pg

# settings
size = 800, 800
maze_size = 80, 80
square_size = size[0] / maze_size[0] - 2, size[1] / maze_size[1] - 2
# the frequency the algorithm calculates at
refreshrate = 60

# creating a maze by performing a depth first algorithm until every single field has been reached
#init drawing library
pg.init()
# create window
screen = pg.display.set_mode(size)
pg.display.set_caption("MazeGenerator")
# to limit loop refreshrate
clock = pg.time.Clock()


# the init function resets the program
def init():
    screen.fill((50, 50, 50))
    pg.display.flip()


# the drawing function
def connect_squares(s1, s2):
    pg.draw.rect()

# the actual calculation
def calculate():
    pass


# this loop is the main loop. every single iteration a new action will be performed and then displayed
loop = True
init()
while loop:
    clock.tick(refreshrate)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False

    calculate()

pg.quit()
