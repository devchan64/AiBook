from __future__ import annotations

import csv
import os
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
MPL_CACHE = REPO_ROOT / ".tmp" / "matplotlib-cache"
MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE))
os.environ.setdefault("XDG_CACHE_HOME", str(MPL_CACHE))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


OUT_DIR = Path(__file__).resolve().parent
DOCUMENT_PATH = OUT_DIR / "p7-6-rag-documents.csv"
CASE_PATH = OUT_DIR / "p7-6-boundary-cases.csv"
PNG_PATH = OUT_DIR / "p7-6-retrieval-eval-report-ko.png"

TOP_K = 3
MIN_SCORE = 0.16
MARGIN_THRESHOLD = 0.04


def choose_font() -> str:
    candidates = [
        "Noto Sans CJK KR",
        "NanumGothic",
        "Apple SD Gothic Neo",
        "AppleGothic",
        "Arial Unicode MS",
        "DejaVu Sans",
    ]
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def configure_font() -> None:
    plt.rcParams["font.family"] = choose_font()
    plt.rcParams["axes.unicode_minus"] = False


def classify_search_state(case: dict[str, str], retrieved_documents: list[dict[str, object]]) -> str:
    question = case["question"]
    top_score = float(retrieved_documents[0]["score"])
    second_score = float(retrieved_documents[1]["score"]) if len(retrieved_documents) > 1 else 0.0
    margin = top_score - second_score
    joined_text = " ".join(str(document["text"]) for document in retrieved_documents)

    if top_score < MIN_SCORE:
        return "문서 범위 밖"
    if any(word in joined_text for word in ["충돌", "최신 정책", "예전 FAQ", "버전"]):
        return "근거 충돌"
    if any(word in question for word in ["항상", "모든", "완전히", "해결되는가"]):
        return "답변 과장 위험"
    if margin < MARGIN_THRESHOLD:
        return "근거 재검토"
    return "근거 기반 답변"


def evaluate_cases() -> list[dict[str, object]]:
    documents = list(csv.DictReader(DOCUMENT_PATH.open(encoding="utf-8")))
    cases = list(csv.DictReader(CASE_PATH.open(encoding="utf-8")))

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    document_matrix = vectorizer.fit_transform([document["text"] for document in documents])
    query_matrix = vectorizer.transform([case["question"] for case in cases])
    similarity_matrix = cosine_similarity(query_matrix, document_matrix)

    records: list[dict[str, object]] = []
    for case_index, case in enumerate(cases):
        ranking = similarity_matrix[case_index].argsort()[::-1][:TOP_K]
        retrieved_documents = [
            {
                "doc_id": documents[document_index]["doc_id"],
                "text": documents[document_index]["text"],
                "score": round(float(similarity_matrix[case_index, document_index]), 3),
            }
            for document_index in ranking
        ]
        predicted_state = classify_search_state(case, retrieved_documents)
        records.append(
            {
                "expected_state": case["expected_state"],
                "predicted_state": predicted_state,
                "failure_stage": case["failure_stage"],
                "match": predicted_state == case["expected_state"],
            }
        )
    return records


def style_axis(ax) -> None:
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def draw_report() -> None:
    configure_font()
    records = evaluate_cases()
    predicted_counts = Counter(str(record["predicted_state"]) for record in records)
    stage_counts = Counter(str(record["failure_stage"]) for record in records if not record["match"])
    total = len(records)
    matches = sum(bool(record["match"]) for record in records)
    mismatches = total - matches

    state_order = ["근거 기반 답변", "문서 범위 밖", "답변 과장 위험", "근거 충돌", "근거 재검토"]
    stage_order = ["검색 단계", "선택 단계", "답변 단계"]

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.4), dpi=180)
    fig.patch.set_facecolor("white")
    left, right = axes

    style_axis(left)
    state_values = [predicted_counts.get(state, 0) for state in state_order]
    left.bar(range(len(state_order)), state_values, color=["#2563eb", "#64748b", "#ea580c", "#7c3aed", "#0f766e"])
    left.set_xticks(range(len(state_order)), state_order, rotation=20, ha="right")
    left.set_ylabel("질문 수")
    left.set_title("예측 상태 분포")
    for index, value in enumerate(state_values):
        left.text(index, value + 0.35, str(value), ha="center", fontsize=8.5)

    style_axis(right)
    stage_values = [stage_counts.get(stage, 0) for stage in stage_order]
    right.bar(range(len(stage_order)), stage_values, color=["#dc2626", "#ea580c", "#0f766e"])
    right.set_xticks(range(len(stage_order)), stage_order)
    right.set_ylabel("mismatch 수")
    right.set_title("실패 단계별 mismatch")
    for index, value in enumerate(stage_values):
        right.text(index, value + 0.35, str(value), ha="center", fontsize=8.5)

    fig.suptitle(
        f"RAG 검색 평가셋 리포트: 일치 {matches}/{total}, 불일치 {mismatches}",
        fontsize=15,
        fontweight="bold",
    )
    fig.tight_layout(pad=1.0)
    fig.savefig(PNG_PATH, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    draw_report()
    print(f"saved={PNG_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
