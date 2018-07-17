import pygame as pg
from Code4Fun.Utility.Vec2 import Vec2
import numpy as np
import sys
import serial
import time
from Code4Fun.ArduinoInteraction.MatrixDraw.Slider import Slider
from Code4Fun.ArduinoInteraction.MatrixDraw.Matrix import Matrix
from copy import deepcopy
import Code4Fun.Utility.PygameAdditionals as pga
from Code4Fun.ArduinoInteraction.MatrixDraw.Animation import Animation


print('''
press "lmb" to draw
press "rmb" to delete
press "u" to pick color under cursor
press "r" to reset matrix
press "f" to append current image to current animation
press "p" to play the animation
press "c" to clear the animation
press "s" to save animation
press "l" to load saved animation
drag sliders to change color values
''')

# the size of the led matrix
rows = 10
columns = 10


background_color = 50, 50, 50
# the half of the thickness of the border between squares
border_thickness_half = 5
window_size = 1200, 800

# the pixel size of the displayed matrix (smaller to leave space for sliders)
matrix_size = 800, 800

origin = Vec2(window_size[0] / 2, window_size[1] / 2)
fps_cap = 30

# the size of one single square of the matrix
square_dx = int(matrix_size[0] / columns)
square_dy = int(matrix_size[1] / rows)

# creates window
pg.init()
screen = pg.display.set_mode(window_size)
pg.display.set_caption("Matrix Draw")
# clock to access time and limit loop fps
clock = pg.time.Clock()
# a font for drawing fps
font = pg.font.SysFont("comicsansms", 20)

# for communication with the arduino
ser = serial.Serial('COM3', 115200, timeout=0.01)

# keeps track of what mouse buttons are pressed
left_mb_pressed = False
right_mb_pressed = False

# keeps track of what color is currently selected
draw_color = [255, 255, 255]

# stores the current animation
animation = Animation()
# stores the current display matrix
matrix = Matrix(columns, rows)

# the three color sliders
sliders = {
    "r": Slider((200, 50, 50), 850, 50, 300, 200),
    "g": Slider((50, 200, 50), 850, 300, 300, 200),
    "b": Slider((50, 50, 200), 850, 550, 300, 200)
}

anim_save_path = "Animations"


# function that gets called if the left mb is pressed
def lm_down():
    # sets sliders that are hovered over to be selected (they will now change their values according to mouse position)
    for s in sliders.values():
        if s.collision(pg.mouse.get_pos()):
            s.selected = True
            # only one can be selected
            break


def lm_up():
    # if button is not pressed no sliders can be selected anymore
    for s in sliders.values():
        s.selected = False


def lm_pressed():
    pass


# resets animation
def clear_animation():
    animation.clear()


# adds another frame to animation
def add_frame_anim():
    animation.add_frame(matrix)


# plays the animation
# this locks the program!
def play_animation():
    global matrix
    for m in animation.play():
        send_matrix_arduino(m)
        draw_matrix(m)
        pg.display.flip()


def save_anim():
    name = input("Enter save name: ")
    animation.save(anim_save_path, name)


def load_anim():
    name = input("Enter load name: ")
    animation.load(anim_save_path, name)


# sets led on arduino
def set_led_arduino(x, y, c):
    ser.write((str(x) + " " + str(y) + " " + str(c[0]) + " " + str(c[1]) + " " + str(c[2]) + " \n").encode())


# displays changes to leds on arduino
def flip_leds_arduino():
    ser.write('a\n'.encode())


# sends complete matrix to arduino and updates led's
def send_matrix_arduino(m):
    for x in range(columns):
        for y in range(rows):
            set_led_arduino(x, y, m.leds[x, y])
    flip_leds_arduino()


# returns current matrix square under mouse
def square_under_mouse():
    m_pos = pg.mouse.get_pos()
    mouse_x = int(m_pos[0] / matrix_size[0] * columns)
    mouse_y = int(m_pos[1] / matrix_size[1] * rows)
    return mouse_x, mouse_y


# draws on matrix and sends to arduino
def draw_on_matrix(c, pos):
    global matrix
    # only draw if on matrix
    if pos[0] < columns and pos[1] < rows:
        matrix.set_led(pos[0], pos[1], c)
        set_led_arduino(pos[0], pos[1], c)
        flip_leds_arduino()


# selects color under mouse
def pick_color():
    global draw_color
    square = square_under_mouse()
    draw_color = matrix.leds[square[0], square[1]].copy()
    sliders["r"].value = int(draw_color[0])
    sliders["g"].value = int(draw_color[1])
    sliders["b"].value = int(draw_color[2])


def init():
    matrix.set_all((0, 0, 0))

    # reset arduino matrix
    for x in range(columns):
        for y in range(rows):
            set_led_arduino(x, y, (0, 0, 0))
            time.sleep(0.005)
    flip_leds_arduino()


def draw_matrix(mat):
    for x in range(columns):
        for y in range(rows):
            pg.draw.rect(screen, mat.leds[x, y], (x * square_dx + border_thickness_half, y * square_dy + border_thickness_half, square_dx - border_thickness_half * 2, square_dy - border_thickness_half * 2))


def draw(dt):
    if left_mb_pressed:
        draw_on_matrix(draw_color, square_under_mouse())
        for s in sliders.values():
            s.update(pg.mouse.get_pos())

        draw_color[0] = sliders["r"].value
        draw_color[1] = sliders["g"].value
        draw_color[2] = sliders["b"].value

    elif right_mb_pressed:
        draw_on_matrix((0, 0, 0), square_under_mouse())

    draw_matrix(matrix)

    for s in sliders.values():
        s.draw(screen)


keydown_func = {
    pg.K_r: init,
    pg.K_u: pick_color,
    pg.K_f: add_frame_anim,
    pg.K_p: play_animation,
    pg.K_c: clear_animation,
    pg.K_s: save_anim,
    pg.K_l: load_anim,
}

init()
loop = True
while loop:
    clock.tick(fps_cap)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False
        elif e.type == pg.KEYDOWN:
            try:
                keydown_func[e.key]()
            except:
                pass
                # sys.stderr.write("No such Key!")
                # sys.stderr.flush()
        elif e.type == pg.MOUSEBUTTONDOWN:
            if e.button == pga.MB_LEFT:
                left_mb_pressed = True
                lm_down()
            elif e.button == pga.MB_RIGHT:
                right_mb_pressed = True
        elif e.type == pg.MOUSEBUTTONUP:
            if e.button == pga.MB_LEFT:
                left_mb_pressed = False
                lm_up()
            elif e.button == pga.MB_RIGHT:
                right_mb_pressed = False

    screen.fill(background_color)
    draw(clock.get_time() / 1000)
    text = font.render("%0.2f" % clock.get_fps(), True, (255, 255, 255))
    screen.blit(text, (10, 10))
    pg.display.flip()
pg.quit()
