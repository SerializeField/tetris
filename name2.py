from copy import deepcopy
from random import choice, randrange
import pygame

pygame.init()

# количество клеток по ширине и высоте
w, h = 10, 15

# размер клетки
tile = 45

size = width, height = w * tile, h * tile
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

field = [pygame.Rect(x * tile, y * tile, tile, tile) for x in range(w) for y in range(h)]

matrix = [[0 for i in range(w)] for j in range(h)]

anim_count, anim_speed, anim_limit = 0, 60, 2000

get_color = lambda: (randrange(30, 256), randrange(30, 256), randrange(30, 256))
color = get_color()


def check_borders():
    if figure[i].x < 0 or figure[i].x > w - 1:
        return False
    elif figure[i].y > h - 1 or matrix[figure[i].y][figure[i].x]:
        return False
    return True


# координаты фигур
figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[pygame.Rect(x + w // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, tile - 2, tile - 2)
# текущая фигура
figure = deepcopy(choice(figures))

running = True

while running:
    dx, rotate = 0, False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_UP:
                rotate = True

    screen.fill((0, 0, 0))

    clock.tick(60)

    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break

    # движение по оси x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break

    # движение по оси y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    matrix[figure_old[i].y][figure_old[i].x] = color
                color = get_color()
                figure = deepcopy(choice(figures))
                break

    # отрисовка поля
    [pygame.draw.rect(screen, (40, 40, 40), i_rect, 1) for i_rect in field]

    # отрисовка текущей фигуры
    for i in range(4):
        figure_rect.x = figure[i].x * tile
        figure_rect.y = figure[i].y * tile
        pygame.draw.rect(screen, color, figure_rect)

    for y, raw in enumerate(matrix):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * tile, y * tile
                pygame.draw.rect(screen, col, figure_rect)
    pygame.display.flip()

pygame.quit()
