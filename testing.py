import numpy as np
import pygame as pg
import sys

background_color = 50, 50, 50
window_size = 800, 800
fps_cap = 60

pg.init()
screen = pg.display.set_mode(window_size)
pg.display.set_caption("Smart Rockets")
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms", 20)


def init():
    pass


def draw(dt):
    pass


keydown_func = {
    pg.K_r: init
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

    screen.fill(background_color)
    draw(clock.get_time() / 1000)
    text = font.render("%0.2f" % clock.get_fps(), True, (255, 255, 255))
    screen.blit(text, (10, 10))
    pg.display.flip()
pg.quit()
