import pygame
import random
import numpy as np
import pygame.surfarray as surfarray
import time


size_x = 700
size_y = 700

pygame.init()
screen = pygame.display.set_mode((size_x, size_y))
pygame.display.set_caption("Test")
pxarray = surfarray.pixels2d(screen)

fun_dict = {
    "small_circles": lambda i, j,: 50 ** np.sin(j * i),
    "waves_horizontal": lambda i, j: (np.sin(i * 0.01 + time.time()) + 1),
    "waves_vertical": lambda i, j: (np.sin(j * 0.01 + time.time()) + 1),
    "test": lambda i, j: (i + j) / 1000
}

functions = [
    "small_circles"
]

def multiply(stack):
    first = stack.pop()
    second = stack.pop()
    stack.append(first * second)

def add(stack):
    first = stack.pop()
    second = stack.pop()
    stack.append(first + second)

def func(i, j):
    stack = []
    for f in functions:
        try:
            float(f)
            stack.append(float(f))
        except:
            if f == "*":
                multiply(stack)
            elif f == "+":
                add(stack)
            elif f == "-i":
                i = -i
            elif f == "-j":
                j = -j
            else:
                stack.append(fun_dict[f](i, j))
    return stack[0] * 255

loop = True
while loop:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            loop = False

    pxarray[:] = np.clip(np.fromfunction(func, (size_x, size_y), dtype=int), 0, 255)
    pygame.display.flip()

pygame.quit()
