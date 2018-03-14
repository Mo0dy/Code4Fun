import numpy as np
import pygame as pg
from Code4Fun.ArduinoInteraction.MatrixDraw.Matrix import Matrix
from copy import deepcopy


class Animation(object):
    def __init__(self):
        self.anim = []

    def add_frame(self, matrix):
        self.anim.append(deepcopy(matrix))

    def play(self):
        for m in self.anim:
            yield m

    def clear(self):
        self.anim = []

    def save(self, path, name):
        savepath = path + "\\" + name
        print("path: " + savepath)
        for i in range(len(self.anim)):
            np.save(savepath + "_" + str(i) + ".npy", self.anim[i].leds)
        print("saved?")

    def load(self, path, name):
        loadpath = path + "\\" + name
        print("path: " + loadpath)

        self.clear()
        for i in range(len(self.anim)):
            file = np.load(loadpath + "_" + str(i) + ".npy")
            tM = Matrix(0, 0)
            tM.leds = file
            self.add_frame(tM)
        print("loaded anim")

