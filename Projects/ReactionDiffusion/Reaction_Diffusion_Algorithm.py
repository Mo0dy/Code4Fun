import pygame
import numpy as np
# import numba as nb
# import pycuda
import pygame.surfarray as surfarray
from scipy.ndimage import convolve
import random


# Constants =======================================================================================
size_x = size_y = 200
laplace_mat = np.array([[0.05, 0.2, 0.05],
                        [0.2, -1, 0.2],
                        [0.05, 0.2, 0.05]])

# options are always of the shape:
# [f, k]

# import options:

my_file = open("ReactionDiffusion.txt", "r")
lines = my_file.readlines()
my_file.close()

options = {
    "coral": [0.0545, 0.062],
    "mitosis": [0.0367, 0.0649],
    "lines": [0.052999, 0.065],
    "random": [random.random() / 10, random.random() / 10]
}

for l in lines:
    opt = l.split(" ")
    options[opt[0]] = [float(opt[1]), float(opt[2])]


option = "coral"

# Setup
pygame.init()

screen = pygame.display.set_mode((size_x, size_y))
pygame.display.set_caption("ReactionDiffusion")
pxarray = surfarray.pixels3d(screen)

initscreen = pygame.Surface((size_x, size_y))
initarray = surfarray.pixels2d(initscreen)


change = 0.001


D_A = 1
D_B = 0.5

f = options[option][0]
k = options[option][1]

grid = np.array([[[1, 0, 0] for i in range(size_x)] for j in range(size_y)], dtype=float)
n_grid = np.array([[[0, 0, 0] for i in range(size_x)] for j in range(size_y)], dtype=float)


# Setup
# pygame.draw.rect(initscreen, 1, pygame.Rect(120, 120, 60, 60))
# pygame.draw.rect(initscreen, 1, pygame.Rect(10, 10, 10, 280))
# pygame.draw.rect(initscreen, 1, pygame.Rect(280, 10, 10, 280))
# pygame.draw.rect(initscreen, 1, pygame.Rect(120, 120, 60, 60))
pygame.draw.circle(initscreen, 1, (int(size_x / 2), int(size_y / 2)), 10, 1)
# pygame.draw.circle(initscreen, 1, (150, 180), 50, 1)
grid[:, :, 1] = initarray
original = 0
buffer = [grid, n_grid]




def save():
    print("name:")
    name = input()
    my_file = open("ReactionDiffusion.txt", "a")
    my_file.write(name + " " + str(f) + " " + str(k) + "\n")
    my_file.close()
    print("saved")

def command():
    global f
    global k
    print("Enter command:")
    my_in = input()
    stack = my_in.split(" ")
    com = stack[0]
    if com == "save":
        save()
    elif com == "load":
        f = options[stack[1]][0]
        k = options[stack[1]][1]
    print("done")


drawA = False
draw = False
loop = True
while loop:
    # time.sleep(0.05)
    orig = buffer[original]
    new = buffer[not original]

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            loop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                original = 0
                grid[:] = np.array([[[1, 0, 0] for i in range(size_x)] for j in range(size_y)], dtype=float)
                n_grid[:] = np.array([[[0, 0, 0] for i in range(size_x)] for j in range(size_y)], dtype=float)
                grid[:, :, 1] = initarray
                buffer = [grid, n_grid]
                # f = random.random() / 10 - 0.02
                # k = random.random() / 10 - 0.02
            elif event.key == pygame.K_RIGHT:
                k += 0.001
                print("k = " + str(k))
            elif event.key == pygame.K_LEFT:
                k -= 0.001
                print("k = " + str(k))
            elif event.key == pygame.K_UP:
                f += 0.001
                print("f = " + str(f))
            elif event.key == pygame.K_DOWN:
                f -= 0.001
                print("f = " + str(f))
            elif event.key == pygame.K_o:
                change *= 10
                print("change = " + str(change))
            elif event.key == pygame.K_l:
                change /= 10
                print("change = " + str(change))
            elif event.key == pygame.K_s:
                save()
            elif event.key == pygame.K_c:
                command()
            elif event.key == pygame.K_p:
                print("f = " + str(f) + "k = " + str(k))
            elif event.key == pygame.K_f:
                drawA = not drawA
        elif event.type == pygame.MOUSEBUTTONDOWN:
            draw = True
        elif event.type == pygame.MOUSEBUTTONUP:
            draw = False

    if draw:
        pos = pygame.mouse.get_pos()
        pos = (pos[1], pos[0])
        initscreen.fill(0)
        pygame.draw.circle(initscreen, 1, pos, 10)
        orig[:, :, 1] = np.clip(orig[:, :, 1] + initarray, 0, 0.7)


    # Updating
    new[:, :, 0] = np.clip(orig[:, :, 0] * (1 - f - np.square(orig[:, :, 1])) + f + D_A * convolve(orig[:, :, 0], laplace_mat), 0, 1)
    new[:, :, 1] = np.clip(orig[:, :, 1] * (1 - k - f + orig[:, :, 1] * orig[:, :, 0]) + D_B * convolve(orig[:, :, 1], laplace_mat), 0, 1)

    # Rendering
    if drawA:
        pxarray[:] = np.transpose(np.tile(np.multiply(new, 255)[:, :, 0], (3, 1, 1)))
    else:
        pxarray[:] = np.transpose(np.tile(np.multiply(new, 255)[:, :, 1], (3, 1, 1)))
    pygame.display.flip()
    original = not original
pygame.quit()

