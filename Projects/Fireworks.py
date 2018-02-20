from Code4Fun.Utility.Vec2 import *
import numpy as np
import pygame as pg
from Code4Fun.Libraries.ParticleSim.ParticleSim import ParticleSim as pSim

background_color = 50, 50, 50
window_size = 800, 800


pg.init()
origin = Vec2(np.array(window_size)) / 2
screen = pg.display.set_mode(window_size)
pg.display.set_caption("test")
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms", 20)


def init():
    global p_sim
    p_sim = pSim(particle_amount=400,
                 gravity=True,
                 grav_const=200,
                 p_force_degree=1,
                 x_bounds=[399, 401],
                 y_bounds=[399, 401],
                 damping=False)
    p_sim.set_force_points(400, 400)

def update():
    p_sim.update(clock.get_time() / 1000)


def draw():
    text = font.render("%0.2f" % clock.get_fps(), True, (255, 255, 255))
    screen.blit(text, (10, 10))

    for p in p_sim.particles:
        pg.draw.circle(screen, (255, 255, 255), p.astype(int), 3)


keydown_func = {
    pg.K_r: init
}


init()
loop = True
while loop:
    clock.tick(60)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False
        elif e.type == pg.KEYDOWN:
            keydown_func[e.key]()

    update()
    screen.fill(background_color)
    draw()
    pg.display.flip()
pg.quit()