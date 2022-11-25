from helpers import Coordinate

class Agent:
    def __init__(
        self,
        position: Coordinate
    ):
        if not type(position) == Coordinate:
            raise ValueError('Parameter position must be of type Coordinate.')
        self.position = position
        self.is_alive = True
