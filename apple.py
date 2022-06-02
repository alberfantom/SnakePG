import random

import pygame

from settings import *

class Apple:
    def __init__(self, snake=None, start_x=None, start_y=None):
        if not start_x and not start_y:
           random_start_x = random.randrange(CELL_SIZE, (WIDTH_OF_SCREEN + 1) - CELL_SIZE, CELL_SIZE)
           random_start_y = random.randrange(CELL_SIZE, (HEIGHT_OF_SCREEN + 1) - CELL_SIZE, CELL_SIZE)

           self.rect = pygame.Rect(random_start_x, random_start_y, CELL_SIZE, CELL_SIZE)

        else:
            pass 

    def draw(self, screen):
        pygame.draw.rect(screen, COLOUR_OF_APPLE, self.rect)
        # print(f"Apple | X {self.rect.x} | Y {self.rect.y}")
        
    def is_collision(self):
        if self.snake.chunks[0].x == self.rect.x:
            if self.snake.chunks[0].y == self.rect.y:
                return True

    def update(self):
        if self.is_collision():
            self.randomize_position()

            self.snake.add_chunk()

    def randomize_position(self):
        self.rect.x = random.randrange(CELL_SIZE, WIDTH_OF_SCREEN - CELL_SIZE, CELL_SIZE)
        self.rect.y = random.randrange(CELL_SIZE, HEIGHT_OF_SCREEN - CELL_SIZE, CELL_SIZE)

    def __repr__(self):
        return f"apple | X {self.x} | Y {self.y}"