import random

import pygame

from settings import *

class Structure:
    def __init__(self, start_x=None, start_y=None, texture_url=None):
        if not start_x and not isinstance(start_x, int):
            random_start_x = random.randrange(CELL_SIZE, WIDTH_OF_CELLS * CELL_SIZE, CELL_SIZE)
            self.x = random_start_x

        else:
            self.x = start_x - (start_x % CELL_SIZE)

        if not start_y and not isinstance(start_x, int):
            random_start_y = random.randrange(CELL_SIZE, HEIGHT_OF_CELLS * CELL_SIZE, CELL_SIZE)
            self.y = random_start_y

        else:
            self.y = start_y - (start_y % CELL_SIZE)

        if not texture_url:
            self.surface = pygame.image.load("sources\\textures\\error.png")

        else:
            self.surface = pygame.image.load(texture_url)

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))