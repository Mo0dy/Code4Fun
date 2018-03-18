import numpy as np
import pygame as pg
import sys
from Code4Fun.Utility.Line import *

background_color = 50, 50, 50
window_size = 800, 800
fps_cap = 60


pg.init()
screen = pg.display.set_mode(window_size)
pg.display.set_caption("Smart Rockets")
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms", 20)

num_points = 10000
point_size = 2
margin = 20

num_partitions = 5
partitions = []
mean_rect_size = 10


# fortunes algorithm
def fortunes(sites):
    type_site = 0
    type_circle = 1


    class Event(object):
        def __init__(self, type, content):
            self.type = type
            self.content = content

    # get event with lowest y value
    def get_first_event(q):
        e = q[0]
        for i in range(1, len(q)):
            if q[i].y < e.y:
                e = q[i]
        return e

    def add_parabola(point):
        pass

    def remove_parabola(parabola):
        pass

    queue = []
    for s in sites:
        queue.append(Event(type_site, s))

    while len(queue) > 0:
        e = get_first_event(queue)
        if e.type == type_site:
            add_parabola(e.content)
        else:
            remove_parabola(e.content)


# k-means algorithm
def update():
    global means
    # calculate new means
    for i in range(num_partitions):
        # the sum of all points in x and y direction
        means[i] = np.sum(partitions[i], axis=0) / partitions[i].shape[0]


def assignment():
    global partitions
    squared_distances = np.zeros((num_partitions, num_points))

    # calculate the squared distances from points to means
    for i in range(num_partitions):
        squared_distances[i, :] = np.sum((points[:] - means[i]) ** 2, axis=1)

    # the index of the minimum argument
    minimum_mean = np.argmin(squared_distances, axis=0)
    partitions = []
    for i in range(num_partitions):
        partitions.append(points[minimum_mean == i])


def init():
    global points, means, colors
    # saves the x and y coordinates of the points
    points = np.random.rand(num_points, 2)
    # scales the random values to be between 0 and window size with margins

    points[:, 0] = points[:, 0] * (window_size[0] - 2 * margin) + margin
    points[:, 1] = points[:, 1] * (window_size[0] - 2 * margin) + margin

    # the means store the means of the partitions
    means = np.random.rand(num_partitions, 2)
    means[:, 0] = means[:, 0] * (window_size[0] - 2 * margin) + margin
    means[:, 1] = means[:, 1] * (window_size[0] - 2 * margin) + margin

    # assign color to partitions (picked with hue values to increase contrast)
    colors = []
    for i in range(num_partitions):
        c = pg.Color(0, 0, 0, 0)
        c.hsla = ((i + 1) / num_partitions * 360, 80, 50, 100)
        colors.append(c)


def draw(dt):
    # draw means as squares:
    for i in range(num_partitions):
        pg.draw.rect(screen, colors[i], (means[i, 0] - mean_rect_size / 2, means[i, 1] - mean_rect_size / 2, mean_rect_size, mean_rect_size))

    # draw points
    for j in range(num_partitions):
        for i in range(partitions[j].shape[0]):
            pg.draw.circle(screen, colors[j], partitions[j][i].astype(int), point_size)

    # draw lines
    # for l in lines:
    #     pg.draw.line(screen, (255, 255, 255), l.p1.tuple_int, l.p2.tuple_int, 10)


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

    assignment()
    update()

    screen.fill(background_color)
    draw(clock.get_time() / 1000)
    text = font.render("%0.2f" % clock.get_fps(), True, (255, 255, 255))
    screen.blit(text, (10, 10))
    pg.display.flip()
pg.quit()
