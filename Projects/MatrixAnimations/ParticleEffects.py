from Code4Fun.Utility.Vec2 import *
import numpy as np
import pygame as pg
from scipy.ndimage.filters import convolve
import time
import random


def color_linear(temp):
    temp *= 2
    if temp < 255:
        return temp, 0, 0
    elif temp < 510:
        return 255, np.clip(510 - temp, 0, 255), 0


class Particle(object):
    def __init__(self, pos):
        self.pos = pos
        self.vel = Vec2()
        self.vel.y = np.random.rand() * -1 - 2
        self.vel.x = np.random.rand() * 0.5 + 1
        self.total_lifetime = np.random.rand() * 4 + 2
        self.lifetime = 0
        self.delta_temp = 255
        self.temp = self.delta_temp

    def update(self, dt):
        self.lifetime += dt
        self.pos += self.vel * dt
        self.vel.y += 0.7 * dt
        self.update_temp()
        return self.lifetime > self.total_lifetime

    def update_temp(self):
        self.temp = self.delta_temp - self.lifetime / self.total_lifetime * self.delta_temp


def init(mat_shape):
    global last_time, particles, m_shape, origin, particle_amount
    m_shape = Vec2(mat_shape[0], mat_shape[1])
    origin = m_shape / 2
    particles = []

    particle_amount = 100


def update(content):
    while len(particles) < particle_amount:
        particles.append(Particle(Vec2(0, m_shape[1])))

    content[:, :, :] = 0
    i = 0
    while i < len(particles):
        if particles[i].update(0.1):
            del particles[i]

        else:
            draw_pos = Vec2(int(particles[i].pos.x), int(particles[i].pos.y))
            if 0 <= draw_pos.x < m_shape.x and 0 <= draw_pos.y < m_shape.y:
                content[draw_pos.x, draw_pos.y] = np.array(color_linear(particles[i].temp), dtype=np.uint8)
        i += 1


