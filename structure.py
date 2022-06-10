import random

import pygame

from field import Field

class Structure:
    def __init__(self, start_x=None, start_y=None, texture_path=None):
        self.coordinates = pygame.math.Vector2(0, 0)

        self.set_texture(texture_path=texture_path)
        self.set_position(x=start_x, y=start_y)

    def set_position(self, x=None, y=None):
        if not x and not isinstance(x, int):
            random_x = random.randrange(Field.cell_size, Field.width, Field.cell_size)
            self.coordinates.x = random_x

        else:
            # TODO: rounding x to the nearest, not to the minimum.
            self.coordinates.x = x - (x % Field.cell_size)

        if not y and not isinstance(x, int):
            random_y = random.randrange(Field.cell_size, Field.height, Field.cell_size)
            self.coordinates.y = random_y

        else:
            # TODO: rounding y to the nearest, not to the minimum.
            self.coordinates.y = y - (y % Field.cell_size)

    def set_texture(self, texture_path=None):
        if not texture_path:
            self.surface = pygame.image.load("sources\\textures\\error.png")

        else:
            self.surface = pygame.image.load(texture_path)

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))