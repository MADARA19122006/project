import pygame
import os
import random
import math
import tytyty


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(walls_group, all_sprites)
        self.image = pygame.image.load('data/box.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.Surface((160, 160))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, board[0] - 161)
        self.rect.y = random.randint(0, board[1] - 161)
        while pygame.sprite.spritecollideany(self, walls_group) or pygame.sprite.spritecollideany(
                self, enemy_group):  # добавить пересечение с игроком
            self.rect.x = random.randint(0, board[0] - 161)
            self.rect.y = random.randint(0, board[0] - 161)
        self.health = 3
        self.x = self.rect.x + 80
        self.y = self.rect.y + 80
        enemy_group.add(self)
        enemy_list.append(self)

    def move(self):
        pass

    def draw(self):
        self.image.fill((255, 255, 255))
        ang_rad = math.atan2(tank_x - self.x, tank_y - self.y)
        x1 = 80 + math.cos(ang_rad) * 80
        y1 = 80 + math.sin(ang_rad) * 80
        pygame.draw.polygon(self.image, (0, 0, 0),
                            ((80 + 15 * math.sin(ang_rad), 80 - 15 * math.cos(ang_rad)),
                             (80 - 15 * math.sin(ang_rad), 80 + 15 * math.cos(ang_rad)),
                             (x1 - 15 * math.sin(ang_rad), y1 + 15 * math.cos(ang_rad)),
                             (x1 + 15 * math.sin(ang_rad), y1 - 15 * math.cos(ang_rad))))
        pygame.draw.circle(self.image, (255, 0, 0), (80, 80), 30)
        pygame.draw.rect(self.image, (255, 0, 0), (80 - 50, 80 - 60, 99, 20))
        pygame.draw.rect(self.image, (0, 255, 0),
                         (80 - 50, 80 - 60, 33 * self.health, 20))


class Tank_bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, x1, y1):
        super().__init__(bullet_group, all_sprites)
        self.x = x
        self.y = y
        self.x1 = x1
        self.y1 = y1
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, (0, 0, 0), (10, 10), 10)
        self.ang_rad = math.atan2(self.y1 - self.y, self.x1 - self.x)

    def update(self):
        self.x += math.cos(self.ang_rad) * 20
        self.y += math.sin(self.ang_rad) * 20
        self.rect.x = self.x - 10 + dx
        self.rect.y = self.y - 10 + dy
        if pygame.sprite.spritecollideany(self, walls_group):
            print('DEL')
            bullet_group.remove(self)
            print(bullet_group)


def draw_tank():
    tank_surf.fill((255, 255, 255))
    ang_rad = math.atan2(pos[1] - tank_y, pos[0] - tank_x)
    x1 = 80 + math.cos(ang_rad) * 80
    y1 = 80 + math.sin(ang_rad) * 80
    pygame.draw.polygon(tank_surf, (0, 0, 0),
                        ((80 + 15 * math.sin(ang_rad), 80 - 15 * math.cos(ang_rad)),
                         (80 - 15 * math.sin(ang_rad), 80 + 15 * math.cos(ang_rad)),
                         (x1 - 15 * math.sin(ang_rad), y1 + 15 * math.cos(ang_rad)),
                         (x1 + 15 * math.sin(ang_rad), y1 - 15 * math.cos(ang_rad))))
    pygame.draw.circle(tank_surf, (255, 0, 0), (80, 80), 30)
    pygame.draw.rect(tank_surf, (255, 0, 0), (80 - 50, 80 - 60, 99, 20))
    pygame.draw.rect(tank_surf, (0, 255, 0),
                     (80 - 50, 80 - 60, 33 * tank_health, 20))


def move_tank(key):
    global tank_x, tank_y
    x = tank_x
    y = tank_y
    for i in range(len(key)):
        if key[i] == pygame.K_d:
            tank_x += 10
        elif key[i] == pygame.K_a:
            tank_x -= 10
        elif key[i] == pygame.K_w:
            tank_y -= 10
        elif key[i] == pygame.K_s:
            tank_y += 10
        tank_sprite.rect.x = tank_x - 30
        tank_sprite.rect.y = tank_y - 30
        if pygame.sprite.spritecollide(tank_sprite, walls_group, False):
            tank_x = x
            tank_y = y
        else:
            x = tank_x
            y = tank_y


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    # создаем стены
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Wall(x, y)
            elif level[y][x] == '@':
                tx = x * tile_width
                ty = y * tile_height
    # генерим врагов
    for i in range(0):  # число врагов
        Enemy()
    # вернем координаты танка
    return tx, ty


def draw():
    screen.fill((196, 98, 16))
    screen.blit(fixed, (dx, dy))
    screen.blit(tank_surf, (screen_size[0] // 2 - 80, screen_size[1] // 2 - 80))
    for el in enemy_list:
        el.draw()
        screen.blit(el.image, (el.x - 80 + dx, el.y - 80 + dy))
    draw_tank()
    bullet_group.draw(screen)
    draw_scope(pos1)


def draw_scope(pos):
    scope.rect.x = pos[0] - 35
    scope.rect.y = pos[1] - 34
    s.draw(screen)


if __name__ == '__main__':
    spisok = [(120, 140, u'Играть', (0, 0, 0), (255, 69, 0), 0),
              (120, 210, u'Выход', (0, 0, 0), (255, 69, 0), 1)]
    zapysk = tytyty.Menu(spisok)
    zapysk.menu()
    pygame.init()
    s = pygame.sprite.Group()
    scope = pygame.sprite.Sprite()
    fullname = os.path.join('data', 'прицел2.png')
    scope.image = pygame.image.load(fullname)
    scope.rect = scope.image.get_rect()
    s.add(scope)
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_size = pygame.display.get_window_size()
    screen.fill((196, 98, 16))
    clock = pygame.time.Clock()
    reload = pygame.event.custom_type()
    tank_sprite = pygame.sprite.Sprite()
    tank_sprite.image = pygame.Surface((60, 60))
    tank_sprite.rect = tank_sprite.image.get_rect()
    all_sprites = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    tile_width = tile_height = 50
    board = (4000, 2000)  # размер игрового поля
    enemy_list = []  # список врагов
    fixed = pygame.Surface(board, pygame.SRCALPHA, 32)
    tank_x, tank_y = generate_level(load_level('level1.txt'))  # изменить имя файла
    walls_group.draw(fixed)
    key = []
    tank_health = 3
    tank_surf = pygame.Surface((160, 160))
    tank_surf.set_colorkey((255, 255, 255))
    pos = (0, 0)
    pos1 = (0, 0)
    running = True
    while running:
        dx = -(tank_x - screen_size[0] // 2)
        dy = -(tank_y - screen_size[1] // 2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                pos = (event.pos[0] - dx, event.pos[1] - dy)
                pos1 = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                Tank_bullet(tank_x, tank_y, event.pos[0] - dx, event.pos[1] - dy)
            if event.type == pygame.KEYDOWN:
                key.append(event.key)
            elif event.type == pygame.KEYUP:
                del key[key.index(event.key)]
        move_tank(key)

        bullet_group.update()
        draw()

        pygame.display.flip()
        delay = clock.tick(50)

    pygame.quit()
