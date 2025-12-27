import numpy as np

def eye_aspect_ratio(eye_points):
    """
    Compute Eye Aspect Ratio (EAR)
    """
    A = np.linalg.norm(eye_points[1] - eye_points[5])
    B = np.linalg.norm(eye_points[2] - eye_points[4])
    C = np.linalg.norm(eye_points[0] - eye_points[3])

    ear = (A + B) / (2.0 * C)
    return ear
