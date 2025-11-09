from fastapi import FastAPI
from contextlib import asynccontextmanager 
from fastapi.middleware.cors import CORSMiddleware # CORSMiddleware is correctly imported here
from .core import models, database 
from .routers import findings, dashboard, reports # Ensure 'reports' is imported
from .crud import crud_compliance

# -------------------------------------------------------------
# 1. LIFESPAN MANAGER (DB SETUP ON STARTUP)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes DB tables and seeds compliance data on startup."""
    
    # 1. Create tables
    models.Base.metadata.create_all(bind=database.engine)
    
    # 2. Run Seeding Logic
    db = database.SessionLocal()
    crud_compliance.seed_initial_compliance_data(db)
    db.close()
    
    yield 
# -------------------------------------------------------------

# 2. INITIALIZE APP
app = FastAPI(
    title="Project GRC-MMAP API",
    lifespan=lifespan 
)

# 3. CRITICAL: ADD CORS CONFIGURATION BLOCK HERE!
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ----------------------------------------------------

# 4. INCLUDE ALL ROUTERS
app.include_router(findings.router) 
app.include_router(dashboard.router)
app.include_router(reports.router) # CRITICAL: Include the reports router now!

# 5. ROOT ENDPOINT
@app.get("/", tags=["Status"])
def read_root():
    """Confirms the API is running."""
    return {"status": "GRC-MMAP API Operational"}