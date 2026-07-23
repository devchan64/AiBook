from collections import Counter
from csv import DictReader
from pathlib import Path
from pprint import pprint

CSV_PATH = Path(__file__).with_name("p6_17_2_failure_cases.csv")

SELECTED_CASES = [
    "timeout_retry_search",
    "timeout_fallback_search",
    "permission_approval_send",
    "risky_action_stop_no_reviewer",
    "hallucination_review_grounded",
    "format_fix_parser",
]


def parse_bool(value):
    return value == "yes"


def load_failure_cases(csv_path=CSV_PATH):
    with csv_path.open(newline="", encoding="utf-8") as file:
        rows = list(DictReader(file))

    cases = []
    for row in rows:
        cases.append(
            {
                "case_id": row["case_id"],
                "case_name": row["case_name"],
                "failure_family": row["failure_family"],
                "step": row["step"],
                "error": row["error"],
                "retry_count": int(row["retry_count"]),
                "max_retries": int(row["max_retries"]),
                "cached_summary_available": parse_bool(
                    row["cached_summary_available"]
                ),
                "trace_saved": parse_bool(row["trace_saved"]),
                "human_review_available": parse_bool(row["human_review_available"]),
                "grounding_available": parse_bool(row["grounding_available"]),
                "approval_required": parse_bool(row["approval_required"]),
            }
        )
    return cases


def decide_recovery(case):
    if not case["trace_saved"]:
        return {
            "decision": "stop_and_escalate",
            "decision_reason": "trace_missing",
            "next_action": "save_trace_before_continuing",
            "user_impact": "cannot_reproduce_failure",
        }
    if case["approval_required"]:
        if case["human_review_available"]:
            return {
                "decision": "approval",
                "decision_reason": "approval_required",
                "next_action": "request_human_approval",
                "user_impact": "wait_for_safe_execution",
            }
        return {
            "decision": "stop_and_escalate",
            "decision_reason": "approval_required_but_unavailable",
            "next_action": "stop_without_execution",
            "user_impact": "unsafe_to_continue",
        }
    if case["error"] in {"permission_error", "tool_not_found", "unsafe_claim"}:
        return {
            "decision": "stop_and_escalate",
            "decision_reason": case["error"],
            "next_action": "ask_human_review",
            "user_impact": "unsafe_or_impossible_to_continue",
        }
    if case["error"] in {"hallucination", "wrong_citation", "grounding_gap"}:
        if case["grounding_available"] and case["human_review_available"]:
            return {
                "decision": "human_review",
                "decision_reason": "compare_answer_with_grounding",
                "next_action": "compare_with_grounding",
                "user_impact": "potential_wrong_answer",
            }
        return {
            "decision": "stop_and_escalate",
            "decision_reason": "grounding_or_review_missing",
            "next_action": "stop_until_evidence_is_available",
            "user_impact": "answer_blocked",
        }
    if case["error"] in {
        "format_mismatch",
        "overlong_answer",
        "tone_mismatch",
    }:
        return {
            "decision": "model_fix",
            "decision_reason": case["error"],
            "next_action": "tighten_prompt_parser_or_schema",
            "user_impact": "delivery_blocked_until_format_fixed",
        }
    if case["error"] in {"ambiguous_answer", "unverified_number", "cache_stale"}:
        return {
            "decision": "human_review",
            "decision_reason": case["error"],
            "next_action": "review_before_user_delivery",
            "user_impact": "needs_review_before_release",
        }
    if case["retry_count"] < case["max_retries"]:
        return {
            "decision": "retry",
            "decision_reason": "retry_budget_remaining",
            "next_action": f"retry_{case['step']}",
            "user_impact": "temporary_delay",
        }
    if case["cached_summary_available"]:
        return {
            "decision": "fallback",
            "decision_reason": "retry_budget_exhausted_with_cache",
            "next_action": "use_cached_or_simplified_path",
            "user_impact": "reduced_freshness_but_service_continues",
        }
    return {
        "decision": "stop_and_escalate",
        "decision_reason": "no_recovery_path_left",
        "next_action": "ask_human_review",
        "user_impact": "service_stopped_for_this_request",
    }


def evaluate_case(case):
    recovery = decide_recovery(case)
    return {
        "case_name": case["case_name"],
        "failure_family": case["failure_family"],
        "step": case["step"],
        "error": case["error"],
        "retry_count": case["retry_count"],
        "max_retries": case["max_retries"],
        "cached_summary_available": case["cached_summary_available"],
        "approval_required": case["approval_required"],
        "trace_saved": case["trace_saved"],
        **recovery,
    }


def load_reports():
    return [evaluate_case(case) for case in load_failure_cases()]


def summarize_reports(reports):
    decision_counts = Counter(report["decision"] for report in reports)
    family_counts = Counter(report["failure_family"] for report in reports)
    return {
        "case_count": len(reports),
        "system_failure_count": family_counts["system"],
        "model_failure_count": family_counts["model"],
        "retry_count": decision_counts["retry"],
        "fallback_count": decision_counts["fallback"],
        "approval_count": decision_counts["approval"],
        "human_review_count": decision_counts["human_review"],
        "stop_and_escalate_count": decision_counts["stop_and_escalate"],
        "model_fix_count": decision_counts["model_fix"],
    }


def compact_report(report):
    return {
        "case_name": report["case_name"],
        "failure_family": report["failure_family"],
        "step": report["step"],
        "error": report["error"],
        "decision": report["decision"],
        "decision_reason": report["decision_reason"],
        "next_action": report["next_action"],
        "user_impact": report["user_impact"],
    }


def main():
    reports = load_reports()
    selected_reports = [
        compact_report(report)
        for report in reports
        if report["case_name"] in SELECTED_CASES
    ]

    print("[summary]")
    pprint(summarize_reports(reports))
    print("[selected_cases]")
    for report in selected_reports:
        pprint(report)


if __name__ == "__main__":
    main()
