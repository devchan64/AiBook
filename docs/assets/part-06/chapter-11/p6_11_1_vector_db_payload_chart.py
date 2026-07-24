from pathlib import Path
import csv
import os

REPO_ROOT = Path(__file__).resolve().parents[4]
MPL_CACHE = REPO_ROOT / ".tmp" / "matplotlib-cache"
MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE))
os.environ.setdefault("XDG_CACHE_HOME", str(MPL_CACHE))

import chromadb
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from sklearn.feature_extraction.text import TfidfVectorizer

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
        "outfile": "vector-db-payload-check-ko.png",
        "ylabel": "질문 수",
        "labels": ["1위 후보\n범주 일치", "원문 payload\n회수", "메타데이터\n회수"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "vector-db-payload-check-en.png",
        "ylabel": "query count",
        "labels": ["top-1\ncategory", "text payload\nreturned", "metadata\nreturned"],
    },
}


def choose_font(candidates: list[str]) -> str:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def configure_font(text: dict[str, object]) -> None:
    plt.rcParams["font.family"] = choose_font(text["font_candidates"])
    plt.rcParams["axes.unicode_minus"] = False


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def build_reports() -> list[dict[str, object]]:
    questions = read_csv(QUESTION_PATH)
    documents = read_csv(DOCUMENT_PATH)
    document_texts = [
        f"{doc['title']} {doc['text']}"
        for doc in documents
    ]

    vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))
    document_vectors = vectorizer.fit_transform(document_texts).toarray().tolist()

    client = chromadb.EphemeralClient()
    collection = client.create_collection(name="p6_11_1_payload_chart")
    collection.add(
        ids=[doc["doc_id"] for doc in documents],
        documents=[doc["text"] for doc in documents],
        metadatas=[
            {
                "case_id": doc["case_id"],
                "title": doc["title"],
                "version_status": doc["version_status"],
                "source_type": doc["source_type"],
            }
            for doc in documents
        ],
        embeddings=document_vectors,
    )

    reports = []
    for question in questions:
        query_embedding = vectorizer.transform([question["question"]]).toarray().tolist()[0]
        result = collection.query(
            query_embeddings=[query_embedding],
            n_results=2,
            include=["documents", "metadatas", "distances"],
        )
        top_metadata = result["metadatas"][0][0]
        top_document = result["documents"][0][0]
        reports.append(
            {
                "category_match": top_metadata["case_id"] == question["case_id"],
                "payload_has_text": bool(top_document),
                "payload_has_metadata": all(
                    key in top_metadata for key in ["title", "version_status", "source_type"]
                ),
            }
        )
    return reports


def summarize(reports: list[dict[str, object]]) -> dict[str, int]:
    return {
        "top1_category_match_count": sum(report["category_match"] for report in reports),
        "payload_has_text_count": sum(report["payload_has_text"] for report in reports),
        "payload_has_metadata_count": sum(report["payload_has_metadata"] for report in reports),
        "query_count": len(reports),
    }


def style_axis(ax) -> None:
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_chart(text: dict[str, object], summary: dict[str, int]) -> None:
    configure_font(text)
    values = [
        summary["top1_category_match_count"],
        summary["payload_has_text_count"],
        summary["payload_has_metadata_count"],
    ]
    colors = ["#2563eb", "#0f766e", "#9333ea"]

    fig, ax = plt.subplots(figsize=(6.4, 3.8), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    bars = ax.bar(text["labels"], values, color=colors, width=0.54)
    for bar in bars:
        value = bar.get_height()
        ax.annotate(
            f"{value:g}",
            (bar.get_x() + bar.get_width() / 2, value),
            textcoords="offset points",
            xytext=(0, 7),
            ha="center",
            fontsize=9,
            color="#172033",
        )

    ax.set_ylabel(text["ylabel"])
    ax.set_ylim(0, summary["query_count"] * 1.25)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    summary = summarize(build_reports())
    for text in LANG_TEXT.values():
        save_chart(text, summary)


if __name__ == "__main__":
    main()
