import random
import numpy as np
from helpers import Coordinate
from organism import Organism
from food import Food
from wall import Wall

class Board:
    def __init__(self, size: tuple[int, int]) -> None:
        self.size = size
        self.board = np.empty(size, dtype=np.object_)
        self.starting_board = np.copy(self.board)
        self.walls = self.generate_walls()
        self.players = []
        self.food = []
        # add walls to the board
        for wall in self.walls:
            self.starting_board[wall.position.y, wall.position.x] = wall
            self.board[wall.position.y, wall.position.x] = wall

    def place_organisms(self, organisms: list[Organism]):
        self.players = organisms

    def place_food(self, food: list[Food]):
        self.food = food

    def generate_walls(self):
        walls = []
        for i in range(self.size[0]):
            walls.append(Wall(Coordinate(0, i)))
            walls.append(Wall(Coordinate(self.size[1] - 1, i)))
        for i in range(self.size[1]):
            walls.append(Wall(Coordinate(i, 0)))
            walls.append(Wall(Coordinate(i, self.size[0] - 1)))
        return walls

    def update(self):
        # TODO - it may be bad for performance to copy the array each update cycle.  Consider refactoring.
        self.board = np.copy(self.starting_board)
        for player in self.players:
            player.update(self)
            self.board[player.position.y, player.position.x] = player
            for peice in self.food:
                if peice.position.x == player.position.x and peice.position.y == player.position.y:
                    peice.get_eaten()
                    player.eat(peice)
        for peice in self.food:
            self.board[peice.position.y, peice.position.x] = peice

    def get_item_at_position(self, position: Coordinate):
        return self.board[position.y, position.x]

    def get_random_open_position(self) -> Coordinate:
        # see https://numpy.org/devdocs/user/absolute_beginners.html#indexing-and-slicing
        open_positions = np.nonzero(self.board == None)  # noqa: E711
        selection_index = random.randint(0, len(open_positions[0]))
        y = open_positions[0][selection_index]
        x = open_positions[1][selection_index]
        return Coordinate(x, y)

    def draw(self, d, input_to_img_ratio):
        # occupied_spaces = self.board[self.board != None]  # noqa: E711
        # for item in occupied_spaces:
        #     item.draw(d, input_to_img_ratio)
        for player in self.players:
            player.draw(d, input_to_img_ratio)
        for peice in [each for each in self.food if each.is_alive]:
            peice.draw(d, input_to_img_ratio)
        for wall in self.walls:
            wall.draw(d, input_to_img_ratio)
