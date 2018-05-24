import pygame as pg
import sys
import serial

background_color = 50, 50, 50
window_size = 800, 800
origin = [window_size[0] / 2, window_size[1] / 2]
fps_cap = 60

pg.init()
screen = pg.display.set_mode(window_size)
pg.display.set_caption("Joystick to Arudino")
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms", 20)

ser = serial.Serial('COM5', 115200)

buttons = {
    0: "A",
    1: "B",
    2: "X",
    3: "Y",
}

button_pressed = {
    "A": False,
    "B": False,
    "X": False,
    "Y": False,
}

offsets = {
    "A": [0, 200],
    "B": [200, 0],
    "X": [-200, 0],
    "Y": [0, -200],
}

colors = {
    "A": (60, 219, 78),
    "B": (208, 66, 66),
    "X": (64, 204, 208),
    "Y": (236, 219, 51),
}

hat_to_button = {
    (1, 0): "B",
    (0, 1): "Y",
    (-1, 0): "X",
    (0, -1): "A"
}

# init joysticks and get joystick
pg.joystick.init()
joysticks = [pg.joystick.Joystick(x) for x in range(pg.joystick.get_count())]

joystick = None

# select xBox controller
for j in joysticks:
    name = j.get_name()
    print(name)
    if name == "Controller (XBOX 360 For Windows)":
        joystick = j

joystick.init()
print("Joystick: " + joystick.get_name())


def send_serial(button):
    ser.write((button.encode()))
    pass


def init():
    pass


def my_quit():
    global loop
    loop = False


def draw(dt):
    for key, item in button_pressed.items():
        if item:
            pg.draw.circle(screen, colors[key], (int(origin[0] + offsets[key][0]), int(origin[1] + offsets[key][1])), 100)


keydown_func = {
    pg.K_r: init,
    pg.K_ESCAPE: my_quit,
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
                sys.stderr.write("No such Key!")
                sys.stderr.flush()
        elif e.type == pg.JOYBUTTONDOWN:
            print("button down")
            if e.button in buttons:
                button_pressed[buttons[e.button]] = True
                send_serial(buttons[e.button])
        elif e.type == pg.JOYBUTTONUP:
            print("button up")
            if e.button in buttons:
                button_pressed[buttons[e.button]] = False
        elif e.type == pg.JOYBUTTONUP:
            print("button up")
            if e.button in buttons:
                button_pressed[buttons[e.button]] = False
        elif e.type == pg.JOYHATMOTION:
            for key, value in button_pressed.items():
                button_pressed[key] = False
            if e.value in hat_to_button:
                button_pressed[hat_to_button[e.value]] = True
                send_serial(hat_to_button[e.value])

    screen.fill(background_color)
    draw(clock.get_time() / 1000)
    text = font.render("%0.2f" % clock.get_fps(), True, (255, 255, 255))
    screen.blit(text, (10, 10))
    pg.display.flip()
pg.quit()
ser.close()
