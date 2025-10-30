from fastapi import FastAPI
from .core import models, database 
from .routers import findings

models.Base.metadata.create_all(bind=database.engine) 

app = FastAPI(title="Project GRC-MMAP API")

# NEW LINE: Include the new router
app.include_router(findings.router) 

@app.get("/", tags=["Status"])
def read_root():
    """Confirms the API is running."""
    return {"status": "GRC-MMAP API Operational"}