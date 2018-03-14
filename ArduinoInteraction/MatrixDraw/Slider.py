import pygame as pg


pg.font.init()
font = pg.font.SysFont("arialblack", 120)


# slider that can select values between 0 and 255
class Slider(object):
    def __init__(self, color, x, y, dx, dy):
        self.color = color
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.value = 255
        self.selected = False

    def draw(self, screen):
        draw_dx = int(self.value / 255 * self.dx)

        pg.draw.rect(screen, self.color, (self.x, self.y, draw_dx, self.dy))
        pg.draw.rect(screen, (40, 40, 40), (self.x, self.y, self.dx, self.dy), 10)
        text = font.render(str(self.value), True, pg.Color(self.color[0], self.color[1], self.color[2]).correct_gamma(2))
        screen.blit(text, (self.x + 30, self.y + 10))

    def collision(self, pos):
        return self.x < pos[0] < self.x + self.dx and self.y < pos[1] < self.y + self.dy

    def update(self, m_pos):
        if self.selected:
            self.value = int((m_pos[0] - self.x) / self.dx * 255)
            self.clip_value()

    def clip_value(self):
        if self.value > 255:
            self.value = 255
        elif self.value < 0:
            self.value = 0

    def lower_value(self):
        self.value -= 5
        if self.value < 0:
            self.value = 0
        return self.value

    def raise_value(self):
        self.value += 5
        if self.value > 255:
            self.value = 255
        return self.value