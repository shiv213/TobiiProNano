import tobii_research as tr
import time
import cv2
import math
from pynput.keyboard import Key, Controller

found_eyetrackers = tr.find_all_eyetrackers()
my_eyetracker = found_eyetrackers[0]
print("Address: " + my_eyetracker.address)
print("Model: " + my_eyetracker.model)
print("Name (It's OK if this is empty): " + my_eyetracker.device_name)
print("Serial number: " + my_eyetracker.serial_number)

global data
data = None
winName = "Visualizer"

cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('videos/GS010002.mp4')
keyboard = Controller()


def pan_screen(direction, velocity):
    for i in range(math.ceil(velocity)):
        keyboard.press(direction)
        keyboard.release(direction)


def gaze_data_callback(gaze_data):
    global data
    data = gaze_data


if __name__ == '__main__':
    my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
    while cap.isOpened():
        ret, frame = cap.read()
        scale_percent = 100
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        height = resized.shape[0]
        width = resized.shape[1]
        if data is not None:
            x = data['left_gaze_point_on_display_area'][0]
            y = data['left_gaze_point_on_display_area'][1]
            if not math.isnan(x) and not math.isnan(y):
                x = math.floor(x * width)
                y = math.floor(y * height)
                resized = cv2.circle(resized, (x, y), 15, (255, 0, 0), 2)
                # diffX = x - (0.5 * height)
                # diffY = y - (0.5 * height)
                # if diffX < 0:
                #     pan_screen(Key.left, (abs(diffX)/width)*10)
                # if diffX > 0:
                #     pan_screen(Key.right, (abs(diffX)/width)*5)
                # print((diffX / width))
                if x < width / 3:
                    pan_screen(Key.left, 3)
                if x > (width / 3) * 2:
                    pan_screen(Key.right, 3)
                if y < height / 4:
                    pan_screen(Key.up, 2)
                if y > (height / 4) * 3:
                    pan_screen(Key.down, 2)

        cv2.imshow(winName, resized)

        key = cv2.waitKey(10)
        if key == 27:
            cv2.destroyWindow(winName)
            break
        if cv2.waitKey(33) == ord('a'):
            print("------------------------------------------")
            print("Left Eye:")
            print(data['left_gaze_point_on_display_area'][0])
            print(data['left_gaze_point_on_display_area'][1])
            print("------------------------------------------")

    my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
