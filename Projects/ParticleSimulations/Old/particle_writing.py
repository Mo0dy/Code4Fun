import pygame as pg
import numpy as np
import numba as nb
import pygame.gfxdraw
import os
import Code4Fun.Utility.Renderer as rnd
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 150)

# goal_surface:
goal_size = [1600, 250]
goal_surf = pg.Surface(goal_size)
surfpos = np.array([0, 0], dtype=np.int32)


# settings
# simulation
particle_amount = 250000
par_mouse_attract_init = 0.3
particle_attraction_init = 0.2
particle_disburtion_init = -0.005
drag_coeff_init = 0.1
# drag_coeff = 0.05
random_factor_init = 0.5
lineheight = 20

text_size = 125
text_pos = 30, 30
character_limit = 33


# display
pg.init()
window_size = goal_size
x_bounds_init = [-100, window_size[0] + 100]
y_bounds_init = [-100, window_size[1] + 100]
screen = pg.display.set_mode(window_size, pg.NOFRAME)
pg.display.set_caption("Particle Writing")
background_color = np.array([20, 20, 20], dtype=np.uint8)
particle_color = np.array([142, 136, 8], dtype=np.uint8)
small_font = pg.font.SysFont("comicsansms", 10)
display_font = pg.font.SysFont("caolibri", text_size)
pg.mouse.set_visible(False)

paint_image = pg.image.load("Assets\\FillEffect.png")
paint_image_rect = paint_image.get_rect()
paint_image_rect.x = window_size[0] - 10


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

render_string = ""
keys_pressed = []
update_animation = True


goal_arr = np.zeros(goal_size, dtype=np.int32)


def update_goals():
    global goals, goal_forces
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
    global particles, velocities, forces, render_string, update_animation
    render_string = "<Codin4all>"
    update_animation = True
    velocities = np.zeros((particle_amount, 2), dtype=np.float32)
    forces = np.zeros((particle_amount, 2), dtype=np.float32)
    update_goals()
    animation()


@nb.guvectorize([(nb.float32[:, :], nb.float32[:, :], nb.float32[:, :], nb.float32[:, :], nb.float32[:], nb.float32, nb.float32[:], nb.float32, nb.float32, nb.float32, nb.int32[:], nb.int32[:])], '(a,b),(a,b),(a,b),(a,b),(a),(),(c),(),(),(),(d),(d)', target='parallel')
def update(p, vel, f, goal_pos, goal_attract, drag, m_p, m_attrack, ran_fac, delta_time, x_b, y_b):
    for i in range(p.shape[0]):
        d_x = goal_pos[i, 0] - p[i, 0]
        d_y = goal_pos[i, 1] - p[i, 1]
        dist = np.sqrt(np.sqrt(d_x ** 2 + d_y ** 2))
        m_d_x = m_p[0] - p[i, 0]
        m_d_y = m_p[1] - p[i, 1]
        m_dist = np.sqrt(np.sqrt(m_d_x ** 2 + m_d_y ** 2))
        f[i, 0] = d_x * goal_attract[i] / dist - vel[i, 0] * drag + (np.random.rand() - 0.5) * ran_fac + m_d_x * m_attrack / m_dist
        f[i, 1] = d_y * goal_attract[i] / dist - vel[i, 1] * drag + (np.random.rand() - 0.5) * ran_fac + m_d_y * m_attrack / m_dist
        vel[i, 0] += f[i, 0] * delta_time
        vel[i, 1] += f[i, 1] * delta_time
        p[i, 0] += vel[i, 0] * delta_time
        p[i, 1] += vel[i, 1] * delta_time

        out_of_bounds = False

        if x_b[1] < p[i, 0]:
            p[i, 0] = x_b[1]
            out_of_bounds = True

        elif p[i, 0] < x_b[0]:
            p[i, 0] = x_b[0]
            out_of_bounds = True

        if y_b[1] < p[i, 1]:
            p[i, 1] = y_b[1]
            out_of_bounds = True

        elif p[i, 1] < y_b[0]:
            p[i, 1] = y_b[0]
            out_of_bounds = True

        if out_of_bounds:
            vel[i, 0] = 0
            vel[i, 1] = 0


def draw(dt):
    global paint_image_rect

    screen.fill(background_color)
    rnd.render_points(particles, particle_color, pg.surfarray.pixels3d(screen))

    text = small_font.render("%.3f" % (1 / dt), True, (100, 80, 80))
    screen.blit(text, (10, 5))
    # draw ink fill
    fill_height = np.argmax(goal_forces < 0) / particle_amount * window_size[1]
    back_color = pg.Color(20, 20, 20).correct_gamma(1.1)
    pg.draw.rect(screen, back_color, (window_size[0], 0, -10, window_size[1]))
    paint_image_rect.y = fill_height
    screen.blit(paint_image, paint_image_rect)
    if 1 < pg.mouse.get_pos()[0] < window_size[0] - 1 and 1 < pg.mouse.get_pos()[1] < window_size[1] - 1:
        pg.gfxdraw.aacircle(screen, pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], 5, (94, 34, 14))
        pg.gfxdraw.aacircle(screen, pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], 4, (94, 34, 14))
    pg.display.flip()


def toggle_attraction():
    global particle_attraction_mouse
    particle_attraction_mouse *= -1


def animation():
    global render_string, keys_pressed, update_animation
    if update_animation:
        update_animation = False
        if len(render_string) < character_limit * 2:
            for k in keys_pressed:
                if len(render_string) == character_limit:
                    render_string += "\n"
                render_string += chr(k)
        keys_pressed = []
        goal_surf.fill(0)
        # render_string += ";"
        lines = render_string.split("\n")
        y_pos = text_pos[1]
        for l in lines:
            text = display_font.render(l, True, (255, 255, 255))
            goal_surf.blit(text, (text_pos[0], y_pos))
            y_pos += text_size - 30
        # render_string = render_string[:-1]
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
            elif e.key == pg.K_F1:
                par_mouse_attract_init *= -1
            elif e.key == pg.K_F2:
                init()
            elif 31 < e.key < 123:
                if e.mod & pg.KMOD_SHIFT:
                    keys_pressed.append(e.key -32)
                else:
                    keys_pressed.append(e.key)
                update_animation = True
            elif e.key == pg.K_BACKSPACE:
                render_string = render_string[:-1]
                update_animation = True
            elif e.key == pg.K_RETURN:
                render_string += "\n"


    animation()
    mouse_pos = np.array(pg.mouse.get_pos(), dtype=np.float32)
    if 1 < mouse_pos[0] < window_size[0] - 1 and 1 < mouse_pos[1] < window_size[1] - 1:
        particle_attraction_mouse = par_mouse_attract_init
        particle_attraction = 0
        drag_coeff = 0.001
        random_factor = 0
        x_bounds = [x_bounds_init[0] - 1000, x_bounds_init[1] + 1000]
        y_bounds = [y_bounds_init[0] - 1000, x_bounds_init[1] + 1000]
    else:
        drag_coeff = drag_coeff_init
        particle_attraction = particle_attraction_init
        random_factor = random_factor_init
        particle_attraction_mouse = 0
        x_bounds = x_bounds_init
        y_bounds = y_bounds_init

    update(particles, velocities, forces, goals, goal_forces, drag_coeff, mouse_pos, particle_attraction_mouse, random_factor, 1.2, x_bounds, y_bounds) # dt * 35)
    draw(dt)












