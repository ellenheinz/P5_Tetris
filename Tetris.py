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

pygame.init()

red = (231, 76, 60)
purple = (155, 89, 182)
blue = (52, 152, 219)

size = (250, 350)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tetris")

done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris()
counter = 0
pressing_down = False

while not done:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "Start":
            game.down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.side(-1)
            if event.key == pygame.K_RIGHT:
                game.side(1)
            if event.key == pygame.K_SPACE:
                game.space()
            if event.key == pygame.K_ESCAPE:
                game.__int__(15, 5)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_DOWN:
            pressing_down = False

    screen.fill(red)

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, purple, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]], [game.x + game.zoom * j + i, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game. zoom - 2])

    font = pygame.font.SysFont("Arial", 13, True, False)
    font1 = pygame.font.SysFont("Arial", 23, True, False)
    text = font.render("Score: " + str(game.score), True, blue)
    text_game_over = font1.render("Game Over", True, (231, 76, 60))
    text_game_over1 = font1.render("Press ESC", True, (231, 76, 60))

    screen.blit(text, [0, 0])
    if game.state == "Game Over":
        screen.blit(text_game_over, [15, 150])
        screen.blit(text_game_over1, [15, 150])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()