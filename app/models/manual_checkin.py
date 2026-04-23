from sqlalchemy import Column, DateTime, Integer, ForeignKey, Text
from sqlalchemy.sql import func
from .base import Base


class ManualCheckin(Base):
    __tablename__ = "manual_checkins"

    id = Column(Integer, primary_key=True, index=True)
    face_id = Column(Integer, ForeignKey("faces.id", ondelete="CASCADE"), nullable=False)
    zone_id = Column(Integer, ForeignKey("zones.id", ondelete="SET NULL"))
    override_time = Column(DateTime(timezone=True), nullable=False)
    reason = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())