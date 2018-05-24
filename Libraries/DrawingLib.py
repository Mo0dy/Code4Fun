import pygame as pg

pg.init()

background_color = 50, 50, 50
refresh_rate = 60


def run(draw_func, screen_size):
    clock = pg.time.Clock()
    screen = pg.display.set_mode(screen_size)
    loop = True
    while loop:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                loop = False

        clock.tick(refresh_rate)
        screen.fill(background_color)
        draw_func(screen, clock.get_time())
        pg.display.flip()
