import cv2
from utils import get_face_embedding
from db import insert_voter

def register_voter():
    name = input("Enter voter name: ")

    cap = cv2.VideoCapture(0)
    print("Press SPACE to capture face")

    embedding = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Voter Registration", frame)

        key = cv2.waitKey(1)

        if key == 32:  # SPACE
            embedding = get_face_embedding(frame)
            if embedding is not None:
                insert_voter(name, embedding)
                print(f"Voter '{name}' registered successfully")
                break
            else:
                print("No face detected. Try again.")

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    register_voter()
