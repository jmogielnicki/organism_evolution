from generation import Generation
from food import Food
from helpers import Coordinate
from image import create_image, open_image, clear_images
from video import make_video, open_video
import sys
import random

num_organisms = 100
num_food = 10
num_ticks_per_generation = 100

# initialize organisms and food
generation = Generation(num_organisms)
food = [Food(Coordinate(random.randint(0, 100), random.randint(0, 100))) for i in range(num_food)]

# prepare files
if "nc" not in sys.argv:
    clear_images()

# loop through the number of ticks that make up a generation and create an image
for i in range(num_ticks_per_generation):
    # render the organisms
    if "skip_images" not in sys.argv:
        print('building image {}...'.format(i))
        create_image(
            generation,
            food,
            i)

    # update the organisms
    generation.update()

# create the video
if "v" in sys.argv:
    print('building video...')
    make_video()
    open_video()

if "o" in sys.argv:
    open_image()
