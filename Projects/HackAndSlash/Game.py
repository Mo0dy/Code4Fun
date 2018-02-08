# game logic
from Code4Fun.Projects.HackAndSlash.Player import *
from Code4Fun.Projects.HackAndSlash.Entity import *


class Game(object):
    def __init__(self):
        self.player = Player()
        print("test")

    def move_player_right(self):
        self.player.move_right()

    def move_player_left(self):
        self.player.move_left()

    def move_player_up(self):
        self.player.move_up()

    def move_player_down(self):
        self.player.move_down()


