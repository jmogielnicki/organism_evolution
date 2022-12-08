from food import Food
from helpers import Coordinate, Direction
from statistics import mean
from agent import Agent
from wall import Wall
from consts import (
    Action,
    debug,
    neuron_bias_lower_bound,
    neuron_bias_upper_bound,
    neuron_weight_lower_bound,
    neuron_weight_upper_bound,
    action_choices)
import random
from PIL import ImageFont
from neural_network import NeuralNetwork, Neuron
import numpy as np
import copy

class Organism(Agent):
    def __init__(
        self,
        position: Coordinate,
        direction: Direction,
        lifespan: int,
        use_brain
    ):
        super().__init__(position)
        self.direction = direction
        self.last_direction = copy.deepcopy(direction)
        self.last_position = copy.deepcopy(position)
        self.memory = []
        self.age = 0
        self.original_lifespan = lifespan
        self.lifespan = lifespan
        self.fitness = 1
        self.chance_to_turn = random.random()
        self.chance_to_wait = random.random()
        self.chance_to_move = random.random()
        self.brain = self.build_brain()
        self.use_brain = use_brain
        self.current_weights = [self.chance_to_move, self.chance_to_turn, self.chance_to_wait]

    def build_brain(self):
        # Set the number of inputs, hidden layer shape, and output nodes
        num_inputs = 1
        hidden_layer_shape = []
        num_outputs = 3
        shape = [num_inputs] + hidden_layer_shape + [num_outputs]

        return NeuralNetwork(shape)

    def wait(self):
        return

    def turn(self):
        direction = 1 if random.choice([True, False]) else -1
        self.direction.x = direction if self.direction.x == 0 else 0
        self.direction.y = direction if self.direction.y == 0 else 0

    def get_thing_ahead(self, board) -> Agent:
        new_position = self.position.add(self.direction)
        return board[new_position.y, new_position.x]

    def get_things_ahead(self, board):
        row_ids = [self.position.y + i for i in range(-1, 2)]
        column_ids = [self.position.x + i for i in range(-1, 2)]

        clipped_row_ids = np.clip(row_ids, 0, board.shape[0] - 1)
        clipped_column_ids = np.clip(column_ids, 0, board.shape[1] - 1)

        idx = np.ix_(clipped_row_ids, clipped_column_ids)

        selected_elements = board[idx]
        return selected_elements.flatten()

    def move(self, board):
        thing_ahead = self.get_thing_ahead(board)
        if type(thing_ahead) == Wall or type(thing_ahead) == Organism and thing_ahead.is_alive:
            return
        self.position.x += self.direction.x
        self.position.y += self.direction.y

    def die(self):
        self.is_alive = False

    def get_brain_inputs(self, board):
        input_values = []
        # things_ahead = self.get_things_ahead(board)
        things_ahead = [self.get_thing_ahead(board)]
        for thing_ahead in things_ahead:
            input_value = 0
            if type(thing_ahead) == Wall or type(thing_ahead) == Organism and thing_ahead.is_alive:
                input_value = -0.5
            elif type(thing_ahead) == Food and thing_ahead.is_alive:
                input_value = 0.5
            input_values.append(input_value)
        return input_values

    def decide(self, board):
        if not self.is_alive:
            return
        weights = [self.chance_to_move,
                   self.chance_to_turn, self.chance_to_wait]
        if self.use_brain:
            weights = self.brain.forward_propagate(inputs=self.get_brain_inputs(
                board))
        self.current_weights = weights
        # print(weights)
        choices = random.choices(action_choices, weights=weights, k=1)
        decision = choices[0]
        return decision

    def update(self, board):
        if not self.is_alive:
            return
        self.last_position.x = self.position.x
        self.last_position.y = self.position.y
        self.last_direction.x = self.direction.x
        self.last_direction.y = self.direction.y

        self.memory.append({'pos': self.position, 'dir': self.direction, 'is_alive': self.is_alive})
        choice = self.decide(board)
        if choice == Action.TURN:
            self.turn()
        elif choice == Action.MOVE:
            self.move(board)
        elif choice == Action.WAIT:
            self.wait()

        # if self.age > self.lifespan:
        #     self.die()
        self.age += 1

    def eat(self, food: Food):
        self.lifespan += food.health_value
        self.fitness += food.health_value
        food.get_eaten()

    def draw(self, d, input_to_img_ratio):
        fill = "white"
        fill = "rgb({})".format(", ".join([str(int(x * 250)) for x in self.current_weights]))
        # print(self.current_weights, fill)
        if not self.is_alive:
            fill = "gray"
        buffer = int(input_to_img_ratio / 4)
        x = self.last_position.x * input_to_img_ratio
        y = self.last_position.y * input_to_img_ratio
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
                x_middle + (buffer if self.last_direction.x == 0 else 0),
                y_middle + (buffer if self.last_direction.y == 0 else 0),
                (
                    x if self.last_direction.x == -1
                    else x2 if self.last_direction.x == 1
                    else x_middle - (buffer if self.last_direction.x == 0 else 0)),
                (
                    y if self.last_direction.y == -1
                    else y2 if self.last_direction.y == 1
                    else y_middle - (buffer if self.last_direction.y == 0 else 0))
            ],
            fill="black",
            outline=None,
            width=0)
        if debug:
            stats = ', '.join([str(self.chance_to_move), str(self.chance_to_turn), str(self.chance_to_wait)])
            font = ImageFont.truetype("Helvetica.ttc", 14)
            d.text((x, y + 10), 'mtw: {}'.format(stats), font=font, stroke_width=0)
