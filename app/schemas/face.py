from pydantic import BaseModel
from typing import Optional

class FaceEnroll(BaseModel):
    name: str
    department_id: Optional[str]

class RecognizeResponse(BaseModel):
    recognized: bool
    name: str
    face_id: Optional[str]
    confidence: float
    bbox: Optional[dict]