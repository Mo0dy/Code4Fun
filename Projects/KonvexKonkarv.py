from Code4Fun.Utility.Vec2 import *
import pygame
import random
import time
import math
from copy import deepcopy

size = [600, 600]

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("KonvexKonkarv")


BLACK = (0, 0, 0)


class Polygon(object):
    def __init__(self, n_vertices):
        self.vertices = []
        self.center = Vec2(300, 300)
        partials = [random.random() for i in range(n_vertices)]
        my_sum = sum(partials)
        partials = [v / my_sum * 2 * math.pi for v in partials]
        angles = [partials[0]]
        for i in range(len(partials) - 1):
            angles.append(angles[i] + partials[i + 1])

        for angle in angles:
            vec = Vec2(random.random() * 150 + 50, 0)
            vec.theta = angle
            self.vertices.append(vec + self.center)


def draw_poly(poly, **kwargs):
    if "color" in kwargs:
        color = kwargs["color"]
    else:
        color = (255, 255, 255)
    # screen.fill((0, 0, 0))
    for i in range(len(poly.vertices) - 1):
        v1 = poly.vertices[i]
        v2 = poly.vertices[i + 1]
        pygame.draw.line(screen, color, (int(v1.x), int(v1.y)), (int(v2.x), int(v2.y)), 2)
    pygame.draw.line(screen, color, (int(poly.vertices[0].x), int(poly.vertices[0].y)), (int(poly.vertices[len(poly.vertices) - 1].x), int(poly.vertices[len(poly.vertices) - 1].y)), 2)
    # pygame.display.flip()


def intersection(p1, v1, p2, v2):
    # check for linear dependency
    if v1.x / v2.x * v2.y == v1.y:
        return None

    # if p1 + a * v1 = p2 + b * v2 then
    b = (v1.y * (p2.x - p1.x) - v1.x * (p2.y - p1.y)) / (v2.y * v1.x - v2.x * v1.y)
    i_p = p2 + v2 * b

    # screen.fill(BLACK)
    # draw_poly(polygon)
    # pygame.draw.line(screen, (0, 255, 255), p1.tuple_int, (p1 + v1).tuple_int, 2)
    # pygame.draw.line(screen, (0, 255, 0), p2.tuple_int, (p2 + v2).tuple_int, 2)
    # pygame.draw.circle(screen, (255, 255, 0), i_p.tuple_int, 10)
    # pygame.display.flip()
    # time.sleep(5)

    return i_p




def konvex_poly(orig_poly):
    global polygon
    poly2 = deepcopy(orig_poly)
    poly = deepcopy(orig_poly)
    vertices = poly.vertices

    i = 0

    redo = True
    for i in range(10):
        my_range = len(vertices) - 2
        redo = False
        while i < my_range:
            v1 = vertices[i]
            v2 = vertices[i + 1]
            v3 = vertices[i + 2]

            i_p = intersection(v1, v1 - v3, poly.center, v2 - poly.center)

            # screen.fill(BLACK)
            # pygame.draw.circle(screen, (255, 0, 0), v1.tuple_int, 5)
            # pygame.draw.circle(screen, (0, 255, 0), v2.tuple_int, 5)
            # pygame.draw.circle(screen, (0, 0, 255), v3.tuple_int, 5)
            # pygame.draw.circle(screen, (0, 255, 255), i_p.tuple_int, 5)
            # draw_poly(poly2)
            # draw_poly(poly, color=(255, 0, 0))
            # pygame.display.flip()
            # time.sleep(3)

            if abs(i_p - poly.center) >= abs(v2 - poly.center):
                del poly.vertices[i + 1]
                my_range -= 1
                i -= 1
            i += 1

        v1 = vertices[-1]
        v2 = vertices[0]
        v3 = vertices[1]

        i_p = intersection(v1, v1 - v3, poly.center, v2 - poly.center)
        if abs(i_p - poly.center) >= abs(v2 - poly.center):
            del poly.vertices[0]
    return poly




polygon = Polygon(80)
kon_poly = konvex_poly(polygon)

loop = True
while loop:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            loop = False

    screen.fill(BLACK)
    draw_poly(polygon)
    draw_poly(kon_poly, color=(255, 255, 0))
    pygame.display.flip()