from ..core.schemas import FindingCreate
from typing import Dict, Any

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
    Transforms raw audit data into the standardized FindingCreate schema.
    """
    
    raw_severity = raw_data.get("Vendor_Severity_Code", "INFO").upper()
    normalized_severity = SEVERITY_MAP.get(raw_severity, "Low")

    
    asset_name = raw_data.get("Raw_IP_Address") 

    return FindingCreate(
        asset_name=asset_name,
        ip_address=asset_name, 
        normalized_title=raw_data.get("Raw_Vulnerability_Title", "Unknown Finding"),
        source_type=source_name,
        normalized_severity=normalized_severity,
        raw_evidence=raw_data 
    )