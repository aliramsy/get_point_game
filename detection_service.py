import cv2
import mediapipe as mp
import grpc
import hand_pos_pb2
import hand_pos_pb2_grpc
import warnings
import os
from dotenv import load_dotenv

load_dotenv()

TRACKING_ADDR = os.getenv("TRACKING_SVC_ADDR")
channel = grpc.insecure_channel(TRACKING_ADDR)

warnings.filterwarnings("ignore", category=UserWarning)

stub = hand_pos_pb2_grpc.HandTrackerStub(channel)

mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: continue
        
        frame = cv2.flip(frame, 1)
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks:
            for res, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                if handedness.classification[0].label == "Right":
                    wrist = res.landmark[0]
                    stub.SendPosition(hand_pos_pb2.Position(x=wrist.x, y=wrist.y))
                    mp.solutions.drawing_utils.draw_landmarks(frame, res, mp_hands.HAND_CONNECTIONS)

        cv2.imshow("Detection Service", frame)
        if cv2.waitKey(1) & 0xFF == 27: break

cap.release()