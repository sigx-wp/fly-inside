import threading

import configparser
import cv2 as cv
from djitellopy import Tello

from handler import *
from utils import CvFpsCalc

def get_args():
    print('# Reading configuration #')
    parser = configparser.ArgParser(default_config_files=['config.txt'])

    parser.add('-c', '--my-config', required=False, is_config_file=True, help='config file path')
    parser.add("--device", type=int)
    parser.add("--width", help='cap width', type=int)
    parser.add("--height", help='cap height', type=int)
    parser.add("--is_keyboard", help='To use Keyboard control by default', type=bool)
    parser.add('--use_static_image_mode', action='store_true', help='True if running on photos')
    parser.add("--min_detection_confidence", help='min_detection_confidence', type=float)
    parser.add("--min_tracking_confidence", help='min_tracking_confidence', type=float)
    parser.add("--buffer_len", help='Length of gesture buffer', type=int)

    args = parser.parse_args()

    return args


def main():
    global gesture_buffer
    global gesture_id
    global battery_status

    # Argument parsing
    args = get_args()
    keyboard_control = args.is_keyboard
    write_control = False
    flying = False

    tello = Tello(host="192.168.1.4")
    tello.connect(wait_for_state=False)
    tello.streamon()

    cap = tello.get_frame_read()

    gesture_controller = TelloGestureController(tello)
    keyboard_controller = TelloKeyboardController(tello)

    gesture_detector = GestureRecognition(
        args.use_static_image_mode,
        args.min_detection_confidence,
        args.min_tracking_confidence
        )
    
    gesture_buffer = GestureBuffer(buffer_len=args.buffer_len)

    def tello_control(key, keyboard_controller, gesture_controller):
        global gesture_buffer

        if keyboard_control:
            keyboard_controller.control(key)
        else:
            gesture_controller.gesture_control(gesture_buffer)

    def tello_battery(tello):
        global battery_status
        try:
            battery_status = tello.get_battery()
        except:
            print("Cannot get battery status")

    cv_fps_calc = CvFpsCalc(buffer_len=10)

    mode = 0
    number = -1
    battery_status = -1

    tello.send_command_without_return("command")

    while True:
        fps = cv_fps_calc.get()

        key = cv.waitKey(1) & 0xff

        if key == 27:  # Esc button.
            break
        elif key == ord('t'):
            tello.takeoff()
            flying = True
        elif key == ord('l'):
            tello.land()
            flying = False
        elif key == ord('k'):  # Move to keyboard mode.
            mode = 0
            keyboard_control = True
            write_control = False
            tello.send_rc_control(0, 0, 0, 0)  # Stop moving
        elif key == ord('g'):  # Move to gesture mode.
            keyboard_control = False
        elif key == ord('n'):
            mode = 1
            write_control = True
            keyboard_control = True

        if write_control:
            number = -1
            if 48 <= key <= 57:  # 0 ~ 9
                number = key - 48

        image = cap.frame

        debug_image, gesture_id = gesture_detector.recognize(image, number, mode)
        gesture_buffer.add_gesture(gesture_id)

        threading.Thread(target=tello_control,
                          args=(key, keyboard_controller, gesture_controller,)
                        ).start()
        
        threading.Thread(target=tello_battery, args=(tello,)).start()

        debug_image = gesture_detector.draw_info(debug_image, fps, mode, number)

        cv.putText(debug_image, "Battery: {}".format(battery_status), (780, 30),
                   cv.QT_FONT_BOLD, 1, (0, 0, 255), 2)
        cv.imshow('Tello gestures', debug_image)

    if flying:
        tello.land()

    cv.destroyAllWindows()
    tello.streamoff()


if __name__ == '__main__':
    main()
