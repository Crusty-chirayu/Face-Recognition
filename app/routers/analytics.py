from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..services.analytics_service import AnalyticsService
from ..schemas.analytics import AnalyticsStats, AnalyticsTrends

router = APIRouter(prefix="/analytics", tags=["analytics"])
service = AnalyticsService()

@router.get("/stats", response_model=AnalyticsStats)
async def get_stats(db: AsyncSession = Depends(get_db)):
    stats = await service.get_stats(db)
    return stats

@router.get("/trends", response_model=AnalyticsTrends)
async def get_trends(days: int = 7, db: AsyncSession = Depends(get_db)):
    trends = await service.get_trends(db, days)
    return {"trends": trends}