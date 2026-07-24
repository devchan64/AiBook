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
        "case_labels": {
            "policy": "정책",
            "manual": "매뉴얼",
            "sdk": "SDK",
            "pricing": "요금",
        },
        "xlabel": "상위 검색 문서 유사도",
        "ready_label": "근거 연결 준비",
        "review_label": "근거 재검토",
        "title_prefix": "상위 문서",
        "label_mode": "title",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "rag-grounding-check-en.png",
        "case_labels": {
            "policy": "policy",
            "manual": "manual",
            "sdk": "SDK",
            "pricing": "pricing",
        },
        "xlabel": "top retrieved document similarity",
        "ready_label": "grounding ready",
        "review_label": "review grounding",
        "title_prefix": "top doc",
        "label_mode": "doc_id",
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
        answer_mentions_expected_update = question_row["current_signal"] in rag_result["answer"]
        grounding_ready = (
            top_doc_matches_case
            and top_doc_is_current
            and answer_mentions_expected_update
        )
        rows.append(
            {
                "case_id": question_row["case_id"],
                "top_doc_id": top_doc["doc_id"] if top_doc else "none",
                "top_title": top_doc["title"] if top_doc else "none",
                "top_similarity": top_doc["similarity"] if top_doc else 0,
                "top_doc_matches_case": top_doc_matches_case,
                "top_doc_is_current": top_doc_is_current,
                "answer_mentions_expected_update": answer_mentions_expected_update,
                "grounding_ready": grounding_ready,
            }
        )

    return rows


def trim_title(title: str, limit: int = 15) -> str:
    if len(title) <= limit:
        return title
    return title[: limit - 1] + "…"


def doc_label(row: dict[str, Any], text: dict[str, str]) -> str:
    if text["label_mode"] == "doc_id":
        status = "current" if row["top_doc_is_current"] else "archived"
        return f"{row['top_doc_id']} ({status})"
    return trim_title(row["top_title"])


def save_chart(text: dict[str, str]) -> None:
    configure_font(text)
    rows = build_rows()

    fig, ax = plt.subplots(figsize=(9.0, 4.2), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.grid(True, axis="x", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)

    y_positions = list(range(len(rows)))
    colors = ["#0f766e" if row["grounding_ready"] else "#dc2626" for row in rows]
    bars = ax.barh(
        y_positions,
        [row["top_similarity"] for row in rows],
        color=colors,
        height=0.56,
    )
    for bar, row in zip(bars, rows):
        top_doc_label = doc_label(row, text)
        label = (
            f"{text['ready_label']}: {top_doc_label}"
            if row["grounding_ready"]
            else f"{text['review_label']}: {top_doc_label}"
        )
        ax.annotate(
            label,
            (bar.get_width(), bar.get_y() + bar.get_height() / 2),
            textcoords="offset points",
            xytext=(8, 0),
            ha="left",
            va="center",
            fontsize=9,
            color="#172033",
        )
        ax.annotate(
            f"{bar.get_width():.3f}",
            (bar.get_width(), bar.get_y() + bar.get_height() / 2),
            textcoords="offset points",
            xytext=(-8, 0),
            ha="right",
            va="center",
            fontsize=9,
            color="white",
            fontweight="bold",
        )

    ax.set_xlim(0, 0.58)
    ax.set_xlabel(text["xlabel"])
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([text["case_labels"].get(row["case_id"], row["case_id"]) for row in rows])
    ax.invert_yaxis()
    ax.tick_params(axis="y", length=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
