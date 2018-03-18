import pygame as pg


# yields colors that are visually different
def different_colors(amount, saturation, lightness):
    for i in range(amount):
        c = pg.Color(0, 0, 0, 0)
        c.hsla = ((i + 1) / amount * 360, saturation, lightness, 100)
        yield c



