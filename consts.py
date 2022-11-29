from helpers import get_argument
from enum import Enum

num_ticks_per_generation = get_argument('t', 100)
num_organisms = get_argument('o', 100)
num_food = get_argument('f', 20)
lifespan = get_argument('ls', 30)
fps = get_argument('fps', 30)
num_generations = get_argument('g', 10)
mutation_rate = get_argument('mr', 1)
food_value = get_argument('fv', 10)


class Action(Enum):
    MOVE = 1
    TURN = 2
    WAIT = 3
