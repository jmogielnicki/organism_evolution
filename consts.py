from enum import Enum
import sys

logs_file_location = 'logs/output_logs.txt'
LAST_GENERATION_KEY = 'last'

def get_argument_int(argument_string: str, default_value: int):
    value = int(next((x.split("=")[1] for x in sys.argv if "{}=".format(argument_string) in x), default_value))
    return value

def get_argument_list(argument_string: str, default_value: str):
    input = next((x.split("=")[1] for x in sys.argv if "{}=".format(argument_string) in x), default_value)
    values = input.split(",")
    print(values)
    return values

num_ticks_per_generation = get_argument_int('t', 100)
num_organisms = get_argument_int('o', 100)
num_food = get_argument_int('f', 20)
lifespan = get_argument_int('ls', 30)
fps = get_argument_int('fps', 30)
num_generations = get_argument_int('g', 10)
mutation_rate = get_argument_int('mr', 1)
food_value = get_argument_int('fv', 10)
debug = get_argument_int('db', 0)
generations_to_render = get_argument_list('rg', LAST_GENERATION_KEY)


class Action(Enum):
    MOVE = 1
    TURN = 2
    WAIT = 3
