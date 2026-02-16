# python
# Requirements:
# pip install mediapipe opencv-python

import time
import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def main():
    cap = cv2.VideoCapture(0)
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    prev_time = 0.0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Flip for selfie view and convert color
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = hands.process(rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    # Draw landmarks and connections
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=3),
                        mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2),
                    )

                    # Example: show label (Left/Right) near wrist landmark
                    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                    h, w, _ = frame.shape
                    cx, cy = int(wrist.x * w), int(wrist.y * h)
                    label = handedness.classification[0].label
                    cv2.putText(frame, label, (cx + 10, cy + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

            # FPS
            curr_time = time.time()
            fps = 1.0 / (curr_time - prev_time) if prev_time else 0.0
            prev_time = curr_time
            cv2.putText(frame, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0), 2)

            cv2.imshow('Hand Tracking', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord('q'):  # Esc or q
                break
    finally:
        hands.close()
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()