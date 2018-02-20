from Code4Fun.Projects.HackAndSlash.Entity import *
import pygame as pg


class Animation(object):
    def __init__(self, anim, anim_time):
        self.anim = anim
        self.curr_sprite = 0
        self.anim_time = anim_time
        self.step_time = anim_time / len(anim)
        self.last_animation = 0

    def update(self, dt):
        self.last_animation += dt
        if self.last_animation > self.step_time:
            self.curr_sprite += 1
            if self.curr_sprite == len(self.anim):
                self.curr_sprite = 0
            self.last_animation = 0

    def get_sprite(self):
        return self.anim[self.curr_sprite]


class Player(LivingE):
    def __init__(self, pos=Vec2(0, 0)):
        super().__init__(pos)
        self.vel = Vec2()
        self.max_vel = 500
        self.animation = Animation(load_animation(r"Assets\WalkingAnimation\0", ".png"), 0.3)
        self.moving = False

    def update(self, dt):
        # scale velocity to max vel
        self.pos += self.vel.normalized() * self.max_vel * dt

        # only update animation if moving
        if self.vel:
            self.animation.update(dt)

            # set angle according to velocity:
            if self.vel.x > 0:
                if self.vel.y > 0:
                    # down right
                    self.angle = -135
                elif self.vel.y < 0:
                    # up right
                    self.angle = -45
                else:
                    # right
                    self.angle = -90
            elif self.vel.x < 0:
                if self.vel.y > 0:
                    # down left
                    self.angle = 135
                elif self.vel.y < 0:
                    # up left
                    self.angle = 45
                else:
                    # left
                    self.angle = 90
            else:
                if self.vel.y > 0:
                    # down
                    self.angle = 180
                elif self.vel.y < 0:
                    # up
                    self.angle = 0
        self.vel.zero()


    def move_right(self):
        self.vel.x = 1

    def move_left(self):
        self.vel.x = -1

    def move_up(self):
        self.vel.y = -1

    def move_down(self):
        self.vel.y = 1

    def get_sprite(self):
        return self.animation.get_sprite()


def load_animation(path, filetype):
    animation = []
    for i in range(1, 4):
        animation.append(pg.image.load(path + str(i) + filetype))
    return animation
