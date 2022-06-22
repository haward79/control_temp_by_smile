
from time import sleep
from datetime import datetime
import cv2
from camera import capture_camera
from azure import is_smiling


# Define constants.
INTERVAL = 3
FONT_SCALE = 0.7
TEXT_COLOR = (0, 0, 255)
TEXT_STROKE = 2
TEXT_FONT = cv2.FONT_HERSHEY_SIMPLEX
TEXT_OFFSET_X = 20
TEXT_DIFF_X = 35


# Define functions.

def append_conments(image, smile: float, action: str, temp: float):
    current_time = datetime.now().strftime('%H:%M:%S')

    if smile < 0:
        smile_text = '?'
    else:
        smile_text = str(int(smile * 100))

    offset_y = 20
    image = cv2.putText(image, 'Time = ' + current_time, org=(TEXT_OFFSET_X, offset_y), fontFace=TEXT_FONT, fontScale=FONT_SCALE, color=TEXT_COLOR, thickness=TEXT_STROKE)

    offset_y += TEXT_DIFF_X
    image = cv2.putText(image, 'Smile = ' + smile_text + '%', org=(TEXT_OFFSET_X, offset_y), fontFace=TEXT_FONT, fontScale=FONT_SCALE, color=TEXT_COLOR, thickness=TEXT_STROKE)

    offset_y += TEXT_DIFF_X
    image = cv2.putText(image, 'Action = ' + action, org=(TEXT_OFFSET_X, offset_y), fontFace=TEXT_FONT, fontScale=FONT_SCALE, color=TEXT_COLOR, thickness=TEXT_STROKE)

    offset_y += TEXT_DIFF_X
    image = cv2.putText(image, 'Temp = ' + str(temp) + ' C', org=(TEXT_OFFSET_X, offset_y), fontFace=TEXT_FONT, fontScale=FONT_SCALE, color=TEXT_COLOR, thickness=TEXT_STROKE)

    return image


# Main

temperature = 28.0
captured_images = []
capture_thread = capture_camera(INTERVAL, captured_images)

while True:
    if len(captured_images) > 0:
        # Preserve last element.
        while len(captured_images) > 1:
            captured_images.pop(0)

        image = captured_images.pop(0)
        encodedImage = cv2.imencode('.jpg', image)[1].tobytes()
        smile = is_smiling(encodedImage)

        if smile >= 0.8:
            temperature += 0.5
            action = 'Increment'
        elif smile >= 0.2:
            temperature += 0
            action = 'Hold'
        else:
            temperature -= 0.5
            action = 'Decrease'

        image_comments = append_conments(image, smile, action, temperature)

        cv2.imshow('Realtime Temperature Control by Smile', image_comments)
        cv2.waitKey(1)

    sleep(INTERVAL / 2)
