import pygame
import os
import random


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('cannot load image', fullname)
        raise SystemExit(message)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image.convert_alpha()
    return image


class Tetris:

    # номера клеток в массиве 4 на 4 начиная с нуля
    figures = [[1, 5, 9, 13], [2, 6, 9, 10], [1, 2, 4, 5], [0, 1, 5, 6], [1, 5, 9, 10],
               [2, 6, 9, 10], [0, 1, 2, 5]]

    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.board = [[0] * width for _ in range(height)]
        self.active_figure = None
        self.is_game_active = False

        self.spawn_x = self.width // 2

    def render(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(screen, pygame.Color('grey'),
                                 (x * self.cell_size, y * self.cell_size,
                                  self.cell_size, self.cell_size), 1)
                if self.board[y][x] == 1:
                    pygame.draw.rect(screen, pygame.Color('red'),
                                     (x * self.cell_size, y * self.cell_size,
                                      self.cell_size, self.cell_size))

    def new_figure(self):
        figure = random.choice(Tetris.figures)
        self.active_figure = []
        for x in range(4):
            for y in range(4):
                if (y * 4) + x in figure:
                    self.board[y][x + self.spawn_x] = 1
                    self.active_figure.append([x + self.spawn_x, y])

    def update(self):
        for i in range(len(self.active_figure)):
            x, y = self.active_figure[i]
            self.board[y][x] = 0
            self.active_figure[i] = (x, y+1)

        for i in self.active_figure:
            self.board[i[1]][i[0]] = 1

    def delete_row(self):
        pass


def main():

    cell_size = 20
    width_cells = 12
    height_cells = 20
    size = cell_size * width_cells, cell_size * height_cells
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    fps = 10
    running = True
    tetris = Tetris(width_cells, height_cells, cell_size)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not tetris.active_figure:
            tetris.new_figure()

        tetris.update()
        screen.fill(pygame.Color('black'))
        tetris.render(screen)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


if __name__ == '__main__':
    main()