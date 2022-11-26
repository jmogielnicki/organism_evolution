import numpy as np
from organism import Organism
from food import Food

class Board:
    def __init__(self, size: tuple[int, int], organisms: list[Organism], food: list[Food]) -> None:
        self.size = size
        self.board = np.empty(size, dtype=np.object_)
        self.players = organisms
        self.food = food

    def update(self):
        for player in self.players + self.food:
            self.board[player.position.y, player.position.x] = player

    def draw(self, d, input_to_img_ratio):
        for player in self.players:
            player.draw(d, input_to_img_ratio)
        for peice in self.food:
            peice.draw(d, input_to_img_ratio)
