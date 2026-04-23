import face_recognition
import numpy as np
from typing import List, Dict

class FaceDetector:
    def detect_faces(self, image: np.ndarray) -> List[Dict]:
        if image.shape[2] == 4:
            image = image[:, :, :3]
        locations = face_recognition.face_locations(image, model="hog")
        faces = []
        for top, right, bottom, left in locations:
            faces.append({
                "top": top,
                "right": right,
                "bottom": bottom,
                "left": left
            })
        return faces