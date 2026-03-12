import csv
import os
import random
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(os.environ.get("NHRIS_DATA", "data"))
OUTPUT_DIR = BASE_DIR / "raw"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REGIONS = ["Karnataka", "Maharashtra", "Delhi", "Tamil Nadu", "Kerala", "Gujarat"]
CITIES = {
    "Karnataka": ["Bengaluru", "Mysuru"],
    "Maharashtra": ["Mumbai", "Pune"],
    "Delhi": ["New Delhi"],
    "Tamil Nadu": ["Chennai", "Coimbatore"],
    "Kerala": ["Kochi", "Thiruvananthapuram"],
    "Gujarat": ["Ahmedabad", "Surat"],
}
DIAGNOSES = ["fever", "respiratory", "cardiac", "diabetes", "trauma", "covid"]


def generate_row():
    region = random.choice(REGIONS)
    city = random.choice(CITIES[region])
    temp = round(random.uniform(97.0, 104.0), 1)
    heart_rate = random.randint(55, 140)
    oxygen = random.randint(85, 100)
    bp_systolic = random.randint(90, 170)
    bp_diastolic = random.randint(60, 110)

    if temp >= 100.4:
        diagnosis = "fever"
    elif oxygen <= 90:
        diagnosis = "respiratory"
    else:
        diagnosis = random.choice(DIAGNOSES)

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "heart_rate": heart_rate,
        "oxygen_level": oxygen,
        "temperature": temp,
        "blood_pressure": f"{bp_systolic}/{bp_diastolic}",
        "patient_location": f"{region}:{city}",
        "diagnosis": diagnosis,
    }


def main(rows: int = 500):
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_path = OUTPUT_DIR / f"health_{ts}.csv"
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "timestamp",
                "heart_rate",
                "oxygen_level",
                "temperature",
                "blood_pressure",
                "patient_location",
                "diagnosis",
            ],
        )
        writer.writeheader()
        for _ in range(rows):
            writer.writerow(generate_row())
    print(f"Generated {rows} rows -> {out_path}")


if __name__ == "__main__":
    main()
