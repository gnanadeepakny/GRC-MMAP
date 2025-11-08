from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from .database import Base
from datetime import datetime

# --- Asset Model ---
class Asset(Base):
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_name = Column(String, index=True)
    ip_address = Column(String, unique=True, index=True)
    asset_type = Column(String)
    
    
    findings = relationship("Finding", back_populates="asset")

class Risk(Base):
    __tablename__ = "risks"
    
    id = Column(Integer, primary_key=True, index=True)
    finding_id = Column(Integer, ForeignKey("findings.id"), unique=True)
    
    
    inherent_score = Column(Float)
    residual_score = Column(Float, default=None)
    risk_rating = Column(String) # Low/Med/High/Critical
    
    
    cia_confidentiality = Column(Float)
    cia_integrity = Column(Float)
    cia_availability = Column(Float)
    
    # Relationship back to Finding
    finding = relationship("Finding", back_populates="risk", uselist=False)

class Framework(Base):
    __tablename__ = "frameworks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)      # e.g., 'NIST 800-53', 'ISO 27001'
    version = Column(String)

    controls = relationship(
        "Control", 
        secondary="framework_control_link", # Use the table name here
        back_populates="frameworks"
    )

class Control(Base):
    __tablename__ = "controls"
    id = Column(Integer, primary_key=True, index=True)
    control_name = Column(String)                       # e.g., 'Configuration Management'
    cia_domain = Column(String)                         # e.g., 'Integrity, Availability'
    # Map back to findings (M:M relationship via finding_control_link)
    findings = relationship("Finding", secondary="finding_control_link", back_populates="controls")

    frameworks = relationship(
        "Framework", 
        secondary="framework_control_link", # Use the table name here
        back_populates="controls"
    )

finding_control_link = Table(
    'finding_control_link', Base.metadata,
    Column('finding_id', ForeignKey('findings.id'), primary_key=True),
    Column('control_id', ForeignKey('controls.id'), primary_key=True)
)

# --- Framework Control Mapping (M:M Linking Table - NEW) ---
framework_control_link = Table(
    'framework_control_link', Base.metadata,
    Column('framework_id', ForeignKey('frameworks.id'), primary_key=True),
    Column('control_id', ForeignKey('controls.id'), primary_key=True)
)


# Finding Model
class Finding(Base):
    __tablename__ = "findings"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    

    normalized_title = Column(String, index=True)
    source_type = Column(String) 
    normalized_severity = Column(String) # 'Low', 'Medium', 'High', 'Critical'
    
    
    raw_evidence = Column(JSONB) 
    ingestion_date = Column(DateTime, default=datetime.utcnow)
    controls = relationship("Control", secondary=finding_control_link, back_populates="findings")
    
    asset = relationship("Asset", back_populates="findings")
    risk = relationship("Risk", back_populates="finding", uselist=False)
    