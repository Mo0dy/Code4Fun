import numpy as np
import pygame as pg

from Code4Fun.Utility.Vec2 import Vec2


def pol2cart(rho, phi):
    return rho * np.stack((np.cos(phi), np.sin(phi)), axis=-1)


class PerlinNoiseMap2D(object):
    def __init__(self, size_x, size_y):
        # generate random 2d vectors (complex numbers)
        # generate random angles
        angles = np.random.rand(size_x, size_y) * (np.pi * 2)
        # turn angles into vectors
        self.vectors = pol2cart(1, angles)

    #linear interpolation
    def lerp(self, a0, a1, w):
        return (1 - w) * a0 + w * a1

    def dotGridGradient(self, ix, iy, x, y):
        dx = x - ix
        dy = y - iy

        ix = int(ix)
        iy = int(iy)

        return dx * self.vectors[ix, iy, 0] + dy * self.vectors[ix, iy, 1]

    def get_noise(self, x, y):
        x0 = np.floor(x)
        x1 = x0 + 1
        y0 = np.floor(y)
        y1 = y0 + 1

        # interpolation weigts
        sx = x - x0
        sy = y - y0

        # interpolate
        n0 = self.dotGridGradient(x0, y0, x, y)
        n1 = self.dotGridGradient(x1, y0, x, y)
        ix0 = self.lerp(n0, n1, sx)
        n0 = self.dotGridGradient(x0, y1, x, y)
        n1 = self.dotGridGradient(x1, y1, x, y)
        ix1 = self.lerp(n0, n1, sx)
        return self.lerp(ix0, ix1, sy)

    def draw_vectors(self, screen):
        screen_size = screen.get_size()

        # the distance between the vectors
        stepsize = [int(screen_size[0] / self.vectors.shape[0]), int(screen_size[1] / self.vectors.shape[1])]

        # draw terrain vectors:
        for i in range(self.vectors.shape[0]):
            for j in range(self.vectors.shape[1]):
                position = [i * stepsize[0] + int(stepsize[0] / 2), j * stepsize[1] + int(stepsize[1] / 2)]
                pg.draw.circle(screen, (255, 255, 0), position, 5)
                pg.draw.line(screen, (200, 200, 0),
                             (position[0] + self.vectors[i, j, 0] * 20, position[1] + self.vectors[i, j, 1] * 20),
                             position, 2)


class Terrain(object):
    def __init__(self, size_x, size_y, elements_x, elements_y):
        noise_x_res = int(elements_x / 10)
        noise_y_res = int(elements_y / 10)

        self.origin = [size_x / 2, size_y / 2]

        threshhold = 100

        self.noise = PerlinNoiseMap2D(noise_x_res, noise_y_res)

        stepsize_x = (noise_x_res - 1.1) / elements_x
        stepsize_y = (noise_y_res - 1.1) / elements_y

        self.noise_map = np.zeros((elements_x, elements_y))
        for i in range(elements_x):
            for j in range(elements_y):
                self.noise_map[i, j] = self.noise.get_noise(stepsize_x * (i + 1), stepsize_y * (j + 1))

        # scale terrain between 0 and 255
        terrain_min = np.min(self.noise_map)
        terrain_max = np.max(self.noise_map)

        self.noise_map = ((self.noise_map - terrain_min) * 255 / (terrain_max - terrain_min)).astype(np.int)

        self.terrain = self.noise_map > threshhold

        self.terrain_surf = pg.Surface((size_x, size_y))
        self.collision_surf = pg.Surface((size_x, size_y))
        self.draw_terrain(self.terrain_surf)

    def draw_noise_map(self, screen):
        screen_size = screen.get_size()

        # the distance between the vectors
        stepsize = [int(screen_size[0] / self.noise_map.shape[0]), int(screen_size[1] / self.noise_map.shape[1])]

        for i in range(self.noise_map.shape[0]):
            for j in range(self.noise_map.shape[1]):
                pg.draw.rect(screen, (0, 0, self.noise_map[i, j]), (i * stepsize[0], j * stepsize[1], stepsize[0], stepsize[1]))

    def draw_terrain(self, screen):
        grass_image = pg.image.load(r"Assets\Terrain\Grass.jpg").convert()
        rock_image = pg.image.load(r"Assets\Terrain\rock.jpg").convert()
        screen_size = screen.get_size()

        # the distance between the vectors
        stepsize = [int(screen_size[0] / self.terrain.shape[0]), int(screen_size[1] / self.terrain.shape[1])]

        self.collision_surf.fill(0)

        for i in range(self.terrain.shape[0]):
            for j in range(self.terrain.shape[1]):
                if self.terrain[i, j]:
                    self.terrain_surf.blit(grass_image, (i * stepsize[0], j * stepsize[1]), (0, 0, stepsize[0], stepsize[1]))
                else:
                    self.terrain_surf.blit(rock_image, (i * stepsize[0], j * stepsize[1]), (0, 0, stepsize[0], stepsize[1]))
                    pg.draw.rect(self.collision_surf, 255, (i * stepsize[0], j * stepsize[1], stepsize[0], stepsize[1]))

        # borders around the edge
        for i in range(self.terrain.shape[0]):
            self.terrain_surf.blit(rock_image, (i * stepsize[0], (self.terrain.shape[1] - 1) * stepsize[1]), (0, 0, stepsize[0], stepsize[1]))
            pg.draw.rect(self.collision_surf, 255, (i * stepsize[0], (self.terrain.shape[1] - 1) * stepsize[1], stepsize[0], stepsize[1]))

            self.terrain_surf.blit(rock_image, (i * stepsize[0], 0), (0, 0, stepsize[0], stepsize[1]))
            pg.draw.rect(self.collision_surf, 255,
                         (i * stepsize[0], 0, stepsize[0], stepsize[1]))

        for i in range(self.terrain.shape[1]):
            self.terrain_surf.blit(rock_image, ((self.terrain.shape[0] - 1) * stepsize[0], i * stepsize[1]), (0, 0, stepsize[0], stepsize[1]))
            pg.draw.rect(self.collision_surf, 255, ((self.terrain.shape[0] - 1) * stepsize[0], i * stepsize[1], stepsize[0], stepsize[1]))

            self.terrain_surf.blit(rock_image, (0, i * stepsize[0]), (0, 0, stepsize[0], stepsize[1]))
            pg.draw.rect(self.collision_surf, 255,
                         (0, i * stepsize[0], stepsize[0], stepsize[1]))