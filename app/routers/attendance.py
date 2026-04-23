from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..core.deps import get_current_user
from ..schemas.attendance import AttendanceLogRead
from ..models.attendance import AttendanceLog
from ..models.user import User
from sqlalchemy import select

router = APIRouter(prefix="/attendance", tags=["attendance"])

@router.get("/", response_model=list[AttendanceLogRead])
async def list_attendance(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(AttendanceLog).order_by(AttendanceLog.recognized_at.desc()))
    logs = result.scalars().all()
    return [AttendanceLogRead.from_orm(log) for log in logs]