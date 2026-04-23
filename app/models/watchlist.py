from sqlalchemy import Column, Text, String, DateTime, func, Integer, ForeignKey
from .base import Base


class Watchlist(Base):
    __tablename__ = "watchlist"

    id = Column(Integer, primary_key=True, index=True)
    face_id = Column(Integer, ForeignKey("faces.id", ondelete="CASCADE"), nullable=False)
    reason = Column(Text)
    priority = Column(String(20), nullable=False, default="medium")
    added_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    added_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())