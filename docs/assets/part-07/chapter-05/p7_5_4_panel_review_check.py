#!/usr/bin/env python3
"""Validate the P7-5.3 full-frame repair gate."""

from __future__ import annotations

import json
from pathlib import Path
import sys


VALID = {"pass", "partial", "fail"}


def main() -> int:
    review = json.loads(Path(sys.argv[1]).read_text())
    errors: list[str] = []
    eligible = 0
    for panel in review["panels"]:
        values = {key: panel[key] for key in ("identity", "structure", "style", "local_detail")}
        if any(value not in VALID for value in values.values()):
            errors.append(f"{panel['panel_id']}: invalid result value")
        full_frame_pass = all(values[key] == "pass" for key in ("identity", "structure", "style"))
        allowed = panel["repair_eligibility"].startswith("eligible")
        if full_frame_pass != allowed:
            errors.append(f"{panel['panel_id']}: repair gate contradicts full-frame results")
        eligible += int(allowed)
    if errors:
        print("FAIL")
        print("\n".join(errors))
        return 1
    print(f"PASS review ledger: {len(review['panels'])} panels, {eligible} eligible for inpaint")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
