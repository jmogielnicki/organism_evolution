import random
from statistics import mean
import numpy as np
import pandas as pd
import json
from helpers import Coordinate, Direction, get_random_direction
from organism import Organism
from food import Food
from wall import Wall
from consts import (
    logs_file_location,
    Action,
    organism_logs_file_location,
    use_brain,
    should_log,
    action_choices,
    neuron_weight_lower_bound,
    neuron_weight_upper_bound,
    neuron_bias_lower_bound,
    neuron_bias_upper_bound
)

class Board:
    def __init__(
        self,
        size: tuple[int, int],
        num_players: int,
        num_food: int,
        lifespan: int,
        mutation_rate: float,
        food_value: int,
        num_ticks_per_generation: int,
    ) -> None:
        self.size = size
        self.num_ticks_per_generation = num_ticks_per_generation
        self.board = np.empty(size, dtype=np.object_)
        self.starting_board = np.copy(self.board)
        self.walls = self.generate_walls()
        self.num_players = num_players
        self.num_food = num_food
        self.mutation_rate = mutation_rate
        self.players = []
        self.food = []
        self.food_value = food_value
        self.lifespan = lifespan
        # add walls to the board
        for wall in self.walls:
            self.starting_board[wall.position.y, wall.position.x] = wall
            self.board[wall.position.y, wall.position.x] = wall
        self.place_organisms(num_players)
        self.place_food(num_food)
        self.generation_number = 0
        self.log_data = []

    def place_organisms(self, num_players):
        for i in range(num_players):
            direction_x, direction_y = get_random_direction()
            new_player = Organism(
                self.get_random_open_position(),
                Direction(direction_x, direction_y),
                self.lifespan,
                use_brain=use_brain
            )
            self.players.append(new_player)
            self.board[new_player.position.y, new_player.position.x] = new_player

    def place_food(self, num_food: int):
        for i in range(num_food):
            new_food = Food(
                self.get_random_open_position(),
                self.food_value
            )
            self.food.append(new_food)
            self.board[new_food.position.y, new_food.position.x] = new_food

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
        board_snapshot = np.copy(self.board)  # this is used to figure out if a player has something in it's way
        self.board = np.copy(self.starting_board)  # start with a clean board
        for player in self.players:  # add players at their new locations to the board
            player.update(board_snapshot)
            self.board[player.position.y, player.position.x] = player
            for peice in [x for x in self.food if x.is_alive]:  # if a player is on top of food, eat it
                if peice.position.x == player.position.x and peice.position.y == player.position.y:
                    player.eat(peice)
        for peice in [x for x in self.food if x.is_alive]:  # place the remaining alive food
            self.board[peice.position.y, peice.position.x] = peice

    def get_random_open_position(self) -> Coordinate:
        # see https://numpy.org/devdocs/user/absolute_beginners.html#indexing-and-slicing
        open_positions = np.nonzero(self.board == None)  # noqa: E711
        selection_index = random.randint(0, len(open_positions[0]) - 1)
        y = open_positions[0][selection_index]
        x = open_positions[1][selection_index]
        return Coordinate(x, y)

    def draw(self, d, input_to_img_ratio):
        # occupied_spaces = self.board[self.board != None]  # noqa: E711
        # for item in occupied_spaces:
        #     item.draw(d, input_to_img_ratio)
        for wall in self.walls:
            wall.draw(d, input_to_img_ratio)
        for peice in [each for each in self.food if each.is_alive]:
            peice.draw(d, input_to_img_ratio)
        for player in self.players:
            player.draw(d, input_to_img_ratio)

    def toJSON(self, obj):
        return json.dumps(
            obj,
            default=lambda o: str(o) if isinstance(o, np.int64) or isinstance(o, np.ndarray) else o.__dict__,  # type: ignore
            sort_keys=True)

    def log_stats(self):
        eaters = [x for x in self.players if x.fitness > 1]
        num_eaters = len(eaters)
        avg_prob_turn = sum(member.chance_to_turn for member in eaters) / len(eaters)
        avg_prob_move = sum(member.chance_to_move for member in eaters) / len(eaters)
        avg_prob_wait = sum(member.chance_to_wait for member in eaters) / len(eaters)
        average_fitness = mean([x.fitness for x in self.players])
        columns = ['weight_' + str(x) for x in action_choices] + \
            ['bias_' + str(x) for x in action_choices] + ['fitness']
        stats = []
        for player in self.players:
            # TODO - weights[0] will only get the first weight for each output neuron.
            # Once we have multiple inputs this will break
            weights = [neuron.weights[0] for neuron in player.brain.output_layer]
            biases = [neuron.bias for neuron in player.brain.output_layer]
            fitness = player.fitness
            stats.append([weights[0], weights[1], weights[2],biases[0], biases[1], biases[2], fitness])
        df = pd.DataFrame(stats, columns=columns)
        if should_log:
            print(df.describe(percentiles=[.5], include='all').transpose())
        log_string = ' '.join(
            ['tmw: ', str(round(avg_prob_turn, 2)), str(round(avg_prob_move, 2)), str(round(avg_prob_wait, 2)),
             ' avg fitness: ', str(average_fitness), ' num_surv: ', str(num_eaters)])
        print(log_string)
        if should_log:
            f = open(logs_file_location, "a")
            f.write("\n{}".format(log_string))
            f.close()
            stuff_to_log = {
                'gen': self.generation_number,
                'players': self.players,
                'food': self.food,
                'walls': self.walls
            }
            self.log_data.append(stuff_to_log)
            f2 = open(organism_logs_file_location, "a")
            f2.write("\n{}".format(self.toJSON(stuff_to_log)))
            f2.close()

    def start_next_generation(self):
        self.log_stats()
        self.board = np.empty(self.size, dtype=np.object_)
        self.starting_board = np.copy(self.board)
        # add walls to the board
        for wall in self.walls:
            self.starting_board[wall.position.y, wall.position.x] = wall
            self.board[wall.position.y, wall.position.x] = wall
        self.breed()
        self.food = []
        self.place_food(self.num_food)
        self.generation_number += 1

    def breed(self):
        use_brain = self.players[0].use_brain
        new_players = []
        player_fitnesses = [x.fitness for x in self.players]

        for i in range(self.num_players):
            direction_x, direction_y = get_random_direction()
            child = Organism(
                self.get_random_open_position(),
                Direction(direction_x, direction_y),
                self.lifespan,
                use_brain=use_brain
            )

            parent_a, parent_b = random.choices(self.players, player_fitnesses, k=2)
            # print(parent_a.fitness, parent_b.fitness)

            if use_brain:
                # create the new hybrid output layer with weights and biases
                for i in range(len(child.brain.output_layer)):

                    # select a random parent to donate the base neuron
                    chosen_parent = random.choice([parent_a, parent_b])

                    # apply the neuron of that parent, including bias and weights
                    child.brain.output_layer[i] = chosen_parent.brain.output_layer[i]

                    # optionally mutate by averaging the value with a random value within the min/max bounds
                    if self.mutation_rate > random.uniform(0, 1.0):
                        child.brain.output_layer[i].bias = mean([
                            child.brain.output_layer[i].bias,
                            random.uniform(
                                neuron_bias_lower_bound, neuron_bias_upper_bound)
                        ])

                    # iterate over weights and select from either parent a or b
                    for weight_idx in range(len(child.brain.output_layer[i].weights)):
                        chosen_parent = random.choice([parent_a, parent_b])
                        child.brain.output_layer[i].weights[weight_idx] = chosen_parent.brain.output_layer[i].weights[weight_idx]
                        if self.mutation_rate > random.uniform(0, 1.0):

                            # optionally mutate by averaging the value with a random value within the min/max bounds
                            child.brain.output_layer[i].weights[weight_idx] = mean([
                                child.brain.output_layer[i].weights[weight_idx],
                                random.uniform(neuron_weight_lower_bound, neuron_weight_upper_bound)
                            ])
            else:
                child.chance_to_turn = random.choice([parent_a.chance_to_turn, parent_b.chance_to_turn])
                child.chance_to_move = random.choice([parent_a.chance_to_move, parent_b.chance_to_move])
                child.chance_to_wait = random.choice([parent_a.chance_to_wait, parent_b.chance_to_wait])
                if self.mutation_rate > random.uniform(0, 1.0):
                    actions = [Action.MOVE, Action.TURN, Action.WAIT]
                    chosen_action = random.choice(actions)
                    child.chance_to_turn = min(child.chance_to_turn + 0.5, 1) if chosen_action == Action.TURN else 0
                    child.chance_to_move = min(child.chance_to_move + 0.5, 1) if chosen_action == Action.MOVE else 0
                    child.chance_to_wait = min(child.chance_to_wait + 0.5, 1) if chosen_action == Action.WAIT else 0

            new_players.append(child)
            self.board[child.position.y, child.position.x] = child
        self.players = new_players
