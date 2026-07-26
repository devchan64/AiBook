# P7-5.4 ANN 검색 설정 실습

Section ID: `P7-5.4`
Version: `v2026.07.26`

RAG 프로젝트에서 문서가 늘어나면 모든 문서를 매번 정확히 비교하는 방식은 점점 부담이 됩니다. 그래서 실제 검색 시스템은 벡터 데이터베이스(vector database)나 근사 최근접 이웃(ANN, approximate nearest neighbor) 검색처럼 후보를 빠르게 찾는 구조를 자주 사용합니다.

다만 초심자가 먼저 잡아야 할 것은 특정 제품 이름이나 튜닝 옵션 목록이 아닙니다. 핵심은 `후보를 적게 보면 빠르지만 놓칠 수 있고, 후보를 넓게 보면 더 잘 찾지만 비용이 늘어난다`는 교환 관계입니다. 이 절에서는 ChromaDB에 문서, 임베딩(embedding), 메타데이터(metadata)를 넣고, 검색 대상 bucket 범위를 바꾸며 후보 수와 top-k 포함률이 어떻게 달라지는지 확인합니다.

## ANN 설정이 바꾸는 것

- exact 검색과 approximate 검색은 무엇이 다른가?
- 후보 수를 줄이면 어떤 근거가 빠질 수 있는가?
- ANN 설정 기록에는 후보 수와 top-k 포함률을 왜 함께 남겨야 하는가?

여기서 `top-k 포함률`은 exact 검색의 상위 k개 문서 중 approximate 검색 결과에도 들어온 문서의 비율입니다. 이 값은 실제 서비스의 정답률 자체가 아니라, 설정을 바꿨을 때 중요한 후보를 얼마나 보존했는지 보는 작은 점검값입니다.

## 판단 기준

- ANN 설정을 `탐색 후보 수`, `top-k 포함률`, `누락된 후보`로 설명할 수 있습니다.
- 후보 수가 줄어드는 것이 항상 좋은 것이 아니라는 점을 말할 수 있습니다.
- 검색 속도와 근거 누락 위험을 같은 실행 기록 안에서 비교할 수 있습니다.

## 왜 exact 기준선이 필요한가

approximate 검색은 처음부터 정답처럼 읽으면 위험합니다. 어떤 후보군 설정이 좋은지 보려면 먼저 비교 기준이 있어야 합니다.

| 비교 대상 | 역할 |
| --- | --- |
| exact top-k | 모든 대표 문서를 같은 벡터 공간에서 비교했을 때의 기준선 |
| vector DB top-k | ChromaDB에서 일부 bucket만 대상으로 검색해 얻은 후보 |
| top-k 포함률 | approximate 결과가 exact 후보를 얼마나 보존했는지 보는 값 |
| 누락된 exact 후보 | 설정을 넓히거나 인덱스 구조를 다시 볼 근거 |

예를 들어 `좁은 후보군`이 빠르게 보인다는 이유만으로 선택하면 `실패 추적` bucket에 있는 중요한 문서를 놓칠 수 있습니다. 반대로 모든 bucket을 넓게 보면 포함률은 좋아지지만, 후보 수가 늘어 exact 검색과 별 차이가 없어질 수 있습니다. 그래서 ANN 설정 기록은 `빠르다`나 `잘 찾는다` 한 줄이 아니라, 후보 수와 누락 후보를 함께 보여 주어야 합니다.

## 입력 파일

- 문서 조각 파일: [`p7-5-rag-documents.csv`](../../../assets/part-07/chapter-05/p7-5-rag-documents.csv){ .csv-preview }
- 한 행의 의미: `검색 가능한 문서 조각 하나`
- 이번 실습 범위: `문서-1`부터 `문서-18`까지의 대표 문서

P7-5.1부터 P7-5.3까지 사용한 같은 문서 집합을 다시 씁니다. 다만 이번 절의 관심은 답변 작성이 아니라, 검색 설정이 후보 목록을 어떻게 바꾸는지입니다.

## 실행 기록 기준

1. 대표 문서 전체를 exact 방식으로 비교해 기준 top-k를 만든다.
2. 문서를 간단한 bucket으로 나누고, 탐색 bucket 수를 바꿔 approximate 후보를 만든다.
3. 설정별 후보 문서 수, top-k 포함률, 누락된 exact 후보를 함께 남긴다.
4. 후보 수가 줄어든 만큼 무엇을 놓쳤는지 한 문장으로 해석한다.

## Python 예제

예제는 ChromaDB를 실제 벡터 데이터베이스로 사용합니다. 다만 외부 모델 다운로드나 API 키가 필요 없도록, 문서 임베딩은 scikit-learn의 `TfidfVectorizer`로 로컬에서 계산해 ChromaDB에 직접 넣습니다. `num_probes`는 실제 ChromaDB 내부 옵션이 아니라, 이번 실습에서 검색 대상 bucket을 몇 개까지 열지 나타내는 프로젝트 설정값입니다.

- 문제 상황: RAG 문서 검색에서 후보군을 줄이면 어떤 근거가 빠질 수 있는지 확인한다.
- 입력: 대표 문서 18개, 질문 1개
- 기대 출력: exact top-k, 설정별 vector DB top-k, top-k 포함률, 누락 후보
- 확인할 개념:
  - 벡터 DB에는 원문, 임베딩, 메타데이터가 함께 들어간다
  - 검색 대상 bucket을 좁히면 exact top-k를 일부 놓칠 수 있다
  - `num_probes`를 늘리면 후보 수와 포함률이 함께 바뀐다
  - 검색 설정은 속도만이 아니라 근거 누락 위험과 함께 기록해야 한다

```python
# ChromaDB에 TF-IDF 임베딩과 metadata를 넣고, 검색 대상 bucket 범위에 따른 후보 누락을 비교하는 예제입니다.
import csv
from pathlib import Path

import chromadb
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

question = "RAG 프로젝트에서 왜 검색 후보와 선택 근거를 답변보다 먼저 기록해야 하는가?"
data_path = Path("docs/assets/part-07/chapter-05/p7-5-rag-documents.csv")
representative_doc_ids = {f"문서-{index}" for index in range(1, 19)}
document_rows = [
    row
    for row in csv.DictReader(data_path.open(encoding="utf-8"))
    if row["doc_id"] in representative_doc_ids
]

def bucket_for(text):
    if any(phrase in text for phrase in ["검색 후보", "선택 근거", "채택 문장", "출처 표시"]):
        return "후보_근거"
    if any(phrase in text for phrase in ["검색 실패", "답변 실패", "문서 범위 밖", "근거 밖"]):
        return "실패_추적"
    if any(phrase in text for phrase in ["문서 분할", "재정렬", "chunking", "reranking"]):
        return "분할_재정렬"
    if any(phrase in text for phrase in ["운영", "승인", "티켓"]):
        return "운영"
    return "기타"

texts = [row["text"] for row in document_rows]
vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
document_embeddings = vectorizer.fit_transform(texts).toarray().astype("float32")
query_embedding = vectorizer.transform([question]).toarray().astype("float32")

# exact 기준선은 같은 TF-IDF 벡터를 전체 문서와 직접 비교해 만든다.
similarities = cosine_similarity(query_embedding, document_embeddings)[0]
for row, score in zip(document_rows, similarities):
    row["bucket"] = bucket_for(row["text"])
    row["exact_score"] = float(score)

exact_top_k = sorted(
    document_rows,
    key=lambda row: row["exact_score"],
    reverse=True,
)[:5]
exact_doc_ids = {row["doc_id"] for row in exact_top_k}

client = chromadb.EphemeralClient()
collection = client.create_collection(
    name="part7_rag_documents",
    embedding_function=None,
    metadata={"hnsw:space": "cosine"},
)
collection.add(
    ids=[row["doc_id"] for row in document_rows],
    documents=texts,
    embeddings=document_embeddings.tolist(),
    metadatas=[{"bucket": row["bucket"]} for row in document_rows],
)

bucket_probe_order = ["후보_근거", "실패_추적", "분할_재정렬", "기타", "운영"]
settings = [
    {"name": "좁은 후보군", "num_probes": 1},
    {"name": "균형 후보군", "num_probes": 2},
    {"name": "넓은 후보군", "num_probes": 4},
]

setting_records = []
for setting in settings:
    selected_buckets = bucket_probe_order[: setting["num_probes"]]
    result = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=5,
        where={"bucket": {"$in": selected_buckets}},
        include=["documents", "metadatas", "distances"],
    )
    retrieved_ids = result["ids"][0]
    retrieved_doc_ids = set(retrieved_ids)
    setting_records.append({
        "설정": setting["name"],
        "탐색 bucket 수": setting["num_probes"],
        "검색 대상 bucket": selected_buckets,
        "후보 문서 수": sum(row["bucket"] in selected_buckets for row in document_rows),
        "top-k 포함률": round(len(exact_doc_ids & retrieved_doc_ids) / len(exact_doc_ids), 2),
        "누락된 exact 후보": sorted(exact_doc_ids - retrieved_doc_ids),
        "vector DB top-k": retrieved_ids,
        "거리": [round(float(distance), 3) for distance in result["distances"][0]],
    })

print("읽은 파일 =", str(data_path))
print("질문 =", question)
print("임베딩 모양 =", document_embeddings.shape)
print("exact top-k =", [
    (row["doc_id"], row["bucket"], round(row["exact_score"], 3))
    for row in exact_top_k
])
print("ChromaDB 설정 비교 =")
for record in setting_records:
    print(record)
```

실행 결과 예시는 다음과 같습니다.

```text
읽은 파일 = docs/assets/part-07/chapter-05/p7-5-rag-documents.csv
질문 = RAG 프로젝트에서 왜 검색 후보와 선택 근거를 답변보다 먼저 기록해야 하는가?
임베딩 모양 = (18, 393)
exact top-k = [('문서-3', '후보_근거', 0.205), ('문서-2', '기타', 0.159), ('문서-4', '후보_근거', 0.138), ('문서-7', '후보_근거', 0.123), ('문서-17', '실패_추적', 0.088)]
ChromaDB 설정 비교 =
{'설정': '좁은 후보군', '탐색 bucket 수': 1, '검색 대상 bucket': ['후보_근거'], '후보 문서 수': 6, 'top-k 포함률': 0.6, '누락된 exact 후보': ['문서-17', '문서-2'], 'vector DB top-k': ['문서-3', '문서-4', '문서-7', '문서-10', '문서-11'], '거리': [0.795, 0.862, 0.877, 0.957, 0.973]}
{'설정': '균형 후보군', '탐색 bucket 수': 2, '검색 대상 bucket': ['후보_근거', '실패_추적'], '후보 문서 수': 9, 'top-k 포함률': 0.8, '누락된 exact 후보': ['문서-2'], 'vector DB top-k': ['문서-3', '문서-4', '문서-7', '문서-17', '문서-14'], '거리': [0.795, 0.862, 0.877, 0.912, 0.921]}
{'설정': '넓은 후보군', '탐색 bucket 수': 4, '검색 대상 bucket': ['후보_근거', '실패_추적', '분할_재정렬', '기타'], '후보 문서 수': 16, 'top-k 포함률': 1.0, '누락된 exact 후보': [], 'vector DB top-k': ['문서-3', '문서-2', '문서-4', '문서-7', '문서-17'], '거리': [0.795, 0.841, 0.862, 0.877, 0.912]}
```

## 결과를 어떻게 읽는가

이번 출력에서 중요한 것은 `넓은 후보군이 항상 정답`이라는 결론이 아닙니다. 설정을 넓히면 exact 후보를 더 잘 보존하지만, 후보 문서 수도 함께 늘어납니다.

| 설정 | 후보 문서 수 | top-k 포함률 | 읽어야 할 점 |
| --- | ---: | ---: | --- |
| 좁은 후보군 | 6 | 0.6 | 빠르지만 `문서-17`, `문서-2`를 놓친다 |
| 균형 후보군 | 9 | 0.8 | 실패 추적 문서는 회수하지만 `문서-2`는 아직 빠진다 |
| 넓은 후보군 | 16 | 1.0 | exact top-k를 모두 포함하지만 후보 수가 크게 늘어난다 |

`문서-17`은 RAG 평가에서 정답 문장 검색 여부와 근거 밖 단정 여부를 나누어 보라는 문서입니다. 좁은 후보군에서는 이 문서가 빠지므로, 답변 경계 검토가 약해질 수 있습니다. `문서-2`는 최신 문서 근거가 왜 필요한지 설명하는 배경 문서입니다. 넓은 후보군까지 열어야 이 문서도 exact top-k와 같이 회수됩니다.

즉, 벡터 DB 검색 설정은 `정확도 손실 없이 빠르게`라는 막연한 약속으로 기록하면 안 됩니다. 이번 실행처럼 `후보 수가 얼마로 줄었는가`, `exact 기준선 중 무엇을 놓쳤는가`, `그 누락이 현재 질문에서 중요한가`를 같이 남겨야 합니다.

## 프로젝트 기록 예시

```text
질문:
exact top-k:
vector DB 설정:
후보 문서 수:
top-k 포함률:
누락된 exact 후보:
누락 후보가 답변 근거에 주는 영향:
다음 설정 변경:
```

한 문단으로 쓰면 다음처럼 정리할 수 있습니다.

> 이번 설정 비교에서는 `좁은 후보군`이 후보 문서 수를 6개까지 줄였지만 exact top-k 포함률은 0.6에 머물렀다. 특히 RAG 평가 경계를 설명하는 `문서-17`이 누락되어, 답변 경계 검토가 약해질 수 있다. `균형 후보군`은 후보 수를 9개로 늘려 `문서-17`을 회수했지만 배경 문서인 `문서-2`는 놓쳤다. 따라서 이번 질문에서는 후보 수만 줄이는 설정보다, 최소한 실패 추적 bucket까지 함께 보는 설정이 더 적절하다.

## 직접 바꿔 보며 확인할 것

1. `settings`에 `{"name": "전체 후보군", "num_probes": 5}`를 추가해 봅니다.  
   관찰할 점: exact 검색과 거의 같아질수록 후보 수가 얼마나 늘어나는가?

2. `bucket_probe_order`에서 `실패_추적`을 뒤로 미뤄 봅니다.  
   관찰할 점: `문서-17`이 다시 누락되며 top-k 포함률과 해석이 어떻게 달라지는가?

3. `question`을 `문서 분할과 재정렬은 검색 품질에 어떤 도움을 주는가?`로 바꿔 봅니다.  
   관찰할 점: 같은 bucket 순서가 다른 질문에서도 적절한가?

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| 기준선 | approximate 결과를 exact top-k와 비교했는가? |
| 후보 수 | 설정별 후보 문서 수를 함께 남겼는가? |
| 포함률 | top-k 포함률이 낮아질 때 어떤 후보가 빠지는지 확인했는가? |
| 해석 | 누락된 후보가 현재 질문의 근거 품질에 어떤 영향을 주는지 적었는가? |
| 다음 설정 | 더 좁힐지, 더 넓힐지, bucket 순서를 바꿀지 다음 실험을 남겼는가? |

## 출처와 참고 자료

- 문서 조각 파일: [`p7-5-rag-documents.csv`](../../../assets/part-07/chapter-05/p7-5-rag-documents.csv){ .csv-preview }
- Chroma, `Adding Data to Chroma Collections`, 확인 날짜: 2026-07-23. [https://docs.trychroma.com/docs/collections/add-data](https://docs.trychroma.com/docs/collections/add-data){: target="_blank" rel="noopener noreferrer" }
- Chroma, `Metadata Filtering`, 확인 날짜: 2026-07-23. [https://docs.trychroma.com/docs/querying-collections/metadata-filtering](https://docs.trychroma.com/docs/querying-collections/metadata-filtering){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `Feature extraction` and `Pairwise metrics`, 확인 날짜: 2026-07-23. [https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction){: target="_blank" rel="noopener noreferrer" }, [https://scikit-learn.org/stable/modules/metrics.html#cosine-similarity](https://scikit-learn.org/stable/modules/metrics.html#cosine-similarity){: target="_blank" rel="noopener noreferrer" }
- 이 문서는 자체 합성 데이터와 자체 실습 예시를 사용했습니다. 외부 자료를 직접 인용하지 않았습니다.
