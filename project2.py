import pygame
import os
import random
import math
import tytyty


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(walls_group, all_sprites)
        self.image = pygame.image.load('data/box.png')
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.Surface((160, 160))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.radius = 30
        self.rect.x = random.randint(0, board[0] - 161)
        self.rect.y = random.randint(0, board[1] - 161)
        while pygame.sprite.spritecollide(self, walls_group, False, collided=collision) or pygame.\
                sprite.spritecollideany(self, enemy_group, pygame.sprite.collide_circle_ratio(1)):
            self.rect.x = random.randint(0, board[0] - 161)
            self.rect.y = random.randint(0, board[0] - 161)
            pygame.sprite.spritecollideany(self, walls_group, collided=collision)
        self.health = 3
        self.x = self.rect.x + 80
        self.y = self.rect.y + 80
        enemy_group.add(self)
        enemy_list.append(self)

    def shot(self):
        Tank_bullet(self.rect.x + 80, self.rect.y + 80, tank_x, tank_y, True)

    def move(self):
        pass

    def draw(self):
        if self.health <= 0:
            enemy_group.remove(self)
            del enemy_list[enemy_list.index(self)]
        self.image.fill((255, 255, 255))
        ang_rad = math.atan2(tank_y - self.y, tank_x - self.x)
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
    def __init__(self, x, y, x1, y1, enemy=False):
        super().__init__(bullet_group, all_sprites)
        self.x = x
        self.y = y
        self.x1 = x1
        if enemy:
            self.enemy = True
        else:
            self.enemy = False
        self.y1 = y1
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, (0, 0, 0), (10, 10), 10)
        self.ang_rad = math.atan2(self.y1 - self.y, self.x1 - self.x)

    def update(self):
        global tank_health, running
        self.x += math.cos(self.ang_rad) * 50
        self.y += math.sin(self.ang_rad) * 50
        self.rect.x = self.x - 10
        self.rect.y = self.y - 10
        if pygame.sprite.spritecollideany(self, walls_group):
            bullet_group.remove(self)
        elif pygame.sprite.spritecollideany(self, enemy_group):
            if not self.enemy:
                pygame.sprite.spritecollideany(self, enemy_group).health -= 1
                bullet_group.remove(self)
        elif abs(self.x - tank_x) < 30 and abs(self.y - tank_y) < 30:
            if tank_health > 1:
                tank_health -= 1
            else:
                running = False
        self.rect.x = self.x - 10 + dx
        self.rect.y = self.y - 10 + dy


def collision(sprite1, sprite2):
    return abs(sprite1.rect.x + 80 - sprite2.rect.x - 25) < 55 and abs(
        sprite1.rect.y + 80 - sprite2.rect.y - 25) < 55


def draw_tank():
    tank_sprite.image.fill((255, 255, 255))
    ang_rad = math.atan2(pos[1] - tank_y, pos[0] - tank_x)
    x1 = 80 + math.cos(ang_rad) * 80
    y1 = 80 + math.sin(ang_rad) * 80
    pygame.draw.polygon(tank_sprite.image, (0, 0, 0),
                        ((80 + 15 * math.sin(ang_rad), 80 - 15 * math.cos(ang_rad)),
                         (80 - 15 * math.sin(ang_rad), 80 + 15 * math.cos(ang_rad)),
                         (x1 - 15 * math.sin(ang_rad), y1 + 15 * math.cos(ang_rad)),
                         (x1 + 15 * math.sin(ang_rad), y1 - 15 * math.cos(ang_rad))))
    pygame.draw.circle(tank_sprite.image, (255, 0, 0), (80, 80), 30)
    pygame.draw.circle(tank_sprite.image, (255, 255, 0), (80, 80), r_circle / 100)
    pygame.draw.rect(tank_sprite.image, (255, 0, 0), (80 - 50, 80 - 60, 99, 20))
    pygame.draw.rect(tank_sprite.image, (0, 255, 0),
                     (80 - 50, 80 - 60, 33 * tank_health, 20))


def move_tank(key):
    global tank_x, tank_y, pos
    x = tank_x
    y = tank_y
    p = pos
    for i in range(len(key)):
        if key[i] == pygame.K_d:
            tank_x += 10
            pos = (pos[0] + 10, pos[1])
        elif key[i] == pygame.K_a:
            tank_x -= 10
            pos = (pos[0] - 10, pos[1])
        elif key[i] == pygame.K_w:
            tank_y -= 10
            pos = (pos[0], pos[1] - 10)
        elif key[i] == pygame.K_s:
            tank_y += 10
            pos = (pos[0], pos[1] + 10)
        tank_sprite.rect.x = tank_x - 80
        tank_sprite.rect.y = tank_y - 80
        if pygame.sprite.spritecollide(tank_sprite, walls_group, False, collided=collision) \
                or pygame.sprite.spritecollide(tank_sprite, enemy_group, False,
                                               pygame.sprite.collide_circle_ratio(1)):

            tank_x = x
            tank_y = y
            pos = p
        else:
            x = tank_x
            y = tank_y
            p = pos


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

    # вернем координаты танка
    return tx, ty


def draw():
    screen.fill((196, 98, 16))
    screen.blit(fixed, (dx, dy))
    screen.blit(tank_sprite.image, (screen_size[0] // 2 - 80, screen_size[1] // 2 - 80))
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
    reload_enemy = pygame.event.custom_type()
    r_circle = 0
    tank_sprite = pygame.sprite.Sprite()
    tank_sprite.image = pygame.Surface((160, 160))
    tank_sprite.image.set_colorkey((255, 255, 255))
    tank_sprite.rect = tank_sprite.image.get_rect()
    tank_sprite.radius = 30
    all_sprites = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    time = True
    pygame.time.set_timer(reload_enemy, 1000, False)
    bullet_group = pygame.sprite.Group()
    tile_width = tile_height = 50
    board = (4000, 2000)  # размер игрового поля
    enemy_list = []  # список врагов
    for i in range(10):
        enemy_list.append(Enemy())
    fixed = pygame.Surface(board, pygame.SRCALPHA, 32)
    tank_x, tank_y = generate_level(load_level('level1.txt'))  # изменить имя файла
    tank_health = 3
    walls_group.draw(fixed)
    key = []
    pos = (0, 0)
    pos1 = (0, 0)
    running = True
    while running:
        dx = -(tank_x - screen_size[0] // 2)
        dy = -(tank_y - screen_size[1] // 2)
        for event in pygame.event.get():
            if event.type == reload:
                time = True
            elif event.type == reload_enemy:
                for i in enemy_group:
                    i.shot()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                pos = (event.pos[0] - dx, event.pos[1] - dy)
                pos1 = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                if time:
                    r_circle = 0
                    pygame.time.set_timer(reload, 3000, True)
                    Tank_bullet(tank_x, tank_y, event.pos[0] - dx, event.pos[1] - dy)
                    time = False
            if event.type == pygame.KEYDOWN:
                key.append(event.key)
            elif event.type == pygame.KEYUP:
                del key[key.index(event.key)]
        move_tank(key)
        bullet_group.update()
        draw()
        pygame.display.flip()
        delay = clock.tick(50)
        if r_circle < 3000:
            r_circle += delay

    pygame.quit()
