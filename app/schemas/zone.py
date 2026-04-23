from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ZoneBase(BaseModel):
    name: str
    description: Optional[str] = None

class ZoneCreate(ZoneBase):
    pass

class ZoneRead(ZoneBase):
    id: str
    is_active: bool
    created_at: datetime

class ZoneUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    is_active: Optional[bool]