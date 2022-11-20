class Organism:
    def __init__(self, position: dict[str, int]):
        self.position = position

    def update(self):
        if self.position.get("x", 0) > 100:
            self.position.x -= 1
        if self.position[0] < 1:
            self.position[0] += 1
