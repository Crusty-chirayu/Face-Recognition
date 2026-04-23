from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AttendanceLogRead(BaseModel):
    id: str
    face_id: Optional[str]
    person_name: str
    department_id: Optional[str]
    zone_id: Optional[str]
    confidence: float
    recognized_at: datetime
    source: str
    is_manual: bool

    class Config:
        orm_mode = True