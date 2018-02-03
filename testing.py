from MyMaths.Vec2 import *
import numpy as np
import pygame as pg


pg.init()
window_size = 800, 800
origin = Vec2(np.array(window_size)) / 2
screen = pg.display.set_mode(window_size)
pg.display.set_caption("test")
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms", 50)


def reset():
    global vector
    vector = Vec2(100, 0)


def update(dt):
    global vector
    m_pos = Vec2(pg.mouse.get_pos())
    vector = m_pos - origin


def draw():
    text = font.render(str(np.degrees(vector.theta)), True, (255, 255, 255))
    screen.blit(text, (50, 50))
    pg.draw.line(screen, (255, 255, 255), origin.tuple_int, (origin + vector).tuple_int)


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

    update(clock.get_time())
    screen.fill((50, 50, 50))
    draw()
    pg.display.flip()
pg.quit()
