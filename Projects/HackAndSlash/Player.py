from Code4Fun.Projects.HackAndSlash.Entity import *


class Player(LivingE):
    def __init__(self, pos=Vec2(0, 0)):
        super().__init__(pos)
        self.vel = 1

    def move_right(self):
        self.pos.x += self.vel

    def move_left(self):
        self.pos.x -= self.vel

    def move_up(self):
        self.pos.y -= self.vel

    def move_down(self):
        self.pos.y += self.vel


