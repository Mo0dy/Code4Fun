import numpy as np
import pygame as pg
import sys
from Code4Fun.Utility.Vec2 import Vec2

background_color = 50, 50, 50
window_size = 800, 800
fps_cap = 10

pg.init()
screen = pg.display.set_mode(window_size)
pg.display.set_caption("Smart Rockets")
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms", 20)


resolution = 1000

flowers = []


class Flower(object):
    def __init__(self):
        self.center = Vec2(np.random.random_integers(20, 780), 750)
        self.size = 1
        self.center_percent = 0.5
        self.max_size = np.random.random_integers(10, 30)

        self.height_mod = np.random.random_integers(10000, 100000)

    def draw(self, screen):

        height = 750 - (self.size * self.height_mod) ** 0.4

        self.center.y = height

        theta = 0
        polygon = []
        for i in range(1000):
            vec = Vec2(1, 0)
            theta = np.pi * 2 * i / resolution
            vec.theta = theta
            vec *= (np.sin(theta * 10) + 1.3) * (self.size ** 1.1)
            polygon.append((vec + self.center).tuple_int)

        pg.draw.polygon(screen, (255, 0, 0), polygon)
        pg.draw.lines(screen, (100, 0, 0), True, polygon, 3)

        pg.draw.circle(screen, (255, 255, 0), self.center.tuple_int, (int)((self.size * self.center_percent) ** 0.8) + 5)

    def grow(self):
        self.size += 1
        if self.size > self.max_size:
            self.size = self.max_size


flower = Flower()


def init():
    pass


def draw(dt):
    for f in flowers:
        f.draw(screen)
        f.grow()

    if np.random.random() > 0.5:
        flowers.append(Flower())


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
