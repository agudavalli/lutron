# python
# Requirements:
# pip install mediapipe opencv-python

import time
import cv2
import mediapipe as mp
from enum import Enum
#from functions import readschedule, take_picture, stop_song, play_song, words_of_affirmation, play_flashing_lights
import subprocess
import sys

#from functions import play_flashing_lights, words_of_affirmation, readschedule, play_song, stop_song, take_picture, calibrate
import functions
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def get_finger_state(landmarks, handedness_label):
    Finger = Enum('Finger', 'THUMB INDEX MIDDLE RING PINKY')
    #tip_idx = {4, Finger.INDEX: 8, Finger.MIDDLE: 12, Finger.RING: 16, Finger.PINKY: 20}
    #pip_idx = {Finger.THUMB: 3, Finger.INDEX: 6, Finger.MIDDLE: 10, Finger.RING: 14, Finger.PINKY: 18}
    tip_idx = [4, 8, 12, 16, 20]
    pip_idx = [3, 6, 10, 14, 18]
    binary = '00000'
    for idx in range(5):
        tip = landmarks.landmark[tip_idx[idx]]
        pip = landmarks.landmark[pip_idx[idx]]
        if idx == 0:
            if handedness_label == 'Right':
                if tip.x < pip.x:
                    binary = binary[:idx] + '1' + binary[idx+1:]
            else:
                if tip.x > pip.x:
                    binary = binary[:idx] + '1' + binary[idx+1:]
        else:
            if tip.y < pip.y:
                binary = binary[:idx] + '1' + binary[idx+1:]
    return binary



def main():
    song_flag = False
    calendar_flag = False
    calibrated = False
    picture = False
    cmajor = True

    functions.boot_up()
    functions.nether()


    cap = cv2.VideoCapture(0)
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    #def send_command(command):
     #   command_line.stdin.write(command + "\n")
      #  command_line.stdin.flush()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Flip for selfie view and convert color
            frame = cv2.flip(frame, 0)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = hands.process(rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    # Draw landmarks and connections
                    label = handedness.classification[0].label
                    if label == 'Left':
                        continue  # Skip left hand for now
                    '''mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=3),
                        mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2),
                    )'''



                    # Example: show label (Left/Right) near wrist landmark
                    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                    h, w, _ = frame.shape
                    cx, cy = int(wrist.x * w), int(wrist.y * h)
                    label = handedness.classification[0].label
                    #cv2.putText(frame, label, (cx + 10, cy + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

                    # Get finger state and display
                    finger_state = get_finger_state(hand_landmarks, label)
                    if finger_state == '01100' and not picture:
                        functions.take_picture(frame)
                        #cv2.putText(frame, 'Picture Taken!', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
                        picture = True
                        calendar_flag = False

                    elif finger_state == '11111' and song_flag:
                        functions.stop_song()
                        song_flag = False
                        picture = False
                        calendar_flag = False

                    elif finger_state == '11001' and not song_flag:
                        functions.play_song()
                        song_flag = True
                        picture = False
                        calendar_flag = False

                    elif finger_state == '01010' and not calendar_flag:
                        functions.readschedule()
                        calendar_flag = True
                        picture = False

                    elif finger_state == '00111':
                        functions.words_of_affirmation()
                        picture = False
                        calendar_flag = False

                    elif finger_state == '01001' and not song_flag:
                        functions.play_flashing_lights()
                        song_flag = True
                        picture = False
                        calendar_flag = False

                    elif finger_state == '10101' and not calibrated:
                        calibrated = True
                        functions.calibrate()
                        picture = False
                        calendar_flag = False

                    elif finger_state == '00100' and cmajor:
                        functions.cmajor()
                        picture = False
                        cmajor = False


                    #cv2.putText(frame, finger_state, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)


            # FPS
            #curr_time = time.time()
            #fps = 1.0 / (curr_time - prev_time) if prev_time else 0.0
            #prev_time = curr_time
            #cv2.putText(frame, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0), 2)
            #cv2.imshow('Hand Tracking', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord('q'):  # Esc or q
                break
    finally:
        hands.close()
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()