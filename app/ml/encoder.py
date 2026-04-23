import face_recognition
import numpy as np
from typing import Dict

class FaceEncoder:
    def encode_face(self, image: np.ndarray, bbox: Dict) -> np.ndarray:
        top, right, bottom, left = bbox["top"], bbox["right"], bbox["bottom"], bbox["left"]
        face_image = image[top:bottom, left:right]
        encodings = face_recognition.face_encodings(face_image)
        if not encodings:
            raise ValueError("No encoding")
        return encodings[0]