import numpy as np
import pygame as pg
from Code4Fun.Libraries.ParticleSim.ParticleSim import *
import Code4Fun.Utility.Renderer as rnd
from Code4Fun.Utility.Transform import *
import time


# Pygame settings
pg.init()
window_size = [800, 800]
screen = pg.display.set_mode(window_size)
pg.display.set_caption("testing particle sim")
font = pg.font.SysFont("comicsansms", 12)
big_font = pg.font.SysFont("comicsansms", 70)
clock = pg.time.Clock()
t = Transformation()


def mouse_point():
    return np.array([pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]])


# create a new particle sim
pSim = ParticleSim((0, window_size[0]), (0, window_size[1]), 2e4,
                   color=rnd.color(153, 40, 0),
                   goal_forces=True,
                   oob_force=True
                   )

pSim.ran_color_distrib()


goal_surf = pg.Surface((300, 300))
# goal_surf.blit(big_font.render("coding is fun", True, (1, 0, 0)), (10, 10))
# pg.draw.line(goal_surf, 1, (0, 100), (100, 100), 20)
# pg.draw.line(goal_surf, 1, (0, 100), (50, 0), 20)
# pg.draw.line(goal_surf, 1, (100, 100), (50, 0), 20)


triangle = np.array([[40, 260], [260, 260], [150, 40]])
for i in range(triangle.shape[0] - 1):
    pg.draw.line(goal_surf, (255, 0, 0), (int(triangle[i, 0]), int(triangle[i, 1])),
                 (int(triangle[i + 1, 0]), int(triangle[i + 1, 1])), 20)
pg.draw.line(goal_surf, (255, 0, 0), (int(triangle[0, 0]), int(triangle[0, 1])),
             (int(triangle[-1, 0]), int(triangle[-1, 1])), 20)


assign_goals(pg.surfarray.pixels2d(goal_surf), pSim.goals, pSim.pursue_goals, - 150, - 150)
orig_goals = pSim.goals.copy()

def draw():
    screen.fill((50, 50, 50))
    rnd.render_points(pSim.particles, pSim.color, pg.surfarray.pixels3d(screen))

    fps = font.render("%0.2f" % clock.get_fps(), True, (255, 255, 255))
    screen.blit(fps, (10, 10))
    pg.display.flip()

def update():
    t.reset()
    t.rotate(time.time())
    t.trans(pg.mouse.get_pos()[0],  pg.mouse.get_pos()[1])

    pSim.goals = t * orig_goals

    # assign_goals(pg.surfarray.pixels2d(goal_surf), pSim.goals, pSim.pursue_goals, pg.mouse.get_pos()[0] - 150, pg.mouse.get_pos()[1] - 150)
    pSim.force_point = mouse_point()
    pSim.update(clock.get_time() / 1000)


loop = True
def my_quit():
    global loop
    loop = False


def toggle_grav():
    global pSim
    pSim.gravity = not pSim.gravity


def toggle_fun():
    global pSim
    pSim.goal_forces = not pSim.goal_forces
    pSim.p_force = not pSim.p_force
    if pSim.p_force:
        pSim.damping_mag = 0.001
    else:
        pSim.damping_mag = 0.1
        pSim.goals = pSim.particles.copy()


keydown_func = {
    pg.K_ESCAPE: my_quit,
    pg.K_g: toggle_grav,
    pg.K_t: toggle_fun,
}


while loop:
    clock.tick()
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
