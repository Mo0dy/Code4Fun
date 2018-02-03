from MyMaths import *
import math
import sys
import pygame
import time
import TimeTest
import random


pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

size = [600, 600]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Diffusion Limited Aggregation Viewer")


walker_color = (255, 255, 255)
walker_size = 4


tree = []
try:
    # importing tree from file
    file = open("tree.txt", "r")
    lines = file.readlines()
    file.close()

    for line in lines:
        coordinates = line.split(" ")
        coordinates[1] = coordinates[1].replace("\n", "")
        pos = Vec2(int(float(coordinates[0])), int(float(coordinates[1])))
        tree.append(pos)
except:
    pass


def draw():
    global tree
    screen.fill((0, 0, 0))
    for w in tree:
        color_array = [0, 0, 0]

        # color manipulation
        dist = abs(w - Vec2(300, 300))
        color_array[0] = dist / 300 * 255
        color_array[1] = (300 - dist) / 300 * 255

        color_array = [int(j) for j in color_array]

        for i in range(len(color_array)):
            if color_array[i] > 255:
                color_array[i] = 255
            elif color_array[i] < 0:
                color_array[i] = 0

        color = tuple(color_array)
        pygame.draw.circle(screen, color, tuple(w), walker_size)
    pygame.display.flip()


my_loop = True
while my_loop:
    # event handling
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            my_loop = False

    draw()
