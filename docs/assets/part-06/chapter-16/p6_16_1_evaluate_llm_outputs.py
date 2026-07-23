from __future__ import annotations

import csv
from pathlib import Path
from pprint import pprint


OUT_DIR = Path(__file__).resolve().parent
CSV_PATH = OUT_DIR / "p6_16_1_llm_eval_outputs.csv"


def split_terms(value: str) -> list[str]:
    return [term.strip() for term in value.split("|") if term.strip()]


def choose_next_fix(evaluation: dict[str, object]) -> str:
    if not evaluation["correctness"]:
        return "fix_missing_or_wrong_core_claim"
    if not evaluation["groundedness"]:
        return "remove_claim_not_supported_by_source"
    if not evaluation["format_compliance"]:
        return "rewrite_to_required_format"
    if not evaluation["helpfulness"]:
        return "add_actionable_guidance"
    return "accept_candidate"


def evaluate_row(row: dict[str, str]) -> dict[str, object]:
    output = row["model_output"]
    source = row["source_excerpt"]
    required_claims = split_terms(row["required_claim_terms"])
    unsupported_claims = split_terms(row["unsupported_claim_terms"])
    format_terms = split_terms(row["format_terms"])
    helpful_terms = split_terms(row["helpful_terms"])

    source_backed_claims = [term for term in required_claims if term in source]
    matched_claims = [term for term in source_backed_claims if term in output]
    unsupported_hits = [
        term for term in unsupported_claims if term in output and term not in source
    ]

    correctness = len(matched_claims) >= max(1, len(source_backed_claims) - 1)
    groundedness = not unsupported_hits
    format_compliance = output.endswith(".") and all(term in output for term in format_terms)
    helpfulness = any(term in output for term in helpful_terms)

    evaluation: dict[str, object] = {
        "correctness": correctness,
        "groundedness": groundedness,
        "format_compliance": format_compliance,
        "helpfulness": helpfulness,
    }
    axes = ["correctness", "groundedness", "format_compliance", "helpfulness"]
    evaluation["passes_all"] = all(evaluation[axis] for axis in axes)
    evaluation["axis_score"] = sum(bool(evaluation[axis]) for axis in axes)
    evaluation["next_fix"] = choose_next_fix(evaluation)
    evaluation["failed_axes"] = [axis for axis in axes if not evaluation[axis]]
    evaluation["matched_claims"] = matched_claims
    evaluation["unsupported_hits"] = unsupported_hits
    return evaluation


def load_reports() -> list[dict[str, object]]:
    with CSV_PATH.open(newline="", encoding="utf-8") as csv_file:
        rows = list(csv.DictReader(csv_file))

    reports = []
    for row in rows:
        reports.append(
            {
                "run_id": row["run_id"],
                "model": row["model"],
                "task_type": row["task_type"],
                "model_output": row["model_output"],
                "evaluation": evaluate_row(row),
            }
        )
    return reports


def summarize_reports(reports: list[dict[str, object]]) -> dict[str, object]:
    axes = ["correctness", "groundedness", "format_compliance", "helpfulness"]
    best_candidate = max(
        reports,
        key=lambda report: int(report["evaluation"]["axis_score"]),  # type: ignore[index]
    )
    return {
        "all_pass_count": sum(
            bool(report["evaluation"]["passes_all"]) for report in reports  # type: ignore[index]
        ),
        "axis_pass_count": {
            axis: sum(
                bool(report["evaluation"][axis]) for report in reports  # type: ignore[index]
            )
            for axis in axes
        },
        "model_count": len({report["model"] for report in reports}),
        "case_count": len(reports),
        "average_axis_score": round(
            sum(int(report["evaluation"]["axis_score"]) for report in reports)  # type: ignore[index]
            / len(reports),
            2,
        ),
        "highest_axis_score_run": best_candidate["run_id"],
    }


def main() -> None:
    reports = load_reports()
    print("[summary]")
    pprint(summarize_reports(reports))
    print()

    for report in reports:
        print("=" * 80)
        print("[case]")
        print(report["run_id"], "/", report["model"], "/", report["task_type"])
        print("[model_output]")
        print(report["model_output"])
        print("[evaluation]")
        pprint(report["evaluation"])


if __name__ == "__main__":
    main()
