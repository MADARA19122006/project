import pygame


class Board:
    def __init__(self):
        self.m = [[300, 300, 0, 0]]
        self.time = 0

    def draw_tank(self):
        global clock
        screen.fill((100, 100, 100))
        if self.m[0][2] - self.m[0][0] == 0 or self.m[0][3] - self.m[0][1] == 0:
            sin = 0
            cos = 1
        else:
            tangent = (self.m[0][3] - self.m[0][1]) / (self.m[0][2] - self.m[0][0])
            cos = (1 / (tangent ** 2 + 1)) ** 0.5
            sin = (tangent ** 2 / (tangent ** 2 + 1)) ** 0.5
        width_gun = 15
        if self.m[0][0] > self.m[0][2]:
            cos = -cos
        if self.m[0][1] > self.m[0][3]:
            sin = -sin
        x1 = self.m[0][0] + cos * 80
        y1 = self.m[0][1] + sin * 80
        pygame.draw.polygon(screen, (0, 0, 0),
                            ((self.m[0][0] + width_gun * sin, self.m[0][1] - width_gun * cos),
                             (self.m[0][0] - width_gun * sin, self.m[0][1] + width_gun * cos),
                             (x1 - width_gun * sin, y1 + width_gun * cos),
                             (x1 + width_gun * sin, y1 - width_gun * cos)))
        pygame.draw.circle(screen, (255, 0, 0), (self.m[0][0], self.m[0][1]), 30)
        if self.time < 3000:
            self.time += clock.tick()
        pygame.draw.circle(screen, (0, 255, 0), (self.m[0][0], self.m[0][1]),
                           30 / (3000 / self.time))

    def move_tank(self):
        global key
        for i in range(len(key)):
            if key[i] == pygame.K_w and self.m[0][1] > 30:
                self.m[0][1] -= 1
            elif key[i] == pygame.K_s and self.m[0][1] < 990:
                self.m[0][1] += 1
            elif key[i] == pygame.K_a and self.m[0][0] > 30:
                self.m[0][0] -= 1
            elif key[i] == pygame.K_d and self.m[0][0] < 1890:
                self.m[0][0] += 1

    def draw_objects(self):
        global shot
        k = []
        index = 0
        self.draw_tank()
        for i in range(1, len(self.m)):
            self.m[i][4] += 30
            if self.m[i][2] - self.m[i][0] == 0 or self.m[i][3] - self.m[i][1] == 0:
                sin = 0
                cos = 1
            else:
                tangent = (self.m[i][3] - self.m[i][1]) / (self.m[i][2] - self.m[i][0])
                cos = (1 / (tangent ** 2 + 1)) ** 0.5
                sin = (tangent ** 2 / (tangent ** 2 + 1)) ** 0.5
            if self.m[i][0] > self.m[i][2]:
                cos = -cos
            if self.m[i][1] > self.m[i][3]:
                sin = -sin
            x1 = self.m[i][0] + cos * self.m[i][4]
            y1 = self.m[i][1] + sin * self.m[i][4]
            if 5 < x1 < 1915 and 5 < y1 < 1015:
                pygame.draw.circle(screen, (0, 0, 0), (x1, y1), 10)
            else:
                k.append(i)
        k.sort()
        for i in k:
            del self.m[i - index]
            index += 1


board = Board()
push = False
key = []
shot = True
screen = pygame.display.set_mode((1920, 1020))
screen.fill((100, 100, 100))
pygame.display.flip()
running = True
x = 0
clock = pygame.time.Clock()
reload = pygame.event.custom_type()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == reload:
            shot = True
        if event.type == pygame.MOUSEMOTION:
            pos = event.pos
            board.m[0] = [board.m[0][0], board.m[0][1], event.pos[0], event.pos[1]]
        if event.type == pygame.MOUSEBUTTONDOWN:
            if shot:
                clock.tick()
                board.time = 0
                pygame.time.set_timer(reload, 3000, True)
                board.m.append([board.m[0][0], board.m[0][1], event.pos[0], event.pos[1], 0])
                shot = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):
                push = True
                key.append(event.key)
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d) and len(key) == 1:
                key = []
                push = False
            elif event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):
                del key[key.index(event.key)]
    if push:
        board.move_tank()
    board.draw_objects()
    pygame.display.flip()
