import random
import time

import pygame

from settings import *

class Snake:
    def __init__(self, start_x=None, start_y=None):
        if not start_x and not start_y:
            random_start_x = random.randrange(CELL_SIZE, (WIDTH_OF_SCREEN + 1) - CELL_SIZE, CELL_SIZE)
            random_start_y = random.randrange(CELL_SIZE, (HEIGHT_OF_SCREEN + 1) - CELL_SIZE, CELL_SIZE)
            
            self.chunks = [pygame.Rect(random_start_x, random_start_y, CELL_SIZE, CELL_SIZE)]

            self._offset = pygame.math.Vector2(0, 0)
        
        else:
            pass

    def draw(self, screen):
        for chunk in self.chunks:
            pygame.draw.rect(screen, COLOUR_OF_SNAKE_CHUNK, chunk)

    def shift(self):
        self.chunks = [self.chunks[0].move(self._offset)] + self.chunks[:-1]

    def update(self):
        self.shift()

        if self.chunks[0].x >= WIDTH_OF_SCREEN:
            self.chunks[0].x = 0

        elif self.chunks[0].x < 0:
            self.chunks[0].x = WIDTH_OF_SCREEN

        elif self.chunks[0].y >= HEIGHT_OF_SCREEN:
            self.chunks[0].y = 0

        elif self.chunks[0].y < 0:
            self.chunks[0].y = HEIGHT_OF_SCREEN

    def set_offset(self, event):
        if event.key == pygame.K_UP:
            self._offset = pygame.math.Vector2(0, -CELL_SIZE)

        elif event.key == pygame.K_DOWN:
            self._offset = pygame.math.Vector2(0, +CELL_SIZE)

        elif event.key == pygame.K_RIGHT:
            self._offset = pygame.math.Vector2(+CELL_SIZE, 0)

        elif event.key == pygame.K_LEFT:
            self._offset = pygame.math.Vector2(-CELL_SIZE, 0)

    def add_chunk(self):
        self.chunks = [self.chunks[0].move(self._offset)] + self.chunks

    def __repr__(self):
        return f"(head_of_snake | X {self.chunks[0].x} | Y {self.chunks[0].y})"