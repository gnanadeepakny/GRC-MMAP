from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

# 1. Schema for the RAW, expected input from a file (Example: A simple AD scan CSV)
class RawInputSchema(BaseModel):
    Raw_IP_Address: str
    Raw_Vulnerability_Title: str
    Vendor_Severity_Code: str  # e.g., 'HIGH', 'CRITICAL', 'INFO'
    Raw_Data_JSON: Optional[Dict[str, Any]] = None

# 2. Schema for the CLEAN, Normalized data ready for the DB
class FindingCreate(BaseModel):
    asset_name: str
    ip_address: str
    normalized_title: str
    source_type: str
    normalized_severity: str
    raw_evidence: Dict[str, Any]
    
# Schema for reading/returning data (includes the ID)
class Finding(FindingCreate):
    id: int
    asset_id: int
    ingestion_date: datetime

    class Config:
        orm_mode = True

class RiskCreate(BaseModel):
    # Data to create a risk entry (mostly from the engine)
    inherent_score: float
    risk_rating: str
    cia_confidentiality: float
    cia_integrity: float
    cia_availability: float

class Risk(RiskCreate):
    id: int
    finding_id: int
    residual_score: Optional[float] = None
    
    class Config:
        orm_mode = True

class ControlBase(BaseModel):
    control_name: str
    cia_domain: str

class Control(ControlBase):
    id: int
    class Config:
        orm_mode = True

# --- Framework Schemas (NEW) ---
class FrameworkBase(BaseModel):
    name: str
    version: str

class Framework(FrameworkBase):
    id: int
    class Config:
        orm_mode = True