class Organism:
    def __init__(self, position: tuple[int, int]):
        self.position = position

    def update(self):
        if self.position > 100:
            self.position -= 1
        if self.position < 1:
            self.position += 1
