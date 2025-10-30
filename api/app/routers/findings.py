from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import pandas as pd
from io import StringIO
from ..core.database import get_db
from ..data_ingestion.normalization import normalize_finding


router = APIRouter(
    prefix="/findings",
    tags=["Findings Ingestion & Management"],
)

@router.post("/upload_csv/{source_name}")
async def upload_findings_csv(
    source_name: str, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    """
    Ingests audit data from a CSV file, normalizes it, and saves it to the database.
    """
    # 1. Read the file content
    content = await file.read()
    
    # 2. Use Pandas to read the CSV content
    df = pd.read_csv(StringIO(content.decode('utf-8')))
    
    normalized_findings = []
    
    # 3. Process and Normalize each row
    for index, row in df.iterrows():
        
        raw_data_dict = row.to_dict()
        
        
        normalized_data = normalize_finding(raw_data_dict, source_name)
        
        normalized_findings.append(normalized_data)
        
        

    return {
        "status": "Normalization complete (Persistence TBD)",
        "source": source_name,
        "count": len(normalized_findings),
        "preview": normalized_findings[0].dict() if normalized_findings else None
    }