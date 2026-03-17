import base64
import numpy as np
import cv2
import face_recognition

def get_face_encoding(image_data):

    # Remove header (data:image/png;base64,...)
    image_data = image_data.split(",")[1]

    # Decode base64
    image_bytes = base64.b64decode(image_data)

    # Convert to numpy array
    np_arr = np.frombuffer(image_bytes, np.uint8)

    # Decode image
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Convert BGR to RGB
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Detect face
    faces = face_recognition.face_locations(rgb_img)

    if len(faces) == 0:
        return None

    # Get encoding
    encoding = face_recognition.face_encodings(rgb_img, faces)[0]

    return encoding