from Code4Fun.Utility.Vec2 import *
import numpy as np
import pygame as pg
import numba as nb
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10, 50)


background_color = 50, 50, 50
particle_color = 240, 100, 30
window_size = 800, 700
particles_x = 10
particles_y = 10
particle_amount = particles_x * particles_y
min_size = 5
max_size = 20
margin = 50
grav = 1e3
oob_force = 1e5
col_force = 1e5
damping = 1


pg.init()
origin = Vec2(np.array(window_size)) / 2
screen = pg.display.set_mode(window_size)
pg.display.set_caption("test")
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms", 10)


def reset():
    global particles, particle_sizes, velocities, forces
    # particles = np.random.rand(particle_amount, 2)
    # particles[:, 0] = particles[:, 0] * (window_size[0] - 2 * margin) + margin
    # particles[:, 1] = particles[:, 1] * (window_size[1] - 2 * margin) + margin

    particles = []
    for i in np.linspace(margin, window_size[0] - margin, particles_x):
        for j in np.linspace(margin, window_size[1] - margin, particles_y):
            particles.append([i, j])
    particles = np.array(particles)


    particle_sizes = np.random.rand(particle_amount) * (max_size - min_size) + min_size
    velocities = (np.random.rand(particle_amount, 2) - 0.5) * 50
    forces = np.zeros((particle_amount, 2))


def apply_gravity():
    forces[:, 1] += grav


def apply_oob():
    # resolve floor collision:
    floor_points = particles[:, 1] > window_size[1]
    forces[floor_points, 1] -= oob_force

    # resolve left collision:
    right_points = particles[:, 0] < 0
    forces[right_points, 0] += oob_force

    # resolve right collision:
    left_points = particles[:, 0] > window_size[0]
    forces[left_points, 0] -= oob_force


@nb.guvectorize([(nb.float64[:, :], nb.float64[:], nb.float64[:, :], nb.float64)], '(a,b),(a),(a,b),()', target='parallel', cache=True)
def apply_collision(p, p_s, f, f_mag):
    for i in range(p.shape[0]):
        for j in range(i + 1, p.shape[0]):
            # from pi to pj
            d_x = p[j, 0] - p[i, 0]
            d_y = p[j, 1] - p[i, 1]

            dist = np.sqrt(d_x ** 2 + d_y ** 2)
            # positive if penetrating
            pen = (p_s[i] / 2 + p_s[j] / 2) - dist
            if pen > 0:
                s = f_mag * pen / dist
                f_x = d_x * s
                f_y = d_y * s

                f[j, 0] += f_x
                f[j, 1] += f_y
                f[i, 0] -= f_x
                f[i, 1] -= f_y

def update(dt):
    global velocities, particles, forces
    apply_gravity()
    apply_oob()
    apply_collision(particles, particle_sizes, forces, col_force)

    velocities += (forces - velocities * damping) * dt
    particles += velocities * dt
    forces = np.zeros((particle_amount, 2))


def draw():
    for i in range(particles.shape[0]):
        pg.draw.circle(screen, particle_color, (int(particles[i, 0]), int(particles[i, 1])), int(particle_sizes[i]))

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

    update(clock.get_time() / 1000)
    screen.fill(background_color)
    draw()
    pg.display.flip()
pg.quit()
