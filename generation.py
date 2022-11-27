from board import Board
from organism import Organism
from helpers import Coordinate, Direction, get_random_direction
import random


class Generation:
    def __init__(self, quantity: int, board: Board):
        self.quantity = quantity
        self.members = []
        self.board = board
        self.generate()

    def generate(self):
        for i in range(self.quantity):
            x = random.randint(0, 99)
            y = random.randint(0, 99)
            direction_x, direction_y = get_random_direction()
            self.members.append(Organism(
                self.board.get_random_open_position(),
                Direction(direction_x, direction_y),
                random.randint(20, 40)
            ))
