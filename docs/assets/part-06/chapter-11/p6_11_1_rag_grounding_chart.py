from pathlib import Path
import csv
import os
from typing import Any

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

QUESTION_PATH = OUT_DIR / "p6-11-rag-need-questions.csv"
DOCUMENT_PATH = OUT_DIR / "p6-11-rag-need-documents.csv"

LANG_TEXT = {
    "ko": {
        "font_candidates": [
            "Noto Sans CJK KR",
            "NanumGothic",
            "Apple SD Gothic Neo",
            "AppleGothic",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "outfile": "rag-grounding-check-ko.png",
        "row_labels": {
            "policy": "정책",
            "manual": "매뉴얼",
            "sdk": "SDK",
            "pricing": "요금",
        },
        "columns": ["기억 답변\n최신 신호", "RAG 답변\n최신 신호", "상위 문서\n주제 일치", "상위 문서\n현재 버전", "근거 연결\n준비"],
        "pass_label": "통과",
        "fail_label": "실패",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "rag-grounding-check-en.png",
        "row_labels": {
            "policy": "policy",
            "manual": "manual",
            "sdk": "SDK",
            "pricing": "pricing",
        },
        "columns": ["memory\nupdate signal", "RAG\nupdate signal", "top doc\ncase match", "top doc\ncurrent", "grounding\nready"],
        "pass_label": "pass",
        "fail_label": "fail",
    },
}


def choose_font(candidates: list[str]) -> str:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def configure_font(text: dict[str, str]) -> None:
    plt.rcParams["font.family"] = choose_font(text["font_candidates"])
    plt.rcParams["axes.unicode_minus"] = False


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def retrieve_docs(
    documents: list[dict[str, str]],
    vectorizer: TfidfVectorizer,
    document_vectors,
    question: str,
    top_k: int = 2,
) -> list[dict[str, Any]]:
    query_vector = vectorizer.transform([question])
    scores = cosine_similarity(query_vector, document_vectors).ravel()
    ranked_indexes = scores.argsort()[::-1]

    retrieved = []
    for index in ranked_indexes:
        if scores[index] <= 0:
            continue
        retrieved.append(
            {
                **documents[index],
                "similarity": round(float(scores[index]), 3),
            }
        )
        if len(retrieved) == top_k:
            break
    return retrieved


def answer_with_rag(retrieved_docs: list[dict[str, Any]]) -> dict[str, Any]:
    if not retrieved_docs:
        return {
            "answer": "관련 근거 문서를 찾지 못해 현재 기준을 확정하기 어렵습니다.",
            "grounding_titles": [],
        }

    top_doc = retrieved_docs[0]
    return {
        "answer": f"근거 문서 '{top_doc['title']}'에 따르면 {top_doc['text']}",
        "grounding_titles": [doc["title"] for doc in retrieved_docs],
    }


def build_rows() -> list[dict[str, Any]]:
    questions = read_csv(QUESTION_PATH)
    documents = read_csv(DOCUMENT_PATH)
    document_texts = [
        f"{doc['title']} {doc['text']}"
        for doc in documents
    ]
    vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))
    document_vectors = vectorizer.fit_transform(document_texts)

    rows = []
    for question_row in questions:
        retrieved_docs = retrieve_docs(documents, vectorizer, document_vectors, question_row["question"])
        rag_result = answer_with_rag(retrieved_docs)
        top_doc = retrieved_docs[0] if retrieved_docs else None
        top_doc_matches_case = bool(top_doc) and top_doc["case_id"] == question_row["case_id"]
        top_doc_is_current = bool(top_doc) and top_doc["version_status"] == "current"
        answer_contains_update_signal = question_row["current_signal"] in rag_result["answer"]
        grounding_ready = (
            top_doc_matches_case
            and top_doc_is_current
            and answer_contains_update_signal
            and len(rag_result["grounding_titles"]) >= 2
        )
        rows.append(
            {
                "case_id": question_row["case_id"],
                "checks": [
                    question_row["current_signal"] in question_row["memory_answer"],
                    answer_contains_update_signal,
                    top_doc_matches_case,
                    top_doc_is_current,
                    grounding_ready,
                ],
            }
        )

    return rows


def save_chart(text: dict[str, str]) -> None:
    configure_font(text)
    rows = build_rows()
    columns = text["columns"]

    fig, ax = plt.subplots(figsize=(9.2, 4.0), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    for row_index, row in enumerate(rows):
        for col_index, passed in enumerate(row["checks"]):
            color = "#0f766e" if passed else "#e5e7eb"
            text_color = "white" if passed else "#475569"
            marker = "✓" if passed else "–"
            rect = plt.Rectangle(
                (col_index - 0.48, row_index - 0.42),
                0.96,
                0.84,
                facecolor=color,
                edgecolor="white",
                linewidth=2,
            )
            ax.add_patch(rect)
            ax.text(
                col_index,
                row_index,
                marker,
                ha="center",
                va="center",
                fontsize=15,
                fontweight="bold",
                color=text_color,
            )

    ax.set_xlim(-0.5, len(columns) - 0.5)
    ax.set_ylim(len(rows) - 0.5, -0.5)
    ax.set_xticks(range(len(columns)))
    ax.set_xticklabels(columns)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([text["row_labels"].get(row["case_id"], row["case_id"]) for row in rows])
    ax.tick_params(axis="both", length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.text(
        0.985,
        0.965,
        f"✓ {text['pass_label']}   – {text['fail_label']}",
        ha="right",
        va="top",
        fontsize=9,
        color="#475569",
    )
    fig.tight_layout(pad=0.9, rect=(0, 0, 1, 0.94))
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
