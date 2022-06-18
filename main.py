import struct
import pygame, sys

import random, time

class Structure:
    # TODO: start_x: int, start_y: int and coordinates: Vector2.
    def __init__(self, start_x=None, start_y=None, texture_path=None):
        self.coordinates = pygame.math.Vector2(0, 0)

        self.set_texture(texture_path=texture_path)
        self.set_coordinates(x=start_x, y=start_y)

    # TODO: start_x: int, start_y: int and coordinates: Vector2.
    def set_coordinates(self, x=None, y=None):
        if not x and not isinstance(x, (int, float)):
            random_x = random.randrange(Field._cell_size, Field.width, Field._cell_size)
            self.coordinates.x = random_x

        else:
            # TODO: rounding x to the nearest, not to the minimum.
            self.coordinates.x = x - (x % Field._cell_size)

        if not y and not isinstance(x, (int, float)):
            random_y = random.randrange(Field._cell_size, Field.height, Field._cell_size)
            self.coordinates.y = random_y

        else:
            # TODO: rounding y to the nearest, not to the minimum.
            self.coordinates.y = y - (y % Field._cell_size)

    def set_texture(self, texture_path=None):
        self.texture_path = texture_path

        if not texture_path:
            self.surface = pygame.image.load("sources\\textures\\error.png")

        else:
            self.surface = pygame.image.load(texture_path)
    
    def copy(self):
        return Structure(start_x=self.coordinates.x, start_y=self.coordinates.y, texture_path=self.texture_path)
    
    def is_collision(self, _with=None):
        if _with:
            if self.coordinates == _with.coordinates:
                return True
            
            return False

    def draw(self, surface):
        surface.blit(self.surface, self.coordinates)

class Apple(Structure):
    def __init__(self, start_x=None, start_y=None, texture_path=None, field=None):
        super().__init__(start_x=start_x, start_y=start_y, texture_path=texture_path)
        self.field = field

    def randomize_coordinates(self):
        self.set_coordinates(x=None, y=None)

        for name_of_obstacle, obstacle in self.field.structures["obstacles"].items():
            if self.is_collision(_with=obstacle):
                self.randomize_coordinates()

        if self.is_collision(_with=self.field.structures["snake"].segments[0]):
            self.randomize_coordinates()

class Obstacle(Structure):
    def __init__(self, start_x=None, start_y=None, texture_path=None, field=None):
        super().__init__(start_x=start_x, start_y=start_y, texture_path=texture_path)
        field = field

class Snake(Structure):
    # TODO: from 1 to 10 (for example)
    velocity_in_millsecond = 175

    # TODO: appears from two segments.
    def __init__(self, start_x=None, start_y=None, texture_path=None, field=None):
        self.field = field

        self.segments = list()

        init_segment = Structure(start_x=start_x, start_y=start_y, texture_path=texture_path)
        self.segments.append(init_segment)
        
        self._offset = pygame.math.Vector2(0, 0)
        
    def set_offset(self, event):
        # TODO: adjust to two segments.
        if event.key == pygame.K_UP:
            self._offset = pygame.math.Vector2(0, -(Field._cell_size))

        elif event.key == pygame.K_LEFT:
            self._offset = pygame.math.Vector2(-(Field._cell_size), 0)

        elif event.key == pygame.K_DOWN:
            self._offset = pygame.math.Vector2(0, +(Field._cell_size))

        elif event.key == pygame.K_RIGHT:
            self._offset = pygame.math.Vector2(+(Field._cell_size), 0)

    def shift(self, add_segment=False):
        copy_segment = self.segments[0].copy()
        copy_segment.coordinates += self._offset

        if add_segment:
            self.segments = [copy_segment] + self.segments

        else:
            self.segments = [copy_segment] + self.segments[:-1]

    def draw(self, surface):
        for segment in self.segments:
            surface.blit(segment.surface, segment.coordinates)

class Field:
    init_map = ["O O O * * * * O O O",
                "O * * * * * * * * O",
                "O * * * * S * * * O",
                "* * * * * * * * * *",
                "* * * * A * * * * *",
                "* * * * * * * * * *",
                "O * * * * * * * * O",
                "O * * * * * * * * O",
                "O O O * * * * O O O"]

    # TODO: structure and structures, obstacle and not obstacales, but obstacles (just example). 
    structures = [("O", "obstacle", Obstacle),
                  ("S", "snake", Snake),
                  ("A", "apple", Apple)]

    for row in range(len(init_map)):
        init_map[row] = init_map[row].replace(" ", "")

    _cell_size = 32

    height = len(init_map) * _cell_size
    width = len(init_map[0]) * _cell_size
    
    def __init__(self):
        self.structures = dict()

        for row in range(len(Field.init_map)):
            for column in range(len(Field.init_map[0])):
                designation = Field.init_map[row][column]

                for short_name_of_structure, full_name_of_structure, class_of_structure in Field.structures:
                    if short_name_of_structure == designation:
                        structure = class_of_structure(start_x=column * Field._cell_size, start_y=row * Field._cell_size, texture_path="sources\\textures\\obstacle.png", field=self)

                        if not self.structures.get(full_name_of_structure) and not self.structures.get(f"{full_name_of_structure}s"):
                            self.structures[full_name_of_structure] = structure
                            self.structures[full_name_of_structure].number = 0

                        elif self.structures.get(full_name_of_structure) and not self.structures.get(f"{full_name_of_structure}s"):  
                            self.structures[f"{full_name_of_structure}s"] = dict()
        
                            structure0 = self.structures.pop(full_name_of_structure)
                            self.structures[f"{full_name_of_structure}s"][f"{full_name_of_structure}{structure0.number}"] = structure0

                            structure.number = structure0.number + 1
                            self.structures[f"{full_name_of_structure}s"][f"{full_name_of_structure}{structure.number}"] = structure

                        elif not self.structures.get(full_name_of_structure) and self.structures.get(f"{full_name_of_structure}s"):
                            structure.number = list(self.structures[f"{full_name_of_structure}s"].values())[-1].number + 1
                            self.structures[f"{full_name_of_structure}s"][f"{full_name_of_structure}{structure.number}"] = structure
                        
                        break

    def draw(self, surface):
        # TODO: recursion.
        for level0_key, level0_value in self.structures.items():
            if isinstance(level0_value, dict):
                for level1_key, level1_value in level0_value.items():
                    level1_value.draw(surface)

            else:
                level0_value.draw(surface)

class Game:
    caption = "Snake"
    fps = 75

    def __init__(self):
        pygame.init()

        self.field = Field()

        pygame.display.set_caption(Game.caption)
        self.screen = pygame.display.set_mode((self.field.width, self.field.height))
        self.clock = pygame.time.Clock()

        self.snake_shift_event = pygame.USEREVENT
        pygame.time.set_timer(self.snake_shift_event, Snake.velocity_in_millsecond)

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
                    
                    self.field.structures["snake"].set_offset(event)
                
                elif event.type == pygame.USEREVENT:
                    if self.field.structures["apple"].coordinates != self.field.structures["snake"].segments[0].coordinates + self.field.structures["snake"]._offset:
                        self.field.structures["snake"].shift(add_segment=False)
                    
                    else:
                        self.field.structures["snake"].shift(add_segment=True)
                        self.field.structures["apple"].randomize_coordinates()

            self.field.draw(self.screen)

            self.clock.tick(Game.fps)
            pygame.display.update()
            self.screen.fill((0, 0, 0))

if __name__ == "__main__":
    game = Game()
    game.loop_with_logic()