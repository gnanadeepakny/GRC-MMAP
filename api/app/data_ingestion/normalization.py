from ..core.schemas import FindingCreate
from typing import Dict, Any
# Note: Since Pandas creates float/NaN, we need a small utility to check for it.
import pandas as pd 

# Define the standard severity mapping for your Risk Engine
SEVERITY_MAP = {
    "CRITICAL": "Critical",
    "HIGH": "High",
    "MEDIUM": "Medium",
    "LOW": "Low",
    "INFO": "Low",
    "WARNING": "Medium",
}

def normalize_finding(raw_data: Dict[str, Any], source_name: str) -> FindingCreate:
    """
    Transforms raw audit data (from CSV/Pandas row) into the standardized FindingCreate schema.
    This function performs the GRC data cleanup and severity mapping.
    """
    
    # 1. Normalize Severity (Ensure string conversion)
    raw_severity = str(raw_data.get("Vendor_Severity_Code", "INFO")).upper()
    normalized_severity = SEVERITY_MAP.get(raw_severity, "Low")

    # 2. Normalize Title (Ensure string conversion to pass Pydantic validation)
    raw_title = raw_data.get("Raw_Vulnerability_Title", "Unknown Finding")
    normalized_title_safe = str(raw_title) 

    # For MVP, asset name is derived from the IP address
    asset_name = raw_data.get("Raw_IP_Address") 

    
    # --- CRITICAL FIX: Sanitize dictionary for JSONB column ---
    # Pandas NaN (float) is not valid JSON. We convert NaN/None to Python None.
    raw_evidence_clean = {}
    for k, v in raw_data.items():
        # Check if the value is NaN (using pd.isna for robustness)
        if isinstance(v, float) and pd.isna(v):
            raw_evidence_clean[k] = None # Converts to JSON 'null', which Postgres accepts
        else:
            raw_evidence_clean[k] = v
    # --------------------------------------------------------
    
    return FindingCreate(
        asset_name=asset_name,
        ip_address=asset_name, 
        normalized_title=normalized_title_safe, # Uses the safe title
        source_type=source_name,
        normalized_severity=normalized_severity,
        raw_evidence=raw_evidence_clean # <--- USE THE CLEANED DICT HERE
    )