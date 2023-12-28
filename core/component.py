import pygame
from pygame.locals import RLEACCEL

class Component(pygame.sprite.Sprite):
    def __init__(self, path, posX, posY):
        super(Component, self).__init__()
        self.surface = pygame.image.load(path).convert_alpha()
        self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surface.get_rect()
        self.posX = posX-self.rect.w/2
        self.posY = posY-self.rect.h/2