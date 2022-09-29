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

class Tetris:
    level = 3
    score = 0
    state = "Start"
    field = []
    height = 0
    width = 0
    x = 100
    y = 70
    zoom = 30
    figure = None

    def __int__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "Start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        self.figure = Figure(3, 0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return  intersection

    def break_lines(self):
        line = 0
        for i in range(1, self.height):
            zero = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zero += 1
                if zero == 0:
                    line += 1
                    for i1 in range(i, 1, -1):
                        for j in range(self.width):
                            self.field[i1][j] = self.field[i1 - 1][j]
        self.score += line ** 2

    def space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
                    self.break_lines()
                    self.new_figure()
        if self.intersects():
            self.state = "Game Over"

    def side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rot = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rot