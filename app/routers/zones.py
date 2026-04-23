from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_db
from ..schemas.zone import ZoneCreate, ZoneRead, ZoneUpdate
from ..core.deps import get_current_user
from ..models.zone import Zone
from ..models.user import User

router = APIRouter(prefix="/zones", tags=["zones"])

@router.get("/", response_model=list[ZoneRead])
async def read_zones(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Zone))
    zones = result.scalars().all()
    return [ZoneRead.from_orm(z) for z in zones]

@router.post("/", response_model=ZoneRead)
async def create_zone(zone: ZoneCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_zone = Zone(name=zone.name, description=zone.description)
    db.add(db_zone)
    await db.commit()
    await db.refresh(db_zone)
    return ZoneRead.from_orm(db_zone)

@router.get("/{zone_id}", response_model=ZoneRead)
async def read_zone(zone_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Zone).where(Zone.id == zone_id))
    zone = result.scalar_one_or_none()
    if not zone:
        raise HTTPException(404, "Zone not found")
    return ZoneRead.from_orm(zone)

@router.patch("/{zone_id}", response_model=ZoneRead)
async def update_zone(zone_id: str, zone_update: ZoneUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Zone).where(Zone.id == zone_id))
    zone = result.scalar_one_or_none()
    if not zone:
        raise HTTPException(404, "Zone not found")
    for k, v in zone_update.dict(exclude_unset=True).items():
        setattr(zone, k, v)
    await db.commit()
    await db.refresh(zone)
    return ZoneRead.from_orm(zone)

@router.delete("/{zone_id}")
async def delete_zone(zone_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Zone).where(Zone.id == zone_id))
    zone = result.scalar_one_or_none()
    if not zone:
        raise HTTPException(404, "Zone not found")
    await db.delete(zone)
    await db.commit()
    return {"message": "Zone deleted"}