from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.notification import Notification
from ..models.user import User

class NotificationService:
    async def create_notification(self, db: AsyncSession, user_id: str, type: str, title: str, body: str | None = None, meta: dict | None = None):
        notification = Notification(user_id=user_id, type=type, title=title, body=body, meta=meta)
        db.add(notification)
        await db.commit()
        await db.refresh(notification)
        return notification

    async def list_notifications(self, db: AsyncSession, user_id: str):
        result = await db.execute(select(Notification).where(Notification.user_id == user_id).order_by(Notification.created_at.desc()))
        return result.scalars().all()

    async def notify_admins(self, db: AsyncSession, title: str, body: str | None = None, meta: dict | None = None):
        result = await db.execute(select(User).where(User.role == "admin", User.is_active == True))
        admins = result.scalars().all()
        notifications = []
        for admin in admins:
            notifications.append(await self.create_notification(db, str(admin.id), "system", title, body, meta))
        return notifications