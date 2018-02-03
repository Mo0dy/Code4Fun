from Code4Fun.Utility.Vec2 import *
import numpy as np
import pygame as pg

mat_shape = (8, 8, 3)
content = np.zeros(mat_shape)
content[2, 2] = [200, 200, 200]

pg.init()
window_size = 800, 800
origin = Vec2(np.array(window_size)) / 2
screen = pg.display.set_mode(window_size)
pg.display.set_caption("test")
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms", 50)


def reset():
    global vector


def clear():
    global content
    content = np.zeros(mat_shape)


def update(dt):
    clear()
    for i in range(content.shape[0]):
        for j in range(content.shape[1]):
            content[i, j] = np.random.random_integers(0, 255, 3)


def draw():
    size_x = window_size[0] / content.shape[0]
    size_y = window_size[1] / content.shape[1]

    for i in range(content.shape[0]):
        for j in range(content.shape[1]):
            pg.draw.rect(screen, content[i, j], (i * size_x + 10, j * size_y + 10, size_x - 20, size_y - 20))


keydown_func = {
    pg.K_r: reset
}


reset()
loop = True
while loop:
    clock.tick(10)
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
