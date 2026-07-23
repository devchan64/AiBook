from csv import DictReader
from pathlib import Path
from pprint import pprint

CSV_PATH = Path(__file__).with_name("p6_17_1_service_candidates.csv")

CONSTRAINTS = {
    "min_quality_score": 0.75,
    "max_latency_ms": 2000,
    "max_cost_per_1k_requests": 3.0,
    "required_requests_per_minute": 80,
}

SELECTED_CASES = [
    "fast_cached_faq",
    "balanced_support",
    "rich_deep_rag",
    "accurate_but_capped",
    "cost_over_budget_support",
    "capacity_shortfall_support",
]


def load_candidates(csv_path=CSV_PATH):
    with csv_path.open(newline="", encoding="utf-8") as file:
        rows = list(DictReader(file))

    candidates = []
    for row in rows:
        candidates.append(
            {
                "service_id": row["service_id"],
                "service_name": row["service_name"],
                "request_profile": row["request_profile"],
                "quality_score": float(row["quality_score"]),
                "avg_latency_ms": int(row["avg_latency_ms"]),
                "estimated_cost_per_1k_requests": float(
                    row["estimated_cost_per_1k_requests"]
                ),
                "max_requests_per_minute": int(row["max_requests_per_minute"]),
            }
        )
    return candidates


def choose_primary_tradeoff(report):
    # 여러 축이 함께 실패하면 사용자 체감과 요청 경로 축소에 바로 연결되는 축을 먼저 잡습니다.
    if "quality" in report["failed_checks"]:
        return "quality_too_low"
    if "latency" in report["failed_checks"]:
        return "latency_too_high"
    if "cost" in report["failed_checks"]:
        return "cost_too_high"
    if "throughput" in report["failed_checks"]:
        return "throughput_too_low"
    return "operational_fit"


def evaluate_candidate(candidate, constraints=CONSTRAINTS):
    quality_ok = candidate["quality_score"] >= constraints["min_quality_score"]
    latency_ok = candidate["avg_latency_ms"] <= constraints["max_latency_ms"]
    cost_ok = (
        candidate["estimated_cost_per_1k_requests"]
        <= constraints["max_cost_per_1k_requests"]
    )
    throughput_ok = (
        candidate["max_requests_per_minute"]
        >= constraints["required_requests_per_minute"]
    )

    report = {
        "service_name": candidate["service_name"],
        "request_profile": candidate["request_profile"],
        "quality_score": candidate["quality_score"],
        "avg_latency_ms": candidate["avg_latency_ms"],
        "estimated_cost_per_1k_requests": candidate[
            "estimated_cost_per_1k_requests"
        ],
        "max_requests_per_minute": candidate["max_requests_per_minute"],
        "quality_ok": quality_ok,
        "latency_ok": latency_ok,
        "cost_ok": cost_ok,
        "throughput_ok": throughput_ok,
    }
    report["failed_checks"] = [
        check_name
        for check_name, passed in [
            ("quality", quality_ok),
            ("latency", latency_ok),
            ("cost", cost_ok),
            ("throughput", throughput_ok),
        ]
        if not passed
    ]
    primary_tradeoff = choose_primary_tradeoff(report)
    next_adjustment_map = {
        "quality_too_low": "raise_answer_quality_before_cost_cutting",
        "latency_too_high": "reduce_steps_context_or_tool_calls",
        "cost_too_high": "shrink_context_model_or_generation_length",
        "throughput_too_low": "increase_capacity_or_simplify_request_path",
        "operational_fit": "keep_as_operational_candidate",
    }
    report["primary_tradeoff"] = primary_tradeoff
    report["next_adjustment"] = next_adjustment_map[primary_tradeoff]
    report["operationally_acceptable"] = all(
        [
            quality_ok,
            latency_ok,
            cost_ok,
            throughput_ok,
        ]
    )
    return report


def load_reports():
    return [evaluate_candidate(candidate) for candidate in load_candidates()]


def summarize_reports(reports):
    acceptable = [report for report in reports if report["operationally_acceptable"]]
    best_acceptable = (
        max(
            acceptable,
            key=lambda report: (
                report["quality_score"],
                -report["avg_latency_ms"],
                -report["estimated_cost_per_1k_requests"],
            ),
        )
        if acceptable
        else None
    )

    return {
        "candidate_count": len(reports),
        "acceptable_count": len(acceptable),
        "quality_fail_count": sum(not report["quality_ok"] for report in reports),
        "latency_fail_count": sum(not report["latency_ok"] for report in reports),
        "cost_fail_count": sum(not report["cost_ok"] for report in reports),
        "throughput_fail_count": sum(
            not report["throughput_ok"] for report in reports
        ),
        "best_operational_candidate": (
            best_acceptable["service_name"] if best_acceptable else None
        ),
    }


def compact_report(report):
    return {
        "service_name": report["service_name"],
        "quality_score": report["quality_score"],
        "avg_latency_ms": report["avg_latency_ms"],
        "estimated_cost_per_1k_requests": report[
            "estimated_cost_per_1k_requests"
        ],
        "max_requests_per_minute": report["max_requests_per_minute"],
        "failed_checks": report["failed_checks"],
        "primary_tradeoff": report["primary_tradeoff"],
        "next_adjustment": report["next_adjustment"],
        "operationally_acceptable": report["operationally_acceptable"],
    }


def main():
    reports = load_reports()
    selected_reports = [
        compact_report(report)
        for report in reports
        if report["service_name"] in SELECTED_CASES
    ]

    print("[constraints]")
    pprint(CONSTRAINTS)
    print("[summary]")
    pprint(summarize_reports(reports))
    print("[selected_cases]")
    for report in selected_reports:
        pprint(report)


if __name__ == "__main__":
    main()
