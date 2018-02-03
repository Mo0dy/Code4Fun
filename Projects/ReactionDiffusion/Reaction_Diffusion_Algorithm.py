import pygame
import numpy as np
import pygame.surfarray as surfarray
from numba import jit, vectorize, guvectorize, float64, complex64, int32, float32, int64
import random
import time
import Code4Fun.Utility.Renderer as rnd


# Constants =======================================================================================
size_x = size_y = 200
laplace_mat = np.array([[0.05, 0.2, 0.05],
                        [0.2, -1, 0.2],
                        [0.05, 0.2, 0.05]], dtype=np.float32)

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


D_A = float32(1)
D_B = float32(0.5)

f = float32(options[option][0])
k = float32(options[option][1])

grid = np.array([[[1, 0, 0] for i in range(size_x)] for j in range(size_y)], dtype=np.float32)
n_grid = np.array([[[0, 0, 0] for i in range(size_x)] for j in range(size_y)], dtype=np.float32)


# Setup
pygame.draw.circle(initscreen, 1, (int(size_x / 2), int(size_y / 2)), 10, 1)
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


@guvectorize([(float32[:, :, :], float32[:, :], float32, float32, float32, float32, float32[:, :, :])], '(x,y,z),(a,a),(),(),(),()->(x,y,z)', target='parallel', nopython=True)
def update(original_a, lap_mat, kill, feed, Da, Db, new_a):
    for i in range(original_a.shape[0] - 2):
        for j in range(original_a.shape[1] - 2):
            ii = i + 1
            jj = j + 1
            sumA = 0
            sumB = 0
            for a in range():
                for b in range(3):
                    sumA += original_a[i + a, j + b, 0] * lap_mat[a, b]
                    sumB += original_a[i + a, j + b, 1] * lap_mat[a, b]
            new_a[ii, jj, 0] = original_a[ii, jj, 0] * (1 - feed - original_a[ii, jj, 1] * original_a[ii, jj, 1]) + feed + Da * sumA
            new_a[ii, jj, 1] = original_a[ii, jj, 1] * (1 - kill - feed + original_a[ii, jj, 1] * original_a[ii, jj, 0]) + Db * sumB

            if new_a[ii, jj, 0] > 1:
                new_a[ii, jj, 0] = 1
            elif new_a[ii, jj, 0] < 0:
                new_a[ii, jj, 0] = 0

            if new_a[ii, jj, 1] > 1:
                new_a[ii, jj, 1] = 1
            elif new_a[ii, jj, 1] < 0:
                new_a[ii, jj, 1] = 0

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
    start_time = time.time()
    update(orig, laplace_mat, k, f, D_A, D_B, new)

    # Rendering
    if drawA:
        pxarray[:] = np.transpose(np.tile(np.multiply(new, 255)[:, :, 0], (3, 1, 1)))
    else:
        pxarray[:] = np.transpose(np.tile(np.multiply(new, 255)[:, :, 1], (3, 1, 1)))
    pygame.display.flip()
    original = not original
pygame.quit()

