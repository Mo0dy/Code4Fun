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
font = pg.font.SysFont("comicsansms", 20)


def init():
    pass


def update():
    pass


def draw():
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

    update()
    screen.fill(background_color)
    draw()
    pg.display.flip()
pg.quit()
