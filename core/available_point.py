import pygame
from pygame.sprite import Sprite

from core.constants import *

class AvailablePoint(Sprite):
    def __init__(self, i, j):
        super(AvailablePoint, self).__init__()
        self.surface = pygame.Surface((POINT_SIZE, POINT_SIZE))
        self.rect = self.surface.get_rect()
        pygame.draw.rect(surface=self.surface, color=POINT_COLOR, rect=self.rect)
        self.i = i
        self.j = j

    def clicked_me(self, posX, posY) -> bool:
        return self.rect.collidepoint(posX, posY)
    
    def erase(self):
        self.kill()