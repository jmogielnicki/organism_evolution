import cv2
import os
import subprocess
import glob

image_folder = 'media/images'
video_folder = 'media/videos'
video_name = 'video.mp4'

video_file_path = os.getcwdb().decode("utf-8") + video_folder

def _sort_stuff(e):
    numeric_values = "".join([each for each in e if each.isdigit()])
    return int(numeric_values)

def _get_files():
    return glob.glob('{}*'.format(video_file_path))

def make_video():
    clear_video()
    close_video()
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images.sort(key=_sort_stuff)

    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    video = cv2.VideoWriter(video_folder + '/' + video_name, fourcc, 10, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()

    video.release()

def open_video():
    subprocess.call(['open', video_folder + '/' + video_name])

def close_video():
    subprocess.call(['osascript', '-e', 'tell application "Quicktime Player" to quit'])

def clear_video():
    files = glob.glob('{}*'.format(video_file_path))
    for file in _get_files():
        os.remove(file)
