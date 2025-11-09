from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..crud import crud_analytics

router = APIRouter(
    prefix="/dashboard",
    tags=["Analytics & Reporting"],
)

@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    """Provides high-level counts for risk and control status cards."""
    risks_by_rating = crud_analytics.get_risks_by_rating(db)
    control_maturity = crud_analytics.get_control_maturity_status(db)
    finding_trend = crud_analytics.get_finding_trend(db)

    # Convert SQLAlchemy result tuples to dictionaries for clean JSON output
    risks = [{"rating": r[0], "count": r[1]} for r in risks_by_rating]
    maturity = [{"control_name": c[0], "finding_count": c[1]} for c in control_maturity]
    # Note: func.date returns a datetime.date object; convert to string for JSON
    trend = [{"date": t[0].strftime('%Y-%m-%d'), "count": t[1]} for t in finding_trend]

    return {
        "risks_by_rating": risks,
        "control_maturity": maturity,
        "finding_trend": trend,
    }

# Endpoint for the Compliance Heatmap (reusing data)
@router.get("/compliance/status")
def get_compliance_status(db: Session = Depends(get_db)):
    """Pulls detailed control status showing compliance gaps."""
    # Reusing the summary function for simplicity for now
    return get_dashboard_summary(db).get('control_maturity')