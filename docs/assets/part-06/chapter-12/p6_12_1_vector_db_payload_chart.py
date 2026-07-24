from pathlib import Path
import csv
import os
from uuid import uuid4
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
import chromadb
from chromadb.config import Settings
from sklearn.feature_extraction.text import TfidfVectorizer

OUT_DIR = Path(__file__).resolve().parent
DOCUMENT_PATH = OUT_DIR / "p6-12-vector-db-documents.csv"
QUERY_PATH = OUT_DIR / "p6-12-vector-db-queries.csv"

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
        "xlabel": "상위 검색 문서 유사도",
        "top1_label": "1위 후보",
        "runner_up_label": "다음 후보",
        "labels": {
            "refund_current": "환불",
            "settings_reset": "설정 초기화",
            "api_retry": "요청 제한",
            "offboarding_asset": "장비 반납",
        },
        "document_path": DOCUMENT_PATH,
        "query_path": QUERY_PATH,
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "vector-db-payload-check-en.png",
        "xlabel": "top retrieved document similarity",
        "top1_label": "top-1 match",
        "runner_up_label": "runner-up",
        "labels": {
            "refund_current": "refund",
            "settings_reset": "reset settings",
            "api_retry": "rate-limit retry",
            "offboarding_asset": "asset return",
        },
        "document_path": DOCUMENT_PATH,
        "query_path": QUERY_PATH,
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK",
            "PingFang SC",
            "Heiti SC",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "outfile": "vector-db-payload-check-zh.png",
        "xlabel": "首位检索文档相似度",
        "top1_label": "首位候选",
        "runner_up_label": "下一候选",
        "labels": {
            "refund_current": "退款",
            "settings_reset": "设置重置",
            "api_retry": "请求限制",
            "offboarding_asset": "设备归还",
        },
        "document_path": OUT_DIR / "p6-12-vector-db-documents-zh.csv",
        "query_path": OUT_DIR / "p6-12-vector-db-queries-zh.csv",
    },
}


def choose_font(candidates: list[str]) -> str:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def configure_font(text: dict[str, Any]) -> None:
    plt.rcParams["font.family"] = choose_font(text["font_candidates"])
    plt.rcParams["axes.unicode_minus"] = False


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def search_rows(text: dict[str, Any], top_k: int = 2) -> list[dict[str, Any]]:
    documents = read_csv(text["document_path"])
    queries = read_csv(text["query_path"])
    document_texts = [f"{doc['title']} {doc['text']}" for doc in documents]
    vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))
    document_vectors = vectorizer.fit_transform(document_texts)
    client = chromadb.Client(Settings(anonymized_telemetry=False))
    collection = client.create_collection(
        name=f"p6_12_chart_payload_{uuid4().hex[:8]}",
        metadata={"hnsw:space": "cosine"},
    )
    collection.add(
        ids=[doc["doc_id"] for doc in documents],
        documents=[doc["text"] for doc in documents],
        embeddings=document_vectors.toarray().tolist(),
        metadatas=[
            {
                "title": doc["title"],
                "source": doc["source"],
                "category": doc["category"],
                "version": doc["version"],
                "status": doc["status"],
            }
            for doc in documents
        ],
    )

    rows = []
    for query in queries:
        query_vector = vectorizer.transform([query["question"]]).toarray().tolist()
        result = collection.query(
            query_embeddings=query_vector,
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )
        matches = [
            {
                "doc_id": doc_id,
                "text": text,
                **metadata,
                "similarity": round(1 - float(distance), 3),
            }
            for doc_id, text, metadata, distance in zip(
                result["ids"][0],
                result["documents"][0],
                result["metadatas"][0],
                result["distances"][0],
            )
        ]

        top_match = matches[0]
        runner_up = matches[1]
        rows.append(
            {
                "query_id": query["query_id"],
                "top_doc_id": top_match["doc_id"],
                "top_category": top_match["category"],
                "top_status": top_match["status"],
                "top_similarity": top_match["similarity"],
                "runner_up_doc_id": runner_up["doc_id"],
                "runner_up_similarity": runner_up["similarity"],
                "payload_has_text": bool(top_match["text"]),
                "payload_has_metadata": all(
                    top_match.get(key)
                    for key in ("source", "category", "version", "status")
                ),
            }
        )
    return rows


def style_axis(ax) -> None:
    ax.grid(True, axis="x", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)


def save_chart(text: dict[str, Any]) -> None:
    configure_font(text)
    rows = search_rows(text)
    y_positions = list(range(len(rows)))
    top1_values = [row["top_similarity"] for row in rows]
    runner_up_values = [row["runner_up_similarity"] for row in rows]
    bar_height = 0.32

    fig, ax = plt.subplots(figsize=(8.2, 4.2), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    top1_bars = ax.barh(
        [y - bar_height / 2 for y in y_positions],
        top1_values,
        height=bar_height,
        color="#0f766e",
        label=text["top1_label"],
    )
    runner_up_bars = ax.barh(
        [y + bar_height / 2 for y in y_positions],
        runner_up_values,
        height=bar_height,
        color="#64748b",
        label=text["runner_up_label"],
    )

    for bars in (top1_bars, runner_up_bars):
        for bar in bars:
            value = bar.get_width()
            ax.annotate(
                f"{value:.3f}",
                (value, bar.get_y() + bar.get_height() / 2),
                textcoords="offset points",
                xytext=(8, 0),
                ha="left",
                va="center",
                fontsize=8.5,
                color="#172033",
            )

    ax.set_xlim(0, max(top1_values) + 0.08)
    ax.set_xlabel(text["xlabel"])
    ax.set_yticks(y_positions)
    ax.set_yticklabels([text["labels"].get(row["query_id"], row["query_id"]) for row in rows])
    ax.invert_yaxis()
    ax.tick_params(axis="y", length=0)
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
