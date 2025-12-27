import cv2
import mediapipe as mp
import numpy as np

from logger import log_auth, log_fraud
from utils import get_face_embedding, euclidean_distance
from db import get_all_voters, mark_voted
from config import FACE_MATCH_THRESHOLD
from liveness import eye_aspect_ratio

mp_face_mesh = mp.solutions.face_mesh

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

EAR_THRESHOLD = 0.2
BLINK_REQUIRED = 1

def verify_voter():
    cap = cv2.VideoCapture(0)
    print("Blink once, then press SPACE to verify")

    blink_count = 0
    eye_closed = False

    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)

            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0]

                left_eye = np.array(
                    [[landmarks.landmark[i].x, landmarks.landmark[i].y] for i in LEFT_EYE]
                )
                right_eye = np.array(
                    [[landmarks.landmark[i].x, landmarks.landmark[i].y] for i in RIGHT_EYE]
                )

                ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2

                if ear < EAR_THRESHOLD and not eye_closed:
                    eye_closed = True
                elif ear >= EAR_THRESHOLD and eye_closed:
                    blink_count += 1
                    eye_closed = False
                    print("Blink detected")

            cv2.imshow("Voter Verification (Blink Required)", frame)
            key = cv2.waitKey(1)

            if key == 32:  # SPACE
                if blink_count < BLINK_REQUIRED:
                    print("❌ Liveness check failed (No blink detected)")
                    log_fraud("LIVENESS_FAILED")
                    break

                live_embedding = get_face_embedding(frame)
                if live_embedding is None:
                    print("No face detected")
                    break

                voters = get_all_voters()
                best_match = None
                min_distance = float("inf")

                for voter_id, name, db_embedding, has_voted in voters:
                    dist = euclidean_distance(live_embedding, db_embedding)
                    if dist < min_distance:
                        min_distance = dist
                        best_match = (voter_id, name, has_voted)

                if best_match and min_distance < FACE_MATCH_THRESHOLD:
                    voter_id, name, has_voted = best_match
                    if has_voted:
                        print(f"🚨 FRAUD DETECTED: {name} already voted")
                        log_fraud(f"VOTER_ID={voter_id}, NAME={name}, REASON=DOUBLE_VOTING")
                    else:
                        print(f"✅ Voter Verified: {name}")
                        log_auth(f"VOTER_ID={voter_id}, NAME={name}, STATUS=VOTED")
                        mark_voted(voter_id)
                else:
                    print("❌ Unregistered voter")
                    log_fraud("UNKNOWN_FACE_DETECTED")

                break

            if key == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    verify_voter()
