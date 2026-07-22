# P7-5.4 ANN 검색 설정 실습

Section ID: `P7-5.4`
Version: `v2026.07.22`

RAG 프로젝트에서 문서가 늘어나면 모든 문서를 매번 정확히 비교하는 방식은 점점 부담이 됩니다. 그래서 실제 검색 시스템은 근사 최근접 이웃(ANN, approximate nearest neighbor) 검색처럼 후보를 빠르게 줄이는 구조를 자주 사용합니다.

다만 초심자가 먼저 잡아야 할 것은 특정 라이브러리 이름이 아닙니다. 핵심은 `후보를 적게 보면 빠르지만 놓칠 수 있고, 후보를 넓게 보면 더 잘 찾지만 비용이 늘어난다`는 교환 관계입니다. 이 절에서는 실제 ANN 라이브러리를 쓰지 않고, 문서를 몇 개의 bucket으로 나눈 뒤 탐색 bucket 수를 바꾸는 작은 모의 실험으로 이 감각을 확인합니다.

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
| exact top-k | 모든 대표 문서를 비교했을 때의 기준선 |
| approximate top-k | 일부 bucket만 보고 얻은 빠른 후보 |
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

예제는 실제 벡터 인덱스 구현이 아니라 ANN 설정 감각을 보여 주는 모의 실험입니다. `num_probes`를 탐색 bucket 수처럼 사용해, 후보군을 좁게 볼 때와 넓게 볼 때 결과가 어떻게 달라지는지 비교합니다.

- 문제 상황: RAG 문서 검색에서 후보군을 줄이면 어떤 근거가 빠질 수 있는지 확인한다.
- 입력: 대표 문서 18개, 질문 1개
- 기대 출력: exact top-k, 설정별 approximate top-k, top-k 포함률, 누락 후보
- 확인할 개념:
  - approximate 검색은 후보군 제한 때문에 exact top-k를 일부 놓칠 수 있다
  - `num_probes`를 늘리면 후보 수와 포함률이 함께 바뀐다
  - ANN 설정은 속도만이 아니라 근거 누락 위험과 함께 기록해야 한다

```python
# RAG 문서 검색에서 exact top-k와 bucket 기반 approximate top-k를 비교해 ANN 설정의 후보 수와 누락 위험을 확인하는 예제입니다.
import csv
import re
from pathlib import Path

question = "RAG 프로젝트에서 왜 검색 후보와 선택 근거를 답변보다 먼저 기록해야 하는가?"
data_path = Path("docs/assets/part-07/chapter-05/p7-5-rag-documents.csv")
document_rows = list(csv.DictReader(data_path.open(encoding="utf-8")))
representative_doc_ids = {f"문서-{index}" for index in range(1, 19)}
document_rows = [
    row for row in document_rows if row["doc_id"] in representative_doc_ids
]

def tokenize(text):
    cleaned = re.sub(r"[^0-9A-Za-z가-힣]+", " ", text).lower()
    return {token for token in cleaned.split() if len(token) > 1}

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

def score_document(question, text):
    overlap_terms = sorted(tokenize(question) & tokenize(text))
    direct_clues = sum(
        phrase in text
        for phrase in ["검색 후보", "선택 근거", "최종 답변", "답변 실패", "검색 실패", "근거 밖"]
    )
    return len(overlap_terms) + direct_clues, overlap_terms

indexed_rows = []
for row in document_rows:
    score, overlap_terms = score_document(question, row["text"])
    indexed_rows.append({
        "doc_id": row["doc_id"],
        "bucket": bucket_for(row["text"]),
        "score": score,
        "overlap_terms": overlap_terms,
        "text": row["text"],
    })

exact_top_k = sorted(
    indexed_rows,
    key=lambda row: (row["score"], len(row["overlap_terms"]), row["doc_id"]),
    reverse=True,
)[:5]
exact_doc_ids = {row["doc_id"] for row in exact_top_k}

bucket_probe_order = ["후보_근거", "실패_추적", "분할_재정렬", "기타", "운영"]
settings = [
    {"name": "좁은 후보군", "num_probes": 1},
    {"name": "균형 후보군", "num_probes": 2},
    {"name": "넓은 후보군", "num_probes": 4},
]

setting_records = []
for setting in settings:
    selected_buckets = set(bucket_probe_order[:setting["num_probes"]])
    candidates = [row for row in indexed_rows if row["bucket"] in selected_buckets]
    approx_top_k = sorted(
        candidates,
        key=lambda row: (row["score"], len(row["overlap_terms"]), row["doc_id"]),
        reverse=True,
    )[:5]
    approx_doc_ids = {row["doc_id"] for row in approx_top_k}
    setting_records.append({
        "설정": setting["name"],
        "탐색 bucket 수": setting["num_probes"],
        "후보 문서 수": len(candidates),
        "top-k 포함률": round(len(exact_doc_ids & approx_doc_ids) / len(exact_doc_ids), 2),
        "누락된 exact 후보": sorted(exact_doc_ids - approx_doc_ids),
        "approx top-k": [row["doc_id"] for row in approx_top_k],
    })

print("읽은 파일 =", str(data_path))
print("질문 =", question)
print("exact top-k =", [(row["doc_id"], row["bucket"], row["score"]) for row in exact_top_k])
print("ANN 설정 비교 =")
for record in setting_records:
    print(record)
```

실행 결과 예시는 다음과 같습니다.

```text
읽은 파일 = docs/assets/part-07/chapter-05/p7-5-rag-documents.csv
질문 = RAG 프로젝트에서 왜 검색 후보와 선택 근거를 답변보다 먼저 기록해야 하는가?
exact top-k = [('문서-4', '후보_근거', 8), ('문서-3', '후보_근거', 5), ('문서-14', '실패_추적', 4), ('문서-2', '기타', 3), ('문서-7', '후보_근거', 3)]
ANN 설정 비교 =
{'설정': '좁은 후보군', '탐색 bucket 수': 1, '후보 문서 수': 6, 'top-k 포함률': 0.6, '누락된 exact 후보': ['문서-14', '문서-2'], 'approx top-k': ['문서-4', '문서-3', '문서-7', '문서-11', '문서-10']}
{'설정': '균형 후보군', '탐색 bucket 수': 2, '후보 문서 수': 9, 'top-k 포함률': 0.8, '누락된 exact 후보': ['문서-2'], 'approx top-k': ['문서-4', '문서-3', '문서-14', '문서-7', '문서-17']}
{'설정': '넓은 후보군', '탐색 bucket 수': 4, '후보 문서 수': 16, 'top-k 포함률': 1.0, '누락된 exact 후보': [], 'approx top-k': ['문서-4', '문서-3', '문서-14', '문서-2', '문서-7']}
```

## 결과를 어떻게 읽는가

이번 출력에서 중요한 것은 `넓은 후보군이 항상 정답`이라는 결론이 아닙니다. 설정을 넓히면 exact 후보를 더 잘 보존하지만, 후보 문서 수도 함께 늘어납니다.

| 설정 | 후보 문서 수 | top-k 포함률 | 읽어야 할 점 |
| --- | ---: | ---: | --- |
| 좁은 후보군 | 6 | 0.6 | 빠르지만 `문서-14`, `문서-2`를 놓친다 |
| 균형 후보군 | 9 | 0.8 | 실패 추적 문서는 회수하지만 `문서-2`는 아직 빠진다 |
| 넓은 후보군 | 16 | 1.0 | exact top-k를 모두 포함하지만 후보 수가 크게 늘어난다 |

`문서-14`는 검색 실패와 답변 실패를 구분하는 데 필요한 문서입니다. 좁은 후보군에서는 이 문서가 빠지므로, 답변 경계 검토가 약해질 수 있습니다. `문서-2`는 최신 문서 근거가 왜 필요한지 설명하는 배경 문서입니다. 넓은 후보군까지 열어야 이 문서도 exact top-k와 같이 회수됩니다.

즉, ANN 설정은 `정확도 손실 없이 빠르게`라는 막연한 약속으로 기록하면 안 됩니다. 이번 실행처럼 `후보 수가 얼마로 줄었는가`, `exact 기준선 중 무엇을 놓쳤는가`, `그 누락이 현재 질문에서 중요한가`를 같이 남겨야 합니다.

## 프로젝트 기록 예시

```text
질문:
exact top-k:
ANN 설정:
후보 문서 수:
top-k 포함률:
누락된 exact 후보:
누락 후보가 답변 근거에 주는 영향:
다음 설정 변경:
```

한 문단으로 쓰면 다음처럼 정리할 수 있습니다.

> 이번 설정 비교에서는 `좁은 후보군`이 후보 문서 수를 6개까지 줄였지만 exact top-k 포함률은 0.6에 머물렀다. 특히 검색 실패와 답변 실패 구분을 설명하는 `문서-14`가 누락되어, RAG 답변 경계 검토가 약해질 수 있다. `균형 후보군`은 후보 수를 9개로 늘려 `문서-14`를 회수했지만 배경 문서인 `문서-2`는 놓쳤다. 따라서 이번 질문에서는 후보 수만 줄이는 설정보다, 최소한 실패 추적 bucket까지 함께 보는 설정이 더 적절하다.

## 직접 바꿔 보며 확인할 것

1. `settings`에 `{"name": "전체 후보군", "num_probes": 5}`를 추가해 봅니다.  
   관찰할 점: exact 검색과 거의 같아질수록 후보 수가 얼마나 늘어나는가?

2. `bucket_probe_order`에서 `실패_추적`을 뒤로 미뤄 봅니다.  
   관찰할 점: `문서-14`가 다시 누락되며 top-k 포함률과 해석이 어떻게 달라지는가?

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
- 이 문서는 자체 합성 데이터와 자체 실습 예시를 사용했습니다. 외부 자료를 직접 인용하지 않았습니다.
