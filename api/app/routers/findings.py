from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import pandas as pd
from io import StringIO
from ..core.database import get_db
from ..data_ingestion.normalization import normalize_finding
from ..crud import crud_findings 
from ..core.schemas import FindingCreate

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
    
    saved_findings: List[schemas.Finding] = [] 
    
    # 3. Process, Normalize, and PERSIST each row (MAJOR CHANGE)
    for index, row in df.iterrows():
        raw_data_dict = row.to_dict()
        
        # 1. Normalize (from Day 3)
        normalized_data = normalize_finding(raw_data_dict, source_name)
        
        # 2. CRUD: Create Asset (or get existing one)
        asset = crud_findings.create_asset_if_not_exists(db, normalized_data)
        
        # 3. CRUD: Create Finding (linked to Asset)
        finding = crud_findings.create_finding(db, normalized_data, asset_id=asset.id)
        
        saved_findings.append(finding)

    return {
        "status": "Success! Ingestion and Persistence Complete.",
        "source": source_name,
        "count": len(saved_findings),
        "preview_id": saved_findings[0].id if saved_findings else None
    }