import pygame
from pygame.locals import RLEACCEL
from core.constants import COMPONENT_SIZE

class Wire(pygame.sprite.Sprite):
    def __init__(self, up, right, down, left, surface_x, surface_y):
        super(Wire, self).__init__()
        self.up = up
        self.right = right
        self.down = down
        self.left = left
        self.surface_x = surface_x-COMPONENT_SIZE/2
        self.surface_y = surface_y-COMPONENT_SIZE/2
        self.line_path = "assets/sprites/line.png"
        self.corner_path = "assets/sprites/corner.png"
        self.update_surface()

    def update_surface(self):
        self.surface = pygame.Surface((COMPONENT_SIZE, COMPONENT_SIZE), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        
        # List of wire parts to render and their transforms
        paths = []
        transforms = [] # tuples: (width offset, height offset, rotation)

        # Only left or right neighbours or no neightbours at all -> horizontal wire
        if ((self.left or self.right) and not(self.up or self.down)) or not(self.left or self.right or self.up or self.down):
            paths.append(self.line_path)
            transforms.append((0, 0.5, 0))
            print('horizontal')

        # Only up or down neighbours -> vertical wire
        if (self.up or self.down) and not(self.left or self.right):
            paths.append(self.line_path)
            transforms.append((0.5, 0, 90))
            print('vertical')

        # Corner cases (stack parts on top of each other)
        if self.right and self.down:
            paths.append(self.corner_path)
            transforms.append((0.5, 0.5, 0))
            print('r-d')
        if self.right and self.up:
            paths.append(self.corner_path)
            transforms.append((0.5, 0, 90))
            print('r-u')
        if self.up and self.left:
            paths.append(self.corner_path)
            transforms.append((0, 0, 180))
            print('u-l')
        if self.left and self.down:
            paths.append(self.corner_path)
            transforms.append((0, 0.5, 270))
            print('l-d')

        index = 0
        for path in paths:
            part = pygame.image.load(path).convert_alpha()
            part.set_colorkey((255, 255, 255), RLEACCEL)
            rotated_part = pygame.transform.rotate(part, transforms[index][2])
            
            x = self.rect.w * transforms[index][0]
            y = self.rect.h * transforms[index][1]

            self.surface.blit(rotated_part, (x, y))

            index += 1
