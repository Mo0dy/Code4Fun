import numpy as np
import pygame as pg
from Code4Fun.Libraries.ParticleSim.ParticleSim import *
import Code4Fun.Utility.Renderer as rnd


# Pygame settings
pg.init()
window_size = [800, 800]
screen = pg.display.set_mode(window_size)
pg.display.set_caption("testing particle sim")
font = pg.font.SysFont("comicsansms", 12)
clock = pg.time.Clock()


# create a new particle sim
pSim = ParticleSim((0, window_size[0]), (0, window_size[1]),
                   gravity=True,
                   random_motion=True,
                   random_magnitude=100)


def draw():
    screen.fill((50, 50, 50))
    rnd.render_points(pSim.particles, rnd.color((200, 100, 100)), pg.surfarray.pixels3d(screen))

    fps = font.render("%0.2f" % clock.get_fps(), True, (255, 255, 255))
    screen.blit(fps, (10, 10))
    pg.display.flip()


def update():
    pSim.update(clock.get_time() / 1000)


loop = True
while loop:
    clock.tick()
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False

    update()
    draw()

pg.quit()
