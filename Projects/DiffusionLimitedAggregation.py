import pygame
import random
import numpy as np


tree_save_path = r"ReactionDiffusion\tree.txt"
walkers_save_path = r"ReactionDiffusion\walkers.txt"


pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

size = [600, 600]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Diffusion Limited Aggregation")


walker_vel = 2
walker_color = (255, 255, 255)
walker_size = 4

border_dist = 100
border_x_min = size[0] / 2 - border_dist
border_x_max = size[0] / 2 + border_dist
border_y_min = size[1] / 2 - border_dist
border_y_max = size[1] / 2 + border_dist


class Walker(object):
    def __init__(self, **kwargs):
        # starting position is on the edge of the screen
        edge_len = size[0] * 2 + size[1] * 2
        ran_pos = int(random.random() * edge_len + 1)
        self.update_iteration = 0
        self.min_dist = 0
        if ran_pos < size[0]:
            self.x = ran_pos
            self.y = 0
        elif ran_pos < size[0] * 2:
            self.x = ran_pos - size[0]
            self.y = size[1]
        elif ran_pos < size[0] * 2 + size[1]:
            self.x = 0
            self.y = ran_pos - size[0] * 2
        else:
            self.x = size[0]
            self.y = ran_pos - size[0] * 2 - size[1]

        if "x" in kwargs:
            self.x = kwargs["x"]
        if "y" in kwargs:
            self.y = kwargs["y"]

        if "pos" in kwargs:
            self.pos = kwargs["pos"]

    @property
    def pos(self):
        return [self.x, self.y]

    @pos.setter
    def pos(self, other):
        self.x = other[0]
        self.y = other[1]


class Tree(object):
    def __init__(self):
        self.walkers = []
        self.color = (255, 0, 0)

    def draw(self):
        global screen
        for w in self.walkers:
            pygame.draw.circle(screen, self.color, (int(w.x), int(w.y)), walker_size)

    def init(self):
        self.walkers.append(Walker(pos=np.array(size) / 2))


walkers = []
tree = Tree()


def draw():
    global walkers
    global tree
    screen.fill((0, 0, 0))
    for w in walkers:
        pygame.draw.circle(screen, walker_color, (int(w.x), int(w.y)), walker_size)
    tree.draw()
    pygame.display.flip()


# load from file
try:
    coordinates = np.loadtxt(walkers_save_path)
    for c in coordinates:
        walkers.append(Walker(pos=c))
except:
    pass

try:
    coordinates = np.loadtxt(tree_save_path)
    for c in coordinates:
        tree.walkers.append(Walker(pos=c))
except:
    tree.init()

dw = 30 - len(walkers)
for i in range(dw):
    walkers.append(Walker())


iterator = 0

my_loop = True
while my_loop:
    # update
    # time.sleep()

    # event handling
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            my_loop = False

    for w in walkers:
        v_x = (random.random() - 0.5) * walker_vel
        v_y = (random.random() - 0.5) * walker_vel
        n_x = w.x + v_x
        n_y = w.y + v_y

        if border_x_min < n_x < border_x_max or (border_x_min > n_x and v_x > 0) or (border_x_max < n_x and v_x < 0):
            w.x = n_x

        if border_y_min < n_y < border_y_max or (border_y_min > n_y and v_y > 0) or (border_y_max < n_y and v_y < 0):
            w.y = n_y

        if w.update_iteration <= iterator:
            # print("Checking")
            # check collision
            w.min_dist = 100000
            for t_w in tree.walkers:
                d_vx = t_w.x - w.x
                d_vy = t_w.y - w.y

                dist_squared = d_vx ** 2 + d_vy ** 2

                if dist_squared < w.min_dist:
                    if dist_squared < 64:
                        # update borders
                        if w.x + border_dist > border_x_max:
                            border_x_max = w.x + border_dist
                        elif w.x - border_dist < border_x_min:
                            border_x_min = w.x - border_dist

                        if w.y + border_dist > border_y_max:
                            border_y_max = w.y + border_dist
                        elif w.y - border_dist < border_y_min:
                            border_y_min = w.y - border_dist

                        # put walker in tree
                        tree.walkers.append(w)
                        walkers.remove(w)
                        walkers.append(Walker())
                        for w in walkers:
                            w.update_iteration = iterator
                        break
                    else:
                        w.min_dist = dist_squared
                        min_reach_dist = int(dist_squared / 8)
                        w.update_iteration = iterator + min_reach_dist

                # next test is either if a walker connects or it it could possibly reach

    if iterator % 50 == 0:
        draw()
    iterator += 1


# save to file
points = np.array(np.zeros((len(tree.walkers), 2)))
for i in range(len(tree.walkers)):
    points[i] = tree.walkers[i].pos
np.savetxt(tree_save_path, points)

points = np.array(np.zeros((len(walkers), 2)))
for i in range(len(walkers)):
    points[i] = walkers[i].pos
np.savetxt(walkers_save_path, points)
