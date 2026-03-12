from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pathlib import Path
import json

app = FastAPI(title="NHRIS API")
ALERTS_PATH = Path("/opt/data/alerts/latest.json")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/alerts")
def get_alerts():
    if not ALERTS_PATH.exists():
        return JSONResponse({"alerts": [], "message": "No alerts yet"}, status_code=200)
    return json.loads(ALERTS_PATH.read_text(encoding="utf-8"))
