from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.watchlist import Watchlist
from ..models.face import Face

class WatchlistService:
    async def add_watchlist(self, face_id: str, reason: str | None, priority: str, added_by: str, db: AsyncSession) -> Watchlist:
        existing = await db.execute(select(Watchlist).where(Watchlist.face_id == face_id))
        if existing.scalar_one_or_none():
            raise ValueError("Already on watchlist")
        entry = Watchlist(face_id=face_id, reason=reason, priority=priority, added_by=added_by)
        db.add(entry)
        face = await db.get(Face, face_id)
        if face:
            face.is_on_watchlist = True
        await db.commit()
        await db.refresh(entry)
        return entry

    async def remove_watchlist(self, watchlist_id: str, db: AsyncSession) -> None:
        entry = await db.get(Watchlist, watchlist_id)
        if not entry:
            raise ValueError("Watchlist entry not found")
        face = await db.get(Face, entry.face_id)
        if face:
            face.is_on_watchlist = False
        await db.delete(entry)
        await db.commit()

    async def list_watchlist(self, db: AsyncSession) -> list[Watchlist]:
        result = await db.execute(select(Watchlist))
        return result.scalars().all()

    async def is_on_watchlist(self, face_id: str, db: AsyncSession) -> bool:
        result = await db.execute(select(Watchlist).where(Watchlist.face_id == face_id))
        return result.scalar_one_or_none() is not None

    async def get_watchlist_entry(self, face_id: str, db: AsyncSession) -> Watchlist | None:
        result = await db.execute(select(Watchlist).where(Watchlist.face_id == face_id))
        return result.scalar_one_or_none()