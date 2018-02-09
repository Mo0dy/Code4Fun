import pygame as pg
import numpy as np
import numba as nb
import pygame.gfxdraw
import os
import Code4Fun.Utility.Renderer as rnd
import time


os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (500, 300)


# goal_surface:
goal_size = [800, 800]
goal_surf = pg.Surface(goal_size)
surfpos = np.array([0, 0], dtype=np.int32)


# settings
# simulation
# this has to be integers
particle_density = 3
# the particle amount is displayed on the right. if this runs out the program crashes (increase the amount)
particle_amount = 47000 * particle_density
par_mouse_attract_init = 0.1
# attraction to goals
particle_attraction_init = 2
# the force with which the particles drift away if not needet
particle_disburtion_init = -0.01
drag_coeff_init = 0.04
# this moves the particles randomly
random_factor_init = 0.4
window_size = goal_size
# the bounds the particles reflect of
x_bounds_init = [-500, window_size[0] + 500]
y_bounds_init = [-100, window_size[1] + 100]

# display
pg.init()
screen = pg.display.set_mode(window_size)  # , pg.NOFRAME)
pg.display.set_caption("Particle Clock")
background_color = np.array([20, 20, 20], dtype=np.uint8)
particle_color = np.array([142, 136, 8], dtype=np.uint8)
# for rendering fps
small_font = pg.font.SysFont("comicsansms", 10)
# for writing stuff to the display
display_font = pg.font.SysFont("caolibri", 250)
pg.mouse.set_visible(False)


# variables
particle_attraction_mouse = par_mouse_attract_init
particle_attraction = particle_attraction_init
particle_disburtion = particle_disburtion_init
drag_coeff = drag_coeff_init
random_factor = random_factor_init
x_bounds = x_bounds_init
y_bounds = y_bounds_init
particles = np.zeros((particle_amount, 2), dtype=np.float32)
velocities = np.zeros((particle_amount, 2), dtype=np.float32)
forces = np.zeros((particle_amount, 2), dtype=np.float32)
init_goals = np.column_stack((np.linspace(50, 750, particle_amount, dtype=np.float32), np.random.rand(particle_amount) * 20)).astype(np.float32)
goals = init_goals
goal_forces = np.ones(particle_amount)
clock = pg.time.Clock()

goal_arr = np.zeros(goal_size, dtype=np.int32)
update_animation = True


def init():
    global particles, velocities, forces
    particles = np.zeros((particle_amount, 2), dtype=np.float32)
    particles = particles.astype(np.float32)
    velocities = np.zeros((particle_amount, 2), dtype=np.float32)
    forces = np.zeros((particle_amount, 2), dtype=np.float32)
    animation()


def update_goals():
    global goals, goal_forces
    # goal_forces = np.zeros(particle_amount, dtype=np.float32)
    goal_forces = np.ones(particle_amount, dtype=np.float32) * particle_disburtion
    goal_arr[:] = pg.surfarray.pixels2d(goal_surf)
    fast_update_goals(goals, goal_arr, surfpos, goal_forces, particle_attraction, particle_density)


@nb.guvectorize([(nb.float32[:, :], nb.int32[:, :], nb.int32[:], nb.float32[:], nb.float32, nb.int32)], '(a,b),(c,d),(e),(a),(),()', target='parallel')
def fast_update_goals(g, input_array, offset, g_f, attrac_f, pd):
    index = 0
    for i in range(input_array.shape[0]):
        for j in range(input_array.shape[1]):
            if input_array[i, j]:
                for ii in range(pd):
                    g_f[index] = attrac_f
                    g[index, 0] = i + offset[0]
                    g[index, 1] = j + offset[1]
                    index += 1


@nb.guvectorize([(nb.float32[:, :], nb.float32[:, :], nb.float32[:, :], nb.float32[:, :], nb.float32[:], nb.float32, nb.float32[:], nb.float32, nb.float32, nb.float32, nb.int32[:], nb.int32[:])], '(a,b),(a,b),(a,b),(a,b),(a),(),(c),(),(),(),(d),(d)', target='parallel')
def update(p, vel, f, goal_pos, goal_attract, drag, m_p, m_attrack, ran_fac, delta_time, x_b, y_b):
    border_force = 0.1
    if m_attrack == 0:
        grav = 0
    else:
        grav = 0.05
    for i in range(p.shape[0]):
        d_x = goal_pos[i, 0] - p[i, 0]
        d_y = goal_pos[i, 1] - p[i, 1]
        dist = np.sqrt(d_x ** 2 + d_y ** 2)
        m_d_x = m_p[0] - p[i, 0]
        m_d_y = m_p[1] - p[i, 1]
        m_dist = np.sqrt(m_d_x ** 2 + m_d_y ** 2)
        vel_mul = np.sqrt(vel[i, 0] ** 2 + vel[i, 1] ** 2)
        f[i, 0] = d_x * goal_attract[i] / dist - vel[i, 0] * drag * vel_mul + (np.random.rand() - 0.5) * ran_fac + m_d_x * m_attrack / m_dist
        f[i, 1] = d_y * goal_attract[i] / dist - vel[i, 1] * drag * vel_mul + (np.random.rand() - 0.5) * ran_fac + m_d_y * m_attrack / m_dist + grav

        # right
        if x_b[1] < p[i, 0]:
            f[i, 0] += (x_b[1] - p[i, 0]) * border_force

        # left
        elif p[i, 0] < x_b[0]:
            f[i, 0] += (x_b[0] - p[i, 0]) * border_force

        # down
        if y_b[1] < p[i, 1]:
            f[i, 1] += (y_b[1] - p[i, 1]) * border_force

        # up
        elif p[i, 1] < y_b[0]:
            f[i, 1] += (y_b[0] - p[i, 1]) * border_force

        vel[i, 0] += f[i, 0] * delta_time
        vel[i, 1] += f[i, 1] * delta_time
        p[i, 0] += vel[i, 0] * delta_time
        p[i, 1] += vel[i, 1] * delta_time


def draw():
    screen.fill(background_color)
    rnd.render_points(particles, particle_color, pg.surfarray.pixels3d(screen))
    text = small_font.render("%.3f" % (clock.get_fps()), True, (100, 80, 80))
    screen.blit(text, (10, 5))
    if 1 < pg.mouse.get_pos()[0] < window_size[0] - 1 and 1 < pg.mouse.get_pos()[1] < window_size[1] - 1:
        pg.gfxdraw.aacircle(screen, pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], 5, (94, 34, 14))
        pg.gfxdraw.aacircle(screen, pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], 4, (94, 34, 14))
    pg.display.flip()


def toggle_attraction():
    global particle_attraction_mouse
    particle_attraction_mouse *= -1


def forier(sin_fac, cos_fac):
    result = 0
    for i in range(len(sin_fac)):
        result += sin_fac[i] * np.sin(time.time() * 1 / (i + 1))
    for i in range(len(cos_fac)):
        result += cos_fac[i] * np.cos(time.time() * 1 / (i + 1))
    return np.clip(int(result), 0, 300)


# modify this function
def animation():
    global update_animation
    if update_animation:
        # update_animation = False
        goal_surf.fill(0)

        # drawing code here
        pg.draw.circle(goal_surf, 1, (int(np.sin(time.time()) * 200 + window_size[0] / 2), int(np.cos(time.time()) * 200 + window_size[0] / 2)), forier([10, -5, 5, 3], [10. -5]) + 50)
        update_goals()


init()
# Main Loop:
loop = True
while loop:
    clock.tick(60)

    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False
        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                loop = False
            elif e.key == pg.K_SPACE:
                par_mouse_attract_init *= -1
        elif e.type == pg.MOUSEBUTTONDOWN:
            par_mouse_attract_init *= -1

    animation()
    mouse_pos = np.array(pg.mouse.get_pos(), dtype=np.float32)
    if 1 < mouse_pos[0] < window_size[0] - 1 and 1 < mouse_pos[1] < window_size[1] - 1:
        particle_attraction_mouse = par_mouse_attract_init
        particle_attraction = 0
        drag_coeff = 0.0005
        random_factor = 0
        x_bounds = [0, window_size[0]]
        y_bounds = [-1000, window_size[1]]
    else:
        drag_coeff = drag_coeff_init
        particle_attraction = particle_attraction_init
        random_factor = random_factor_init
        particle_attraction_mouse = 0
        x_bounds = x_bounds_init
        y_bounds = y_bounds_init

    update(particles, velocities, forces, goals, goal_forces, drag_coeff, mouse_pos, particle_attraction_mouse, random_factor, 1.2, x_bounds, y_bounds)
    draw()

