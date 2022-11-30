from board import Board
from helpers import clear_all_files_in_directory, debug_print
from image import create_image, open_image, clear_images
from video import make_videos, open_videos
from consts import (
    num_ticks_per_generation,
    num_organisms,
    num_food,
    num_generations,
    lifespan,
    mutation_rate,
    food_value,
    logs_file_location,
    generations_to_render,
    LAST_GENERATION_KEY
)
import sys
import time

start = time.time()

############
# step 1: prepare files
############
if "-nc" not in sys.argv:
    clear_images()
clear_all_files_in_directory(logs_file_location)


############
# step 2: run the simulation
############
board = Board(
    (100, 100),
    num_organisms,
    num_food,
    lifespan,
    mutation_rate,
    food_value
)

for generation_num in range(num_generations):
    should_render = "-ni" not in sys.argv and (
        str(generation_num) in generations_to_render or (
            LAST_GENERATION_KEY in generations_to_render and generation_num == num_generations - 1)
    )
    debug_print('start generation{}'.format(generation_num))
    if should_render:
        print('building images for generation {}...'.format(generation_num))
    # loop through the number of ticks that make up a generation and create an image
    for i in range(num_ticks_per_generation):
        # render the organisms
        if should_render:
            create_image(
                board,
                generation_num,
                i)

        # update the organisms
        board.update()
    board.start_next_generation()

############
# step 3: create video
############
if "-v" in sys.argv and "-ni" not in sys.argv:
    print('building video...')
    make_videos()
    open_videos()

if "-o" in sys.argv:
    open_image()

end = time.time()
print('time elapsed: ', end - start)
