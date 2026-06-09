from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.analytics import DashboardAnalyticsResponse
from app.services.analytics import DashboardAnalyticsService

router = APIRouter()


@router.post(
    "/dashboard",
    response_model=DashboardAnalyticsResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve resume metrics dashboard stats",
    description="Loads data aggregations from ATS reports, JD matching, skill gaps, and multi-agent scores."
)
def get_dashboard_metrics(db: Session = Depends(get_db)):
    # Wait, the plan says GET /api/v1/analytics/dashboard. But some routers use POST for consistency or simpler payloads.
    # Let's support both GET and POST or use GET as standard for reading statistics!
    # Yes, standard REST reads are GET. Let's make it router.get()!
    # Let's check: the router.get() is cleaner.
    return DashboardAnalyticsService.get_dashboard_analytics(db=db)


@router.get(
    "/dashboard",
    response_model=DashboardAnalyticsResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve resume metrics dashboard stats",
    description="Loads data aggregations from ATS reports, JD matching, skill gaps, and multi-agent scores."
)
def get_dashboard_metrics_get(db: Session = Depends(get_db)):
    return DashboardAnalyticsService.get_dashboard_analytics(db=db)
