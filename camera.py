
from time import sleep
from threading import Thread
import cv2


# Define constants.
__CAM_INDEX = 0  # 0 for general webcam. 4 for Intel RealSense Camera.
__IMG_WIDTH = 640
__IMG_HEIGHT = 480


# Define functions.

def __open_camera(cam_index: int):
    camera = cv2.VideoCapture(cam_index)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, __IMG_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, __IMG_HEIGHT)

    return camera


def __read_stream(cam, interval: float, saved_images: list):
    while True:
        (isSuccess, frame) = cam.read()

        if isSuccess:
            saved_images.append(frame)
        else:
            print('Failed to fetch image from camera.')

        sleep(interval)


def capture_camera(interval: float, saved_images: list) -> Thread:
    cam = __open_camera(__CAM_INDEX)

    thread = Thread(target=__read_stream, args=(cam, interval, saved_images))
    thread.start()

    return thread
