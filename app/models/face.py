from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer, ForeignKey, JSON
from sqlalchemy.sql import func
from .base import Base


class Face(Base):
    __tablename__ = "faces"

    id = Column(Integer, primary_key=True, index=True)
    person_name = Column(String(255), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)

    # ✅ FIXED (ARRAY → JSON)
    embedding = Column(JSON, nullable=False)

    primary_photo_path = Column(String, nullable=True)
    is_on_watchlist = Column(Boolean, nullable=False, default=False)
    enrolled_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())