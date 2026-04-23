from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, distinct
from ..models.attendance import AttendanceLog
from ..models.face import Face

class AnalyticsService:
    async def get_stats(self, db: AsyncSession) -> dict:
        # Total attendance
        total_attendance = await db.execute(select(func.count(AttendanceLog.id)))
        total = total_attendance.scalar()

        # Unique users (distinct face_id)
        unique_users = await db.execute(select(func.count(distinct(AttendanceLog.face_id))))
        unique = unique_users.scalar()

        # Unknown count (face_id is null)
        unknown_count = await db.execute(select(func.count(AttendanceLog.id)).where(AttendanceLog.face_id.is_(None)))
        unknown = unknown_count.scalar()

        return {
            "total_attendance": total,
            "unique_users": unique,
            "unknown_count": unknown
        }

    async def get_trends(self, db: AsyncSession, days: int = 7) -> list[dict]:
        # Simple daily trends: count per day for last days
        from sqlalchemy import text
        query = text("""
            SELECT DATE(recognized_at) as date, COUNT(*) as count
            FROM attendance_logs
            WHERE recognized_at >= CURRENT_DATE - INTERVAL ':days days'
            GROUP BY DATE(recognized_at)
            ORDER BY date
        """)
        result = await db.execute(query, {"days": days})
        trends = result.fetchall()
        return [{"date": str(row[0]), "count": row[1]} for row in trends]