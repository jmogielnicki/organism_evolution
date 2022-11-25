from generation import Generation
from image import create_image, open_image, clear_images
from video import make_video, open_video
import sys

# initialize a population
generation = Generation(100)

# loop through number of ticks that make up each organisms life
num_ticks_per_generation = 40

if "nc" not in sys.argv:
    clear_images()

for i in range(num_ticks_per_generation):
    # render the organisms
    if "skip_images" not in sys.argv:
        print('building image {}...'.format(i))
        create_image(generation, i)

    # update the organisms
    generation.update()

# create the video
if "v" in sys.argv:
    print('building video...')
    make_video()
    open_video()

if "o" in sys.argv:
    open_image()
