"""Check that a locally generated background style-pack review ledger is complete."""

import json
from pathlib import Path


REQUIRED_CAMERAS = {"high angle", "low angle", "wide eye-level", "oblique side view", "overhead high angle"}
REQUIRED_TIMES = {"dawn", "day", "sunset", "night", "rainy night"}


def main() -> None:
    ledger_path = Path(__file__).with_name("p7-5-1-local-style-pack-review.json")
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    matrix = ledger["next_run_matrix"]
    cameras = {row["camera"] for row in matrix}
    times = {row["time"] for row in matrix}
    locations = {row["location"] for row in matrix}

    missing = []
    for name, actual, expected in (
        ("camera", cameras, REQUIRED_CAMERAS),
        ("time", times, REQUIRED_TIMES),
        ("location", locations, {"indoor", "outdoor"}),
    ):
        if actual != expected:
            missing.append(f"{name}: missing {sorted(expected - actual)}")

    if ledger["status"] != "approved_for_downstream_reference":
        missing.append("review status: no approved frame-free style pack")

    if missing:
        print("BLOCKED style pack")
        for item in missing:
            print(f"- {item}")
        return

    print("PASS background style pack is approved for downstream use")


if __name__ == "__main__":
    main()
