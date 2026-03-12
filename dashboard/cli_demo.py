from pathlib import Path
import json

ALERTS_PATH = Path("data/alerts/latest.json")

if not ALERTS_PATH.exists():
    print("No alerts yet. Run the generator and Spark job first.")
    raise SystemExit(0)

alerts = json.loads(ALERTS_PATH.read_text(encoding="utf-8")).get("alerts", [])

print("NHRIS Alerts")
print("============")
if not alerts:
    print("No active alerts.")
else:
    for a in alerts:
        print(f"{a['region']} / {a['city']} ? {a['diagnosis']} ({a['case_count']}) :: {a['alert_reason']}")
