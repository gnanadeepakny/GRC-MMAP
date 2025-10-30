from fastapi import FastAPI

app = FastAPI(title="Project GRC-MMAP API")
@app.get("/", tags=["Status"])
def read_root():
    """Confirms the API is running."""
    return {"status": "GRC-MMAP API Operational"}

