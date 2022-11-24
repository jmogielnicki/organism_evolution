from helpers import Coordinate, Direction
from statistics import mean

class Organism:
    def __init__(self, position: Coordinate, direction: Direction):
        if not type(position) == Coordinate:
            raise ValueError('Parameter position must be of type Coordinate.')
        self.position = position
        self.direction = direction

    def update(self):
        if self.position.x < 99:
            self.position.x += 1
        if self.position.y < 1:
            self.position.y += 1

    def draw(self, d, input_to_img_ratio):
        x = self.position.x * input_to_img_ratio
        y = self.position.y * input_to_img_ratio
        x2 = x + input_to_img_ratio - 1
        y2 = y + input_to_img_ratio - 1
        x_middle = mean([x, x2])
        y_middle = mean([y, y2])
        print(x, y, x2, y2, x_middle, y_middle)
        print(self.direction.x, self.direction.y)
        print(x_middle + (self.direction.x * input_to_img_ratio), y_middle + (self.direction.y * input_to_img_ratio))
        d.rectangle(
            [x, y, x2, y2],
            fill="white",
            outline=None,
            width=0)
        d.rectangle(
            [
                x_middle + (1 if self.direction.x == 0 else 0),
                y_middle + (1 if self.direction.y == 0 else 0),
                x_middle + (self.direction.x * (input_to_img_ratio / 2)) - (1 if self.direction.x == 0 else 0),
                y_middle + (self.direction.y * (input_to_img_ratio / 2)) - (1 if self.direction.y == 0 else 0)
            ],
            fill="red",
            outline=None,
            width=0)
        # d.line(
        #     [
        #         x_middle,
        #         y_middle,
        #         x_middle + self.direction.x * input_to_img_ratio,
        #         y_middle + self.direction.y * input_to_img_ratio
        #     ],
        #     fill="black",
        #     width=int(input_to_img_ratio / 2) + 1
        # )
