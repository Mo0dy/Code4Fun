import pygame as pg
import numpy as np
import numba as nb
import pygame.gfxdraw
import datetime
import os
from Code4Fun.Utility.Renderer import render_points


os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 100)


# settings
# simulation
particle_amount = 400000
par_mouse_attract_init = 0.1
drag_coeff_init = 0.0005
# drag_coeff = 0.05
random_factor_init = 0.01 # 0.025


# display
pg.init()
window_size = 800, 800
x_bounds_init = [0, window_size[0]]
y_bounds_init = [-1000, window_size[1]]
screen = pg.display.set_mode(window_size)  # , pg.NOFRAME)
pg.display.set_caption("Particle Storm")
# background_color = 206, 195, 163
# particle_color = np.array([206, 59, 22], dtype=int)
background_color = 20, 20, 20
particle_color = np.array([142, 136, 8], dtype=np.uint8)
small_font = pg.font.SysFont("comicsansms", 10)
pg.mouse.set_visible(False)
border_force_init = 0.1
gravity_init = 0.05

# variables
particle_attraction_mouse = par_mouse_attract_init
drag_coeff = drag_coeff_init
random_factor = random_factor_init
x_bounds = x_bounds_init
y_bounds = y_bounds_init
particles = np.zeros((particle_amount, 2), dtype=np.float32)
velocities = np.zeros((particle_amount, 2), dtype=np.float32)
forces = np.zeros((particle_amount, 2), dtype=np.float32)
clock = pg.time.Clock()

border_force = border_force_init
gravity = gravity_init * 0


render_arr = np.zeros((window_size[0], window_size[1], 3), dtype=np.int32)

last_second = -1




def init():
    global particles, velocities, forces
    particles = np.random.rand(particle_amount, 2)
    particles[:, 0] *= window_size[0]
    particles[:, 1] *= window_size[1]
    particles = particles.astype(np.float32)
    velocities = np.zeros((particle_amount, 2), dtype=np.float32)


@nb.guvectorize([(nb.float32[:, :], nb.float32[:, :], nb.float32[:, :], nb.float32, nb.float32[:], nb.float32, nb.float32, nb.float32, nb.int32[:], nb.int32[:], nb.float32, nb.float32)], '(a,b),(a,b),(a,b),(),(c),(),(),(),(d),(d),(),()', target='parallel')
def update(p, vel, f, drag, m_p, m_attrack, ran_fac, delta_time, x_b, y_b, grav, b_force):
    for i in range(p.shape[0]):
        m_d_x = m_p[0] - p[i, 0]
        m_d_y = m_p[1] - p[i, 1]
        m_dist = np.sqrt(m_d_x ** 2 + m_d_y ** 2)
        vel_mul = np.sqrt(vel[i, 0] ** 2 + vel[i, 1] ** 2)
        f[i, 0] = - vel[i, 0] * drag * vel_mul + (np.random.rand() - 0.5) * ran_fac + m_d_x * m_attrack / m_dist
        f[i, 1] = - vel[i, 1] * drag * vel_mul + (np.random.rand() - 0.5) * ran_fac + m_d_y * m_attrack / m_dist + grav

        # right
        if x_b[1] < p[i, 0]:
            f[i, 0] += (x_b[1] - p[i, 0]) * b_force

        # left
        elif p[i, 0] < x_b[0]:
            f[i, 0] += (x_b[0] - p[i, 0]) * b_force

        # down
        if y_b[1] < p[i, 1]:
            f[i, 1] += (y_b[1] - p[i, 1]) * b_force

        # up
        elif p[i, 1] < y_b[0]:
            f[i, 1] += (y_b[0] - p[i, 1]) * b_force

        vel[i, 0] += f[i, 0] * delta_time
        vel[i, 1] += f[i, 1] * delta_time
        p[i, 0] += vel[i, 0] * delta_time
        p[i, 1] += vel[i, 1] * delta_time


def draw(dt):
    global render_arr

    screen.fill(background_color)
    render_points(particles, particle_color, pg.surfarray.pixels3d(screen))
    text = small_font.render("%.3f" % (1 / dt), True, (100, 80, 80))
    screen.blit(text, (10, 5))
    if 1 < pg.mouse.get_pos()[0] < window_size[0] - 1 and 1 < pg.mouse.get_pos()[1] < window_size[1] - 1:
        pg.gfxdraw.aacircle(screen, pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], 5, (94, 34, 14))
        pg.gfxdraw.aacircle(screen, pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], 4, (94, 34, 14))
    pg.display.flip()


def toggle_attraction():
    global particle_attraction_mouse
    particle_attraction_mouse *= -1


init()
# Main Loop:
loop = True
while loop:
    clock.tick()
    dt = clock.get_time() / 1000

    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False
        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                loop = False
            elif e.key == pg.K_SPACE:
                par_mouse_attract_init *= -1
            elif e.key == pg.K_g:
                if gravity:
                    gravity = 0
                else:
                    gravity = gravity_init
            elif e.key == pg.K_r:
                init()
        elif e.type == pg.MOUSEBUTTONDOWN:
            if particle_attraction_mouse:
                particle_attraction_mouse = 0
            else:
                particle_attraction_mouse = par_mouse_attract_init

    mouse_pos = np.array(pg.mouse.get_pos(), dtype=np.float32)

    update(particles, velocities, forces, drag_coeff, mouse_pos, particle_attraction_mouse, random_factor, 1.2, x_bounds, y_bounds, gravity, border_force) # dt * 35)
    draw(dt)

