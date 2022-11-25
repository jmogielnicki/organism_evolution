import numpy as np
from agent import Agent

class Board:
    def __init__(self, size: tuple[int, int]) -> None:
        self.size = size
        self.board = np.empty(size, dtype=np.object_)

    def update(self, agents: list[Agent]):
        for agent in agents:
            self.board[agent.position.y, agent.position.x] = agent

    def draw(self, d, input_to_img_ratio):

