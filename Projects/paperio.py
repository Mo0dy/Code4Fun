import numpy as np
import pygame as pg
import sys

# game settings
player_color = 200, 50, 50
mapsize = 20, 20
mid_x, mid_y = mapsize[0] / 2, mapsize[1] / 2

# the size of the squares (zoom)
square_x, square_y = 20, 20


background_color = 50, 50, 50
window_size = 800, 800
fps_cap = 5

pg.init()
screen = pg.display.set_mode(window_size)
pg.display.set_caption("Smart Rockets")
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms", 20)

# game variables
# gameworld holds int values for team association 0 is no team
grid = np.zeros(mapsize)
pos_x, pos_y = 5, 5

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

direction = 2


def init():
    pass


# returns the color according to the team
def get_color(team):
    if team:
        return player_color
    else:
        return background_color


def draw(dt):
    global pos_x, pos_y
    screen.fill((0, 0, 0))

    # update the square
    if direction == 0:
        pos_y -= 1
    elif direction == 1:
        pos_x += 1
    elif direction == 2:
        pos_y += 1
    elif direction == 3:
        pos_x -= 1

    # update color under square
    grid[pos_x, pos_y] = 1

    # draw grid
    for x in range(mapsize[0]):
        for y in range(mapsize[0]):
            pg.draw.rect(screen, get_color(grid[x, y]), ((x - pos_x - 5) * square_x + window_size[0] / 2, (y - pos_y - 5)* square_y + window_size[1] / 2, square_x, square_y))


def dir_up():
    global direction
    direction = 0

def dir_right():
    global direction
    direction = 1

def dir_down():
    global direction
    direction = 2

def dir_left():
    global direction
    direction = 3


keydown_func = {
    pg.K_r: init,
    pg.K_UP: dir_up,
    pg.K_DOWN: dir_down,
    pg.K_LEFT: dir_left,
    pg.K_RIGHT: dir_right,
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
