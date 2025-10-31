from typing import Dict, Any
from ..core.schemas import FindingCreate, RiskCreate


LIKELIHOOD_MAP = {
    "Critical": 5,
    "High": 4,
    "Medium": 3,
    "Low": 1,
}


IMPACT_MAP = {
    "Critical": 5, 
    "High": 4, 
    "Medium": 3,
    "Low": 2, 
}

def calculate_risk(finding: FindingCreate) -> RiskCreate:
    """
    Calculates the inherent risk score (Likelihood x Impact) for a finding
    and assigns basic CIA mapping.
    """
    
    likelihood = LIKELIHOOD_MAP.get(finding.normalized_severity, 1)

    
    impact = IMPACT_MAP.get(finding.normalized_severity, 2)
    
    
    inherent_score = float(likelihood * impact)

    
    if inherent_score >= 21:
        risk_rating = "Critical"
    elif inherent_score >= 13:
        risk_rating = "High"
    elif inherent_score >= 7:
        risk_rating = "Medium"
    else:
        risk_rating = "Low"

    
    cia_score = impact
    
    return RiskCreate(
        inherent_score=inherent_score,
        risk_rating=risk_rating,
        cia_confidentiality=cia_score,
        cia_integrity=cia_score,
        cia_availability=cia_score,
    )