import tobii_research as tr
import keyboard
import time
import csv

found_eyetrackers = tr.find_all_eyetrackers()
my_eyetracker = found_eyetrackers[0]
print("Address: " + my_eyetracker.address)
print("Model: " + my_eyetracker.model)
print("Name (It's OK if this is empty): " + my_eyetracker.device_name)
print("Serial number: " + my_eyetracker.serial_number)

global data
data = None
header = ["timestamp", "right_x", "right_y", "left_x", "left_y"]
i = 0
username = "SHIV"


def gaze_data_callback(gaze_data):
    global data
    data = gaze_data


if __name__ == '__main__':
    my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
    while True:
        while True:
            if keyboard.is_pressed("s"):
                i += 1
                started = True
                f = open('output/' + username + '/' + str(i) + '.csv', 'a')
                writer = csv.writer(f, lineterminator='\n')
                writer.writerow(header)
                break
        while True:
            if started:
                row = [time.time(), data['left_gaze_point_on_display_area'][0],
                       data['left_gaze_point_on_display_area'][1], data['right_gaze_point_on_display_area'][0],
                       data['right_gaze_point_on_display_area'][1]]
                writer.writerow(row)
                print("You pressed s")
                print("------------------------------------------")
                print("Both Eyes:")
                print(data['left_gaze_point_on_display_area'])
                print(data['right_gaze_point_on_display_area'])
                print("------------------------------------------")
                if keyboard.is_pressed("e"):
                    break

my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
