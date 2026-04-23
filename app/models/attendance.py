from sqlalchemy import Column, String, Float, Boolean, DateTime, func, Integer, ForeignKey, Text
from .base import Base


class AttendanceLog(Base):
    __tablename__ = "attendance_logs"

    id = Column(Integer, primary_key=True, index=True)
    face_id = Column(Integer, ForeignKey("faces.id", ondelete="SET NULL"))
    person_name = Column(String(255), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"))
    zone_id = Column(Integer, ForeignKey("zones.id", ondelete="SET NULL"))
    confidence = Column(Float, nullable=False)
    is_spoofed = Column(Boolean, nullable=False, default=False)
    photo_path = Column(String)
    recognized_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    source = Column(String(20), nullable=False, default="webcam")
    is_manual = Column(Boolean, nullable=False, default=False)
    manual_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))