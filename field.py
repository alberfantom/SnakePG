from snake_segment_base import SnakeSegmentBase
from obstacle import Obstacle
from apple import Apple

class Field:
    init_map = ["* * * * *",
                "* A * * *",
                "* * * * *",
                "* * * S *",
                "* * * * *"]

    for row in range(len(init_map)):
        init_map[row] = init_map[row].replace(" ", "")

    cell_size = 32

    width = len(init_map) * cell_size
    height = len(init_map[0]) * cell_size
    
    def __init__(self):
        for row in range(len(Field.init_map)):
            for column in range(len(Field.init_map[0])):
                designation = Field.init_map[row][column]

                if designation == "S":
                    self.snake_segment_base = None
                
                elif designation == "O":
                    self.obstacle = None

                elif designation == "A":
                    self.apple = None

field = Field()

# print(field.snake_segment_base)
# print(field.obstacle)
# print(field.apple)
