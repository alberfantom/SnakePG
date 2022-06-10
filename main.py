import pygame, sys

import random

class Structure:
    def __init__(self, start_x=None, start_y=None, texture_path=None):
        self.coordinates = pygame.math.Vector2(0, 0)

        self.set_texture(texture_path=texture_path)
        self.set_position(x=start_x, y=start_y)

    def set_position(self, x=None, y=None):
        if not x and not isinstance(x, int):
            random_x = random.randrange(Field._cell_size, Field.width, Field._cell_size)
            self.coordinates.x = random_x

        else:
            # TODO: rounding x to the nearest, not to the minimum.
            self.coordinates.x = x - (x % Field._cell_size)

        if not y and not isinstance(x, int):
            random_y = random.randrange(Field._cell_size, Field.height, Field._cell_size)
            self.coordinates.y = random_y

        else:
            # TODO: rounding y to the nearest, not to the minimum.
            self.coordinates.y = y - (y % Field._cell_size)

    def set_texture(self, texture_path=None):
        if not texture_path:
            # TODO: 32x32, but not 16x16
            self.surface = pygame.image.load("sources\\textures\\error.png")

        else:
            self.surface = pygame.image.load(texture_path)
    
    def draw(self, surface):
        surface.blit(self.surface, self.coordinates)

class Apple(Structure):
    def __init__(self, start_x=None, start_y=None, texture_path=None):
        super().__init__(start_x=start_x, start_y=start_y, texture_path=texture_path)

class Obstacle(Structure):
    def __init__(self, start_x=None, start_y=None, texture_path=None):
        super().__init__(start_x=start_x, start_y=start_y, texture_path=texture_path)

class Snake:
    class SegmentBase(Structure):
        def __init__(self, start_x=None, start_y=None, texture_path=None):
            super().__init__(start_x=start_x, start_y=start_y, texture_path=texture_path)
            
            self._offset = pygame.math.Vector2(0, 0)

        def set_offset(self, event):
            if event.key == pygame.K_UP:
                self._offset = pygame.math.Vector2(0, +Field._cell_size)

            elif event.key == pygame.K_LEFT:
                self._offset = pygame.math.Vector2(-Field._cell_size, 0)

            elif event.key == pygame.K_DOWN:
                self._offset = pygame.math.Vector2(0, -Field._cell_size)

            elif event.key == pygame.K_RIGHT:
                self._offset = pygame.math.Vector2(+Field._cell_size, 0)

        def shift(self):
            pass

        def update(self):
            pass

    class Segment(Structure):
        def __init__(self, start_x=None, start_y=None, texture_path=None):
            super().__init__(self, start_x=start_x, start_y=start_y, texture_path=texture_path)

    def __init__(self, start_x=None, start_y=None, texture_path=None):
        self.segment_base = Snake.SegmentBase(start_x=start_x, start_y=start_y, texture_path=texture_path)
    
    def draw(self, surface):
        surface.blit(self.segment_base.surface, self.segment_base.coordinates)

class Field:
    init_map = ["O O * O O",
                "O * * * O",
                "* * A * *",
                "* * * S *",
                "* * * * *"]

    for row in range(len(init_map)):
        init_map[row] = init_map[row].replace(" ", "")

    _cell_size = 32

    width = len(init_map) * _cell_size
    height = len(init_map[0]) * _cell_size
    
    def __init__(self):
        self.obstacles = list()

        self.apple = None
        self.snake = None

        for row in range(len(Field.init_map)):
            for column in range(len(Field.init_map[0])):
                designation = Field.init_map[row][column]

                if designation == "O":
                    self.obstacles.append(Obstacle(start_x=column * Field._cell_size, start_y=row * Field._cell_size, texture_path=None))

                elif designation == "A":
                    self.apple = Apple(start_x=column * Field._cell_size, start_y=row * Field._cell_size, texture_path=None)

                elif designation == "S":
                    self.snake = Snake(start_x=column * Field._cell_size, start_y=row * Field._cell_size, texture_path=None)

    def draw(self, surface):
        if self.obstacles:
            for obstacle in self.obstacles:
                obstacle.draw(surface)

        if self.apple:
            self.apple.draw(surface)

        if self.snake:
            self.snake.draw(surface)

class Game:
    caption = "Snake"

    def __init__(self):
        pygame.init()

        self.field = Field()

        pygame.display.set_caption(Game.caption)
        self.screen = pygame.display.set_mode((self.field.width, self.field.height))

    def loop_with_logic(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    
                    self.field.snake.segment_base.set_offset(event)


            self.field.draw(self.screen)

            pygame.display.update()
            self.screen.fill((0, 0, 0))

if __name__ == "__main__":
    game = Game()
    game.loop_with_logic()
