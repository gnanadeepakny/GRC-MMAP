from fastapi import FastAPI
from contextlib import asynccontextmanager # 1. Import Lifespan Utility
from .core import models, database 
from .routers import findings
from .crud import crud_compliance

# -------------------------------------------------------------
# 2. DEFINE THE LIFESPAN MANAGER (STARTUP/SHUTDOWN LOGIC)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes DB tables and seeds compliance data on startup."""
    
    # 3. CRITICAL: Move ALL DB setup logic inside here
    # ------------------------------------------------------------------
    # NOTE: The DB connection must be resilient to slight delays here.
    #       It's assumed Docker Compose handles the main DB startup sequence.
    
    # Create tables (ensure all models are imported at the top)
    models.Base.metadata.create_all(bind=database.engine)
    
    # Run Seeding Logic
    db = database.SessionLocal()
    crud_compliance.seed_initial_compliance_data(db)
    db.close()
    # ------------------------------------------------------------------
    
    yield # Application continues running and starts serving requests
    # Cleanup happens after 'yield' on graceful shutdown (not needed now)

# 4. CREATE THE APPLICATION, PASSING THE NEW LIFESPAN FUNCTION
app = FastAPI(
    title="Project GRC-MMAP API",
    lifespan=lifespan # Pass the startup logic here
)
# -------------------------------------------------------------

# DELETE the previous global calls to create_all and seed_initial_compliance_data

# Include the new router
app.include_router(findings.router) 

@app.get("/", tags=["Status"])
def read_root():
    """Confirms the API is running."""
    return {"status": "GRC-MMAP API Operational"}