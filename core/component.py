import pygame
from pygame.locals import RLEACCEL
from core.constants import VERTICAL_ROTATION

class Component(pygame.sprite.Sprite):
    def __init__(self, path, posX, posY, horizontal):
        super(Component, self).__init__()
        self.path = path
        self.surface = pygame.image.load(path).convert_alpha()
        self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surface.get_rect()
        self.posX = posX-self.rect.w/2
        self.posY = posY-self.rect.h/2
        self.horizontal = horizontal
        self.rotate()
    
    def rotate(self):
        if not(self.horizontal):
            self.surface = pygame.transform.rotate(self.surface, VERTICAL_ROTATION)