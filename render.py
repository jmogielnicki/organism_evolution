from food import Food
from board import Board
from helpers import Coordinate
from image import create_image, open_image, clear_images
from video import make_video, open_video
from consts import (
    num_ticks_per_generation,
    num_organisms,
    num_food,
    num_generations,
    lifespan,
    mutation_rate,
    food_value
)
import sys
import random
import time

start = time.time()

mutation_rate = mutation_rate / 1000

# initialize organisms and food
board = Board(
    (100, 100),
    num_organisms,
    num_food,
    lifespan,
    mutation_rate,
    food_value
)
# generation = Generation(num_organisms, board)

# prepare files
if "-nc" not in sys.argv:
    clear_images()

for generation_num in range(num_generations):
    # loop through the number of ticks that make up a generation and create an image
    for i in range(num_ticks_per_generation):
        # render the organisms
        if "-ni" not in sys.argv and generation_num == num_generations - 1:
            print('building image {}...'.format(i))
            create_image(
                board,
                i)

        # update the organisms
        board.update()
    board.start_next_generation()

# create the video
if "-v" in sys.argv and "-ni" not in sys.argv:
    print('building video...')
    make_video()
    open_video()

if "-o" in sys.argv:
    open_image()

end = time.time()
print('time elapsed: ', end - start)
