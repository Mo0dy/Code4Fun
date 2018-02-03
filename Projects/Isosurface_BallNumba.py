import pygame
import random
import numpy as np
import pygame.surfarray as surfarray
from numba import jit, vectorize, guvectorize, float64, complex64, int32, float32, int64

size_x = 1200
size_y = 700

max_speed = 20


pygame.init()
screen = pygame.display.set_mode((size_x, size_y))
pygame.display.set_caption("Test")
pxarray = surfarray.pixels2d(screen)

balls_amount = 3
dt = 0.5

spring_tension = 0.08
spring_tension_between = 1

c_arr = np.empty((size_x, size_y), dtype=np.float32)


def init():
    global balls, velocities, forces
    balls = np.array([[random.random() * size_x, random.random() * size_y] for _ in range(balls_amount)], dtype=np.float32)
    velocities = np.array([[random.random() * max_speed, random.random() * max_speed] for _ in range(balls_amount)], dtype=np.float32)
    forces = np.zeros(velocities.shape)


@guvectorize([(float32[:, :], float32[:, :])], '(a,b),(c,d)', target='parallel', nopython=True)
def update(passed_balls, output):
    for i in range(output.shape[0]):
        for j in range(output.shape[1]):
            my_sum = 0
            for a in range(passed_balls.shape[0]):
                my_sum += 8000 / ((i - passed_balls[a, 0]) ** 2 + (j - passed_balls[a, 1]) ** 2) ** 0.5
            if my_sum > 255:
                my_sum = 255
            output[i, j] = my_sum


init()
loop = True
while loop:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            loop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                init()

    for i in range(balls.shape[0]):
        x, y = balls[i, 0], balls[i, 1]
        if x < 0:
            forces[i, 0] = -x * spring_tension
        elif x > size_x:
            forces[i, 0] = (size_x - x) * spring_tension
        if y < 0:
            forces[i, 1] = -y * spring_tension
        elif y > size_y:
            forces[i, 1] = (size_y - y) * spring_tension

    for i in range(balls.shape[0]):
        j = i + 1
        while j < balls.shape[0]:
            dx = balls[i, 0] - balls[j, 0]
            dy = balls[i, 1] - balls[j, 1]
            dist_sqared = dx ** 2 + dy ** 2
            forces[i, 0] -= dx / dist_sqared * spring_tension_between
            forces[i, 1] -= dy / dist_sqared * spring_tension_between
            forces[j, 0] += dx / dist_sqared * spring_tension_between
            forces[j, 1] += dy / dist_sqared * spring_tension_between
            j += 1


    velocities += forces * dt
    balls += velocities * dt
    forces[:, :] = 0

    update(balls, c_arr)
    pxarray[:] = c_arr
    pygame.display.flip()

pygame.quit()
