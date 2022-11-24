from population import Population
from image import create_image
from video import make_video

# initialize a population
population = Population(10)

# loop through number of ticks that make up each organisms life
num_ticks_per_life = 100

for i in range(num_ticks_per_life):
    # render the organisms
    create_image(population, i)

    # update the organisms
    population.update()

# create the video
make_video()