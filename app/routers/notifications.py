from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..core.deps import get_current_user
from ..services.notification_service import NotificationService
from ..schemas.notification import NotificationRead
from ..models.user import User

router = APIRouter(prefix="/notifications", tags=["notifications"])
service = NotificationService()

@router.get("/", response_model=list[NotificationRead])
async def list_notifications(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    entries = await service.list_notifications(db, str(current_user.id))
    return [NotificationRead.from_orm(entry) for entry in entries]