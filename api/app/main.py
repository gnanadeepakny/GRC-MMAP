from fastapi import FastAPI
from .core import models, database # NEW IMPORTS

# Create all database tables defined in models.py (if they don't exist)
models.Base.metadata.create_all(bind=database.engine) # NEW LINE

# Initialize the FastAPI application
app = FastAPI(title="Project GRC-MMAP API")

@app.get("/", tags=["Status"])
def read_root():
    """Confirms the API is running."""
    return {"status": "GRC-MMAP API Operational"}