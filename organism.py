from food import Food
from helpers import Coordinate, Direction
from statistics import mean
from agent import Agent
from wall import Wall
from consts import Action
import random

class Organism(Agent):
    def __init__(
        self,
        position: Coordinate,
        direction: Direction,
        lifespan: int,
    ):
        super().__init__(position)
        self.direction = direction
        self.memory = []
        self.age = 0
        self.original_lifespan = lifespan
        self.lifespan = lifespan
        self.chance_to_turn = random.randint(0, 100)
        self.chance_to_wait = random.randint(0, 100)
        self.chance_to_move = random.randint(0, 100)

    def wait(self):
        return

    def turn(self):
        direction = 1 if random.choice([True, False]) else -1
        self.direction.x = direction if self.direction.x == 0 else 0
        self.direction.y = direction if self.direction.y == 0 else 0

    def move(self, board):
        new_position = self.position.add(self.direction)
        thing_ahead = board[new_position.y, new_position.x]
        # print(thing_ahead)
        if type(thing_ahead) == Wall or type(thing_ahead) == Organism and thing_ahead.is_alive:
            # print("blocked")
            return
        # if self.position.x < 99 and self.position.x > 0:
        self.position.x += self.direction.x
        # if self.position.y < 99 and self.position.y > 0:
        self.position.y += self.direction.y

    def die(self):
        self.is_alive = False

    def update(self, board):
        if not self.is_alive:
            return
        self.memory.append((self.position, self.direction))
        choices = [Action.MOVE, Action.TURN, Action.WAIT]
        weights = (self.chance_to_move, self.chance_to_turn, self.chance_to_wait)
        choices = random.choices(choices, weights=weights, k=1)
        choice = choices[0]
        if choice == Action.TURN:
            self.turn()
        elif choice == Action.MOVE:
            self.move(board)
        elif choice == Action.WAIT:
            self.wait()

        if self.age > self.lifespan:
            self.die()
        self.age += 1

    def eat(self, food: Food):
        self.lifespan += food.health_value
        food.get_eaten()

    def draw(self, d, input_to_img_ratio):
        fill = "white" if self.is_alive else "gray"
        buffer = int(input_to_img_ratio / 4)
        x = self.position.x * input_to_img_ratio
        y = self.position.y * input_to_img_ratio
        x2 = x + input_to_img_ratio - 1
        y2 = y + input_to_img_ratio - 1
        x_middle = mean([x, x2])
        y_middle = mean([y, y2])
        d.rectangle(
            [x, y, x2, y2],
            fill=fill,
            outline=None,
            width=0)
        # TODO - fix this terribly convoluted drawing logic
        d.rectangle(
            [
                x_middle + (buffer if self.direction.x == 0 else 0),
                y_middle + (buffer if self.direction.y == 0 else 0),
                (
                    x if self.direction.x == -1
                    else x2 if self.direction.x == 1
                    else x_middle - (buffer if self.direction.x == 0 else 0)),
                (
                    y if self.direction.y == -1
                    else y2 if self.direction.y == 1
                    else y_middle - (buffer if self.direction.y == 0 else 0))
            ],
            fill="black",
            outline=None,
            width=0)
