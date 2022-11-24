import os
import glob
from PIL import Image, ImageDraw
from population import Population

img_width = 800
img_height = 800

input_width = 100
input_height = 100

input_to_img_width_ratio = img_width / input_width
input_to_img_height_ratio = img_height / input_height

file_path = '/Users/johnmogielnicki/code/evolve/media/images/'

def clear_images():
    files = glob.glob('{}*'.format(file_path))
    for file in files:
        os.remove(file)

def create_image(population: Population, tick: int):
    img = Image.new('RGB', (img_width, img_height))
    d = ImageDraw.Draw(img)
    for organism in population.members:
        x = organism.position.x * input_to_img_width_ratio
        y = organism.position.y * input_to_img_height_ratio
        d.rectangle(
            [x, y, x + input_to_img_width_ratio - 1, y + input_to_img_height_ratio - 1],
            fill="white",
            outline=None,
            width=0)
    img.save('{}{}.png'.format(file_path, tick), 'PNG')
