import numpy as np
import pygame

from core.component import Component

class Board(pygame.sprite.Sprite):
    def __init__(self, dimX, dimY, surface, bg_color):
        super(Board, self).__init__()
        self.surface = surface
        self.surface.fill(bg_color)
        self.rect = self.surface.get_rect()
        self.dimX = dimX
        self.dimY = dimY
        self.gridWidth = self.rect.w / self.dimX * 1.0
        self.gridHeight = self.rect.h / self.dimY * 1.0
        self.board = np.zeros(shape=[dimX, dimY], dtype=int)
        self.components = []

    def insert(self, pos, item):
        self.board[pos[0], pos[1]] = item

    def read(self, pos):
        return self.board[pos[0], pos[1]]
    
    def get_dimX(self):
        return self.dimX
    
    def get_dimY(self):
        return self.dimY
    
    def draw_grid(self):
        for x in range(self.dimX):
            pygame.draw.line(surface=self.surface, color=pygame.Color(195, 172, 208), 
                             start_pos=((x+0.5)*self.gridWidth, 0), 
                             end_pos=((x+0.5)*self.gridWidth, self.dimY*self.gridHeight), width=2)
        for y in range(self.dimY):
            pygame.draw.line(surface=self.surface, color=pygame.Color(195, 172, 208),
                             start_pos=(0, (y+0.5)*self.gridHeight),
                             end_pos=(self.dimX*self.gridWidth, (y+0.5)*self.gridHeight), width=2)
        
    def update_components(self):
        for i in range(self.dimX):
            for j in range(self.dimY):
                id = self.board[i, j]
                if id == 1: # source
                    source = Component("assets/sprites/source.png", (i+0.5)*self.gridWidth, (j+0.5)*self.gridHeight)
                    self.components.append(source)

        