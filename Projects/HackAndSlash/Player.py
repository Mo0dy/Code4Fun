from Code4Fun.Projects.HackAndSlash.Entity import *
import Code4Fun.Projects.HackAndSlash.Animation as Anim
import pygame as pg


class Player(LivingE):
    def __init__(self, pos=Vec2(0, 0)):
        super().__init__(pos)
        self.vel = Vec2()
        self.max_vel = 500
        self.leg_anim = Anim.Anim(Anim.load_animation(r"Assets\WalkingAnimation", ".png", 4), 0.3)
        self.body_anim = Anim.Anim(Anim.load_animation(r"Assets\BodyAnimation\Idle", ".png", 3), 1)
        self.body_anim.reflect = True
        self.moving = False
        self.leg_angle = 0
        self.body_angle = 0

    def update(self, dt):
        # scale velocity to max vel
        self.pos += self.vel.normalized() * self.max_vel * dt

        # aim_to_mouse:
        self.body_angle = np.degrees((self.pos - Vec2(pg.mouse.get_pos())).theta)

        # only update animation if moving
        self.body_anim.update(dt)
        if self.vel:
            self.leg_anim.update(dt)
            self.body_anim.set_anim_time(0.2)

            # set angle according to velocity:
            if self.vel.x > 0:
                if self.vel.y > 0:
                    # down right
                    self.leg_angle = -135
                elif self.vel.y < 0:
                    # up right
                    self.leg_angle = -45
                else:
                    # right
                    self.leg_angle = -90
            elif self.vel.x < 0:
                if self.vel.y > 0:
                    # down left
                    self.leg_angle = 135
                elif self.vel.y < 0:
                    # up left
                    self.leg_angle = 45
                else:
                    # left
                    self.leg_angle = 90
            else:
                if self.vel.y > 0:
                    # down
                    self.leg_angle = 180
                elif self.vel.y < 0:
                    # up
                    self.leg_angle = 0
        else:
            self.body_anim.set_anim_time(0.8)
        self.vel.zero()

    def move_right(self):
        self.vel.x = 1

    def move_left(self):
        self.vel.x = -1

    def move_up(self):
        self.vel.y = -1

    def move_down(self):
        self.vel.y = 1

    def get_surf(self):
        leg_surf = pg.transform.rotate(pg.transform.scale(self.leg_anim.get_sprite(), (100, 100)), self.leg_angle)
        body_surf = pg.transform.rotate(pg.transform.scale(self.body_anim.get_sprite(), (150, 150)), self.body_angle)

        ret_surf = pg.Surface((300, 300), pg.SRCALPHA)
        ret_surf.blit(leg_surf, (150 - leg_surf.get_size()[0] / 2, 150 - leg_surf.get_size()[1] / 2))
        ret_surf.blit(body_surf, (150 - body_surf.get_size()[0] / 2, 150 - body_surf.get_size()[1] / 2))

        return ret_surf
