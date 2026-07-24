from collections import Counter
from csv import DictReader
from pathlib import Path
from pprint import pprint

OUT_DIR = Path(__file__).resolve().parent
DOCUMENTS_CSV = OUT_DIR / "p6_18_2_policy_documents.csv"
QUESTIONS_CSV = OUT_DIR / "p6_18_2_policy_questions.csv"

SELECTED_QUERIES = {
    "query_001",
    "query_002",
    "query_003",
    "query_007",
    "query_026",
    "query_030",
}
DETAILED_QUERY = "query_001"


def split_groups(value):
    return [item for item in value.split("|") if item]


def parse_bool(value):
    return value == "yes"


def read_documents():
    with DOCUMENTS_CSV.open(newline="", encoding="utf-8") as file:
        return [
            {
                "doc_id": row["doc_id"],
                "title": row["title"],
                "policy_text": row["policy_text"],
                "keyword_groups": split_groups(row["keyword_groups"]),
            }
            for row in DictReader(file)
        ]


def read_questions():
    with QUESTIONS_CSV.open(newline="", encoding="utf-8") as file:
        return [
            {
                "query_id": row["query_id"],
                "question": row["question"],
                "query_groups": split_groups(row["query_groups"]),
                "requires_review": parse_bool(row["requires_review"]),
                "scenario": row["scenario"],
            }
            for row in DictReader(file)
        ]


def score_document(question, document):
    matched_groups = sorted(
        set(question["query_groups"]).intersection(document["keyword_groups"])
    )
    return {
        "doc_id": document["doc_id"],
        "title": document["title"],
        "policy_text": document["policy_text"],
        "score": len(matched_groups),
        "matched_groups": matched_groups,
    }


def retrieve_documents(question, documents, top_k=3):
    scored = [score_document(question, document) for document in documents]
    scored.sort(key=lambda item: (-item["score"], item["doc_id"]))
    return scored[:top_k], scored


def draft_answer(question, retrieved):
    positive_docs = [doc for doc in retrieved if doc["score"] > 0]
    if not positive_docs:
        return "관련 규정을 찾지 못했습니다. 답변을 확정하지 말고 사람 검토로 넘깁니다."

    evidence_lines = [
        f"- {doc['doc_id']}: {doc['policy_text']}" for doc in positive_docs
    ]
    if len(positive_docs) == 1:
        summary_line = "초안 판단: 근거가 하나뿐이므로 예외 조항과 최신 공지를 다시 확인해야 합니다."
    else:
        summary_line = "초안 판단: 여러 근거를 함께 읽어 조건 충돌과 적용 순서를 확인해야 합니다."
    return "\n".join(
        [
            f"질문: {question['question']}",
            "확인된 근거:",
            *evidence_lines,
            summary_line,
        ]
    )


def evaluate_run(question, retrieved):
    positive_docs = [doc for doc in retrieved if doc["score"] > 0]
    notes = []
    if not positive_docs:
        run_status = "retrieval_failed"
        notes.append("검색 실패: 관련 문서를 찾지 못했으므로 사람 검토가 필요함")
        next_patch = "expand_index_or_add_policy_documents"
    elif len(positive_docs) == 1:
        run_status = "single_evidence"
        notes.append("근거 부족 가능성: 한 문서만 잡혔으므로 예외 조항 누락을 점검")
        next_patch = "expand_retrieval_or_add_review_gate"
    else:
        run_status = "multi_evidence"
        notes.append("다중 근거 확인: 여러 문서를 함께 읽어 조건 충돌 여부를 점검")
        next_patch = "improve_grounded_answer_rules"

    if question["requires_review"]:
        notes.append("질문 특성상 자동 확답보다 사람 검토 상태를 남김")

    needs_human_review = (
        run_status != "multi_evidence" or question["requires_review"]
    )
    return {
        "run_status": run_status,
        "needs_human_review": needs_human_review,
        "notes": notes,
        "next_patch": next_patch,
    }


def build_run_record(question, documents):
    top_docs, full_scores = retrieve_documents(question, documents)
    positive_top_docs = [doc for doc in top_docs if doc["score"] > 0]
    evaluation = evaluate_run(question, top_docs)
    return {
        "query_id": question["query_id"],
        "question": question["question"],
        "document_scores": [
            {
                "doc_id": item["doc_id"],
                "score": item["score"],
                "matched_groups": item["matched_groups"],
            }
            for item in full_scores
        ],
        "retrieved_doc_ids": [doc["doc_id"] for doc in positive_top_docs],
        "draft_answer": draft_answer(question, top_docs),
        "evaluation": evaluation,
    }


def load_run_records():
    documents = read_documents()
    return [build_run_record(question, documents) for question in read_questions()]


def summarize_records(records):
    status_counts = Counter(record["evaluation"]["run_status"] for record in records)
    patch_counts = Counter(record["evaluation"]["next_patch"] for record in records)
    return {
        "run_count": len(records),
        "multi_evidence_count": status_counts["multi_evidence"],
        "single_evidence_count": status_counts["single_evidence"],
        "retrieval_failed_count": status_counts["retrieval_failed"],
        "needs_human_review_count": sum(
            record["evaluation"]["needs_human_review"] for record in records
        ),
        "next_patch_counts": dict(sorted(patch_counts.items())),
    }


def compact_record(record):
    return {
        "query_id": record["query_id"],
        "question": record["question"],
        "retrieved_doc_ids": record["retrieved_doc_ids"],
        "run_status": record["evaluation"]["run_status"],
        "needs_human_review": record["evaluation"]["needs_human_review"],
        "next_patch": record["evaluation"]["next_patch"],
        "notes": record["evaluation"]["notes"],
    }


def detailed_record(record):
    return {
        "query_id": record["query_id"],
        "question": record["question"],
        "top_document_scores": record["document_scores"][:5],
        "retrieved_doc_ids": record["retrieved_doc_ids"],
        "draft_answer": record["draft_answer"],
        "evaluation": record["evaluation"],
    }


def main():
    records = load_run_records()
    selected_records = [
        compact_record(record)
        for record in records
        if record["query_id"] in SELECTED_QUERIES
    ]
    detail = next(record for record in records if record["query_id"] == DETAILED_QUERY)

    print("[summary]")
    pprint(summarize_records(records))
    print("[selected_records]")
    for record in selected_records:
        pprint(record)
    print("[detailed_record]")
    pprint(detailed_record(detail))


if __name__ == "__main__":
    main()
