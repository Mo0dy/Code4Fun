from Code4Fun.Libraries.DrawingLib import *
import numpy as np


NUM_ROCKETS = 50
GEN_LENGTH = 500


# starts with random rockets. they can turn left or right. if the genome is 1 it means they turn right else they turn left

rockets = np.random.random_integers(0, 1, NUM_ROCKETS * GEN_LENGTH).reshape((NUM_ROCKETS, GEN_LENGTH))
print(rockets)


def draw(screen, dt):
    pass


run(draw, (800, 800))


