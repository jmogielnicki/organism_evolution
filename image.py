import os
import glob
import shutil
import subprocess

from PIL import Image, ImageDraw, ImageFont
from food import Food
from board import Board

img_width = 900
img_height = 940

input_width = 100
input_height = 100

input_to_img_ratio = int(img_width / input_width)

file_path = os.getcwdb().decode("utf-8") + '/media/images/'

img = Image.new('RGB', (img_width, img_height))

def _get_files():
    return glob.glob('{}*'.format(file_path))

def clear_images():
    for dir_path in _get_files():
        try:
            shutil.rmtree(dir_path)
        except OSError as e:
            print("Error: %s : %s" % (dir_path, e.strerror))
        # os.remove(file)

def create_image(board: Board, generation_num: int, tick: int):
    img = Image.new('RGB', (img_width, img_height))
    d = ImageDraw.Draw(img)
    board.draw(d, input_to_img_ratio)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Helvetica.ttc", 18)
    draw.text((10, img_height - 20), 'tick: {}'.format(str(tick)), font=font)
    image_path = '{}{}/'.format(file_path, generation_num)
    image_name = '{}.png'.format(tick)
    if not os.path.exists(image_path):
        os.mkdir(image_path)
    img.save(image_path + image_name, 'PNG')

def open_image():
    files = _get_files()
    subprocess.call(['open', files[0]])
