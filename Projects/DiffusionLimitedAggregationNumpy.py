import pygame
import numpy as np
from numba import jit, vectorize, guvectorize, float64, complex64, int32, float32, int64
from time import sleep

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

square_size = 600
size = [square_size, square_size]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Diffusion Limited Aggregation")


walker_vel = 3
walker_color = (255, 255, 255)
walker_size = 4
walker_size_squared = np.float32(walker_size * walker_size * 4)

border_dist = 100
border_x_min = size[0] / 2 - border_dist
border_x_max = size[0] / 2 + border_dist
border_y_min = size[1] / 2 - border_dist
border_y_max = size[1] / 2 + border_dist


walker_amount = 30


def new_walker():
    edge_len = size[0] * 2 + size[1] * 2
    ran_pos = np.random.random_integers(0, edge_len)
    if ran_pos < size[0]:
        x = ran_pos
        y = 0
    elif ran_pos < size[0] * 2:
        x = ran_pos - size[0]
        y = size[1]
    elif ran_pos < size[0] * 2 + size[1]:
        x = 0
        y = ran_pos - size[0] * 2
    else:
        x = size[0]
        y = ran_pos - size[0] * 2 - size[1]
    return [x, y]


walkers = np.array([new_walker() for i in range(walker_amount)], dtype=np.float32)
tree = np.array([[square_size / 2, square_size / 2]], dtype=np.float32)
dists = np.zeros(walkers.shape[0], dtype=np.float32)
touching = np.zeros(walkers.shape[0], dtype=np.float32)


@guvectorize([(float32[:, :], float32[:, :], float32, float32, float32[:], float32[:])], '(a,b),(c,d),(),(),(a)->(a)', target='parallel')
def check_touching(_walkers, _tree, _w_size, _w_speed, _dists, output):
    _w_size_squared = _w_size ** 2 * 4
    for i in range(_walkers.shape[0]):
        _dists[i] -= _w_speed
        output[i] = 0
        if _dists[i] <= 0:
            mindist = 10000
            for j in range(_tree.shape[0]):
                # this stepdist leaves more room then it has to
                stepdist = np.absolute(_walkers[i, 0] - _tree[j, 0]) + np.absolute(_walkers[i, 1] - _tree[j, 1])
                if stepdist < mindist:
                    mindist = stepdist
                    dist_squared = (_walkers[i, 0] - _tree[j, 0]) ** 2 + (_walkers[i, 1] - _tree[j, 1]) ** 2
                    if _w_size_squared > dist_squared:
                        output[i] = 1
            _dists[i] = mindist - 2 * _w_size


iterator = 0
loop = True
while loop:
    # sleep(0.01)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            loop = False

    # Do a random Step
    steps = (np.random.rand(walker_amount, 2) - 0.5) * 2 * walker_vel
    walkers = np.add(walkers, steps)

    # bound the walkers
    walkers = np.clip(walkers, np.minimum(border_y_min, border_x_min), np.minimum(border_y_max, border_x_max))
    touching = check_touching(walkers.astype(np.float32), tree.astype(np.float32), walker_size, walker_vel, dists)
    touching = touching.astype(np.bool)

    tree = np.append(tree, walkers[touching], axis=0)
    walkers = walkers[np.logical_not(touching)]
    if walkers.shape[0] < walker_amount:
        new_walkers = np.array([new_walker() for i in range(walker_amount - walkers.shape[0])])
        walkers = np.append(walkers, new_walkers, axis=0)
        border_x_max = np.max(tree[:, 0]) + border_dist
        border_x_min = np.min(tree[:, 0]) - border_dist
        border_y_max = np.max(tree[:, 1]) + border_dist
        border_y_min = np.min(tree[:, 1]) - border_dist

    if iterator % 200 == 0:
        # Display
        screen.fill(0)
        # Walkers
        walkers_int = np.array(walkers, dtype=int)
        tree_int = np.array(tree, dtype=int) # this doesn't have to be done very update
        for w in walkers_int:
            pygame.draw.circle(screen, 255, tuple(w), walker_size)
        for w in tree_int:
            pygame.draw.circle(screen, (255, 0, 0), tuple(w), walker_size)

        pygame.display.flip()

    iterator += 1
pygame.quit()