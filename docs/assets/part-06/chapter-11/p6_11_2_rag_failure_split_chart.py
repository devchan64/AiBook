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

QUESTION = "벡터 검색이 왜 필요한가요?"
DOCUMENT_PATH = OUT_DIR / "p6-11-rag-documents.csv"
EXPERIMENT_PATH = OUT_DIR / "p6-11-rag-experiments.csv"

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
        "outfile": "rag-failure-split-ko.png",
        "row_labels": {
            "clean_grounded_vector_search": "정상 검색 예",
            "noisy_retrieval_marketing_copy": "검색 오염 예",
            "clean_but_overclaim_vector_search": "답변 과장 예",
        },
        "columns": ["관련 문서\n상위 회수", "무관 문서\n포함", "답변\n오염", "과장 표현", "검색 실패", "생성 실패"],
        "pass_label": "신호 있음",
        "fail_label": "신호 없음",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "rag-failure-split-en.png",
        "row_labels": {
            "clean_grounded_vector_search": "clean example",
            "noisy_retrieval_marketing_copy": "noisy retrieval example",
            "clean_but_overclaim_vector_search": "answer overclaim example",
        },
        "columns": ["relevant doc\ntop result", "irrelevant doc\nincluded", "answer\nleak", "overclaim", "retrieval\nfailure", "generation\nfailure"],
        "pass_label": "signal on",
        "fail_label": "signal off",
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


def build_query(experiment: dict[str, str]) -> str:
    terms = experiment["retrieval_terms"].split(";")
    return f"{QUESTION} {' '.join(terms)}"


def retrieve_documents(
    documents: list[dict[str, str]],
    vectorizer: TfidfVectorizer,
    document_vectors,
    query: str,
    top_k: int = 2,
) -> list[dict[str, Any]]:
    query_vector = vectorizer.transform([query])
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


def generate_answer(retrieved_docs: list[dict[str, Any]], generation_style: str) -> str:
    first = str(retrieved_docs[0]["text"]) if retrieved_docs else "참고 문서가 없다."
    second = str(retrieved_docs[1]["text"]) if len(retrieved_docs) > 1 else "추가 근거가 부족하다."

    if generation_style == "overclaim":
        return f"{first} 그래서 항상 최신 정보와 정답을 자동으로 보장한다."

    return f"{first} 그래서 {second}"


def inspect_result(retrieved_docs: list[dict[str, Any]], answer: str) -> dict[str, bool]:
    contains_irrelevant_doc = any(
        doc["category"] == "irrelevant" for doc in retrieved_docs
    )
    top_doc_is_relevant = bool(retrieved_docs) and retrieved_docs[0]["category"] == "retrieval"
    irrelevant_fragments = [
        str(doc["text"]).split(".")[0]
        for doc in retrieved_docs
        if doc["category"] == "irrelevant"
    ]
    answer_mentions_irrelevant_content = any(
        fragment and fragment in answer
        for fragment in irrelevant_fragments
    )
    answer_overclaims = "항상 최신 정보와 정답을 자동으로 보장" in answer

    return {
        "top_doc_is_relevant": top_doc_is_relevant,
        "contains_irrelevant_doc": contains_irrelevant_doc,
        "answer_mentions_irrelevant_content": answer_mentions_irrelevant_content,
        "answer_overclaims": answer_overclaims,
        "retrieval_failed": contains_irrelevant_doc,
        "generation_failed": (not contains_irrelevant_doc) and answer_overclaims,
    }


def build_rows() -> list[dict[str, Any]]:
    documents = read_csv(DOCUMENT_PATH)
    experiments = read_csv(EXPERIMENT_PATH)
    document_texts = [
        f"{doc['title']} {doc['text']}"
        for doc in documents
    ]
    vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))
    document_vectors = vectorizer.fit_transform(document_texts)

    selected_names = {
        "clean_grounded_vector_search",
        "noisy_retrieval_marketing_copy",
        "clean_but_overclaim_vector_search",
    }
    rows = []
    for experiment in experiments:
        if experiment["name"] not in selected_names:
            continue
        query = build_query(experiment)
        retrieved_docs = retrieve_documents(documents, vectorizer, document_vectors, query)
        answer = generate_answer(retrieved_docs, experiment["generation_style"])
        inspection = inspect_result(retrieved_docs, answer)
        rows.append(
            {
                "name": experiment["name"],
                "checks": [
                    inspection["top_doc_is_relevant"],
                    inspection["contains_irrelevant_doc"],
                    inspection["answer_mentions_irrelevant_content"],
                    inspection["answer_overclaims"],
                    inspection["retrieval_failed"],
                    inspection["generation_failed"],
                ],
            }
        )

    order = [
        "clean_grounded_vector_search",
        "noisy_retrieval_marketing_copy",
        "clean_but_overclaim_vector_search",
    ]
    rows.sort(key=lambda row: order.index(row["name"]))
    return rows


def save_chart(text: dict[str, str]) -> None:
    configure_font(text)
    rows = build_rows()
    columns = text["columns"]

    fig, ax = plt.subplots(figsize=(10.0, 3.6), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    signal_colors = ["#0f766e", "#f59e0b", "#dc2626", "#7c3aed", "#dc2626", "#2563eb"]
    for row_index, row in enumerate(rows):
        for col_index, active in enumerate(row["checks"]):
            color = signal_colors[col_index] if active else "#e5e7eb"
            text_color = "white" if active else "#475569"
            label = "✓" if active else "-"
            rect = plt.Rectangle(
                (col_index - 0.48, row_index - 0.40),
                0.96,
                0.80,
                facecolor=color,
                edgecolor="white",
                linewidth=2,
            )
            ax.add_patch(rect)
            ax.text(
                col_index,
                row_index,
                label,
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
    ax.set_yticklabels([text["row_labels"][row["name"]] for row in rows])
    ax.tick_params(axis="both", length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.text(
        0.985,
        0.965,
        f"✓ {text['pass_label']}   - {text['fail_label']}",
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
