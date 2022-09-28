import pygame
import random

colors = [(255, 20, 147),
          (139, 0, 139),
          (138, 43, 226),
          (186, 85, 211),
          (32, 178, 170),
          (46, 139, 87),
          (127, 255, 0)]

class Figure:

    x = 0
    y = 0

    figures = [[[1, 5, 9, 13], [4, 5, 6, 7]],
               [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
               [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
               [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
               [[1, 2, 5, 6]]]

    def __int__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])