import sys

# num_ticks_per_generation = int(sys.argv[1]) if sys.argv[1].isnumeric() else 100
num_ticks_per_generation = next((int(x.split("=")[1]) for x in sys.argv if "t=" in x), 100)
num_organisms = next((int(x.split("=")[1]) for x in sys.argv if "o=" in x), 100)
num_food = next((int(x.split("=")[1]) for x in sys.argv if "f=" in x), 20)