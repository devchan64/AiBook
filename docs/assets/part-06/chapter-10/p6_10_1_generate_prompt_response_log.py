from __future__ import annotations

import csv
import json
import os
import urllib.request
from pathlib import Path


OUT_DIR = Path(__file__).resolve().parent
DEFAULT_OUT_PATH = OUT_DIR / "p6-10-1-prompt-response-log.csv"

MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:latest")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
REPEAT_COUNT = int(os.environ.get("P6_10_1_REPEAT_COUNT", "5"))
TEMPERATURE = float(os.environ.get("P6_10_1_TEMPERATURE", "0.2"))

SLOTS = ["situation", "immediate action", "remaining risk"]

CARDS = [
    {
        "card_name": "billing outage",
        "note": (
            "Mobile checkout approvals failed for 17 minutes. The payment gateway was rolled back. "
            "Operations still need to collect transaction logs before closing the incident."
        ),
        "keywords": ["approval", "rollback", "logs"],
    },
    {
        "card_name": "shipping delay",
        "note": (
            "Fresh food deliveries are delayed by a day and a half because of heavy rain. "
            "Customer messages were sent, and the carrier must recheck the route at 6 PM."
        ),
        "keywords": ["fresh food", "6 PM", "day and a half"],
    },
    {
        "card_name": "account lock",
        "note": (
            "External partners cannot log in because SSO group sync is delayed. "
            "The help desk should track the sync status and keep a manual access procedure ready."
        ),
        "keywords": ["external partners", "sync", "manual access"],
    },
    {
        "card_name": "refund backlog",
        "note": (
            "Refund reviews are backed up by 320 cases after a tax rule update. "
            "Finance must approve the exception queue before support sends final customer replies."
        ),
        "keywords": ["320 cases", "tax rule", "finance"],
    },
]


def build_prompt(card: dict[str, object], prompt_type: str) -> str:
    note = card["note"]
    if prompt_type == "simple":
        return f"Summarize this operations note briefly.\n\nNote:\n{note}"
    if prompt_type == "instruction_context":
        return (
            "Summarize this operations note for an operations owner.\n"
            "Return exactly three numbered lines.\n"
            "Use these slot labels exactly: Situation, Immediate action, Remaining risk.\n"
            "Keep the important operational facts from the note.\n\n"
            f"Note:\n{note}"
        )
    if prompt_type == "instruction_context_example":
        return (
            "Summarize this operations note for an operations owner.\n"
            "Return exactly three numbered lines.\n"
            "Use these slot labels exactly: Situation, Immediate action, Remaining risk.\n"
            "Keep the important operational facts from the note.\n\n"
            "Example output format:\n"
            "1. Situation: One sentence about what happened.\n"
            "2. Immediate action: One sentence about what the operator should do now.\n"
            "3. Remaining risk: One sentence about what still needs watching.\n\n"
            f"Note:\n{note}"
        )
    return (
        "Summarize this operations note for an operations owner.\n"
        "Return exactly three numbered lines.\n"
        "Use these slot labels exactly: Situation, Immediate action, Remaining risk.\n"
        "Keep the important operational facts from the note.\n\n"
        "Before answering, check that each important fact from the note appears in the final answer.\n"
        "Do not add an introduction or closing sentence.\n\n"
        "Example output format:\n"
        "1. Situation: One sentence about what happened.\n"
        "2. Immediate action: One sentence about what the operator should do now.\n"
        "3. Remaining risk: One sentence about what still needs watching.\n\n"
        f"Note:\n{note}"
    )


def call_ollama(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": TEMPERATURE,
            "num_predict": 160,
        },
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.loads(response.read().decode("utf-8"))
    return result["response"].strip()


def normalize(text: str) -> str:
    return " ".join(text.lower().split())


def analyze_response(response: str, card: dict[str, object]) -> dict[str, object]:
    lines = [line.strip() for line in response.splitlines() if line.strip()]
    lowered = normalize(response)
    numbered_lines = all(
        line.startswith((f"{index}.", f"{index})"))
        for index, line in enumerate(lines, start=1)
    ) if lines else False
    slot_count = sum(slot in lowered for slot in SLOTS)
    keyword_hits = sum(normalize(keyword) in lowered for keyword in card["keywords"])
    missing_slots = [slot for slot in SLOTS if slot not in lowered]
    return {
        "line_count": len(lines),
        "numbered_lines": numbered_lines,
        "slot_count": slot_count,
        "keyword_hits": keyword_hits,
        "keyword_total": len(card["keywords"]),
        "missing_slots": ";".join(missing_slots),
        "response_note": response[:160].replace("\n", " / "),
    }


def generate_rows() -> list[dict[str, object]]:
    rows = []
    run_index = 1
    prompt_types = [
        "simple",
        "instruction_context",
        "instruction_context_example",
        "instruction_context_example_check",
    ]
    for prompt_type in prompt_types:
        for card in CARDS:
            for _ in range(REPEAT_COUNT):
                response = call_ollama(build_prompt(card, prompt_type))
                metrics = analyze_response(response, card)
                rows.append({
                    "run_id": f"R{run_index:02d}",
                    "prompt_type": prompt_type,
                    "card_name": card["card_name"],
                    "log_source": "ollama_generated",
                    "model_name": MODEL,
                    "temperature": TEMPERATURE,
                    "slot_language": "en",
                    **metrics,
                })
                run_index += 1
    return rows


def write_rows(rows: list[dict[str, object]], path: Path) -> None:
    fieldnames = [
        "run_id",
        "prompt_type",
        "card_name",
        "log_source",
        "model_name",
        "temperature",
        "slot_language",
        "line_count",
        "numbered_lines",
        "slot_count",
        "keyword_hits",
        "keyword_total",
        "missing_slots",
        "response_note",
    ]
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    out_path = Path(os.environ.get("P6_10_1_OUT_PATH", str(DEFAULT_OUT_PATH)))
    write_rows(generate_rows(), out_path)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
