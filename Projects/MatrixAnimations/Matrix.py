from Code4Fun.Utility.Vec2 import *
import numpy as np
import pygame as pg
from scipy.ndimage.filters import convolve
import Code4Fun.Projects.MatrixAnimations.GridFlame as gFlame
import Code4Fun.Projects.MatrixAnimations.Rain as Rain

mat_shape = np.array([8, 8, 3])
margins = 5
resolution = 1
content = np.zeros(mat_shape)

Rain.init(mat_shape, 10)


pg.init()
window_size = mat_shape[0] * 100, mat_shape[1] * 100
origin = Vec2(np.array(window_size)) / 2
screen = pg.display.set_mode(window_size)
pg.display.set_caption("Matrix Animations")
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms", 50)


def reset():
    pass


def clear():
    global content
    content = np.zeros(mat_shape)


def update():
    global content
    Rain.update(content)

def draw():
    global content
    size_x = window_size[0] / content.shape[0]
    size_y = window_size[1] / content.shape[1]

    for i in range(content.shape[0]):
        for j in range(content.shape[1]):
            pg.draw.rect(screen, content[i, j], (i * size_x + margins, j * size_y + margins, size_x - margins * 2, size_y - margins * 2))


keydown_func = {
    pg.K_r: reset
}


reset()
loop = True
while loop:
    clock.tick(20)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False
        elif e.type == pg.KEYDOWN:
            try:
                keydown_func[e.key]()
            except:
                pass

    update()
    screen.fill((50, 50, 50))
    draw()
    pg.display.flip()
pg.quit()
