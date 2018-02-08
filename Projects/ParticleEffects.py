from Code4Fun.Utility.Vec2 import *
import numpy as np
import pygame as pg
from Code4Fun.Utility.Renderer import *
from Code4Fun.Utility.Utility import flame_color_vec


# settings
background_color = 50, 50, 50
window_size = 800, 800
particle_amount = 4000
max_lifetime_s = 10
min_lifetime_s = 5


# variables
origin = Vec2(np.array(window_size)) / 2
particles = np.zeros((particle_amount, 2))
velocities = (np.random.rand(particle_amount, 2) - 0.5) * 100

# set particle positions to the middle
particles[:, 0] = origin.x
particles[:, 1] = origin.y

# saves the time the particles are supposed to be alive
cooling_factor = np.random.rand(particle_amount) * (1 / ((max_lifetime_s - min_lifetime_s) + min_lifetime_s) * 255)
temps = np.ones(particle_amount) * 255


# pygame init
pg.init()
screen = pg.display.set_mode(window_size)
pg.display.set_caption("test")
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms", 20)


def apply_gravit(dt):
    global velocities
    velocities[:, 1] += 9.81 * dt


def update_particles(p, v, t, cool_f, dt):
    p += v * dt
    t -= cool_f * dt
    x_oob = np.logical_or(particles[:, 0] < 0, particles[:, 0] > window_size[0])
    y_oob = np.logical_or(particles[:, 1] < 0, particles[:, 1] > window_size[0])
    cooled = t < 0
    reset_p = np.logical_or(np.logical_or(x_oob, y_oob), cooled)
    particles[reset_p, :] = np.array([origin.x, origin.y])
    velocities[reset_p] = (np.random.rand(particle_amount, 2) - 0.5)[reset_p]
    velocities[reset_p, 0] *= 20
    velocities[reset_p, 1] *= 30
    velocities[reset_p, 1] -= 80
    # the cooling factor stays the same
    t[reset_p] = 255


def reset():
    pass


def update():
    dt = clock.get_time() / 500
    apply_gravit(dt)
    update_particles(particles, velocities, temps, cooling_factor, dt)


def draw():
    colors = flame_color_vec(temps)
    render_points_multicolor(particles, colors, pg.surfarray.pixels3d(screen))

    text = font.render("%0.2f" % clock.get_fps(), True, (255, 255, 255))
    screen.blit(text, (10, 10))


keydown_func = {
    pg.K_r: reset
}


reset()
loop = True
while loop:
    clock.tick()
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



