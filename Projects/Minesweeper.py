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
total_tiles = content_shape[0] * content_shape[1]
distances = np.zeros(content_shape)
mines = np.zeros(content_shape)
# the information the player currently has
info = np.ones(content_shape) * -1
display_mines = False
chosen_fileds = 0
mines_amount = 0


def under_mouse():
    mouse_pos = Vec2(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
    # normalize mouse pos
    # scale mouse pos to array size:
    mouse_pos.x = int(mouse_pos.x / window_size[0] * content_shape[0])
    mouse_pos.y = int(mouse_pos.y / window_size[1] * content_shape[1])
    return mouse_pos


def choice(x, y):
    global chosen_fileds
    if mines[x, y]:
        game_over()
    else:
        if distances[x, y]:
            info[x, y] = distances[x, y]
            chosen_fileds += 1
        else:
            depth_f = depth_first(x, y)
            for i in depth_f:
                info[i[0], i[1]] = distances[i[0], i[1]]
            chosen_fileds += len(depth_f)


def calc_dist():
    global distances
    distances = convolve(mines, con_mat, mode='constant', cval=0).astype(np.uint8)


def fill_mines(density):
    global mines
    mines = (np.random.rand(content_shape[0], content_shape[1]) < density).astype(np.uint8)


def reset():
    global info, chosen_fileds, mines_amount
    fill_mines(mines_density)
    calc_dist()
    info = np.ones(content_shape) * -1
    chosen_fileds = 0
    mines_amount = mines[mines.astype(bool)].shape[0]


def game_over():
    print("game over")
    reset()


def on_click():
    m_pos = under_mouse()
    choice(m_pos[0], m_pos[1])


def update():
    if chosen_fileds > total_tiles - mines_amount:
        print("won")
        reset()


def depth_first(x, y):
    result = [[x, y]]
    path = [[x, y]]
    possible = distances == 0
    already_searched = np.zeros(possible.shape, dtype=np.bool)

    while len(path) > 0:
        for i in range(3):
            for j in range(3):
                look_x = path[0][0] + i - 1
                look_y = path[0][1] + j - 1
                if 0 <= look_x < possible.shape[0] and 0 <= look_y < possible.shape[1]:
                    if not already_searched[look_x, look_y]:
                        result.append([look_x, look_y])
                        already_searched[look_x, look_y] = True
                        if possible[look_x, look_y]:
                            path.append([look_x, look_y])
                            possible[look_x, look_y] = False
        del path[0]
    return result


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

    if display_mines:
        # draw mines in red
        for i in range(mines.shape[0]):
            for j in range(mines.shape[1]):
                if mines[i, j]:
                    pg.draw.circle(screen, (255, 0, 0), (i * scale + int(scale / 2), j * scale + int(scale / 2)), 4)



def toggle_mines():
    global display_mines
    display_mines = not display_mines


keydown_func = {
    pg.K_r: reset,
    pg.K_m: toggle_mines,
}


reset()
loop = True
while loop:
    clock.tick(30)
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
