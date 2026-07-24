from collections import Counter
from csv import DictReader
import json
import os
from pathlib import Path
from pprint import pprint
from urllib import request

CSV_PATH = Path(__file__).with_name("p6_17_2_failure_cases.csv")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:1b")
USE_OLLAMA = os.environ.get("P6_17_2_USE_OLLAMA") == "1"
GRADER_RUBRIC = """
Grade the failure trace, but do not choose the final recovery route.
- suggested_family is "system" when the failure is in retrieval, tools,
  permissions, timeout, cache, queue, API, or trace capture.
- suggested_family is "model" when the failure is in generation, grounding,
  citation, tone, format, or unsupported content.
- suggested_risk is "high" when the trace is missing, evidence is missing,
  approval is required, or unsafe output may reach a user.
- suggested_risk is "medium" when service can continue only after retry,
  fallback, parser repair, or human review.
- suggested_risk is "low" only when the failure is minor and already contained.

Examples:
- error=timeout at step=search_docs -> system, medium
- error=permission_error at step=send_email -> system, high
- error=risky_action at step=update_database -> system, high
- error=hallucination at step=answer_generation -> model, high
- error=format_mismatch at step=answer_generation -> model, medium
"""

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


def build_failure_observation(case):
    return (
        f"step={case['step']}; error={case['error']}; "
        f"retry_count={case['retry_count']}; max_retries={case['max_retries']}; "
        f"cached_summary_available={case['cached_summary_available']}; "
        f"trace_saved={case['trace_saved']}; "
        f"human_review_available={case['human_review_available']}; "
        f"grounding_available={case['grounding_available']}; "
        f"approval_required={case['approval_required']}"
    )


def fallback_grade_failure_trace(case):
    if case["error"] in {
        "hallucination",
        "wrong_citation",
        "grounding_gap",
        "format_mismatch",
        "overlong_answer",
        "tone_mismatch",
        "ambiguous_answer",
        "unverified_number",
        "unsafe_claim",
        "unsupported_instruction",
    }:
        suggested_family = "model"
    else:
        suggested_family = "system"

    if not case["trace_saved"] or case["approval_required"]:
        suggested_risk = "high"
    elif case["error"] in {"hallucination", "wrong_citation", "unsafe_claim"}:
        suggested_risk = "high"
    elif case["error"] in {"timeout", "rate_limit", "format_mismatch"}:
        suggested_risk = "medium"
    else:
        suggested_risk = "medium"

    reason_by_error = {
        "timeout": "Timeout belongs to the service path, so retry budget and fallback state must be checked next.",
        "rate_limit": "Rate limit is a system capacity signal, so retry and fallback policy should be checked next.",
        "permission_error": "Permission failure crosses an execution boundary, so approval or stop policy must be checked next.",
        "risky_action": "Risky external action needs an approval boundary before any execution continues.",
        "hallucination": "Hallucination is a model output risk, so grounding and human review must be checked next.",
        "wrong_citation": "Wrong citation is a model grounding risk, so evidence comparison must be checked next.",
        "format_mismatch": "Format mismatch blocks delivery or parsing, so prompt and schema repair must be checked next.",
    }
    return {
        "grader_source": "fallback",
        "suggested_family": suggested_family,
        "suggested_risk": suggested_risk,
        "reason": reason_by_error.get(
            case["error"],
            f"The observed {case['error']} should be graded before the policy gate chooses a recovery route.",
        ),
    }


def call_ollama_grader(case):
    prompt = f"""
You are an LLM grader for AI service failure traces.
Return only compact JSON with these keys:
suggested_family: "system" or "model"
suggested_risk: "low", "medium", or "high"
reason: one short sentence

Rubric:
{GRADER_RUBRIC}

Failure observation:
{build_failure_observation(case)}
"""
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0},
    }
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with request.urlopen(req, timeout=20) as response:
        body = json.loads(response.read().decode("utf-8"))
    return json.loads(body["response"])


def llm_grade_failure_trace(case):
    if USE_OLLAMA:
        try:
            grade = call_ollama_grader(case)
            return {
                "grader_source": "ollama",
                "suggested_family": grade["suggested_family"],
                "suggested_risk": grade["suggested_risk"],
                "reason": grade["reason"],
            }
        except Exception:
            pass
    return fallback_grade_failure_trace(case)


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
    # The LLM grader reads the trace and produces bounded tags. The policy
    # gate below still makes the final recovery decision from explicit signals.
    grade = llm_grade_failure_trace(case)
    recovery = decide_recovery(case)
    return {
        "case_name": case["case_name"],
        "failure_family": case["failure_family"],
        **grade,
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
        "grader_source": report["grader_source"],
        "suggested_family": report["suggested_family"],
        "suggested_risk": report["suggested_risk"],
        "reason": report["reason"],
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
