from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Boolean
from .base import Base


class Session(Base):
    __tablename__ = "sessions"

    jti = Column(String(255), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked = Column(Boolean, nullable=False, default=False)