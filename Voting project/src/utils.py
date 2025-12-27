import cv2
import mediapipe as mp
import numpy as np

mp_face = mp.solutions.face_mesh

def get_face_embedding(frame):
    """
    Detect face landmarks using MediaPipe
    and return a flattened embedding vector.
    """
    with mp_face.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            return None

        landmarks = results.multi_face_landmarks[0]

        embedding = []
        for lm in landmarks.landmark:
            embedding.extend([lm.x, lm.y, lm.z])

        return np.array(embedding, dtype=np.float32)
def euclidean_distance(a, b):
    return np.linalg.norm(a - b)
