import os
import glob
import subprocess

from PIL import Image, ImageDraw
from population import Population

img_width = 800
img_height = 800

input_width = 100
input_height = 100

input_to_img_ratio = img_width / input_width

file_path = '/Users/johnmogielnicki/code/evolve/media/images/'

img = Image.new('RGB', (img_width, img_height))

def _get_files():
    return glob.glob('{}*'.format(file_path))

def clear_images():
    files = glob.glob('{}*'.format(file_path))
    for file in _get_files():
        os.remove(file)

def create_image(population: Population, tick: int):
    img = Image.new('RGB', (img_width, img_height))
    d = ImageDraw.Draw(img)
    for organism in population.members:
        organism.draw(d, input_to_img_ratio)
    img.save('{}{}.png'.format(file_path, tick), 'PNG')

def open_image():
    files = _get_files()
    subprocess.call(['open', files[0]])
