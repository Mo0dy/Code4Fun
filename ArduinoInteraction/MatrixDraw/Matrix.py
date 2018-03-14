import numpy as np

class Matrix(object):
    def __init__(self, columns, rows):
        self.leds = np.zeros((columns, rows, 3))

    def set_led(self, x, y, color):
        self.leds[x, y, :] = color[:]

    def set_all(self, color):
        self.leds[:, :] = color