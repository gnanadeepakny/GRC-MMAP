from sqlalchemy.orm import Session
from ..core import models

# --- Core Mapping Data for MVP ---
# Simplified mapping: Link a generic Control to multiple Framework Controls
FRAMEWORK_DATA = {
    "NIST 800-53": "Rev 5",
    "ISO 27001": "2022",
}

CONTROL_DATA = [
    # General Control Type (Maps to asset configuration finding)
    {"control_name": "Patch Management & Configuration Hardening", "cia_domain": "Integrity, Availability"},
    # Security Control Type (Maps to access/authentication finding)
    {"control_name": "Access Control & Principle of Least Privilege", "cia_domain": "Confidentiality"},
]

# This is the critical cross-walk logic!
CONTROL_FRAMEWORK_MAP = {
    "Patch Management & Configuration Hardening": [
        ("NIST 800-53", "CM-3"), # Configuration Change Control
        ("ISO 27001", "A.12.6.1"), # Management of technical vulnerability
    ],
    "Access Control & Principle of Least Privilege": [
        ("NIST 800-53", "AC-3"), # Access Enforcement
        ("ISO 27001", "A.9.2.3"), # Management of privileged access rights
    ],
}

def seed_initial_compliance_data(db: Session):
    """Creates initial frameworks and controls if they don't exist."""
    # 1. Create Frameworks
    for name, version in FRAMEWORK_DATA.items():
        if not db.query(models.Framework).filter(models.Framework.name == name).first():
            db_framework = models.Framework(name=name, version=version)
            db.add(db_framework)
    db.commit()

    # 2. Create Controls and their Framework Links
    for item in CONTROL_DATA:
        if not db.query(models.Control).filter(models.Control.control_name == item["control_name"]).first():
            # Create the general Control
            db_control = models.Control(**item)
            db.add(db_control)
            db.commit()
            db.refresh(db_control)
            
            # Link Control to Frameworks (M:M)
            for fw_name, fw_id in CONTROL_FRAMEWORK_MAP.get(item["control_name"], []):
                db_framework = db.query(models.Framework).filter(models.Framework.name == fw_name).first()
                if db_framework:
                    # Append the control to the framework's controls list
                    db_control.frameworks.append(db_framework)
            db.commit()
            
def map_finding_to_controls(db: Session, finding_id: int, finding_title: str):
    """
    MVP: Maps a finding to controls based on simple title matching.
    (This will be enhanced by NLP later)
    """
    db_finding = db.query(models.Finding).filter(models.Finding.id == finding_id).first()
    if not db_finding:
        return []
    
    # 1. Simple Keyword Mapping Logic:
    # List to hold the NAMES of controls we want to find
    control_names_to_find = []

    if "patch" in finding_title.lower() or "ssh" in finding_title.lower() or "config" in finding_title.lower():
        control_names_to_find.append("Patch Management & Configuration Hardening")

    if "access" in finding_title.lower() or "privilege" in finding_title.lower():
        control_names_to_find.append("Access Control & Principle of Least Privilege")


    # 2. Retrieve Controls and Link them
    for control_name in control_names_to_find:
        # Get the Control object from the DB
        control = db.query(models.Control).filter(
            models.Control.control_name == control_name
        ).first()
    
        if control:
            # CRITICAL FIX: Merge the control object into the session before linking.
            merged_control = db.merge(control) 
        
            # This condition should always be true, but it's safety measure
            if merged_control not in db_finding.controls: 
                db_finding.controls.append(merged_control)
    
    # Save the finding object and the new relationship link
    db.add(db_finding) 
    db.commit()
    db.refresh(db_finding)

    # Now the control names should be available
    return db_finding.controls