import numpy as np
import pygame

from core.component import Component
from core.available_point import AvailablePoint
from core.constants import *
from components.source import Source
from components.resistance import Resistance
from components.wire import Wire

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
        self.points = []
        self.wires = []

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
        self.components.clear()
        for i in range(self.dimX):
            for j in range(self.dimY):
                id = self.board[i, j]
                x = (i+0.5)*self.gridWidth
                y = (j+0.5)*self.gridHeight
                if id == SOURCE_ID:
                    self.components.append(Source(x, y, DEFAULT_VOLTAGE))
                if id == RESISTANCE_ID:
                    self.components.append(Resistance(x, y, DEFAULT_RESISTANCE))
                if id == AMPEROMETER_ID:
                    self.components.append(Component("assets/sprites/amperometer.png", x, y))
                if id == VOLTOMETER_ID:
                    self.components.append(Component("assets/sprites/voltometer.png", x, y))
                if id == LINE_ID:
                    up, right, down, left = True, True, True, True
                    if (j-1) < 0: 
                        up = False
                    else:
                        #print(self.board[i, j-1])
                        if self.board[i, j-1] == EMPTY_ID: 
                            up = False

                    if (j+1) > self.dimY:
                        down = False
                    else:
                        #print(self.board[i, j+1])
                        if self.board[i, j+1] == EMPTY_ID:
                            down = False

                    if (i-1) < 0:
                        left = False
                    else:
                        #print(self.board[i-1, j])
                        if self.board[i-1, j] == EMPTY_ID:
                            left = False

                    if (i+1) > self.dimX:
                        right = False
                    else:
                        #print(self.board[i+1, j])
                        if self.board[i+1, j] == EMPTY_ID:
                            right = False
                    print('u=',up,'r=',right,'d=',down,'l=',left)
                    self.wires.append(Wire(up, right, down, left, x, y))

    def update_available_points(self):
        for i in range(self.dimX):
            for j in range(self.dimY):
                if self.board[i, j] == EMPTY_ID:
                    self.points.append(AvailablePoint(i, j))

    def erase_and_clear_points(self):
        #print("erasing points...")
        for point in self.points:
            point.erase()
        self.points.clear()