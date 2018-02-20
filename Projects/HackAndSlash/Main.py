# rendering
from Code4Fun.Utility.Vec2 import *
from Code4Fun.Projects.HackAndSlash.Game import *
import numpy as np
import pygame as pg

background_color = 50, 50, 50
window_size = 800, 800


# pygame stuff
pg.init()
origin = Vec2(np.array(window_size)) / 2
screen = pg.display.set_mode(window_size)
pg.display.set_caption("test")
clock = pg.time.Clock()
font = pg.font.SysFont("comicsansms", 20)


# game stuff
game = Game()


def reset():
    pass


def update(dt):
    game.update(dt)


def draw():
    global game
    player_surf = pg.transform.rotate(pg.transform.scale(game.player.get_sprite(), (100, 100)), game.player.angle)
    screen.blit(player_surf, (game.player.pos - Vec2(player_surf.get_size()) / 2).tuple_int)
    # pg.draw.circle(screen, (200, 200, 150), game.player.pos.tuple_int, 20)

    text = font.render("%0.2f" % clock.get_fps(), True, (255, 255, 255))
    screen.blit(text, (10, 10))


keydown_func = {
    pg.K_r: reset,
}

keypressed_func = {
    pg.K_w: game.move_player_up,
    pg.K_s: game.move_player_down,
    pg.K_a: game.move_player_left,
    pg.K_d: game.move_player_right,
}


pressed_keys = set()


reset()
loop = True
while loop:
    clock.tick(60)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False
        elif e.type == pg.KEYDOWN:
            pressed_keys.add(e.key)
            try:
                keydown_func[e.key]()
            except:
                pass
        elif e.type == pg.KEYUP:
            pressed_keys.remove(e.key)

    for e in pressed_keys:
        try:
            keypressed_func[e]()
        except:
            pass

    update(clock.get_time() / 1000)
    screen.fill(background_color)
    draw()
    pg.display.flip()
pg.quit()
