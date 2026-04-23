from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    color: str = "#6366F1"

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentRead(DepartmentBase):
    id: str
    created_by: Optional[str]
    created_at: datetime

class DepartmentUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    color: Optional[str]