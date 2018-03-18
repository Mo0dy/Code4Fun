# game logic
from Code4Fun.Projects.HackAndSlash.Player import *
from Code4Fun.Projects.HackAndSlash.Entity import *
from Code4Fun.Projects.HackAndSlash.Terrain import Terrain


class Game(object):
    def __init__(self):
        self.player = Player()
        self.terrain = Terrain(100, 100)

    def reset(self):
        self.terrain = Terrain(100, 100)

    def update(self, dt):
        self.player.update(dt)

    def move_player_right(self):
        self.player.move_right()

    def move_player_left(self):
        self.player.move_left()

    def move_player_up(self):
        self.player.move_up()

    def move_player_down(self):
        self.player.move_down()


