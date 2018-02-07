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
pressed_tile = pg.Surface((scale, scale))
pressed_tile.fill((50, 50, 50))
pg.draw.rect(pressed_tile, (100, 100, 100), (1, 1, scale - 2, scale - 2))


background = pg.Surface(window_size)

for i in range(content_shape[0]):
    for j in range(content_shape[1]):
        background.blit(tile, (i * scale, j * scale))


# variables
distances = np.zeros(content_shape)
mines = np.zeros(content_shape)
# the information the player currently has
info = np.ones(content_shape) * -1


def under_mouse():
    mouse_pos = Vec2(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
    # normalize mouse pos
    # scale mouse pos to array size:
    mouse_pos.x = int(mouse_pos.x / window_size[0] * content_shape[0])
    mouse_pos.y = int(mouse_pos.y / window_size[1] * content_shape[1])
    return mouse_pos


def choice(x, y):
    info[x, y] = distances[x, y]


def calc_dist():
    global distances
    distances = convolve(mines, con_mat).astype(np.uint8)


def fill_mines(density):
    global mines
    mines = (np.random.rand(content_shape[0], content_shape[1]) < density).astype(np.uint8)


def reset():
    global info
    fill_mines(mines_density)
    calc_dist()
    info = np.ones(content_shape) * -1


def game_over():
    reset()


def on_click():
    m_pos = under_mouse()
    if mines[m_pos[0], m_pos[1]]:
        game_over()
    else:
        choice(m_pos[0], m_pos[1])

def update():
    pass


def draw():
    # draw tile background
    screen.blit(background, (0, 0))

    # render the distances
    offset = int(scale / 2 - 3)
    for i in range(info.shape[0]):
        for j in range(info.shape[1]):
            dist = info[i, j]
            if dist > 0:
                if dist < 1:
                    color = (50, 50, 50)
                elif dist < 3:
                    color = (50, 50, 200)
                elif dist < 5:
                    color = (220, 100, 50)
                else:
                    color = (250, 50, 50)

                d = d_font.render("%d" % dist, True, color)
                screen.blit(d, (i * scale + offset, j * scale))

            elif dist == 0:
                screen.blit(pressed_tile, (i * scale, j * scale))


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
        elif e.type == pg.MOUSEBUTTONDOWN:
            on_click()

    update()
    draw()
    pg.display.flip()
pg.quit()
