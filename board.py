import numpy as np
from helpers import Coordinate
from organism import Organism
from food import Food
from wall import Wall

class Board:
    def __init__(self, size: tuple[int, int], organisms: list[Organism], food: list[Food]) -> None:
        self.size = size
        self.board = np.empty(size, dtype=np.object_)
        self.players = organisms
        self.food = food
        self.walls = self.generate_walls()

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
        for player in self.players:
            player.update()
            self.board[player.position.y, player.position.x] = player
            for peice in self.food:
                if peice.position == player.position:
                    peice.get_eaten()
        for peice in [each for each in self.food if each.is_alive]:
            self.board[peice.position.y, peice.position.x] = peice

    def draw(self, d, input_to_img_ratio):
        for player in self.players:
            player.draw(d, input_to_img_ratio)
        for peice in [each for each in self.food if each.is_alive]:
            peice.draw(d, input_to_img_ratio)
        for wall in self.walls:
            wall.draw(d, input_to_img_ratio)