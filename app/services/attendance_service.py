import os
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.attendance import AttendanceLog
from ..models.face import Face

class AttendanceService:
    async def log_attendance(self, db: AsyncSession, face: Face, confidence: float, zone_id: str | None = None) -> AttendanceLog:
        entry = AttendanceLog(
            face_id=face.id,
            person_name=face.person_name,
            department_id=face.department_id,
            zone_id=zone_id,
            confidence=confidence,
            source="webcam",
        )
        db.add(entry)
        await db.commit()
        await db.refresh(entry)
        return entry