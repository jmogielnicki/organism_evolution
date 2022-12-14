import cv2
import os
import subprocess
from consts import fps
from helpers import clear_all_files_in_directory, get_items_in_directory

image_folder = 'media/images'
video_folder = 'media/videos'
video_name = 'video'

video_file_path = os.getcwdb().decode("utf-8") + '/' + video_folder + '/'

def _sort_stuff(e):
    numeric_values = "".join([each for each in e if each.isdigit()])
    return int(numeric_values)

def make_video(image_directory_name):
    images_directory_path = image_folder + '/' + image_directory_name
    images = [img for img in os.listdir(images_directory_path) if img.endswith(".png")]
    images.sort(key=_sort_stuff)

    frame = cv2.imread(os.path.join(images_directory_path, images[0]))
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_name = '{}.mp4'.format('gen_' + image_directory_name)
    video = cv2.VideoWriter(video_folder + '/' + video_name, fourcc, fps, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(images_directory_path, image)))

    cv2.destroyAllWindows()

    video.release()

def make_videos():
    clear_all_files_in_directory(video_file_path)
    close_video()
    image_directories = [img for img in os.listdir(image_folder) if not img.startswith(".")]
    for image_directory_name in image_directories:
        make_video(image_directory_name)

def open_videos():
    files = get_items_in_directory(video_file_path)
    for file in sorted(files, key=lambda x: int(x.split('_')[1].replace('.mp4', ''))):
        subprocess.call(['open', file])


def close_video():
    subprocess.call(['osascript', '-e', 'tell application "Quicktime Player" to quit'])
