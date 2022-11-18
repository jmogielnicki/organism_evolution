import cv2
import os

image_folder = 'media/images'
video_folder = 'media/videos'
video_name = 'video.mp4'

def sort_stuff(e):
    numeric_values = "".join([each for each in e if each.isdigit()])
    return int(numeric_values)

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
images.sort(key=sort_stuff)

frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
video = cv2.VideoWriter(video_folder + '/' + video_name, fourcc, 30, (width, height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()