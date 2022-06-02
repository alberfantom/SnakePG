import sys
import random

import pygame

from settings import *

from apple import Apple
from snake import Snake

class WindowOfGame: 
    def __init__(self):
        pygame.init()
        
        self.clock = pygame.time.Clock()
        
        self.snake = Snake()
        self.apple = Apple()

        self.apple.snake = self.snake
        self.snake.apple = self.apple

        userevent = pygame.USEREVENT
        pygame.time.set_timer(userevent, VELOCITY_OF_SNAKE)

        self.screen = pygame.display.set_mode((WIDTH_OF_SCREEN - (WIDTH_OF_SCREEN % CELL_SIZE), (HEIGHT_OF_SCREEN - (HEIGHT_OF_SCREEN % CELL_SIZE))))
        print(self.screen.get_width())
        self.logic_with_loop()

    def logic_with_loop(self):
        while True:
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

WindowOfGame()