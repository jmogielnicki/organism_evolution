from generation import Generation
from food import Food
from board import Board
from helpers import Coordinate
from image import create_image, open_image, clear_images
from video import make_video, open_video
from consts import num_ticks_per_generation, num_organisms, num_food
import sys
import random
import time

start = time.time()

# initialize organisms and food
board = Board((100, 100))
generation = Generation(num_organisms, board)
food = [
    Food(
        board.get_random_open_position(),
        10
    )
    for i in range(num_food)
]

board.place_organisms(generation.members)
board.place_food(food)

# prepare files
if "-nc" not in sys.argv:
    clear_images()

# loop through the number of ticks that make up a generation and create an image
for i in range(num_ticks_per_generation):
    # render the organisms
    if "-ni" not in sys.argv:
        print('building image {}...'.format(i))
        create_image(
            board,
            i)

    # update the organisms
    board.update()

# create the video
if "-v" in sys.argv and "-ni" not in sys.argv:
    print('building video...')
    make_video()
    open_video()

if "-o" in sys.argv:
    open_image()

end = time.time()
print('time elapsed: ', end - start)
