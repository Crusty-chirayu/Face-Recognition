import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import async_session
from ..models.user import User
from ..models.department import Department
from ..models.zone import Zone
from ..services.auth_service import get_password_hash
from ..config import settings

async def seed():
    async with async_session() as db:
        # Admin user
        admin = await db.execute(select(User).where(User.email == settings.admin_email))
        if not admin.scalar_one_or_none():
            hashed = get_password_hash(settings.admin_password)
            admin_user = User(email=settings.admin_email, name=settings.admin_name, role="admin", password_hash=hashed)
            db.add(admin_user)

        # Departments
        depts = [
            {"name": "Engineering", "color": "#3B82F6"},
            {"name": "HR", "color": "#10B981"},
            {"name": "Security", "color": "#EF4444"}
        ]
        for d in depts:
            existing = await db.execute(select(Department).where(Department.name == d["name"]))
            if not existing.scalar_one_or_none():
                dept = Department(name=d["name"], color=d["color"])
                db.add(dept)

        # Zones
        zones = [
            {"name": "Main Gate"},
            {"name": "Office Floor"},
            {"name": "Server Room"}
        ]
        for z in zones:
            existing = await db.execute(select(Zone).where(Zone.name == z["name"]))
            if not existing.scalar_one_or_none():
                zone = Zone(name=z["name"])
                db.add(zone)

        await db.commit()

if __name__ == "__main__":
    asyncio.run(seed())