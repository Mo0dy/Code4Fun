import pygame as pg


class Anim(object):
    def __init__(self, anim, anim_time):
        self.anim = anim
        self.curr_sprite = 0
        self.step_time = anim_time / len(anim)
        self.last_animation = 0

        # determines if the animation begins from the front or runs backwards
        self.reflect = False
        # iterate rightwards through the array
        self.dir = 1

    def update(self, dt):
        self.last_animation += dt
        if self.last_animation > self.step_time:
            self.curr_sprite += self.dir
            if self.reflect:
                if self.curr_sprite == len(self.anim) or self.curr_sprite < 0:
                    self.dir *= -1
                    self.curr_sprite += self.dir
            if not self.reflect:
                if self.curr_sprite == len(self.anim):
                    self.curr_sprite = 0
            self.last_animation = 0

    def get_sprite(self):
        return self.anim[self.curr_sprite]

    def set_anim_time(self, anim_time):
        self.step_time = anim_time / len(self.anim)


def load_animation(path, filetype, amount):
    anim = []
    for i in range(1, amount + 1):
        anim.append(pg.image.load(path + "\\" + str(i) + filetype))
    return anim