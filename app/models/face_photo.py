from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, JSON
from sqlalchemy.sql import func
from .base import Base


class FacePhoto(Base):
    __tablename__ = "face_photos"

    id = Column(Integer, primary_key=True, index=True)
    face_id = Column(Integer, ForeignKey("faces.id", ondelete="CASCADE"), nullable=False)
    photo_path = Column(String, nullable=False)

    # ✅ FIXED (ARRAY → JSON)
    embedding = Column(JSON, nullable=False)

    is_primary = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())