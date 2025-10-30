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
    
    