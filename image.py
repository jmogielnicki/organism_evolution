import os
import glob
from PIL import Image, ImageDraw
from population import Population

img_width = 400
img_height = 400

input_width = 100
input_height = 100

input_to_img_width_ratio = img_width / input_width
input_to_img_height_ratio = img_height / input_height

file_path = '/Users/johnmogielnicki/code/evolve/media/images/'
files = glob.glob('{}*'.format(file_path))
for file in files:
    os.remove(file)


img = Image.new('RGB', (img_width, img_height))
d = ImageDraw.Draw(img)

population = Population(10)
for organism in population.members:
    x = organism.position.get("x") * input_to_img_width_ratio
    y = organism.position.get("y") * input_to_img_height_ratio
    d.rectangle(
        [x, y, x + input_to_img_width_ratio - 1, y + input_to_img_height_ratio - 1], 
        fill="white",
        outline=None,
        width=0)
img.save('{}{}.png'.format(file_path, 1), 'PNG')
img.show()