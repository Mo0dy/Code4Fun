import numpy as np
import pygame as pg

class Matrix(object):
    bordercolor = (50, 50, 50)
    bordersize = 5

    def __init__(self, rows, columns, *args, **kwargs):
        # stores the color values of the matrix
        self.matrix = np.zeros((rows, columns, 3))

        # add kwargs to the matrix
        for k, val in kwargs.items():
            if k in self.__dict__:
                self.__dict__[k] = val
            else:
                print("kwarg not allowed")

    @property
    def rows(self):
        return self.matrix.shape[0]

    @property
    def columns(self):
        return self.matrix.shape[1]

    def __getitem__(self, item):
        return self.matrix[item]

    def draw(self, screen, size, origin):
        '''
        :param screen: the screen to draw on
        :param size: the size the matrix will be drawn
        :return: void
        '''

        # fill the background of the screen:
        pg.draw.rect(screen, self.bordercolor, (origin[0], origin[1], size[0], size[1]))

        # this way of drawing the matrix can produce unprecice results if the size is not divisible by the amount of squares
        # borders should be drawn
        if self.bordersize:
            # the total length that needs to be filled by squares
            total_squares_x = size[0] - (self.columns + 1) * self.bordersize
            # the size of the squares
            square_size_x = int(total_squares_x / self.columns)
            # the distance between the beginning of squares
            square_dx = int((size[0] - self.bordersize) / self.columns)

            total_squares_y = size[1] - (self.rows + 1) * self.bordersize
            square_size_y = int(total_squares_y / self.rows)
            square_dy = int((size[1] - self.bordersize) / self.rows)

            for i in range(self.columns):
                for j in range(self.rows):
                    pg.draw.rect(screen, self.matrix[j, i], (self.bordersize + j * square_dy, self.bordersize + i * square_dx, square_size_y, square_size_x))