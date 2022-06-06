import random

import pygame

from settings import *

class Structure:
    def __init__(self, start_x=None, start_y=None, texture_path=None):
        self.set_position(x=start_x, y=start_y)

        self.set_texture(texture_path=texture_path)

    def set_position(self, x=None, y=None):
        if not x and not isinstance(x, int):
            random_x = random.randrange(CELL_SIZE, WIDTH_OF_CELLS * CELL_SIZE, CELL_SIZE)
            self.x = random_x

        else:
            self.x = x - (x % CELL_SIZE)

        if not y and not isinstance(x, int):
            random_y = random.randrange(CELL_SIZE, HEIGHT_OF_CELLS * CELL_SIZE, CELL_SIZE)
            self.y = random_y

        else:
            self.y = y - (y % CELL_SIZE)

    def set_texture(self, texture_path=None):
        if not texture_path:
            self.surface = pygame.image.load("sources\\textures\\error.png")

        else:
            self.surface = pygame.image.load(texture_path)

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))