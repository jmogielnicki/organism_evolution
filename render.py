from population import Population
from image import create_image, open_image, clear_images
from video import make_video, open_video
import sys

# initialize a population
population = Population(100)

# loop through number of ticks that make up each organisms life
num_ticks_per_life = 40

if "nc" not in sys.argv:
    clear_images()

for i in range(num_ticks_per_life):
    # render the organisms
    create_image(population, i)

    # update the organisms
    population.update()

# create the video
if "v" in sys.argv:
    make_video()
    open_video()

if "o" in sys.argv:
    open_image()
