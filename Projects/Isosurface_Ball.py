import pygame
import random
import numpy as np
import pygame.surfarray as surfarray

size_x = 700
size_y = 700

max_speed = 20


pygame.init()
screen = pygame.display.set_mode((size_x, size_y))
pygame.display.set_caption("Test")
pxarray = surfarray.pixels2d(screen)


x = random.random() * size_x
y = random.random() * size_y
dx = random.random() * max_speed
dy = random.random() * max_speed

x2 = random.random() * size_x
y2 = random.random() * size_y
dx2 = random.random() * max_speed
dy2 = random.random() * max_speed

sprint_tension = 0.08
sprint_tension_between = 0.01


loop = True
while loop:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            loop = False

    Fx = Fx2 = Fy = Fy2 = 0

    if x < 0:
        Fx = -x * sprint_tension
    elif x > size_x:
        Fx = (size_x - x) * sprint_tension
    if y < 0:
        Fy = -y * sprint_tension
    elif y > size_y:
        Fy = (size_y - y) * sprint_tension

    if x2 < 0:
        Fx2 = -x2 * sprint_tension
    elif x2 > size_x:
        Fx2 = (size_x - x2) * sprint_tension
    if y2 < 0:
        Fy2 = -y2 * sprint_tension
    elif y2 > size_y:
        Fy2 = (size_y - y2) * sprint_tension

    dist_x = x2 - x
    dist_y = y2 - y

    # Fx += dist_x * sprint_tension
    # Fy += dist_y * sprint_tension
    # Fx2 -= dist_x * sprint_tension
    # Fy2 -= dist_y * sprint_tension

    dx += Fx
    dy += Fy
    dx2 += Fx2
    dy2 += Fy2

    x += dx
    y += dy

    x2 += dx2
    y2 += dy2

    pxarray[:] = np.fromfunction(lambda i, j: np.minimum(np.multiply(np.divide(800000, np.add(np.square(np.subtract(i, x)), np.square(np.subtract(j, y)))), np.divide(800000, np.add(np.square(np.subtract(i, x2)), np.square(np.subtract(j, y2))))), 255), (size_x, size_x), dtype=int)
    # pxarray[:] = np.fromfunction(lambda i, j: np.minimum(np.add(np.divide(5000000, np.add(np.square(np.subtract(i, x)), np.square(np.subtract(j, y)))), np.divide(5000000, np.add(np.square(np.subtract(i, x2)), np.square(np.subtract(j, y2))))), 255), (size_x, size_x), dtype=int)
    pygame.display.flip()

pygame.quit()
