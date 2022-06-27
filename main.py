import pygame, sys

import random, time

# TODO: generalized is_collision (Structure.is_collision())
class Structure:
    # TODO: start_x: int, start_y: int and coordinates: Vector2.
    def __init__(self, start_x=None, start_y=None, start_coordinates=None, texture_path=None):
        self.coordinates = pygame.math.Vector2(0, 0)

        self.set_texture(texture_path=texture_path)
        self.set_coordinates(x=start_x, y=start_y, coordinates=start_coordinates)

    # TODO: start_x: int, start_y: int and coordinates: Vector2.
    def set_coordinates(self, x=None, y=None, coordinates=None) -> None:
        if not x and not isinstance(x, (int, float)):
            random_x = random.randrange(Field.cell_size, Field.width, Field.cell_size)
            self.coordinates.x = random_x

        else:
            # TODO: rounding x to the nearest, not to the minimum.
            self.coordinates.x = x - (x % Field.cell_size)

        if not y and not isinstance(x, (int, float)):
            random_y = random.randrange(Field.cell_size, Field.height, Field.cell_size)
            self.coordinates.y = random_y

        else:
            # TODO: rounding y to the nearest, not to the minimum.
            self.coordinates.y = y - (y % Field.cell_size) 

        if not x and not y and coordinates:
            self.coordinates = pygame.math.Vector2(coordinates)

    def set_texture(self, texture_path=None):
        self.texture_path = texture_path

        if not texture_path:
            self.surface = pygame.image.load("sources\\textures\\error.png")

        else:
            self.surface = pygame.image.load(texture_path)
    
    def copy(self):
        return Structure(start_x=self.coordinates.x, start_y=self.coordinates.y, texture_path=self.texture_path)
    
    def is_collision(self, _with=None) -> bool:
        if self.coordinates == _with.coordinates:
            return True

        return False

    def draw(self, surface):
        surface.blit(self.surface, self.coordinates)

class Apple(Structure):
    texture_paths = {
        "apple": None
    }

    def __init__(self, start_x=None, start_y=None, start_coordinates=None, texture_path=None):
        super().__init__(start_x=start_x, start_y=start_y, start_coordinates=start_coordinates, texture_path=texture_path)

    def randomize_coordinates(self):
        self.set_coordinates(x=None, y=None)

        for obstacle in Field.structures["obstacles"].values():
            if self.is_collision(_with=obstacle):
                self.randomize_coordinates()

        for segment in Field.structures["snake"].segments:
            if self.is_collision(_with=segment):
                self.randomize_coordinates()

class Obstacle(Structure):
    texture_paths = {
        "obstacle": None
    }

    def __init__(self, start_x=None, start_y=None, start_coordinates=None, texture_path=None):
        super().__init__(start_x=start_x, start_y=start_y, start_coordinates=start_coordinates, texture_path=texture_path)

class Snake(Structure): 
    texture_paths = {
        "snake": None,
        "segment": None
    }

    # TODO: from 1 to 10 (for example)
    velocity = 175 # in millsecond

    def __init__(self, start_x=None, start_y=None, start_coordinates=None, texture_path=None):
        self._offsets = {
            "up": pygame.math.Vector2(0, +1 * Field.cell_size),
            "right": pygame.math.Vector2(+1 * Field.cell_size, 0),
            "down": pygame.math.Vector2(0, -1 * Field.cell_size),
            "left": pygame.math.Vector2(-1 * Field.cell_size, 0)
        }

        self.segments = list()
        self.past_segments = list()

        random_offset = self.get_random_offset()

        init_segment_base = Structure(start_coordinates=start_coordinates, texture_path=texture_path)
        self.segments.append(init_segment_base)

        init_segment = Structure(start_x=init_segment_base.coordinates.x + random_offset.x, start_y=init_segment_base.coordinates.y + random_offset.y, texture_path=Snake.texture_paths["segment"])
        self.segments.append(init_segment)
        
        # self._offset change to tuple data type (not Vector2).
        self._offset = pygame.math.Vector2(0, 0)
        self.is_static = False

    def get_random_offset(self):
        return random.choice(list(self._offsets.values()))
        
    def set_offset(self, event):
        # TODO: adjust to two segments.
        if event.key == pygame.K_UP and self._offset != (0, Field.cell_size):
            self._offset = pygame.math.Vector2(0, -(Field.cell_size))

        elif event.key == pygame.K_LEFT and self._offset != (Field.cell_size, 0):
            self._offset = pygame.math.Vector2(-(Field.cell_size), 0)

        elif event.key == pygame.K_DOWN and self._offset != (0, -Field.cell_size):
            self._offset = pygame.math.Vector2(0, +(Field.cell_size))

        elif event.key == pygame.K_RIGHT and self._offset != (-Field.cell_size, 0):
            self._offset = pygame.math.Vector2(+(Field.cell_size), 0)

    def update_past_segments(self): 
        self.past_segments = [segment.copy() for segment in self.segments]

    def shift(self, add_segment=False):
        if not self.is_static and self._offset.xy != (0, 0):
            self.update_past_segments()
            
            self.segments.reverse()

            if add_segment:
                copy_segment = self.segments[0].copy()

            for index in range(len(self.segments)):
                if index == len(self.segments) - 1:
                    self.segments[index].coordinates += self._offset

                else:
                    self.segments[index].coordinates = self.segments[index + 1].coordinates.xy

            if add_segment:
                self.segments.insert(0, copy_segment)

            self.segments.reverse()

    def logic_at_the_obstacle(self):
        if not self.is_static:
            for obstacle in Field.structures["obstacles"].values():
                if obstacle.is_collision(_with=Field.structures["snake"].segments[0]):
                    self.segments = self.past_segments
                    self.is_static = True


    def logic_at_the_segment(self):
        if not self.is_static:
            for segment in  self.segments[2:]:
                if  self.segments[0].is_collision(_with=segment):
                    self.segments = self.past_segments
                    self.is_static = True
    
    def logic_at_the_border(self):
        if not self.is_static:
            if  self.segments[0].coordinates.x == Field.width:
                self.segments[0].coordinates.x = 0

            elif  self.segments[0].coordinates.x == -Field.cell_size:
                self.segments[0].coordinates.x = Field.width

            elif  self.segments[0].coordinates.y == Field.height:
                self.segments[0].coordinates.y = 0

            elif  self.segments[0].coordinates.y == -Field.cell_size:
                self.segments[0].coordinates.y = Field.height

    def logic_at_the_apple(self):
        if not self.is_static:
            if self.segments[0].is_collision(_with=Field.structures["apple"]):
                Field.structures["apple"].randomize_coordinates()
                self.shift(add_segment=True)

    def draw(self, surface):
        for segment in self.segments:
            surface.blit(segment.surface, segment.coordinates)

class Field:
    # TODO: what will the second segment do, if there is an apple next to it.
    init_map = ["O O * * * * * O O",
                "O * * * * * * * O",
                "* * * * * * * * *",
                "* * * * A * * * *",
                "* * * * * * * * *",
                "* * * * S * * * *",
                "* * * * * * * * *",
                "O * * * * * * * O",
                "O O * * * * * O O"]

    for row in range(len(init_map)):
        init_map[row] = init_map[row].replace(" ", "")

    structures_of_map = [("O", "obstacle", Obstacle),
                         ("S", "snake", Snake),
                         ("A", "apple", Apple)]

    structures = dict()

    cell_size = 32

    height = len(init_map) * cell_size
    width = len(init_map[0]) * cell_size
    
    def __init__(self):
        # TODO: self.structures (dict) into Field.structures (dict).
        for row in range(len(Field.init_map)):
            for column in range(len(Field.init_map[0])):
                designation = Field.init_map[row][column]

                for short_name_of_structure, full_name_of_structure, class_of_structure in Field.structures_of_map:
                    if short_name_of_structure == designation:
                        structure = class_of_structure(start_coordinates=(column * Field.cell_size, row * Field.cell_size), texture_path=class_of_structure.texture_paths[full_name_of_structure])

                        if not Field.structures.get(full_name_of_structure) and not Field.structures.get(f"{full_name_of_structure}s"):
                            Field.structures[full_name_of_structure] = structure
                            Field.structures[full_name_of_structure].number = 0

                        elif Field.structures.get(full_name_of_structure) and not Field.structures.get(f"{full_name_of_structure}s"):  
                            Field.structures[f"{full_name_of_structure}s"] = dict()
        
                            structure0 = Field.structures.pop(full_name_of_structure)
                            Field.structures[f"{full_name_of_structure}s"][f"{full_name_of_structure}{structure0.number}"] = structure0

                            structure.number = structure0.number + 1
                            Field.structures[f"{full_name_of_structure}s"][f"{full_name_of_structure}{structure.number}"] = structure

                        elif not Field.structures.get(full_name_of_structure) and Field.structures.get(f"{full_name_of_structure}s"):
                            structure.number = list(Field.structures[f"{full_name_of_structure}s"].values())[-1].number + 1
                            Field.structures[f"{full_name_of_structure}s"][f"{full_name_of_structure}{structure.number}"] = structure
                        
                        break

    def draw(self, surface):
        # TODO: recursion.
        for level0_key, level0_value in Field.structures.items():
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
        self.screen = pygame.display.set_mode((Field.width, Field.height))
        self.clock = pygame.time.Clock()

        self.snake_shift_event = pygame.USEREVENT
        pygame.time.set_timer(self.snake_shift_event, Snake.velocity)

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
                    
                    if not Field.structures["snake"].is_static:
                        Field.structures["snake"].set_offset(event)
                
                # TODO: update method for snake.
                elif event.type == pygame.USEREVENT:
                    self.field.structures["snake"].shift()

                    self.field.structures["snake"].logic_at_the_obstacle()
                    self.field.structures["snake"].logic_at_the_segment()
                    self.field.structures["snake"].logic_at_the_border()
                    self.field.structures["snake"].logic_at_the_apple()

            self.field.draw(self.screen)

            self.clock.tick(Game.fps)
            pygame.display.update()
            self.screen.fill((0, 0, 0))

if __name__ == "__main__":
    game = Game()
    game.loop_with_logic()

# TODO: GOD MODE