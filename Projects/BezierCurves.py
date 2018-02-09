from Code4Fun.Utility.Vec2 import *
import numpy as np
import pygame as pg

background_color = 50, 50, 50
window_size = 800, 800



pg.init()
origin = Vec2(np.array(window_size)) / 2
screen = pg.display.set_mode(window_size)
pg.display.set_caption("test")
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms", 10)


def bezier_curve(p0, p1, p2, amount):
    t = np.linspace(0, 1, amount)

    points_x = (1 - t) * ((1 - t) * p0[0] + t * p1[0]) + t * ((1 - t) * p1[0] + t * p2[0])
    points_y = (1 - t) * ((1 - t) * p0[1] + t * p1[1]) + t * ((1 - t) * p1[1] + t * p2[1])
    return np.stack((points_x, points_y), axis=1)


def reset():
    global curve
    curve = bezier_curve(np.array([0, 0]), np.array([50, 100]), np.array([200, 0]), 10)


def update():
    pass


def draw():
    for p in curve:
        pg.draw.circle(screen, (255, 255, 255), (int(p[0]), int(p[1])), 1)

    text = font.render("%0.2f" % clock.get_fps(), True, (255, 255, 255))
    screen.blit(text, (10, 10))


keydown_func = {
    pg.K_r: reset
}


reset()
loop = True
while loop:
    clock.tick()
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False
        elif e.type == pg.KEYDOWN:
            keydown_func[e.key]()

    update()
    screen.fill(background_color)
    draw()
    pg.display.flip()
pg.quit()
