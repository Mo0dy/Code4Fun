from Code4Fun.Utility.Vec2 import *


# everything that can interact is an entity
class Entity(object):
    def __init__(self, pos):
        self.pos = pos
        self.angle = 0


# living entities have hp and can die
class LivingE(Entity):
    def __init__(self, pos):
        super().__init__(pos)
        self.hp = 100


class Enemy(LivingE):
    def __init__(self, pos):
        super().__init__(pos)




