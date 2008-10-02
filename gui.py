import sys
from itertools_recipes import pairwise
from astar import Problema, ASTAR, AVARA

import pygame
from pygame.locals import *

WHITE = (255,255,255)
BLACK = (10,20,30)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)
DRED = (215,0,0)
BROWN = (222,170,100)

WINDOW_TITLE = "A*"
WINDOW = (800,600)

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class GUI(object):

    def __init__(self, screen):
        self.bg = pygame.Surface(WINDOW)
        self.bg.blit(screen, (0,0))
        self.screen = screen
        self.ink = BLACK
        self.exit = False
        self.sprites = pygame.sprite.RenderUpdates()
        self.clock = pygame.time.Clock()
        self.points = []
        self.buffer = []
        self.inicio = None
        self.fin = None
        self.only_esc = False

    def loop(self):
       pygame.display.flip()
       while not self.exit:
            
            self.clock.tick(100)
            
            for event in pygame.event.get():
                self.control(event)
            
            self.update()
            self.draw()
            
            pygame.display.flip()
            
    def control(self, event):
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == KEYDOWN:
            self.keydown(event)
        elif event.type == MOUSEBUTTONDOWN:
            self.mouseclick(event) 
        
    def update(self):
        self.sprites.update()
        
    def mouseclick(self, event):
        if not self.only_esc:
            p = event.pos
            if not self.inicio:
                self.ink = GREEN
                self.inicio = p
            elif not self.fin:
                self.ink = RED
                self.fin = p    
            else:
                self.buffer.append(p)
            pygame.draw.circle(self.screen, self.ink, p, 4)
            self.ink = BLACK
            
    def keydown(self, event):
        if event.key == K_ESCAPE:
            self.reset()   
        if not self.only_esc:     
            if event.key == K_SPACE:
                if len(self.buffer) == 0:
                    pass
                elif len(self.buffer) == 1:
                    self.points.append(self.buffer.pop())
                elif len(self.buffer) == 2:
                    self.points.append(self.buffer.pop(0))
                    self.points.append(self.buffer.pop())
                else:
                    self.points.append(self.buffer[:])
                    for tri in [(p1, p2, p3) for p1 in self.buffer for p2 in self.buffer for p3 in self.buffer]:
                        pygame.draw.polygon(self.screen, BROWN, tri)
                    self.buffer = []
            if event.key == K_RETURN:
                self.points = [self.inicio] + self.points + [self.fin]
                pr_avara = Problema(self.points, AVARA)
                pr_astar = Problema(self.points, ASTAR)
                for i,j in pairwise(pr_avara.resolver()):
                    pygame.draw.line(self.screen, DRED, i.pos(), j.pos(), 4)
                for i,j in pairwise(pr_astar.resolver()):
                    pygame.draw.line(self.screen, BLUE, i.pos(), j.pos(), 2)
                self.only_esc = True
        
    def reset(self):
        self.screen.blit(self.bg, (0,0))
        self.inicio = self.fin = None
        self.buffer = []
        self.points = []
        self.only_esc = False

    def draw(self):
        self.sprites.draw(self.screen)

def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW)
    screen.fill(WHITE)
    pygame.display.set_caption(WINDOW_TITLE)

    app = GUI(screen)
    app.loop()

if __name__ == "__main__":
    main()
