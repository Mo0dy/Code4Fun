import pygame as pg
import numpy as np
import Code4Fun.Libraries.ParticleSim.ParticleSim as pSim
import Code4Fun.Utility.Renderer as rnd

# settings
size = [800, 800]
particle_amount = 4e5
mouse_attraction = 1e3
drag_coeff = 1
ran_mag = 0.01
background_color = np.array([20, 20, 20], dtype=np.uint8)
particle_color = np.array([142, 136, 8], dtype=np.uint8)
border_force = 0.1


# pygame
pg.init()
screen = pg.display.set_mode(size)
pg.display.set_caption("Lib Particle Storm")
small_font = pg.font.SysFont("comicsansms", 10)
clock = pg.time.Clock()


# particle sim
p_sim = pSim.ParticleSim(
    (0, size[0]), (0, size[1]),
    particle_amount,
    color=particle_color,
    random_motion=True,
    random_magnitude=ran_mag,
    p_force=True,
    damping=False,
    oob_force=True,
    goal_forces=False,
    p_force_mag=2e3,
    damping_mag=1e4,
    oob_force_mag=1e2
)

goal_screen = pg.Surface((400, 400))
pg.draw.circle(goal_screen, (255, 255, 255), (200, 200), 100)
pSim.assign_goals(pg.surfarray.pixels2d(goal_screen), p_sim.goals, p_sim.pursue_goals, 200, 200)


def get_mouse_pos():
    return np.array([pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]])


def update():
    p_sim.force_point = get_mouse_pos()
    p_sim.update(clock.get_time() / 1000)


def draw():
    screen.fill(background_color)
    rnd.render_points(p_sim.particles, p_sim.color, pg.surfarray.pixels3d(screen))
    pg.display.flip()


def my_quit():
    global loop
    loop = False


keydown_function = {
    pg.K_ESCAPE: my_quit
}


loop = True
while loop:
    clock.tick()
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False
        elif e.type == pg.KEYDOWN:
            try:
                keydown_function[e.key]()
            except:
                pass

    update()
    draw()











