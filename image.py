import os
import subprocess

from PIL import Image, ImageDraw, ImageFont
from board import Board
from helpers import clear_all_folders_in_directory, get_items_in_directory
from consts import debug

img_width = 900
img_height = 940

input_width = 100
input_height = 100

input_to_img_ratio = int(img_width / input_width)

file_path = os.getcwdb().decode("utf-8") + '/media/images/'

def clear_images():
    clear_all_folders_in_directory(file_path)

def create_image(board: Board, generation_num: int, tick: int):
    img = Image.new('RGBA', (img_width, img_height))
    d = ImageDraw.Draw(img)
    board.draw(d, input_to_img_ratio)
    font = ImageFont.truetype("Helvetica.ttc", 18)
    d.text((10, img_height - 20), 'tick: {}'.format(str(tick)), font=font)
    image_path = '{}{}/'.format(file_path, generation_num)
    image_name = '{}.png'.format(tick)
    if not os.path.exists(image_path):
        os.mkdir(image_path)
    img.save(image_path + image_name, 'PNG')

def open_image():
    files = get_items_in_directory(file_path)
    subprocess.call(['open', files[0]])
