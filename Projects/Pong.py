# pong from scratch
import pygame as pg
import random
import sys
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10, 10)

paddle_dir_stat = 0
paddle_dir_up = 1
paddle_dir_down = 1

# settings
background_color = 50, 50, 50
window_size = 1200, 800
paddle_length = 100
paddle_margin = 50
paddle_width = 20
paddle_speed = 10
paddle_y_margin = 5
paddle_speed_mul = 0.5

# variables
l_paddle_y = 0
l_paddle_x = paddle_margin
r_paddle_y = 0
r_paddle_x = window_size[0] - paddle_margin

r_paddle_dir = paddle_dir_stat
l_paddle_dir = paddle_dir_stat

b_x = window_size[0] / 2
b_y = window_size[1] / 2
b_size = 10
b_vx = 0
b_vy = 0

pg.init()
screen = pg.display.set_mode(window_size)
pg.display.set_caption("Pong!")
clock = pg.time.Clock()


def init():
    global l_paddle_y, r_paddle_y, b_x, b_y, b_vx, b_vy
    l_paddle_y = window_size[1] / 2 - paddle_length / 2
    r_paddle_y = window_size[1] / 2 - paddle_length / 2

    b_x = window_size[0] / 2
    b_y = window_size[1] / 2
    b_vx = 10
    b_vy = (random.random() - 0.5) * 3


def update():
    global b_x, b_y, b_vx, b_vy
    # move ball
    b_x += b_vx
    b_y += b_vy


    b_vx *= 1.001
    b_vy *= 1.001

    # collision with upper and lower edge:
    if b_y - b_size / 2 < 0:
        b_y = b_size / 2
        b_vy *= -1
    elif b_y + b_size > window_size[1]:
        b_y = window_size[1] - b_size / 2 - 2
        b_vy *= -1

    # collision with paddles
    if b_x - b_size / 2 < l_paddle_x and l_paddle_y < b_y < l_paddle_y + paddle_length:
        b_x = l_paddle_x + b_size / 2
        b_vx *= -1
        # change y velocity
        if l_paddle_dir == paddle_dir_up:
            print("up")
            b_vy += paddle_speed * paddle_speed_mul
        elif l_paddle_dir == paddle_dir_down:
            b_vy -= paddle_speed * paddle_speed_mul
    elif b_x + b_size / 2 > r_paddle_x and r_paddle_y < b_y < r_paddle_y + paddle_length:
        b_x = r_paddle_x - b_size / 2
        b_vx *= -1
        # change y velocity
        if r_paddle_dir == paddle_dir_up:
            b_vy += paddle_speed * paddle_speed_mul
        elif r_paddle_dir == paddle_dir_down:
            b_vy -= paddle_speed * paddle_speed_mul


def draw():
    screen.fill(background_color)

    # draw paddles
    pg.draw.rect(screen, (255, 255, 255), (l_paddle_x, int(l_paddle_y), -paddle_width, paddle_length))
    pg.draw.rect(screen, (255, 255, 255), (r_paddle_x, int(r_paddle_y), paddle_width, paddle_length))

    # draw_ball
    pg.draw.circle(screen, (255, 255, 255), (int(b_x), int(b_y)), b_size)
    pg.display.flip()


def move_r_paddle_up():
    global r_paddle_y, r_paddle_dir
    r_paddle_y -= paddle_speed
    if r_paddle_y < paddle_y_margin:
        r_paddle_y = paddle_y_margin
    r_paddle_dir = paddle_dir_up


def move_r_paddle_down():
    global r_paddle_y, r_paddle_dir
    r_paddle_y += paddle_speed
    if r_paddle_y + paddle_length > window_size[1] - paddle_y_margin:
        r_paddle_y = window_size[1] - paddle_y_margin - paddle_length
    r_paddle_dir = paddle_dir_down


def move_l_paddle_up():
    global l_paddle_y, l_paddle_dir
    l_paddle_y -= paddle_speed
    if l_paddle_y < paddle_y_margin:
        l_paddle_y = paddle_y_margin
    l_paddle_dir = paddle_dir_up


def move_l_paddle_down():
    global l_paddle_y, l_paddle_dir
    l_paddle_y += paddle_speed
    if l_paddle_y + paddle_length > window_size[1] - paddle_y_margin:
        l_paddle_y = window_size[1] - paddle_y_margin - paddle_length
    l_paddle_dir = paddle_dir_down


def my_quit():
    global loop
    loop = False


keydown_functions = {
    pg.K_ESCAPE: my_quit,
    pg.K_r: init
}

keypressed_functions = {
    pg.K_UP: move_r_paddle_up,
    pg.K_DOWN: move_r_paddle_down,
    pg.K_w: move_l_paddle_up,
    pg.K_s: move_l_paddle_down,
}

pressed_keys = set()

init()
loop = True
while loop:
    clock.tick(30)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False
        elif e.type == pg.KEYDOWN:
            try:
                keydown_functions[e.key]()
            except:
                sys.stderr.write("No such key\n")
                sys.stderr.flush()
            pressed_keys.add(e.key)
        elif e.type == pg.KEYUP:
            pressed_keys.remove(e.key)

    r_paddle_dir = paddle_dir_stat
    l_paddle_dir = paddle_dir_stat

    for k in pressed_keys:
        try:
            print(k)
            keypressed_functions[k]()
        except:
            pass

    update()
    draw()

pg.quit()
