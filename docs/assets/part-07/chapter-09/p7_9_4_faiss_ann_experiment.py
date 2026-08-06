"""Measure FAISS IVF ANN recall and latency for the Part 7 RAG document set."""

import csv
import time
from pathlib import Path

import faiss
from sklearn.feature_extraction.text import TfidfVectorizer


DATA_PATH = Path("docs/assets/part-07/chapter-09/p7-9-rag-documents.csv")
OUTPUT_PATH = Path("docs/assets/part-07/chapter-09/p7-9-4-faiss-ann-results.csv")
QUESTION = "RAG 프로젝트에서 왜 검색 후보와 선택 근거를 답변보다 먼저 기록해야 하는가?"
TOP_K = 5
N_LIST = 4
REPEAT_COUNT = 1000


def main():
    rows = list(csv.DictReader(DATA_PATH.open(encoding="utf-8")))
    texts = [row["text"] for row in rows]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    document_vectors = vectorizer.fit_transform(texts).toarray().astype("float32")
    query_vector = vectorizer.transform([QUESTION]).toarray().astype("float32")
    faiss.normalize_L2(document_vectors)
    faiss.normalize_L2(query_vector)

    exact_index = faiss.IndexFlatIP(document_vectors.shape[1])
    exact_index.add(document_vectors)
    _, exact_ids = exact_index.search(query_vector, TOP_K)
    exact_id_set = set(exact_ids[0])

    ivf_index = faiss.IndexIVFFlat(
        faiss.IndexFlatIP(document_vectors.shape[1]),
        document_vectors.shape[1],
        N_LIST,
        faiss.METRIC_INNER_PRODUCT,
    )
    ivf_index.train(document_vectors)
    ivf_index.add(document_vectors)

    result_rows = []
    for nprobe in (1, 2, 4):
        ivf_index.nprobe = nprobe
        started = time.perf_counter()
        for _ in range(REPEAT_COUNT):
            _, retrieved_ids = ivf_index.search(query_vector, TOP_K)
        elapsed_ms = (time.perf_counter() - started) * 1000 / REPEAT_COUNT
        retrieved_id_set = set(retrieved_ids[0])
        result_rows.append(
            {
                "run_id": f"p7-9-4-faiss-ivf-nprobe-{nprobe}",
                "run_date": "2026-08-01",
                "log_source": "actual_cpu_run",
                "index_type": "IndexIVFFlat",
                "vectorizer": "TfidfVectorizer(ngram_range=(1, 2))",
                "document_count": len(rows),
                "vector_dimension": document_vectors.shape[1],
                "nlist": N_LIST,
                "nprobe": nprobe,
                "top_k": TOP_K,
                "repeat_count": REPEAT_COUNT,
                "mean_search_ms": round(elapsed_ms, 4),
                "exact_top_k_recall": round(len(exact_id_set & retrieved_id_set) / TOP_K, 2),
                "missing_exact_doc_ids": "|".join(
                    rows[index]["doc_id"] for index in sorted(exact_id_set - retrieved_id_set)
                ),
                "retrieved_doc_ids": "|".join(rows[index]["doc_id"] for index in retrieved_ids[0]),
            }
        )

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=result_rows[0].keys())
        writer.writeheader()
        writer.writerows(result_rows)
    print(f"wrote {len(result_rows)} ANN setting results to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
