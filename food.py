from helpers import Coordinate
from agent import Agent
from statistics import mean

class Food(Agent):
    def __init__(self, position: Coordinate, health_value: int):
        super().__init__(position)
        self.health_value = health_value

    def draw(self, d, input_to_img_ratio):
        fill = "green" if self.is_alive else "gray"
        x = self.position.x * input_to_img_ratio
        y = self.position.y * input_to_img_ratio
        x2 = x + input_to_img_ratio - 1
        y2 = y + input_to_img_ratio - 1
        x_middle = mean([x, x2])
        y_middle = mean([y, y2])
        d.rectangle(
            [x_middle - 2, y_middle - 2, x_middle + 2, y_middle + 2],
            fill=fill,
            outline=None,
            width=0)

    def get_eaten(self):
        self.is_alive = False
