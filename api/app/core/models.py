from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
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
    
    
    asset = relationship("Asset", back_populates="findings")
    risk = relationship("Risk", back_populates="finding", uselist=False)
    