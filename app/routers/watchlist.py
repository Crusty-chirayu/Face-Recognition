from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..core.deps import get_current_user
from ..schemas.watchlist import WatchlistCreate, WatchlistRead
from ..services.watchlist_service import WatchlistService
from ..models.user import User

router = APIRouter(prefix="/watchlist", tags=["watchlist"])
service = WatchlistService()

@router.get("/", response_model=list[WatchlistRead])
async def list_watchlist(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    entries = await service.list_watchlist(db)
    return [WatchlistRead.from_orm(entry) for entry in entries]

@router.post("/", response_model=WatchlistRead)
async def add_watchlist(item: WatchlistCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        entry = await service.add_watchlist(item.face_id, item.reason, item.priority, str(current_user.id), db)
        return WatchlistRead.from_orm(entry)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.delete("/{watchlist_id}")
async def remove_watchlist(watchlist_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        await service.remove_watchlist(watchlist_id, db)
        return {"message": "Removed"}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))