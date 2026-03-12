# NHRIS ADK Agent
# Run with: adk api_server --host 0.0.0.0 --port 8000 /path/to/agent

from pathlib import Path
import json
import os
from typing import Dict, List
from google.adk.agents import Agent

DATA_DIR = Path(os.environ.get("NHRIS_DATA", "data"))
ALERTS_PATH = DATA_DIR / "alerts" / "latest.json"


def _load_alerts() -> Dict:
    if not ALERTS_PATH.exists():
        return {"generated_at": None, "alerts": []}
    try:
        return json.loads(ALERTS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"generated_at": None, "alerts": []}


def get_latest_alerts() -> Dict:
    """Return the latest alert batch."""
    return _load_alerts()


def get_fever_spikes() -> List[Dict]:
    """Return fever spike alerts."""
    data = _load_alerts()
    return [a for a in data.get("alerts", []) if a.get("diagnosis") == "fever"]


def get_overload_risks(limit: int = 5) -> List[Dict]:
    """Return highest case count alerts as overload signals."""
    data = _load_alerts()
    alerts = sorted(data.get("alerts", []), key=lambda x: x.get("case_count", 0), reverse=True)
    return alerts[:limit]


def get_region_alerts(region: str) -> List[Dict]:
    """Return alerts for a specific region (case-insensitive match)."""
    region_lower = region.lower()
    data = _load_alerts()
    return [a for a in data.get("alerts", []) if a.get("region", "").lower() == region_lower]


root_agent = Agent(
    name="nhris_health_agent",
    model="gemini-2.0-flash",
    instruction=(
        "You are the NHRIS health risk analyst. Use tools to answer with the latest alerts. "
        "If there are no alerts, clearly say no active alerts. Be concise and action-oriented."
    ),
    tools=[
        get_latest_alerts,
        get_fever_spikes,
        get_overload_risks,
        get_region_alerts,
    ],
)
