import pygame as pg
import numpy as np
import numba as nb
from copy import deepcopy
import time
import pygame.gfxdraw
from TimeTest import Tester


# settings
# simulation
particle_amount = 2000000
particle_attraction_mouse = 0.5
drag_coeff = 0.005
# drag_coeff = 0.05


# display
pg.init()
window_size = 800, 800
screen = pg.display.set_mode(window_size, pg.NOFRAME)
pg.display.set_caption("Particle Storm")
# background_color = 206, 195, 163
# particle_color = np.array([206, 59, 22], dtype=int)
background_color = 20, 20, 20
particle_color = np.array([142, 136, 8], dtype=int)
small_font = pg.font.SysFont("comicsansms", 10)
pg.mouse.set_visible(False)

# variables
particles = np.zeros((particle_amount, 2), dtype=np.float32)
velocities = np.zeros((particle_amount, 2), dtype=np.float32)
forces = np.zeros((particle_amount, 2), dtype=np.float32)
render_arr = np.zeros((window_size[0], window_size[1], 3), dtype=np.int32)


dummy_arr = np.zeros(window_size)


def init():
    global particles, velocities, forces

    particles = np.random.rand(particle_amount, 2)
    particles[:, 0] *= window_size[0]
    particles[:, 1] *= window_size[1]
    particles = particles.astype(np.float32)
    velocities = np.zeros((particle_amount, 2), dtype=np.float32)
    forces = np.zeros((particle_amount, 2), dtype=np.float32)


@nb.guvectorize([(nb.float32[:, :], nb.float32[:, :], nb.float32[:, :], nb.float32[:], nb.float32, nb.float32)], '(a,b),(a,b),(a,b),(c),(),()', target='parallel')
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

    render_arr[:, :] = background_color
    render(render_arr, particles, particle_color)
    pg.surfarray.pixels3d(screen)[:] = render_arr

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


def toggle_attraction():
    global particle_attraction_mouse
    particle_attraction_mouse *= -1


keydown_functions = {
    pg.K_r: init,
    pg.K_SPACE: toggle_attraction,
}


init()
# Main Loop:
loop = True
while loop:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False
        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                loop = False
            else:
                try:
                    keydown_functions[e.key]()
                except:
                    pass
    mouse_pos = np.array(pg.mouse.get_pos(), dtype=np.float32)
    update(particles, velocities, forces, mouse_pos, particle_attraction_mouse, drag_coeff)
    draw()












