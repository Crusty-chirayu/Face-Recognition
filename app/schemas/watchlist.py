from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WatchlistCreate(BaseModel):
    face_id: str
    reason: Optional[str]
    priority: str = "medium"

class WatchlistRead(BaseModel):
    id: str
    face_id: str
    reason: Optional[str]
    priority: str
    added_by: Optional[str]
    added_at: datetime

    class Config:
        orm_mode = True