from Code4Fun.Utility.Vec2 import *
import numpy as np
import pygame as pg


# settings
background_color = 50, 50, 50
ball_color = 200, 150, 30
window_size = 1600, 800
ball_size = 10
string_tension = 100
spring_origin = Vec2(300, window_size[1] - 300)
g = 4000
damping = 500
spring_len = 50


pg.init()
origin = Vec2(np.array(window_size)) / 2
screen = pg.display.set_mode(window_size)
pg.display.set_caption("test")
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms", 20)


# variables
b_pos = Vec2()
b_vel = Vec2()
mouse_pressed = False


# connected to spring
b_attatched = True


def init():
    global b_pos, b_attatched
    b_pos = Vec2(100, window_size[1] - 100)
    b_attatched = True


def update(dt):
    global b_vel, b_pos, b_attatched
    b_force = Vec2()

    if mouse_pressed:
        b_pos.x = pg.mouse.get_pos()[0]
        b_pos.y = pg.mouse.get_pos()[1]
        b_vel = Vec2()
    else:
        if b_attatched:
            # ball spring tension:
            d_spring = spring_origin - b_pos
            elongation = abs(d_spring)
            d_spring_scalar = elongation - spring_len
            if d_spring_scalar > 0:
                b_force = d_spring / elongation * (d_spring_scalar) * string_tension
            else:
                b_attatched = False
        b_force.y += g
        b_vel += b_force * dt
        b_vel -= b_vel / abs(b_vel) * damping * dt
        b_pos += b_vel * dt


def draw():
    # render ball
    if b_attatched:
        pg.draw.line(screen, (40, 40, 40), b_pos.tuple_int, spring_origin.tuple_int, 4)

    pg.draw.circle(screen, ball_color, b_pos.tuple_int, ball_size)
    pg.draw.circle(screen, (80, 80, 80), spring_origin.tuple_int, 5)

    # render FPS
    text = font.render("%0.2f" % clock.get_fps(), True, (255, 255, 255))
    screen.blit(text, (10, 10))


keydown_func = {
    pg.K_r: init
}


init()
loop = True
while loop:
    clock.tick(60)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False
        elif e.type == pg.KEYDOWN:
            keydown_func[e.key]()
        elif e.type == pg.MOUSEBUTTONDOWN:
            mouse_pressed = True
            b_attatched = True
        elif e.type == pg.MOUSEBUTTONUP:
            mouse_pressed = False

    update(clock.get_time() / 1000)
    screen.fill(background_color)
    draw()
    pg.display.flip()
pg.quit()
