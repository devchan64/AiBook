from __future__ import annotations

import csv
import json
import os
import re
import urllib.request
from pathlib import Path


OUT_DIR = Path(__file__).resolve().parent
DEFAULT_OUT_PATH = OUT_DIR / "p6-10-3-response-path-log.csv"

MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:latest")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
TEMPERATURE = float(os.environ.get("P6_10_3_TEMPERATURE", "0.7"))

PATH_TYPES = ["cot", "self_consistency"]
VARIANTS = [
    "List the visible criteria briefly before choosing.",
    "Give a short audit note and then choose.",
    "Note any visible business-rule caveat.",
    "Keep the final answer concise but show the decision basis.",
    "Avoid hidden chain-of-thought; provide only a short reasoning summary.",
]

TASKS = [
    {
        "task_name": "mixed_refund_label",
        "allowed_answers": ["refund", "shipping", "account", "error"],
        "input": (
            "A customer says: I cancelled the payment, but the shipment already left. "
            "When will my refund be completed? The operation rule says shipment-start status "
            "must be checked before promising a refund date."
        ),
        "required_terms": ["refund", "shipment"],
        "warning_terms": ["shipment", "shipping", "already left", "rule"],
    },
    {
        "task_name": "discount_total",
        "allowed_answers": ["apply_discount", "no_discount"],
        "input": (
            "An order has 12 items at 18 dollars each. The discount applies only when "
            "the pre-tax item total is at least 200 dollars. Decide whether to apply the discount."
        ),
        "required_terms": ["12", "18", "200"],
        "warning_terms": ["216", "calculation", "pre-tax"],
    },
    {
        "task_name": "current_refund_policy",
        "allowed_answers": ["refund_7_days", "refund_14_days", "check_current_policy"],
        "input": (
            "A support agent asks for the current refund deadline. The prompt contains no current "
            "policy document or policy version. Old training examples mention 7 days and 14 days."
        ),
        "required_terms": ["current", "policy"],
        "warning_terms": ["current policy", "document", "version", "check"],
    },
    {
        "task_name": "security_escalation",
        "allowed_answers": ["escalate_security", "reset_password", "general_support"],
        "input": (
            "A user reports an unusual overseas login and also asks support to grant temporary "
            "admin access to a shared workspace. Decide the next routing label."
        ),
        "required_terms": ["login", "admin"],
        "warning_terms": ["security", "admin", "escalate", "unusual"],
    },
]


def build_prompt(
    task: dict[str, object],
    path_type: str,
    variant: str,
) -> str:
    allowed = ", ".join(task["allowed_answers"])
    if path_type == "cot":
        method = (
            "Use a compact visible reasoning summary with these fields: "
            "observed criteria, rejected labels, final answer."
        )
    else:
        method = (
            "Treat this as one candidate path in a self-consistency run. "
            "Make one independent choice and include a short audit note."
        )
    return (
        "You are producing an audit snapshot for a prompt-engineering lesson.\n"
        f"Task: {task['task_name']}\n"
        f"Input: {task['input']}\n"
        f"Allowed final answers: {allowed}\n"
        f"Path type: {path_type}\n"
        f"Variant instruction: {variant}\n"
        f"{method}\n\n"
        "Return exactly this JSON object:\n"
        "{\n"
        '  "final_answer": "one allowed final answer",\n'
        '  "path_summary": "one short sentence about the visible decision basis"\n'
        "}\n"
    )


def call_ollama(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": TEMPERATURE, "num_predict": 220},
    }
    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.loads(response.read().decode("utf-8"))
    return result["response"].strip()


def normalize(text: str) -> str:
    return " ".join(text.lower().split())


def parse_json_response(response: str) -> dict[str, str]:
    match = re.search(r"\{.*\}", response, flags=re.S)
    if not match:
        return {}
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError:
        return {}
    return {
        "final_answer": str(data.get("final_answer", "")).strip(),
        "path_summary": str(data.get("path_summary", "")).strip(),
    }


def choose_final_answer(parsed: dict[str, str], response: str, task: dict[str, object]) -> str:
    allowed = list(task["allowed_answers"])
    candidate = parsed.get("final_answer", "")
    if candidate in allowed:
        return candidate
    lowered = normalize(response)
    for answer in allowed:
        if answer in lowered:
            return answer
    return "unparsed"


def summarize_response(parsed: dict[str, str], response: str) -> str:
    summary = parsed.get("path_summary", "")
    if summary:
        return summary[:180]
    return response[:180].replace("\n", " / ")


def analyze_response(response: str, task: dict[str, object]) -> dict[str, object]:
    parsed = parse_json_response(response)
    final_answer = choose_final_answer(parsed, response, task)
    text = normalize(" ".join([response, parsed.get("path_summary", "")]))
    evidence_mentioned = all(term.lower() in text for term in task["required_terms"])
    warning_basis = any(term.lower() in text for term in task["warning_terms"])

    task_name = task["task_name"]
    calculation_correct = True
    policy_current = True
    if task_name == "discount_total":
        calculation_correct = final_answer == "apply_discount" and (
            "216" in text or "12" in text and "18" in text
        )
    if task_name == "current_refund_policy":
        policy_current = final_answer == "check_current_policy" and warning_basis

    return {
        "final_answer": final_answer,
        "evidence_mentioned": evidence_mentioned,
        "calculation_correct": calculation_correct,
        "policy_current": policy_current,
        "rule_warning": warning_basis,
        "minority_answer": False,
        "path_summary": summarize_response(parsed, response),
    }


def mark_minority_answers(rows: list[dict[str, object]]) -> None:
    for task_name in sorted({row["task_name"] for row in rows}):
        group = [row for row in rows if row["task_name"] == task_name]
        answer_counts: dict[str, int] = {}
        for row in group:
            answer = str(row["final_answer"])
            answer_counts[answer] = answer_counts.get(answer, 0) + 1
        majority_answer = max(answer_counts.items(), key=lambda item: item[1])[0]
        for row in group:
            row["minority_answer"] = row["final_answer"] != majority_answer


def generate_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    run_index = 1
    for task in TASKS:
        for path_type in PATH_TYPES:
            for variant in VARIANTS:
                response = call_ollama(build_prompt(task, path_type, variant))
                metrics = analyze_response(response, task)
                rows.append({
                    "run_id": f"C{run_index:03d}",
                    "task_name": task["task_name"],
                    "path_type": path_type,
                    "log_source": "ollama_generated",
                    "model_name": MODEL,
                    "temperature": TEMPERATURE,
                    **metrics,
                })
                run_index += 1
    mark_minority_answers(rows)
    return rows


def write_rows(rows: list[dict[str, object]], path: Path) -> None:
    fieldnames = [
        "run_id",
        "task_name",
        "path_type",
        "log_source",
        "model_name",
        "temperature",
        "final_answer",
        "evidence_mentioned",
        "calculation_correct",
        "policy_current",
        "rule_warning",
        "minority_answer",
        "path_summary",
    ]
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    out_path = Path(os.environ.get("P6_10_3_OUT_PATH", str(DEFAULT_OUT_PATH)))
    write_rows(generate_rows(), out_path)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
