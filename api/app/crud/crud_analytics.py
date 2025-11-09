from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from ..core import models

# 1. Total Risks by Rating (For Risk Matrix/Summary Card)
def get_risks_by_rating(db: Session):
    """Counts the total number of findings grouped by risk rating (Low/Med/High/Critical)."""
    return db.query(
        models.Risk.risk_rating,
        func.count(models.Risk.id).label('count')
    ).group_by(models.Risk.risk_rating).all()

# 2. Control Maturity (For Compliance Dashboard)
def get_control_maturity_status(db: Session):
    """Counts how many times each control is referenced (showing compliance footprint)."""
    # Join on the M:M link table (finding_control_link) to count related findings
    return db.query(
        models.Control.control_name,
        func.count(models.finding_control_link.c.finding_id).label('finding_count')
    ).join(models.finding_control_link).group_by(models.Control.control_name).all()

# 3. Findings Trend (Simple count for the trending chart)
def get_finding_trend(db: Session):
    """Counts the number of new findings per ingestion date (simple daily/monthly chart)."""
    return db.query(
        func.date(models.Finding.ingestion_date).label('date'),
        func.count(models.Finding.id).label('count')
    ).group_by(func.date(models.Finding.ingestion_date)).order_by('date').all()