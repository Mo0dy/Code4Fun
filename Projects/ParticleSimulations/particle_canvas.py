import pygame as pg
import numpy as np
import numba as nb
import pygame.gfxdraw
import datetime
import os


os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (500, 300)


# goal_surface:
goal_size = [800, 250]
goal_surf = pg.Surface(goal_size)
surfpos = np.array([0, 0], dtype=np.int32)


# settings
# simulation
particle_amount = 120000
par_mouse_attract_init = 0.1
particle_attraction_init = 2
particle_disburtion_init = -0.01
drag_coeff_init = 0.04
# drag_coeff = 0.05
random_factor_init = 0.4
lineheight = 20


# display
pg.init()
window_size = 800, 250
x_bounds_init = [-500, window_size[0] + 500]
y_bounds_init = [-100, window_size[1] + 100]
screen = pg.display.set_mode(window_size, pg.NOFRAME)
pg.display.set_caption("Particle Clock")
# background_color = 206, 195, 163
# particle_color = np.array([206, 59, 22], dtype=int)
background_color = 20, 20, 20
particle_color = np.array([142, 136, 8], dtype=int)
small_font = pg.font.SysFont("comicsansms", 10)
display_font = pg.font.SysFont("caolibri", 250)
pg.mouse.set_visible(False)


image = pg.image.load("Potato-Transparent-PNG.png")


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
init_goals = np.column_stack((np.linspace(50, 750, particle_amount, dtype=np.float32), np.random.rand(particle_amount) * 20 + lineheight)).astype(np.float32)
goals = init_goals
color_factors = np.ones(particle_amount)
goal_forces = np.ones(particle_amount)
clock = pg.time.Clock()


render_arr = np.zeros((window_size[0], window_size[1], 3), dtype=np.int32)

last_second = -1
goal_arr = np.zeros(goal_size, dtype=np.int32)


def update_goals():
    global goals, goal_forces
    # goal_forces = np.zeros(particle_amount, dtype=np.float32)
    goal_forces = np.ones(particle_amount, dtype=np.float32) * particle_disburtion
    goal_arr[:] = pg.surfarray.pixels2d(goal_surf)
    fast_update_goals(goals, goal_arr, surfpos, goal_forces, particle_attraction)


@nb.guvectorize([(nb.float32[:, :], nb.int32[:, :], nb.int32[:], nb.float32[:], nb.float32)], '(a,b),(c,d),(e),(a),()', target='parallel')
def fast_update_goals(g, input_array, offset, g_f, attrac_f):
    index = 0
    for i in range(input_array.shape[0]):
        for j in range(input_array.shape[1]):
            if input_array[i, j]:
                g_f[index] = attrac_f
                g_f[index + 1] = attrac_f
                g_f[index + 2] = attrac_f
                g[index] = [i + offset[0], j + offset[1]]
                g[index + 1] = [i + offset[0], j + offset[1]]
                g[index + 2] = [i + offset[0], j + offset[1]]
                index += 3


def init():
    global particles, velocities, forces
    particles = np.zeros((particle_amount, 2), dtype=np.float32)
    particles = particles.astype(np.float32)
    velocities = np.zeros((particle_amount, 2), dtype=np.float32)
    forces = np.zeros((particle_amount, 2), dtype=np.float32)
    # animation()
    goal_surf.blit(image, (50, 50))
    update_goals()


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


@nb.guvectorize([(nb.int32[:, :, :], nb.float32[:, :], nb.float32[:], nb.int32[:])], '(a,b,c),(d,e),(d),(c)', target='parallel')
def render(input_arr, p, g_f, p_c):
    for i in range(p.shape[0]):
        if 0 < p[i, 0] < input_arr.shape[0] and 0 < p[i, 1] < input_arr.shape[1]:
            i1 = nb.int32(p[i, 0])
            i2 = nb.int32(p[i, 1])
            input_arr[i1, i2, 0] = p_c[0]
            input_arr[i1, i2, 1] = p_c[1]
            input_arr[i1, i2, 2] = p_c[2]


def draw(dt):
    global render_arr

    render_arr[:, :] = background_color
    render(render_arr, particles, goal_forces, particle_color)
    pg.surfarray.pixels3d(screen)[:] = render_arr
    text = small_font.render("%.3f" % (1 / dt), True, (100, 80, 80))
    screen.blit(text, (10, 5))
    if 1 < pg.mouse.get_pos()[0] < window_size[0] - 1 and 1 < pg.mouse.get_pos()[1] < window_size[1] - 1:
        pg.gfxdraw.aacircle(screen, pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], 5, (94, 34, 14))
        pg.gfxdraw.aacircle(screen, pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], 4, (94, 34, 14))
    pg.display.flip()


def toggle_attraction():
    global particle_attraction_mouse
    particle_attraction_mouse *= -1


def animation():
    global last_second
    time = datetime.datetime.now()
    if time.second != last_second:
        last_second = time.second
        goal_surf.fill(0)
        text = display_font.render("%02d:%02d:%02d" % (time.hour, time.minute, time.second), True, (255, 255, 255))
        goal_surf.blit(text, (45, 50))
        update_goals()


init()
# Main Loop:
loop = True
while loop:
    clock.tick(60)
    dt = clock.get_time() / 1000

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

    update(particles, velocities, forces, goals, goal_forces, drag_coeff, mouse_pos, particle_attraction_mouse, random_factor, 1.2, x_bounds, y_bounds) # dt * 35)
    draw(dt)

