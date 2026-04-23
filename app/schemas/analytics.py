from pydantic import BaseModel
from typing import List

class AnalyticsStats(BaseModel):
    total_attendance: int
    unique_users: int
    unknown_count: int

class TrendData(BaseModel):
    date: str
    count: int

class AnalyticsTrends(BaseModel):
    trends: List[TrendData]