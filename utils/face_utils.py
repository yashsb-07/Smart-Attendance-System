import base64
import numpy as np
import cv2
import face_recognition

def get_face_encoding(image_data):
    try:
        if "," in image_data:
            image_data = image_data.split(",")[1]
        else:
            return None

        image_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        face_locations = face_recognition.face_locations(img)

        if len(face_locations) == 0:
            return None

        encoding = face_recognition.face_encodings(img, face_locations)[0]
        return encoding

    except Exception as e:
        print("Error in face encoding:", e)
        return None