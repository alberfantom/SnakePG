import sys
import random

import pygame

from settings import *

from apple import Apple
from snake import Snake

class Game: 
    def __init__(self):
        pygame.init()
        
        self.clock = pygame.time.Clock()
        
        self.snake = Snake()
        self.apple = Apple(start_x=None, start_y=None, texture_path="sources\\textures\\apple.png", snake=self.snake)

        self.apple.snake = self.snake
        self.snake.apple = self.apple

        userevent = pygame.USEREVENT
        pygame.time.set_timer(userevent, VELOCITY_OF_SNAKE)

        self.screen = pygame.display.set_mode((WIDTH_OF_CELLS * CELL_SIZE, HEIGHT_OF_CELLS * CELL_SIZE))
        pygame.display.set_caption("Snake")

    def logic_with_loop(self):  
        self.is_active = True    
        while self.is_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    
                    # define offset for movement
                    self.snake.set_offset(event)
    
                elif event.type == pygame.USEREVENT:
                    self.snake.update()

            self.apple.update()
            self.apple.draw(self.screen)
            
            self.snake.draw(self.screen)

            pygame.display.update()
            self.screen.fill(COLOUR_OF_BACKGROUND)
            self.clock.tick(FPS)
    
    def stop_loop(self):
        self.is_active = False

if __name__ == "__main__":
    game = Game()
    game.logic_with_loop()