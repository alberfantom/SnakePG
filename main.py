import pygame, sys

import random, time

class Structure:
    def __init__(self, start_x=None, start_y=None, start_coordinates=None, texture_path=None):
        self.coordinates = pygame.math.Vector2(0, 0)

        self.set_texture(texture_path=texture_path)
        self.set_coordinates(x=start_x, y=start_y, coordinates=start_coordinates)

    def set_coordinates(self, x=None, y=None, coordinates=None) -> None:
        if not x and not isinstance(x, (int, float)):
            random_x = random.randrange(Field.cell_size, Field.width, Field.cell_size)
            self.coordinates.x = random_x

        else:
            # TODO: rounding x to the nearest, not to the minimum.
            self.coordinates.x = round(x, Field.cell_size)

        if not y and not isinstance(x, (int, float)):
            random_y = random.randrange(Field.cell_size, Field.height, Field.cell_size)
            self.coordinates.y = random_y

        else:
            # TODO: rounding y to the nearest, not to the minimum.
            self.coordinates.y = round(y, Field.cell_size)

        if not x and not y and coordinates:
            self.coordinates = pygame.math.Vector2(coordinates)

    def set_texture(self, texture_path=None):
        self.texture_path = texture_path

        if not texture_path:
            self.surface = pygame.image.load("sources\\textures\\error.png")

        else:
            self.surface = pygame.image.load(texture_path)
    
    def round(what: int, _at_step: int) -> int:
        at_step_average = int(_at_step / 2)

        if what % _at_step <= at_step_average - 1:            
            return what - (what % _at_step)

        else:
            return what + ((_at_step * (what // _at_step + 1)) - what)

    def is_collision(self, _with=None) -> bool:
        if self.coordinates == _with.coordinates:
            return True

        return False

    def copy(self):
        return Structure(start_x=self.coordinates.x, start_y=self.coordinates.y, texture_path=self.texture_path)

    def draw(self, surface):
        surface.blit(self.surface, self.coordinates)

class Apple(Structure):
    texture_paths = {
        "apple": "sources\\textures\\food.png"
    }

    def __init__(self, start_x=None, start_y=None, start_coordinates=None, texture_path=None):
        super().__init__(start_x=start_x, start_y=start_y, start_coordinates=start_coordinates, texture_path=texture_path)

    # TODO: make sure that the apple occupies a new place among the free ones, and does not go through the already occupied ones.
    def randomize_coordinates(self):
        self.set_coordinates(x=None, y=None)
        
        for obstacle in Field.get_instances_of(_class_name="Obstacle"):
            if obstacle.is_collision(_with=self):
                self.randomize_coordinates()

        for snake in Field.get_instances_of(_class_name="Snake"):
            for segment in snake.segments:
                if segment.is_collision(_with=self):
                    self.randomize_coordinates()
        
        for apple in Field.get_instances_of(_class_name="Apple"):
            if apple.is_collision(_with=self) and apple != self:
                self.randomize_coordinates()

class Obstacle(Structure):
    texture_paths = {
        "obstacle": "sources\\textures\\obstacle.png"
    }

    def __init__(self, start_x=None, start_y=None, start_coordinates=None, texture_path=None):
        super().__init__(start_x=start_x, start_y=start_y, start_coordinates=start_coordinates, texture_path=texture_path)

class Snake(Structure): 
    texture_paths = {
        "snake": "sources\\textures\\segment.png"
    }

    speed = 7 * 25 # in milliseconds 
    assert speed >= 25 and speed <= 250

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

        init_segment = Structure(start_x=init_segment_base.coordinates.x + random_offset.x, start_y=init_segment_base.coordinates.y + random_offset.y, texture_path=Snake.texture_paths["snake"])
        self.segments.append(init_segment)
    
        self._offset = (0, 0)
        self.is_static = False

    def get_random_offset(self):
        return random.choice(list(self._offsets.values()))
        
    def set_offset(self, event):
        match event.key:
            case pygame.K_UP:
                if self._offset != (0, Field.cell_size):
                    self._offset = pygame.math.Vector2(0, -(Field.cell_size))

            case pygame.K_LEFT:
                if self._offset != (Field.cell_size, 0):
                    self._offset = pygame.math.Vector2(-(Field.cell_size), 0)

            case pygame.K_DOWN:
                if self._offset != (0, -Field.cell_size):
                    self._offset = pygame.math.Vector2(0, +(Field.cell_size))
            
            case pygame.K_RIGHT:
                if self._offset != (-Field.cell_size, 0):
                    self._offset = pygame.math.Vector2(+(Field.cell_size), 0)

    def update_past_segments(self): 
        self.past_segments = [segment.copy() for segment in self.segments]

    def shift(self, add_segment=False):
        if not self.is_static and self._offset != (0, 0):
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
            for obstacle in Field.get_instances_of(_class_name="Obstacle"):
                for snake in Field.get_instances_of(_class_name="Snake"):
                    if obstacle.is_collision(_with=snake.segments[0]):
                        self.segments = self.past_segments
                        self.is_static = True

    def logic_at_the_segment(self):
        if not self.is_static:
            for segment in  self.segments[2:]:
                if self.segments[0].is_collision(_with=segment):
                    self.segments = self.past_segments
                    self.is_static = True
    
    def logic_at_the_border(self):
        if not self.is_static:
            if self.segments[0].coordinates.x == Field.width:
                self.segments[0].coordinates.x = 0

            elif self.segments[0].coordinates.x == -Field.cell_size:
                self.segments[0].coordinates.x = Field.width

            elif self.segments[0].coordinates.y == Field.height:
                self.segments[0].coordinates.y = 0

            elif self.segments[0].coordinates.y == -Field.cell_size:
                self.segments[0].coordinates.y = Field.height

    def logic_at_the_apple(self):
        if not self.is_static:
            for apple in Field.get_instances_of(_class_name="Apple"):
                if self.segments[0].is_collision(_with=apple):
                    apple.randomize_coordinates()

                    self.segments = self.past_segments
                    self.shift(add_segment=True)

    def logic_at_the_snake(self):
        for snake in Field.get_instances_of("Snake"):
            if snake != self:
                for segment in snake.segments:
                    if segment.is_collision(_with=self.segments[0]):
                        self.segments = self.past_segments
                        self.is_static = True

    def draw(self, surface):
        for segment in self.segments:
            surface.blit(segment.surface, segment.coordinates)

class Field:
    default_field = ["O O * * * * * O O",
                     "O * * * * * * * O",
                     "* * * * A * * * *",
                     "* * * * * * * * *",
                     "* * * * * * * * *",
                     "* * * * * * * * *",
                     "* * * * * * * * *",
                     "O * * * S * * * O",
                     "O O * * * * * O O"]

    for row in range(len(default_field)):
        default_field[row] = default_field[row].replace(" ", "")

    structures_of_map = [("O", "obstacle", Obstacle),
                         ("S", "snake", Snake),
                         ("A", "apple", Apple)]

    structures = dict()

    cell_size = 32
    average_cell_size = cell_size / 2

    height = len(default_field) * cell_size
    width = len(default_field[0]) * cell_size

    def get_instances_of(_class_name: str = None) -> list:
        _class_name = _class_name.lower()

        if f"{_class_name}s" in Field.structures:
            return list(Field.structures[f"{_class_name}s"].values()) 

        elif _class_name in Field.structures:
            return [ Field.structures[_class_name] ]
        
        return [ ]

    def __init__(self, init_field=default_field):
        for row in range(len(init_field)):
            for column in range(len(init_field[0])):
                designation = init_field[row][column]

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

    def draw(self, screen=None, structures=None) -> None:
        for structure in structures.values():
            if isinstance(structure, dict):
                self.draw(screen=screen, structures=structure)

            elif isinstance(structure, Structure):
                structure.draw(surface=screen)

class Game:
    caption = "Snake"
    fps = 75 * 5

    def __init__(self):
        pygame.init()

        self.field = Field()

        pygame.display.set_caption(Game.caption)
        self.screen = pygame.display.set_mode((Field.width, Field.height))
        self.clock = pygame.time.Clock()

        self.snake_shift_event = pygame.USEREVENT
        pygame.time.set_timer(self.snake_shift_event, Snake.speed)

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
                    
                    for snake in Field.get_instances_of(_class_name="Snake"):
                        if not snake.is_static:
                            snake.set_offset(event)
                
                elif event.type == pygame.USEREVENT:
                    for snake in Field.get_instances_of(_class_name="Snake"):
                        snake.shift()

                        snake.logic_at_the_obstacle()
                        snake.logic_at_the_segment()
                        snake.logic_at_the_border()
                        snake.logic_at_the_apple()
                        snake.logic_at_the_snake()

            self.field.draw(screen=self.screen, structures=Field.structures)

            self.clock.tick(Game.fps)
            pygame.display.update()
            self.screen.fill((0, 0, 0))

if __name__ == "__main__":
    game = Game()
    game.loop_with_logic()