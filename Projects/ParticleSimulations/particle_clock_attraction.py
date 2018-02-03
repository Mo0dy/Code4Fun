import pygame as pg
import numpy as np
import numba as nb
import time
import pygame.gfxdraw
import datetime


# goal_surface:
goal_size = [800, 250]
goal_surf = pg.Surface(goal_size)
surfpos = np.array([0, 0], dtype=np.int32)



# settings
# simulation
particle_amount = 120000
par_mouse_attract_init = 0.3
particle_attraction_init = 0.2
drag_coeff_init = 0.1
# drag_coeff = 0.05
random_factor_init = 0.7
lineheight = 20


# display
pg.init()
window_size = 800, 250
screen = pg.display.set_mode(window_size, pg.NOFRAME)
pg.display.set_caption("Particle Storm")
# background_color = 206, 195, 163
# particle_color = np.array([206, 59, 22], dtype=int)
background_color = 20, 20, 20
particle_color = np.array([142, 136, 8], dtype=int)
small_font = pg.font.SysFont("comicsansms", 10)
display_font = pg.font.SysFont("caolibri", 250)
pg.mouse.set_visible(False)


# print(pg.font.get_fonts())


# variables
particle_attraction_mouse = par_mouse_attract_init
particle_attraction = particle_attraction_init
drag_coeff = drag_coeff_init
random_factor = random_factor_init
particles = np.zeros((particle_amount, 2), dtype=np.float32)
velocities = np.zeros((particle_amount, 2), dtype=np.float32)
forces = np.zeros((particle_amount, 2), dtype=np.float32)
goals = np.zeros(particles.shape, dtype=np.float32)

clock = pg.time.Clock()

render_arr = np.zeros((window_size[0], window_size[1], 3), dtype=np.int32)

last_second = -1
init_goals = np.column_stack((np.linspace(50, 750, particle_amount, dtype=np.float32), np.random.rand(particle_amount) * 20 + lineheight)).astype(np.float32)
goal_arr = np.zeros(goal_size, dtype=np.int32)


def update_goals():
    global goals
    goals[:] = init_goals
    goal_arr[:] = pg.surfarray.pixels2d(goal_surf)
    fast_update_goals(goals, goal_arr, surfpos)


@nb.guvectorize([(nb.float32[:, :], nb.int32[:, :], nb.int32[:])], '(a,b),(c,d),(e)', target='parallel')
def fast_update_goals(g, input_array, offset):
    index = 0
    for i in range(input_array.shape[0]):
        for j in range(input_array.shape[1]):
            if input_array[i, j]:
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

    animation()

@nb.guvectorize([(nb.float32[:, :], nb.float32[:, :], nb.float32[:, :], nb.float32[:, :], nb.float32, nb.float32, nb.float32[:], nb.float32, nb.float32, nb.float32)], '(a,b),(a,b),(a,b),(a,b),(),(),(c),(),(),()', target='parallel')
def update(p, vel, f, goal_pos, goal_attract, drag, m_p, m_attrack, ran_fac, delta_time):
    # random_mul = p_attract
    for i in range(p.shape[0]):
        d_x = goal_pos[i, 0] - p[i, 0]
        d_y = goal_pos[i, 1] - p[i, 1]
        dist = np.sqrt(np.sqrt(d_x ** 2 + d_y ** 2))
        m_d_x = m_p[0] - p[i, 0]
        m_d_y = m_p[1] - p[i, 1]
        m_dist = np.sqrt(np.sqrt(m_d_x ** 2 + m_d_y ** 2))
        f[i, 0] = d_x * goal_attract / dist - vel[i, 0] * drag + (np.random.rand() - 0.5) * ran_fac + m_d_x * m_attrack / m_dist
        f[i, 1] = d_y * goal_attract / dist - vel[i, 1] * drag + (np.random.rand() - 0.5) * ran_fac + m_d_y * m_attrack / m_dist
        vel[i, 0] += f[i, 0] * delta_time
        vel[i, 1] += f[i, 1] * delta_time
        p[i, 0] += vel[i, 0] * delta_time
        p[i, 1] += vel[i, 1] * delta_time


@nb.guvectorize([(nb.int32[:, :, :], nb.float32[:, :], nb.float32[:, :], nb.int32[:])], '(a,b,c),(d,e),(d,e),(c)', target='parallel')
def render(input_arr, p, v, p_c):
    for i in range(p.shape[0]):
        if 0 < p[i, 0] < input_arr.shape[0] and 0 < p[i, 1] < input_arr.shape[1]:
            i1 = nb.int32(p[i, 0])
            i2 = nb.int32(p[i, 1])
            vel = np.sqrt(v[i, 0] ** 2 + v[i, 1] ** 2)
            if vel < 5:
                input_arr[i1, i2, 0] = p_c[0]
                input_arr[i1, i2, 1] = p_c[1]
                input_arr[i1, i2, 2] = p_c[2]
            else:
                input_arr[i1, i2, 0] = p_c[0] / vel
                input_arr[i1, i2, 1] = p_c[1] * vel
                input_arr[i1, i2, 2] = p_c[2] / vel


def draw(dt):
    global old_time, render_arr

    render_arr[:, :] = background_color
    render(render_arr, particles, velocities, particle_color)
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
        text = display_font.render(str(time.hour) + ":" + str(time.minute) + ":" + str(time.second), True, (255, 255, 255))
        goal_surf.blit(text, (50, 70))
        update_goals()


old_time = time.time()
init()
# Main Loop:
loop = True
while loop:
    curr_time = time.time()
    dt = curr_time - old_time
    old_time = time.time()

    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False
        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                loop = False
            elif e.key == pg.K_SPACE:
                par_mouse_attract_init *= -1

    animation()
    mouse_pos = np.array(pg.mouse.get_pos(), dtype=np.float32)
    if 1 < mouse_pos[0] < window_size[0] - 1 and 1 < mouse_pos[1] < window_size[1] - 1:
        particle_attraction_mouse = par_mouse_attract_init
        particle_attraction = 0
        drag_coeff = 0.001
        random_factor = 0
    else:
        drag_coeff = drag_coeff_init
        particle_attraction = particle_attraction_init
        random_factor = random_factor_init
        particle_attraction_mouse = 0

    update(particles, velocities, forces, goals, particle_attraction, drag_coeff, mouse_pos, particle_attraction_mouse, random_factor, 0.65) # dt * 35)
    draw(dt)












