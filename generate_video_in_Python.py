#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 10:34:01 2024

@author: mario
"""

import cv2 # pip install opencv-python
import os

image_folder = 'film_dishwasher'
video_name = 'optimization2_dishwasher_film.avi'
fps = 10

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
print(images)

# we need to order the images in the list 'images', otherwise we get a complete mess
images.sort()
print("\nSorted images.....")
print(images)

frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

#video = cv2.VideoWriter(video_name, 0, 1, (width,height)) # these videos are HUGE!!! DONT USE!
video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'XVID'), fps, (width,height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()

print(".......Finished!")