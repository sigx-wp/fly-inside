import cv2
import mediapipe as mp
from djitellopy import Tello

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    min_detection_confidence=0.5, min_tracking_confidence=0.5)

tello = Tello()
tello.connect()

tello.streamon()
frame_read = tello.get_frame_read()

while True:
    image = frame_read.frame

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    image.flags.writeable = False
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('Drone', image)

    key = cv2.waitKey(1) & 0xff

    print("Per il decollo, clicca T")

    match key:
        case 27:  # ESC
            break
        case ord('t'):
            tello.takeoff()
        case ord('l'):
            tello.land()
        case ord('w'):
            tello.move_forward(30)
        case ord('s'):
            tello.move_back(30)
        case ord('a'):
            tello.move_left(30)
        case ord('d'):
            tello.move_right(30)
        case ord('e'):
            tello.rotate_clockwise(30)
        case ord('q'):
            tello.rotate_counter_clockwise(30)
        case ord('r'):
            tello.move_up(30)
        case ord('f'):
            tello.move_down(30)

hands.close()
tello.land()
