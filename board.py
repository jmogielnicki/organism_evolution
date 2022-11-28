import random
import numpy as np
from helpers import Coordinate, Direction, get_random_direction
from organism import Organism
from food import Food
from wall import Wall

class Board:
    def __init__(
        self,
        size: tuple[int, int],
        num_players: int,
        num_food: int,
        lifespan: int,
        mutation_rate: float
    ) -> None:
        self.size = size
        self.board = np.empty(size, dtype=np.object_)
        self.starting_board = np.copy(self.board)
        self.walls = self.generate_walls()
        self.num_players = num_players
        self.num_food = num_food
        self.mutation_rate = mutation_rate
        self.players = []
        self.food = []
        self.lifespan = lifespan
        # add walls to the board
        for wall in self.walls:
            self.starting_board[wall.position.y, wall.position.x] = wall
            self.board[wall.position.y, wall.position.x] = wall
        self.place_organisms(num_players)
        self.place_food(num_food)

    def place_organisms(self, num_players):
        for i in range(num_players):
            direction_x, direction_y = get_random_direction()
            self.players.append(Organism(
                self.get_random_open_position(),
                Direction(direction_x, direction_y),
                self.lifespan
            ))

    def place_food(self, num_food: int):
        self.food = [
            Food(
                self.get_random_open_position(),
                20
            )
            for i in range(num_food)
        ]

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
        starting_board = np.copy(self.board)
        self.board = np.copy(self.starting_board)  # start with a clean board
        for player in self.players:  # add players at their new locations to the board
            player.update(starting_board)
            self.board[player.position.y, player.position.x] = player
            for peice in self.food:  # if a player is on top of food, eat it
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

    def log_stats(self):
        # import pdb; pdb.set_trace()
        surviving_members = [x for x in self.players if x.is_alive is True]
        num_surviving = len(surviving_members)
        max_prob_turn = max(member.chance_to_turn for member in surviving_members)
        min_prob_turn = min(member.chance_to_turn for member in surviving_members)
        print(min_prob_turn, max_prob_turn, num_surviving)
        f = open("logs/output_logs.txt", "a")
        f.write("\nnum surviving: {}".format(num_surviving))

    def start_next_generation(self):
        self.log_stats()
        self.breed()
        self.place_food(self.num_food)

    def breed(self):
        surviving_members = [x for x in self.players if x.is_alive is True]
        self.players = []
        random.shuffle(surviving_members)
        for i in range(self.num_players):
            parent_a = random.choice(surviving_members)
            parent_b = random.choice(surviving_members)
            direction_x, direction_y = get_random_direction()
            child = Organism(
                self.get_random_open_position(),
                Direction(direction_x, direction_y),
                self.lifespan
            )
            child.chance_to_turn = int((parent_a.chance_to_turn + parent_b.chance_to_turn) / 2)
            if self.mutation_rate > random.uniform(0, 1.0):
                child.chance_to_turn += random.randint(-10, 10)
            self.players.append(child)
