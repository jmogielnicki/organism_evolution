import random
import glob
import shutil
import os
import consts
import numpy as np

class Direction:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Coordinate:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def add(self, other: Direction):
        x = self.x + other.x
        y = self.y + other.y
        return Coordinate(x, y)

def get_random_direction():
    facing_up_down = random.choice([True, False])
    direction = -1 if random.choice([True, False]) else 1
    x = direction if not facing_up_down else 0
    y = direction if facing_up_down else 0
    return [x, y]

def clear_all_folders_in_directory(filepath):
    for dir_path in get_items_in_directory(filepath):
        try:
            shutil.rmtree(dir_path)
        except OSError as e:
            print("Error: %s : %s" % (dir_path, e.strerror))

def clear_all_files_in_directory(filepath):
    for file in get_items_in_directory(filepath):
        os.remove(file)

def get_items_in_directory(file_path):
    return glob.glob('{}*'.format(file_path))

def debug_print(string):
    if consts.debug:
        print(string)

def get_random_neuron_weights(num_weights):
    return [np.random.uniform(
        consts.neuron_weight_lower_bound,
        consts.neuron_weight_upper_bound
    ) for _ in range(num_weights)]

def get_random_neuron_bias():
    return np.random.uniform(
        consts.neuron_bias_lower_bound,
        consts.neuron_bias_upper_bound
    )

def normalize(value, min, max):
    # Figure out how 'wide' each range is
    span = max - min

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - min) / float(span)
    return valueScaled