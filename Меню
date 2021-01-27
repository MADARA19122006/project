import sys
import pygame
import project2


pygame.init()
window = pygame.display.set_mode((400, 400))
screen = pygame.Surface((400, 400))
string = pygame.Surface((400, 30))


class Menu:
    def __init__(self, spisok):
        self.spisok = spisok

    def proris(self, pov, shrift, number):
        for i in self.spisok:
            if number == i[5]:
                pov.blit(shrift.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                pov.blit(shrift.render(i[2], 1, i[3]), (i[0], i[1]))

    def menu(self):
        run = True
        shrift_menu = pygame.font.SysFont('Calibri', 50)
        number = 0
        while run:
            string.fill((0, 100, 200))
            screen.fill((255, 255, 255))
            mp = pygame.mouse.get_pos()
            for i in self.spisok:
                if i[0] < mp[0] < i[0] + 155 and i[1] < mp[1] < i[1] + 50:
                    number = i[5]
            self.proris(screen, shrift_menu, number)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if number == 0:
                        run = False
                    elif number == 0:
                        sys.exit()
                    if number == 1:
                        sys.exit()

            window.blit(screen, (0, 0))
            pygame.display.flip()


spisok = [(120, 140, u'Играть', (0, 0, 0), (255, 69, 0), 0),
          (120, 210, u'Выход', (0, 0, 0), (255, 69, 0), 1)]
zapysk = Menu(spisok)
zapysk.menu()
