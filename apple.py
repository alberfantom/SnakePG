import random

import pygame

from structure import Structure

from settings import *

class Apple(Structure):
    def __init__(self, start_x=None, start_y=None, texture_path=None, snake=None):
        super().__init__(start_x=start_x, start_y=start_y, texture_path=texture_path)

        self.snake = snake
        
    def is_collision(self):
        if self.snake.chunks[0].x == self.x:
            if self.snake.chunks[0].y == self.y:
                return True

    def update(self):
        if self.is_collision():
            self.randomize_position()

            self.snake.add_chunk()

    def randomize_position(self):
        self.x = random.randrange(CELL_SIZE, WIDTH_OF_CELLS * CELL_SIZE, CELL_SIZE)
        self.y = random.randrange(CELL_SIZE, HEIGHT_OF_CELLS * CELL_SIZE, CELL_SIZE)

    def __repr__(self):
        return f"apple | X {self.x} | Y {self.y}"