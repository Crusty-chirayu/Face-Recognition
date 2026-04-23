import numpy as np
from typing import List


def cosine_distance(a: np.ndarray, b: np.ndarray) -> float:
    a = np.array(a)
    b = np.array(b)
    similarity = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return 1 - similarity


class FaceMatcher:
    def match(
        self,
        embedding: np.ndarray,
        known_embeddings: List[np.ndarray],
        threshold: float = 0.4
    ) -> tuple[bool, float, int]:

        if not known_embeddings:
            return False, 0.0, -1

        distances = [cosine_distance(embedding, known) for known in known_embeddings]

        min_dist = min(distances)
        index = distances.index(min_dist)

        confidence = 1 - min_dist
        matched = min_dist < threshold

        return matched, confidence, index