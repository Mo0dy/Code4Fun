from Code4Fun.Utility.Vec2 import *
import numpy as np
import pygame as pg
from scipy.ndimage.filters import convolve


con_mat = np.array([[1, 1, 1],
                    [1, 1, 1],
                    [1, 1, 1]], dtype=np.uint8)


# settings
background_color = 50, 50, 50
content_shape = 50, 20
scale = 20
mines_density = 0.1
window_size = content_shape[0] * scale, content_shape[1] * scale


# pygame init
pg.init()
origin = Vec2(np.array(window_size)) / 2
screen = pg.display.set_mode(window_size)
pg.display.set_caption("test")
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms", 20)
d_font = pg.font.SysFont("arialblack", 12)
tile = pg.image.load(r"Assets\Minesweeper\tile.png")
tile = pg.transform.scale(tile, (scale, scale))

background = pg.Surface(window_size)
for i in range(content_shape[0]):
    for j in range(content_shape[1]):
        background.blit(tile, (i * scale, j * scale))


# variables
distances = np.zeros(content_shape)
mines = np.zeros(content_shape)


def calc_dist():
    global distances
    distances = convolve(mines, con_mat).astype(np.uint8)


def fill_mines(density):
    global mines
    mines = (np.random.rand(content_shape[0], content_shape[1]) < density).astype(np.uint8)


def reset():
    fill_mines(mines_density)
    calc_dist()


def update():
    pass


def draw():
    # draw tile background
    screen.blit(background, (0, 0))

    # render the distances
    offset = int(scale / 2 - 3)
    for i in range(distances.shape[0]):
        for j in range(distances.shape[1]):
            dist = distances[i, j]
            if dist < 1:
                color = (50, 50, 50)
            elif dist < 3:
                color = (50, 50, 200)
            elif dist < 5:
                color = (220, 100, 50)
            else:
                color = (250, 50, 50)

            d = d_font.render(str(dist), True, color)
            screen.blit(d, (i * scale + offset, j * scale))


    # draw mines in red
    for i in range(mines.shape[0]):
        for j in range(mines.shape[1]):
            if mines[i, j]:
                pg.draw.circle(screen, (255, 0, 0), (i * scale + int(scale / 2), j * scale + int(scale / 2)), 4)


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
    draw()
    pg.display.flip()
pg.quit()
