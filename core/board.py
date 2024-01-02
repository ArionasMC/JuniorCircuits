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
        self.components = [] # tuples (Component, (pos_i, pos_j))
        self.points = []
        self.wires = []
        self.rotations = np.zeros(shape=[dimX, dimY], dtype=int)

    def insert(self, pos, item, rotate=False):
        self.board[pos[0], pos[1]] = item
        self.rotations[pos[0], pos[1]] = rotate

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
        self.wires.clear()
        for i in range(self.dimX):
            for j in range(self.dimY):
                id = self.board[i, j]
                x = (i+0.5)*self.gridWidth
                y = (j+0.5)*self.gridHeight
                if id == SOURCE_ID:
                    source = Source(x, y, DEFAULT_VOLTAGE)
                    source.horizontal = ~self.rotations[i, j]
                    source.rotate()
                    self.components.append((source, (i, j)))
                if id == RESISTANCE_ID:
                    resistance = Resistance(x, y, DEFAULT_RESISTANCE)
                    resistance.horizontal = ~self.rotations[i, j]
                    resistance.rotate()
                    self.components.append((resistance, (i, j)))
                if id == AMPEROMETER_ID:
                    self.components.append((Component("assets/sprites/amperometer.png", x, y, ~self.rotations[i,j]), (i, j)))
                if id == VOLTOMETER_ID:
                    self.components.append((Component("assets/sprites/voltometer.png", x, y, ~self.rotations[i,j]), (i, j)))
                if id == LINE_ID:
                    up, right, down, left = True, True, True, True # change it to more compact code
                    if (j-1) < 0: 
                        up = False
                    else:
                        #print(self.board[i, j-1])
                        if (self.board[i, j-1] == EMPTY_ID) or (self.board[i, j-1] == SOURCE_ID): 
                            up = False
                        else:
                            if self.board[i, j-1] in ORIENTED_COMPONENT_IDS:
                                up = not(self.is_horizontal_at(i, j-1))

                    if (j+1) >= self.dimY:
                        down = False
                    else:
                        #print(self.board[i, j+1])
                        if (self.board[i, j+1] == EMPTY_ID) or (self.board[i, j+1] == SOURCE_ID):
                            down = False
                        else:
                            if self.board[i, j+1] in ORIENTED_COMPONENT_IDS:
                                down = not(self.is_horizontal_at(i, j+1))

                    if (i-1) < 0:
                        left = False
                    else:
                        #print(self.board[i-1, j])
                        if self.board[i-1, j] == EMPTY_ID:
                            left = False
                        else:
                            if self.board[i-1,j] in ORIENTED_COMPONENT_IDS:
                                left = self.is_horizontal_at(i-1,j)

                    if (i+1) >= self.dimX:
                        right = False
                    else:
                        #print(self.board[i+1, j])
                        if self.board[i+1, j] == EMPTY_ID:
                            right = False
                        else:
                            if self.board[i+1,j] in ORIENTED_COMPONENT_IDS:
                                right = self.is_horizontal_at(i+1,j)

                    print('u=',up,'r=',right,'d=',down,'l=',left)
                    self.wires.append(Wire(up, right, down, left, x, y))

    def update_available_points(self, current_id): # change it later
        if current_id == LINE_ID:
            for i in range(self.dimX):
                for j in range(self.dimY):
                    if self.board[i, j] != EMPTY_ID:
                        self.points.append(AvailablePoint(i, j))
        else:
            for i in range(self.dimX):
                for j in range(self.dimY):
                    if self.board[i, j] == EMPTY_ID:
                        self.points.append(AvailablePoint(i, j))

    def update_points_for_deletion(self):
        for i in range(self.dimX):
            for j in range(self.dimY):
                if (self.board[i, j] != EMPTY_ID) and (self.board[i, j] != SOURCE_ID):
                    self.points.append(AvailablePoint(i, j, DELETE_COLOR))

    def update_points_for_second_wire(self, first_point):
        fpi, fpj = first_point[0], first_point[1]
        if self.board[fpi, fpj] != LINE_ID:
            if self.is_horizontal_at(fpi, fpj):
                self.fill_points_horizontally(fpi, fpj)
            else:
                self.fill_points_vertically(fpi, fpj)
        else: # if first point is wire then available points are both vertical and horizontal
            self.fill_points_horizontally(fpi, fpj)
            self.fill_points_vertically(fpi, fpj)

    def fill_points_horizontally(self, fpi, fpj):
        li = fpi - 1
        # Check left
        while (li >= 0) and (self.board[li, fpj] == EMPTY_ID):
            self.points.append(AvailablePoint(li, fpj))
            li -= 1
        li = fpi + 1
        # Check right
        while (li < self.dimX) and (self.board[li, fpj] == EMPTY_ID):
            self.points.append(AvailablePoint(li, fpj))
            li += 1

    def fill_points_vertically(self, fpi, fpj):
        lj = fpj - 1
        # Check up
        while (lj >= 0) and (self.board[fpi, lj] == EMPTY_ID):
            self.points.append(AvailablePoint(fpi, lj))
            lj -= 1
        lj = fpj + 1
        # Check down
        while (lj < self.dimY) and (self.board[fpi, lj] == EMPTY_ID):
            self.points.append(AvailablePoint(fpi, lj))
            lj += 1
    
    def clear_board(self):
        for i in range(self.dimX):
            for j in range(self.dimY):
                if (self.board[i, j] != EMPTY_ID) and (self.board[i, j] != SOURCE_ID):
                    self.board[i, j] = EMPTY_ID

    def is_horizontal_at(self, i, j):
        for (com, pos) in self.components:
            if (pos[0] == i) and (pos[1] == j):
                return com.horizontal
        return True

    def erase_and_clear_points(self):
        #print("erasing points...")
        for point in self.points:
            point.erase()
        self.points.clear()

    def is_empty_at(self, pos_i, pos_j):
        return self.board[pos_i, pos_j] == EMPTY_ID