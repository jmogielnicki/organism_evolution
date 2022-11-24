from helpers import Coordinate, Direction
from statistics import mean

class Organism:
    def __init__(self, position: Coordinate, direction: Direction):
        if not type(position) == Coordinate:
            raise ValueError('Parameter position must be of type Coordinate.')
        self.position = position

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
        d.rectangle(
            [x, y, x2, y2],
            fill="white",
            outline=None,
            width=0)
        d.line(
            [mean([x, x2]), mean([y, y2]), mean([x, x2]), y2],
            fill="black",
            width=2
        )