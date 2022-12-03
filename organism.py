from food import Food
from helpers import Coordinate, Direction
from statistics import mean
from agent import Agent
from wall import Wall
from consts import Action, debug
import random
from PIL import ImageFont
from neural_network import NeuralNetwork, Neuron
import random
import numpy as np

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
        self.chance_to_turn = random.random()
        self.chance_to_wait = random.random()
        self.chance_to_move = random.random()
        self.brain = self.build_brain()
        self.use_brain = True
        self.current_weights = [self.chance_to_move, self.chance_to_turn, self.chance_to_wait]

    def build_brain(self):
        # Set the number of input, hidden, and output nodes
        num_inputs = 1
        num_hidden = 3
        num_outputs = 3

        # Create the hidden layer neurons
        hidden_layers = [
            # [Neuron([0, 0], 0) for _ in range(num_hidden)]
        ]

        # Create the output layer neurons with output layer weights and biases with value between -0.5 to 0.5
        output_layer = [
            Neuron(
                [random.uniform(-100, 100) for _ in range(num_inputs)],
                random.uniform(-100, 100)) for _ in range(num_outputs)]

        # Create the NeuralNetwork object
        return NeuralNetwork(hidden_layers, output_layer)

    def wait(self):
        return

    def turn(self):
        direction = 1 if random.choice([True, False]) else -1
        self.direction.x = direction if self.direction.x == 0 else 0
        self.direction.y = direction if self.direction.y == 0 else 0

    def get_thing_ahead(self, board) -> Agent:
        new_position = self.position.add(self.direction)
        return board[new_position.y, new_position.x]

    def move(self, board):
        thing_ahead = self.get_thing_ahead(board)
        if type(thing_ahead) == Wall or type(thing_ahead) == Organism and thing_ahead.is_alive:
            return
        self.position.x += self.direction.x
        self.position.y += self.direction.y

    def die(self):
        self.is_alive = False

    def get_brain_inputs(self, board):
        input_value = 0
        thing_ahead = self.get_thing_ahead(board)
        if type(thing_ahead) == Wall or type(thing_ahead) == Organism and thing_ahead.is_alive:
            input_value = -0.5
        elif type(thing_ahead) == Food and thing_ahead.is_alive:
            input_value = 0.5
        return [input_value]

    def update(self, board):
        if not self.is_alive:
            return
        self.memory.append({'pos': self.position, 'dir': self.direction, 'is_alive': self.is_alive})

        choices = [Action.MOVE, Action.TURN, Action.WAIT]
        weights = [self.chance_to_move,
                   self.chance_to_turn, self.chance_to_wait]
        if self.use_brain:
            weights = self.brain.forward_propagate(inputs=self.get_brain_inputs(
                board))
            # print(weights)
        self.current_weights = weights
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

    def get_fitness(self):
        return self.lifespan

    def eat(self, food: Food):
        self.lifespan += food.health_value
        food.get_eaten()

    def draw(self, d, input_to_img_ratio):
        fill = "white"
        fill = "rgb({})".format(", ".join([str(int(x * 250)) for x in self.current_weights]))
        if not self.is_alive:
            fill = "gray"
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
        if debug:
            stats = ', '.join([str(self.chance_to_move), str(self.chance_to_turn), str(self.chance_to_wait)])
            font = ImageFont.truetype("Helvetica.ttc", 14)
            d.text((x, y + 10), 'mtw: {}'.format(stats), font=font, stroke_width=0)
