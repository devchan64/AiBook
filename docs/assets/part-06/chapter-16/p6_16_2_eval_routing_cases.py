from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from pprint import pprint


OUT_DIR = Path(__file__).resolve().parent
CSV_PATH = OUT_DIR / "p6_16_2_eval_routing_cases.csv"


def split_terms(value: str) -> list[str]:
    return [term.strip() for term in value.split("|") if term.strip()]


def automatic_gate(row: dict[str, str]) -> dict[str, bool]:
    output = row["model_output"]
    banned_hits = [term for term in split_terms(row["banned_terms"]) if term in output]
    return {
        "source_marker_ok": row["source_marker"] in output,
        "required_action_ok": row["required_action"] in output,
        "format_ok": output.endswith(row["format_marker"]),
        "length_ok": len(output) <= int(row["max_length"]),
        "cost_ok": int(row["latency_ms"]) <= 2500
        and int(row["tool_call_count"]) <= 6
        and int(row["failed_tool_call_count"]) <= 1,
        "banned_terms_ok": not banned_hits,
    }


def gate_fix_note(gate: dict[str, bool]) -> str:
    failed = [name for name, passed in gate.items() if not passed]
    if not failed:
        return "-"
    return "자동 게이트 실패 항목을 먼저 수정한다: " + ", ".join(failed)


def human_review_question(row: dict[str, str]) -> str:
    if row["risk_level"] == "low":
        return "가벼운 최종 확인만 남긴다: 말투와 안내 순서가 자연스러운가?"
    focus_to_question = {
        "missing_next_action": "사용자가 다음 행동을 바로 이해할 수 있는가?",
        "policy_exception_check": "정책 예외나 제한 조건을 지나치게 단정하지 않았는가?",
        "too_general": "답이 너무 일반적이어서 실제 판단에 필요한 조건을 빠뜨리지 않았는가?",
        "borderline_cost": "경계 수준의 비용이 실제 작업 복잡도에 비해 필요한 수준인가?",
        "missing_cost_detail": "최종 성공만 말하고 비용과 실패 신호를 숨기지 않았는가?",
        "missing_ticket_number": "지원팀이 이어서 처리할 요청 번호가 남아 있는가?",
        "missing_reset_link": "사용자가 실제로 따라 할 재설정 경로가 보이는가?",
        "missing_expert_guidance": "안전한 대안만 있고 전문가 상담 안내가 빠지지 않았는가?",
    }
    return focus_to_question.get(
        row["human_review_focus"],
        "문맥상 오해, 과도한 단정, 말투 위험을 사람이 끝까지 확인해야 하는가?",
    )


def route_case(row: dict[str, str]) -> dict[str, object]:
    gate = automatic_gate(row)
    auto_pass = all(gate.values())
    if not auto_pass:
        route = "reject_before_human_review"
    elif row["risk_level"] == "low":
        route = "approve_candidate"
    else:
        route = "send_to_human_review"

    return {
        "case_id": row["case_id"],
        "domain": row["domain"],
        "auto_pass": auto_pass,
        "gate": gate,
        "risk_level": row["risk_level"],
        "human_review_focus": row["human_review_focus"],
        "gate_fix_note": gate_fix_note(gate),
        "human_review_question": human_review_question(row) if auto_pass else "-",
        "route": route,
    }


def load_reports() -> list[dict[str, object]]:
    with CSV_PATH.open(newline="", encoding="utf-8") as csv_file:
        rows = list(csv.DictReader(csv_file))
    return [route_case(row) for row in rows]


def summarize_reports(reports: list[dict[str, object]]) -> dict[str, object]:
    route_counts = Counter(str(report["route"]) for report in reports)
    auto_pass_count = sum(bool(report["auto_pass"]) for report in reports)
    risk_counts = Counter(str(report["risk_level"]) for report in reports)
    return {
        "case_count": len(reports),
        "auto_pass_count": auto_pass_count,
        "auto_fail_count": len(reports) - auto_pass_count,
        "send_to_human_review_count": route_counts["send_to_human_review"],
        "approve_candidate_count": route_counts["approve_candidate"],
        "reject_before_human_review_count": route_counts["reject_before_human_review"],
        "risk_level_count": dict(sorted(risk_counts.items())),
        "route_count": dict(sorted(route_counts.items())),
    }


def main() -> None:
    reports = load_reports()
    print("[summary]")
    pprint(summarize_reports(reports))
    print()

    for report in reports[:8]:
        print("=" * 80)
        print(report["case_id"], "/", report["domain"])
        print("auto_pass =", report["auto_pass"])
        print("gate =")
        pprint(report["gate"])
        print("risk_level =", report["risk_level"])
        print("gate_fix_note =", report["gate_fix_note"])
        print("human_review_question =", report["human_review_question"])
        print("route =", report["route"])


if __name__ == "__main__":
    main()
