from sqlalchemy.orm import Session
from ..core import models, schemas
from ..core.schemas import FindingCreate
from typing import List


def get_asset_by_ip(db: Session, ip_address: str):
    """Retrieves an asset by IP address."""
    return db.query(models.Asset).filter(models.Asset.ip_address == ip_address).first()

def create_asset_if_not_exists(db: Session, finding: FindingCreate):
    """Creates an asset if it doesn't exist, or returns the existing one."""
    db_asset = get_asset_by_ip(db, ip_address=finding.ip_address)
    if db_asset:
        return db_asset
    
    
    db_asset = models.Asset(
        asset_name=finding.asset_name,
        ip_address=finding.ip_address,
        asset_type="Server" 
    )
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

# --- Finding CRUD ---

def create_finding(db: Session, finding: FindingCreate, asset_id: int):
    """Creates a new finding linked to an existing asset."""
    # Create the DB model instance
    db_finding = models.Finding(
        asset_id=asset_id,
        normalized_title=finding.normalized_title,
        source_type=finding.source_type,
        normalized_severity=finding.normalized_severity,
        raw_evidence=finding.raw_evidence,
    )
    db.add(db_finding)
    db.commit()
    db.refresh(db_finding)
    return db_finding