import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from data_generator.generate_data import generate_row

STREAM_DIR = Path(os.environ.get("NHRIS_STREAM", "data/stream/input"))
STREAM_DIR.mkdir(parents=True, exist_ok=True)


def main():
    print(f"Streaming to {STREAM_DIR} ...")
    while True:
        row = generate_row()
        row["timestamp"] = datetime.now(timezone.utc).isoformat()
        fname = STREAM_DIR / f"event_{int(time.time()*1000)}.json"
        with fname.open("w", encoding="utf-8") as f:
            json.dump(row, f)
        time.sleep(1)


if __name__ == "__main__":
    main()
