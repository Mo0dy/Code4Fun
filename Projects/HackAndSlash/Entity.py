from Code4Fun.Utility.Vec2 import *


class Entity(object):
    def __init__(self, pos):
        self.pos = pos


class LivingE(Entity):
    def __init__(self, pos):
        super().__init__(pos)
        self.hp = 100


class Enemy(LivingE):
    def __init__(self, pos):
        super().__init__(pos)




