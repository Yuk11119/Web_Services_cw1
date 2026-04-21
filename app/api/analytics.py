from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_id
from app.core.db import get_db
from app.core.responses import success_response
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"], dependencies=[Depends(get_current_user_id)])


@router.get("/genre-trends")
def genre_trends(start_year: int | None = Query(default=None), end_year: int | None = Query(default=None), db: Session = Depends(get_db)):
    data = AnalyticsService(db).genre_trends(start_year, end_year)
    return success_response(data)


@router.get("/rating-distribution")
def rating_distribution(db: Session = Depends(get_db)):
    data = AnalyticsService(db).rating_distribution()
    return success_response(data)


@router.get("/recommendations/{user_id}")
def recommendations(user_id: int, limit: int = Query(default=5, ge=1, le=20), db: Session = Depends(get_db)):
    data = AnalyticsService(db).recommendations(user_id, limit)
    return success_response(data)
