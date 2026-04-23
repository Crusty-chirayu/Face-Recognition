from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NotificationRead(BaseModel):
    id: str
    user_id: str
    type: str
    title: str
    body: Optional[str]
    meta: Optional[dict]
    is_read: bool
    created_at: datetime

    class Config:
        orm_mode = True