import numpy as np
import MyMaths as math
import pygame as pg

DAMPENING_COEFF = 100


class Node(object):
    def __init__(self, pos, size=10, mass=50, color=(206, 59, 22), vel=math.Vec2()):
        if type(pos) == tuple:
            self.pos = math.Vec2(pos[0], pos[1])
        else:
            self.pos = pos
        self.mass = mass
        self.vel = vel
        self.size = size
        self.color = color
        self.forces = math.Vec2()
        # this dict saves connections to other objects and their relative angles
        self.connections = []

    def add_connection(self, con):
        self.connections.append(con)

    def update(self, dt):
        # update position
        self.vel += self.forces * (dt / self.mass)
        self.pos += self.vel * dt
        self.forces = math.Vec2()
        self.push_forces()

    def push_forces(self):
        for other in self.connections:
            node2 = other.node
            length = other.length
            tention = other.tention

            # connection from self to node 2
            c_vec = node2.pos - self.pos
            c_length = abs(c_vec)
            c_vec *= 1 / c_length

            # is negative if spring is longer
            spring_len = length - c_length

            spring_force = c_vec * spring_len * tention
            damping_force = node2.vel * DAMPENING_COEFF
            node2.add_force(spring_force - damping_force)


    def add_force(self, force):
        self.forces += force

    def draw(self, screen):
        for c in self.connections:
            pg.draw.line(screen, (80, 80, 80), self.pos.tuple_int, c.node.pos.tuple_int, 3)
        pg.draw.circle(screen, self.color, self.pos.tuple_int, self.size)


class Connection(object):
    def __init__(self, node, length, tention=1e5):
        self.node = node
        self.tention = tention
        self.length = length


def apply_connection(node1, node2, length):
    node1.add_connection(Connection(node2, length))
    node2.add_connection(Connection(node1, length))


