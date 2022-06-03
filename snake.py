import random
import time

import pygame

from settings import *

class Snake:
    def __init__(self, start_x=None, start_y=None):   
        self.is_static = False

        if not start_x and not start_y:
            random_start_x = random.randrange(CELL_SIZE, WIDTH_OF_CELLS * CELL_SIZE, CELL_SIZE)
            random_start_y = random.randrange(CELL_SIZE, HEIGHT_OF_CELLS * CELL_SIZE, CELL_SIZE)
            
            self.chunks = [pygame.Rect(random_start_x, random_start_y, CELL_SIZE, CELL_SIZE)]

            self._temp_offset = pygame.math.Vector2(0, 0)
            self._offset = pygame.math.Vector2(0, 0)

        
        else:
            pass

    def draw(self, screen):
        for chunk in self.chunks:
            pygame.draw.rect(screen, COLOUR_OF_SNAKE_CHUNK, chunk)

    def shift(self):
        self.chunks = [self.chunks[0].move(self._offset)] + self.chunks[:-1]

    def update(self):
        if not self.is_static:
            self.shift()

            if self.chunks[0].x >= WIDTH_OF_CELLS * CELL_SIZE:
                self.chunks[0].x = 0

            elif self.chunks[0].x < 0:
                self.chunks[0].x = WIDTH_OF_CELLS * CELL_SIZE

            elif self.chunks[0].y >= HEIGHT_OF_CELLS * CELL_SIZE:
                self.chunks[0].y = 0

            elif self.chunks[0].y < 0:
                self.chunks[0].y = HEIGHT_OF_CELLS * CELL_SIZE

            for chunk in self.chunks[2:]:
                if chunk.topleft == self.chunks[0].topleft:
                    self.chunks[0].move_ip(self._offset * -1)
                    self.is_static = True

    def set_offset(self, event):
        if event.key == pygame.K_UP:
            self._temp_offset = pygame.math.Vector2(0, -CELL_SIZE)

        elif event.key == pygame.K_DOWN:
            self._temp_offset = pygame.math.Vector2(0, +CELL_SIZE)

        elif event.key == pygame.K_RIGHT:
            self._temp_offset = pygame.math.Vector2(+CELL_SIZE, 0)

        elif event.key == pygame.K_LEFT:
            self._temp_offset = pygame.math.Vector2(-CELL_SIZE, 0)

        if len(self.chunks) > 1:
            if self.chunks[0].move(self._temp_offset).topleft != self.chunks[1].topleft:
                self._offset = self._temp_offset

        else:
            self._offset = self._temp_offset

    def add_chunk(self):
        self.chunks = [self.chunks[0].move(self._offset)] + self.chunks

    def __repr__(self):
        return f"(head_of_snake | X {self.chunks[0].x} | Y {self.chunks[0].y})"