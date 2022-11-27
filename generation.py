from board import Board
from organism import Organism
from helpers import Coordinate, Direction, get_random_direction
import random


class Generation:
    def __init__(self, quantity: int, board: Board):
        self.quantity = quantity
        self.members: list[Organism] = []
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
                20
            ))

    def breed(self):
        surviving_members = [x for x in self.members if x.is_alive]
        self.members = []
        random.shuffle(surviving_members)
        for i in range(self.quantity):
            parent_a = random.choice(surviving_members)
            parent_b = random.choice(surviving_members)
            direction_x, direction_y = get_random_direction()
            child = Organism(
                self.board.get_random_open_position(),
                Direction(direction_x, direction_y),
                100
            )
            child.chance_to_turn = int((parent_a.chance_to_turn + parent_b.chance_to_turn) / 2)
            self.members.append(child)
