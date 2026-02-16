import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import numpy as np
import time

#model_path = './model/hand_landmarker.task'
#BaseOptions = mp.tasks.BaseOptions
#HandLandmarker = mp.tasks.vision.HandLandmarker
#HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
#HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
#VisionRunningMode = mp.tasks.vision.RunningMode

#def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):

#options = HandLandmarkerOptions(
#    base_options=BaseOptions(model_asset_path=model_path),
#   running_mode=VisionRunningMode.LIVE_STREAM,
#    result_callback=print_result)
#with HandLandmarker.create_from_options(options) as landmarker:

#    videoCap = cv2.VideoCapture(0)
#    while True:
#        success, img = videoCap.read()
#        if success:
#            start_time = time.time()
#            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)
#            landmarker.detect_async(mp_image, int(time.time() * 1000))
#            end_time = time.time()
#            cv2.imshow("camera", img)
#            print('Inference time: {} ms'.format((end_time - start_time) * 1000))

videoCap = cv2.VideoCapture(0)
handSolution = mp.solutions.hands
hands = handSolution.Hands()
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
        cv2.imshow("camera", img)
        cv2.waitKey(1)






