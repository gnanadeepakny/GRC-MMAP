from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..report_generator import generate_executive_report
from .dashboard import get_dashboard_summary # Reuse data endpoint

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)

# In api/app/routers/reports.py:
@router.get("/generate/executive", response_class=HTMLResponse)
def generate_executive_report_endpoint(db: Session = Depends(get_db)):
    """Triggers report generation and returns the HTML output."""
    
    # 1. Get all required dashboard data
    dashboard_data = get_dashboard_summary(db)

    if not dashboard_data['risks_by_rating']:
        raise HTTPException(status_code=404, detail="No data found to generate report.")

    try:
        # 2. Generate HTML Report (THIS IS THE LINE THAT CRASHES)
        html_content = generate_executive_report(dashboard_data)
        
    except Exception as e:
        # CRASH PROTECTION: Return a detailed error page showing the exception message.
        error_message = (
            f"<h1>Report Generation Error!</h1>"
            f"<p>The application crashed during report rendering (Jinja2).</p>"
            f"<p>Source of Error: <b>{e}</b></p>"
        )
        return HTMLResponse(error_message, status_code=500)

    # If successful, return the report
    return html_content