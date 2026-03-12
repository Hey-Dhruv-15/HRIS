from pathlib import Path
import json
import os
from typing import List, Dict

DATA_DIR = Path(os.environ.get("NHRIS_DATA", "data"))
ALERTS_PATH = DATA_DIR / "alerts" / "latest.json"


def load_alerts() -> List[Dict]:
    if not ALERTS_PATH.exists():
        return []
    try:
        return json.loads(ALERTS_PATH.read_text(encoding="utf-8")).get("alerts", [])
    except Exception:
        return []


def answer_question(question: str) -> str:
    alerts = load_alerts()
    if not alerts:
        return "No alerts detected yet."

    q = question.lower()
    if "overload" in q or "overloaded" in q:
        top = sorted(alerts, key=lambda x: x.get("case_count", 0), reverse=True)[:3]
        return "Top overloaded regions: " + ", ".join(
            f"{a.get('city')} ({a.get('region')})" for a in top
        )
    if "fever" in q:
        fever = [a for a in alerts if a.get("diagnosis") == "fever"]
        if not fever:
            return "No abnormal fever spikes today."
        return "Abnormal fever regions: " + ", ".join(
            f"{a.get('city')} ({a.get('region')})" for a in fever
        )
    if "respiratory" in q:
        resp = [a for a in alerts if a.get("diagnosis") == "respiratory"]
        if not resp:
            return "No abnormal respiratory spikes today."
        return "Abnormal respiratory regions: " + ", ".join(
            f"{a.get('city')} ({a.get('region')})" for a in resp
        )

    return "I can answer about fever spikes, respiratory spikes, or overloaded hospitals."
