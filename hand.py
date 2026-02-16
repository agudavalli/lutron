import mediapipe as mp
import cv2
import numpy as np

videoCap = cv2.VideoCapture(0)
handsol = mp.solutions.hands
hands = handsol.Hands()

while True:
    success, img = videoCap.read()

    if success:

        rechands = hands.process(img)
        if rechands.multi_hand_landmarks:
            for hand in rechands.multi_hand_landmarks:
                for dp, p in enumerate(hand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(p.x * w), int(p.y * h)
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)



        cv2.imshow('CamOutput', img)
        cv2.waitKey(1)



