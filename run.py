#!/usr/bin/env python3
"""
GitGeist Web Server & API (FastAPI).
Serves the Haunted Terminal + Día de los Muertos Digital Ofrenda UI on localhost:8080.
"""
import os
from pathlib import Path
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

from gitgeist.forecaster import HauntingForecaster
from gitgeist.scanner import PRESET_HAUNTED_ARTIFACTS, scan_local_git_repo
from gitgeist.seance_llm import generate_seance_whisper, generate_ofrenda_tribute

app = FastAPI(
    title="GitGeist: Ghost in the Machine",
    description="Offline-First Haunted Git Séance, Code Ofrenda & TabPFN Anomaly Forecaster",
    version="1.0.0",
)

STATIC_DIR = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

forecaster = HauntingForecaster()


class CustomSeanceRequest(BaseModel):
    commit_hash: str = "d3adbeef"
    author: str = "Late-Night Developer"
    date: str = "2026-10-31 02:45:00"
    message: str = "hotfix: bypass mutex timeout during midnight spike"
    file_path: str = "src/daemon/worker.py"
    suspicious_line: str = "retry_limit = 9999  # temporary fix"
    deleted_code: str = "def graceful_backoff(attempt): return min(60, 2 ** attempt)"
    legacy_purpose: str = "Protected worker queues during the early beta launch."
    commit_hour: int = 2
    lines_churned: int = 340
    files_touched: int = 7
    cyclomatic_delta: float = 28.0
    days_since_last_touch: int = 820
    prior_authors_count: int = 5
    cpu_temp_spike_c: float = 75.5
    test_coverage_pct: float = 34.0


@app.get("/")
def index():
    return FileResponse(str(STATIC_DIR / "index.html"))


@app.get("/api/presets")
def get_presets():
    results = []
    for item in PRESET_HAUNTED_ARTIFACTS:
        forecast = forecaster.predict_risk(item["telemetry"])
        seance = generate_seance_whisper(item, forecast)
        ofrenda = generate_ofrenda_tribute(item, forecast)
        results.append({
            **item,
            "forecast": forecast,
            "seance": seance,
            "ofrenda": ofrenda,
        })
    return {"presets": results, "forecaster_backend": forecaster.backend_name}


@app.post("/api/seance")
def run_custom_seance(req: CustomSeanceRequest):
    is_witch = 1 if req.commit_hour in (0, 1, 2, 3, 4) else 0
    telemetry = {
        "commit_hour": req.commit_hour,
        "is_witching_hour": is_witch,
        "lines_churned": req.lines_churned,
        "files_touched": req.files_touched,
        "cyclomatic_delta": req.cyclomatic_delta,
        "days_since_last_touch": req.days_since_last_touch,
        "prior_authors_count": req.prior_authors_count,
        "cpu_temp_spike_c": req.cpu_temp_spike_c,
        "test_coverage_pct": req.test_coverage_pct,
    }
    artifact = {
        "id": f"custom-{req.commit_hash}",
        "commit_hash": req.commit_hash,
        "author": req.author,
        "date": req.date,
        "message": req.message,
        "file_path": req.file_path,
        "suspicious_line": req.suspicious_line,
        "deleted_code": req.deleted_code,
        "legacy_purpose": req.legacy_purpose,
        "telemetry": telemetry,
    }
    forecast = forecaster.predict_risk(telemetry)
    seance = generate_seance_whisper(artifact, forecast)
    ofrenda = generate_ofrenda_tribute(artifact, forecast)
    return {
        "artifact": artifact,
        "forecast": forecast,
        "seance": seance,
        "ofrenda": ofrenda,
    }


@app.get("/api/scan-local")
def scan_local(path: Optional[str] = None):
    target = Path(path).resolve() if path else Path(__file__).resolve().parent
    records = scan_local_git_repo(target)
    enriched = []
    for item in records:
        forecast = forecaster.predict_risk(item["telemetry"])
        seance = generate_seance_whisper(item, forecast)
        ofrenda = generate_ofrenda_tribute(item, forecast)
        enriched.append({
            **item,
            "forecast": forecast,
            "seance": seance,
            "ofrenda": ofrenda,
        })
    return {"repo": str(target), "artifacts": enriched}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"👻 GitGeist summoning on http://localhost:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
