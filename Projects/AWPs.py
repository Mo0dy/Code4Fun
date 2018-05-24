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


p1x, p1y = 400, 400
p2x, p2y = 400, 400

c1 = 200, 50, 50
c2 = 50, 50, 200

size = 10

spring_tension = 1

# gets position returns acceleration (needs to be integrated twice)
def diff_eq(x, y, mx, my):
    dx = mx - x
    dy = my - y

    dist = np.sqrt(dx ** 2, dy ** 2)
    return dx * dist * spring_tension, dy * dist * spring_tension


def init():
    pass


def draw(dt):
    m_pos = pg.mouse.get_pos()

    # euler cromer


    screen.fill((50, 50, 50))
    pg.draw.circle(screen, c1, (int(p1x), int(p1y)), size)
    pg.draw.circle(screen, c2, (int(p2x), int(p2y)), size)


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
