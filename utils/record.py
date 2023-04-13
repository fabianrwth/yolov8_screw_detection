import numpy as np
import cv2
import time
import os

file_name = "test.avi"

DIR_PATH = "../data/input/videos"
FILE_PATH = os.path.join(DIR_PATH, file_name)


# Python program to save a
# video using OpenCV


# Create an object to read
# from camera
cap = cv2.VideoCapture(0)

# We need to check if camera
# is opened previously or not
if cap.isOpened() == False:
    print("Error reading video file")

# We need to set resolutions.
# so, convert them from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

size = (frame_width, frame_height)

# Below VideoWriter object will create
# a frame of above defined The output
# is stored in 'filename.avi' file.
result = cv2.VideoWriter(FILE_PATH, cv2.VideoWriter_fourcc(*"MJPG"), 10, size)

while True:
    ret, frame = cap.read()

    if ret == True:

        # Write the frame into the
        # file 'filename.avi'
        result.write(frame)

        # Display the frame
        # saved in the file
        cv2.imshow("Frame", frame)

        # Press S on keyboard
        # to stop the process
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Break the loop
    else:
        break

# When everything done, release
# the video capture and video
# write objects
cap.release()
result.release()

# Closes all the frames
cv2.destroyAllWindows()

print("The video was successfully saved")
