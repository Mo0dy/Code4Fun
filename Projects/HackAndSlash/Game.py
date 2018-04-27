# game logic
from Code4Fun.Projects.HackAndSlash.Player import *
from Code4Fun.Projects.HackAndSlash.Entity import *
from Code4Fun.Projects.HackAndSlash.Terrain import Terrain


class Game(object):
    def __init__(self):
        self.player = Player()
        self.terrain = Terrain(8000, 8000, 100, 100)
        self.minimap = pg.Surface((200, 200))
        pg.transform.scale(self.terrain.terrain_surf, (200, 200), self.minimap)

    def reset(self):
        self.terrain = Terrain(8000, 8000, 100, 100)
        self.minimap = pg.Surface((200, 200))
        pg.transform.scale(self.terrain.terrain_surf, (200, 200), self.minimap)

    def draw(self, screen):
        screen_size = screen.get_size()
        screen.blit(self.terrain.terrain_surf, (0, 0), (self.terrain.origin[0] - screen_size[0] / 2 + self.player.pos.tuple_int[0], self.terrain.origin[1] - screen_size[1] / 2 + self.player.pos.tuple_int[1], screen_size[0], screen_size[1]))
        self.player.draw(screen)

        # draws map shape
        screen.blit(self.minimap, (0, 600))
        # draws player transformed to map
        player_x = int((self.player.pos.x + 4000) / 8000 * 200)
        player_y = int((self.player.pos.y + 4000) / 8000 * 200)
        pg.draw.circle(screen, (200, 50, 50), (player_x, 600 + player_y), 3)


    def update(self, dt):
        self.player.update(dt, self.terrain.collision_surf)

    def move_player_right(self):
        self.player.move_right()

    def move_player_left(self):
        self.player.move_left()

    def move_player_up(self):
        self.player.move_up()

    def move_player_down(self):
        self.player.move_down()

    def player_lunge(self):
        self.player.lunge()


