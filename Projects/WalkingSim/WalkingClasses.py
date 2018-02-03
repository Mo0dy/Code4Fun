from Code4Fun.Utility.Vec2 import *
import pygame as pg

DAMPENING_COEFF = 150


class Node(object):
    def __init__(self, pos, size=10, mass=0.5, color=(206, 59, 22), vel=Vec2()):
        if type(pos) == tuple:
            self.pos = Vec2(pos[0], pos[1])
        else:
            self.pos = pos
        self.mass = mass
        self.vel = vel
        self.size = size
        self.color = color
        self.forces = Vec2()
        # this dict saves connections to other objects and their relative angles
        self.connections = []

    def add_connection(self, con):
        self.connections.append(con)

    def update(self, dt):
        # update position
        if abs(self.vel) > DAMPENING_COEFF:
            self.add_force(-1 * self.vel / abs(self.vel) * DAMPENING_COEFF)
        self.vel += self.forces * (dt / self.mass)
        self.pos += self.vel * dt
        self.forces = Vec2()

    def push_forces(self):
        for other in self.connections:
            node2 = other.node
            # connection from self to node 2
            c_vec = node2.pos - self.pos
            c_length = abs(c_vec)
            c_vec *= 1 / c_length

            # is negative if spring is longer
            spring_len = (other.length - c_length) / 2

            node2.add_force(c_vec * spring_len * other.tension)

    def add_force(self, force):
        self.forces += force

    def draw(self, screen):
        for c in self.connections:
            pg.draw.line(screen, (80, 80, 80), self.pos.tuple_int, c.node.pos.tuple_int, 3)
        pg.draw.circle(screen, self.color, self.pos.tuple_int, self.size)
        # pg.draw.line(screen, (255, 255, 0), self.pos.tuple_int, (self.pos + self.forces).tuple_int)




class Connection(object):
    def __init__(self, node, length, tension=200):
        self.node = node
        self.length = length
        self.tension = tension


def apply_connection(node1, node2, length):
    node1.add_connection(Connection(node2, length))
    node2.add_connection(Connection(node1, length))


