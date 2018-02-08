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


def mouse_point():
    return np.array([pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]])


# create a new particle sim
pSim = ParticleSim((0, window_size[0]), (0, window_size[1]), 4e5,
                   gravity=False,
                   random_motion=True,
                   p_force=True,
                   p_force_mag=300,
                   grav_const=5e3,
                   random_magnitude=10,
                   oob_force=True,
                   multicolor=True
                   )

pSim.ran_color_distrib()

def draw():
    screen.fill((50, 50, 50))
    rnd.render_points_multicolor(pSim.particles, pSim.colors, pg.surfarray.pixels3d(screen))

    fps = font.render("%0.2f" % clock.get_fps(), True, (255, 255, 255))
    screen.blit(fps, (10, 10))
    pg.display.flip()


def update():
    pSim.force_point = mouse_point()
    pSim.update(clock.get_time() / 1000)


loop = True
def my_quit():
    global loop
    loop = False


def toggle_grav():
    global pSim
    pSim.gravity = not pSim.gravity


keydown_func = {
    pg.K_ESCAPE: my_quit,
    pg.K_g: toggle_grav,
}


while loop:
    clock.tick(60)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False
        if e.type == pg.KEYDOWN:
            try:
                keydown_func[e.key]()
            except:
                pass

    update()
    draw()

pg.quit()
