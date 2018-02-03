import pygame as pg
import numpy as np
import numba as nb
from copy import deepcopy
import time
import pygame.gfxdraw
from PIL import Image


# settings
# simulation
particle_amount = 2000000
scale_factor = 0.1
particle_attraction_mouse = np.float32(1 * scale_factor)
particle_attraction_self = np.float32(-0.0005 * scale_factor)
drag_coeff = np.float32(0.015 * scale_factor)
render_tail = False
fast_render = True


# display
pg.init()
window_size = 2048, 1152
screen = pg.display.set_mode(window_size)
pg.display.set_caption("Particle Storm")
# background_color = 206, 195, 163
# particle_color = np.array([206, 59, 22], dtype=int)
background_color = 20, 20, 20
particle_color = np.array([142, 136, 8], dtype=int)
tail_color = particle_color
particle_size = max(int(5 * scale_factor), 1)
tail_length = int(50 * scale_factor)
font = pg.font.SysFont("comicsansms", 50)
small_font = pg.font.SysFont("comicsansms", 10)
pg.mouse.set_visible(False)

# variables
particles = np.zeros((particle_amount, 2), dtype=np.float32)
velocities = np.zeros((particle_amount, 2), dtype=np.float32)
forces = np.zeros((particle_amount, 2), dtype=np.float32)
render_arr = np.zeros((window_size[0], window_size[1], 3), dtype=np.int32)

tail = np.zeros((tail_length, particle_amount, 2))
tail_index = 1

alpha_b = np.linspace(0, tail_length, tail_length) / tail_length
alpha_a = 1 - alpha_b
tail_colors = np.transpose(np.array([(background_color[i] * alpha_a + tail_color[i] * alpha_b * (1 - alpha_a)) / (alpha_a + alpha_b * (1 - alpha_a)) for i in range(3)], dtype=int))
tail_sizes = np.linspace(1, particle_size, tail_length, dtype=int)


def save_image(iter):
    Image.fromarray(pg.surfarray.pixels3d(screen)).save("Images\\" + str(iter) + ".png")


def add_tail():
    global tail, tail_index
    tail[tail_index] = deepcopy(particles.astype(int))
    tail_index = (tail_index + 1) % tail_length


def init():
    global particles, velocities, forces

    particles = np.random.rand(particle_amount, 2)
    particles[:, 0] *= window_size[0]
    particles[:, 1] *= window_size[1]
    particles = particles.astype(np.float32)
    velocities = np.zeros((particle_amount, 2), dtype=np.float32)
    forces = np.zeros((particle_amount, 2), dtype=np.float32)


@nb.guvectorize([(nb.float32[:, :], nb.float32[:, :], nb.float32[:, :], nb.float32[:], nb.float32, nb.float32)], '(a,b),(a,b),(a,b),(c),(),()', target='parallel')
# @nb.jit
def update(p, vel, f, m_pos, m_attract, drag):
    # random_mul = p_attract
    for i in range(p.shape[0]):
        d_x = m_pos[0] - p[i, 0]
        d_y = m_pos[1] - p[i, 1]
        dist = np.sqrt(d_x ** 2 + d_y ** 2)
        f[i, 0] = d_x * m_attract / dist - vel[i, 0] * drag
        f[i, 1] = d_y * m_attract / dist - vel[i, 1] * drag

        vel[i, 0] += f[i, 0]
        vel[i, 1] += f[i, 1]
        p[i, 0] += vel[i, 0]
        p[i, 1] += vel[i, 1]


def draw_tail():
    global screen
    for j in range(particle_amount):
        for i in range(tail_index + 1, tail_length + tail_index - 1):
            index1 = i % tail_length
            index2 = (i + 1) % tail_length
            index3 = i - tail_index - 1
            pg.draw.line(screen, tail_colors[index3], (tail[index1, j, 0], tail[index1, j, 1]), (tail[index2, j, 0], tail[index2, j, 1]), tail_sizes[index3])


@nb.guvectorize([(nb.int32[:, :, :], nb.float32[:, :], nb.int32[:])], '(a,b,c),(d,e),(c)', target='parallel')
def render(input_arr, p, p_c):
    for i in range(p.shape[0]):
        if 0 < p[i, 0] < input_arr.shape[0] and 0 < p[i, 1] < input_arr.shape[1]:
            i1 = nb.int32(p[i, 0])
            i2 = nb.int32(p[i, 1])
            input_arr[i1, i2, 0] = p_c[0]
            input_arr[i1, i2, 1] = p_c[1]
            input_arr[i1, i2, 2] = p_c[2]


old_time = 0
def draw():
    global old_time, render_arr

    if fast_render:
        render_arr[:, :] = background_color
        render(render_arr, particles, particle_color)
        pg.surfarray.pixels3d(screen)[:] = render_arr
    else:
        screen.fill(background_color)
        if render_tail:
            draw_tail()
        for p in particles:
            pg.draw.circle(screen, particle_color, (int(p[0]), int(p[1])), particle_size)

    curr_time = time.time()
    try:
        fps = 1 / (curr_time - old_time)
    except:
        fps = 0
    old_time = time.time()
    text = small_font.render("%.3f" % fps, True, (100, 80, 80))
    screen.blit(text, (10, 20))
    pg.gfxdraw.aacircle(screen, pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], 5, (94, 34, 14))
    pg.gfxdraw.aacircle(screen, pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], 4, (94, 34, 14))
    pg.display.flip()


keydown_functions = {
    pg.K_SPACE: init
}

iteration = 0
save_time = time.time() + 1
init()
# Main Loop:
loop = True
while loop:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False
        elif e.type == pg.KEYDOWN:
            try:
                keydown_functions[e.key]()
            except:
                pass

    if time.time() > save_time:
        save_image(iteration)
        save_time = time.time() + 1
        iteration += 1

    mouse_pos = np.array(pg.mouse.get_pos(), dtype=np.float32)
    update(particles, velocities, forces, mouse_pos, particle_attraction_mouse, drag_coeff)
    if render_tail:
        add_tail()
    draw()












