# P5-11.1 벡터 데이터베이스(vector database)

P5-10.2에서는 검색 결과가 생성 전에 입력 맥락으로 붙는다는 점을 보았습니다. 그러면 다음 질문이 자연스럽게 이어집니다.

그 검색은 실제로 어떤 저장 구조 위에서 돌아가는가?

이 절은 그 질문에 답합니다.

벡터 데이터베이스(vector database)는 임베딩(embedding) 벡터와 그에 연결된 원문, 메타데이터를 저장하고, 비슷한 벡터를 빠르게 찾도록 돕는 시스템이다.

## 이 절의 범위

이 절은 다음 질문에 답합니다.

- 왜 텍스트를 그대로 검색하지 않고 벡터를 저장하는가?
- 벡터 데이터베이스는 무엇을 저장하고 무엇을 돌려주는가?
- 왜 RAG 구조에서 벡터 데이터베이스가 자주 등장하는가?

이 절에서는 다음 내용을 깊게 다루지 않습니다.

- 특정 상용 제품 비교
- ANN(approximate nearest neighbor) 알고리즘 수식
- 샤딩과 클러스터 운영 세부

벡터 저장소의 역할은 여기서 잡고, 속도와 근사 검색의 균형은 바로 다음 P5-11.2 인덱스와 검색 품질에서 다시 회수합니다. 특정 제품 비교와 클러스터 운영 세부는 빠르게 바뀌는 주제라 현재 본편 범위 밖으로 둡니다.

벡터 데이터베이스는 `새로운 종류의 마법 저장소`가 아니라, 임베딩 검색을 서비스 구조 안에서 다루기 쉽게 만든 시스템으로 읽는 편이 맞습니다.

이 절은 `retrieval 저장소 손잡이 축`으로 읽으면 됩니다.

| 단계 | 지금 붙잡을 질문 | 바로 이어지는 위치 |
| --- | --- | --- |
| 검색 결과와 생성 결합 | 찾아온 문서를 답변 전에 어디에 붙일 것인가? | P5-10.2 |
| retrieval 저장소 | 임베딩, 원문, 메타데이터를 어떤 저장 구조에 함께 담아 둘 것인가? | P5-11.1 |
| 인덱스와 검색 품질 | 그 저장 구조 안에서 후보를 어떤 속도와 품질 균형으로 좁힐 것인가? | P5-11.2 |

여기서 한 번 더 층위를 나누어 보면, 바로 앞 절과 지금 절의 역할 차이가 더 분명해집니다.

| 지금까지 본 층위 | 중심 질문 | 지금 절에서 더해지는 것 |
| --- | --- | --- |
| P5-10.2 검색 결과와 생성의 결합 | 찾아온 문서가 답변 전에 어디에 붙는가? | 검색 결과가 생성 전에 입력 맥락으로 붙는다는 점 |
| P5-11.1 벡터 데이터베이스 | 그 문서를 실제로 어떤 저장 구조에서 다시 꺼내 오는가? | 임베딩, 원문, 메타데이터가 함께 저장된 retrieval 저장소 관점 |
| P5-11.2 인덱스와 검색 품질 | 그 저장 구조 안에서 후보를 얼마나 빠르고 정확하게 좁힐 것인가? | 속도와 top-k 품질의 균형 |

즉, P5-10장이 `검색 후 생성`이라는 흐름을 잡았다면, P5-11장은 그 검색을 실제 서비스에서 떠받치는 저장소와 탐색 구조를 읽는 자리입니다. 이 기준이 잡혀야 벡터 데이터베이스를 또 하나의 유행 기술명이 아니라, `RAG 검색 단계를 운영 가능한 구조로 바꾸는 층`으로 읽을 수 있습니다.

벡터 데이터베이스는 Part 5 본류의 `retrieval 저장소 손잡이`로 읽으면 됩니다. 바로 앞 장의 RAG 결합이 `찾아온 문서를 생성 전에 어디에 붙일까`를 맡았다면, 지금 장은 그 문서를 어떤 retrieval 저장 구조에서 다시 꺼낼지를 맡고, 바로 다음 인덱스 장에서는 그 저장 구조 안에서 후보를 얼마나 빠르고 정확하게 좁힐지를 더 봅니다. 즉, 흐름은 `검색 후 생성 흐름 -> retrieval 저장소 -> 탐색 구조와 검색 품질`로 이어지며, 여기서 손잡이는 `문서를 붙이는가`에서 `그 문서를 서비스 안에서 다시 꺼내 쓸 저장 구조가 있는가`로 바뀝니다.

## 이 절의 목표

- 벡터 데이터베이스를 입문 수준에서 설명할 수 있습니다.
- 임베딩, 문서 조각(chunk), 메타데이터가 함께 저장된다는 점을 말할 수 있습니다.
- 왜 RAG에서 일반 키워드 검색만으로는 부족할 수 있는지 설명할 수 있습니다.
- 다음 절의 인덱스와 검색 품질 문제로 자연스럽게 넘어갈 수 있습니다.

## 이 절을 읽는 순서

이 절은 다음 순서로 읽으면 흐름이 잘 잡힙니다.

1. 먼저 `왜 벡터를 저장하나`와 `벡터 데이터베이스는 무엇을 저장하나`를 읽고, 표현이 달라도 의미가 가까운 문서를 찾기 위해 벡터를 저장하지만 실제로는 원문과 메타데이터도 같이 보관한다는 점을 잡습니다.
2. 그다음 `무엇을 돌려주나`, `왜 RAG에서 자주 등장하나`, `일반 데이터베이스와 무엇이 다른가`를 읽으면서 이 저장 구조가 검색 파이프라인 안에서 어떤 역할을 맡는지 구분합니다.
3. 마지막으로 사례와 Python 예제를 보면서, 같은 저장 구조라도 질문 벡터가 바뀌면 top-1 문서, 출처, 범주, retrieval payload가 함께 바뀐다는 점을 확인합니다.

## 왜 벡터를 저장하나

앞 절에서 보았듯, RAG는 관련 문서를 먼저 찾는 구조입니다. 그런데 질문과 문서가 항상 같은 단어를 쓰는 것은 아닙니다.

예를 들어 사용자는:

- `환불 기준이 바뀌었나요?`

라고 묻고, 문서에는:

- `반품 처리 기간 변경`

처럼 다른 표현이 있을 수 있습니다.

이런 경우 단순 키워드 검색은 놓칠 수 있지만, 의미가 비슷한 표현을 벡터 공간에서 가깝게 찾는 방식은 도움이 될 수 있습니다.

즉, 벡터 데이터베이스는 `문장을 숫자 벡터로 바꾼 뒤, 의미가 가까운 것을 빠르게 찾는 일`을 서비스 안에서 관리하기 쉽게 해 줍니다.

## 벡터 데이터베이스는 무엇을 저장하나

독자가 가장 자주 오해하는 지점은 `벡터만 저장하는가?`입니다. 실제로는 보통 다음이 함께 들어갑니다.

- 임베딩 벡터
- 원문 또는 문서 조각(chunk)
- 문서 ID
- 제목, 날짜, 출처 같은 메타데이터(metadata)

즉, 벡터 데이터베이스는 보통 `숫자 벡터만 덩그러니 모아 둔 곳`이 아니라, `검색 후 다시 원문을 꺼내 올 수 있게 연결된 저장소`로 보는 편이 맞습니다.

## 무엇을 돌려주나

질문을 임베딩으로 바꿔 검색하면, 시스템은 보통 다음을 돌려줍니다.

- 가까운 벡터 항목들
- 그 항목에 연결된 문서 조각
- 유사도 점수
- 메타데이터

그리고 RAG 파이프라인은 이 결과를 다시 프롬프트 맥락으로 붙여 생성 단계에 넘깁니다.

## 왜 RAG에서 자주 등장하나

RAG는 `질문 -> 관련 문서 검색 -> 생성` 구조입니다. 여기서 검색이 의미 기반으로 이루어지려면, 벡터 저장과 유사도 검색을 효율적으로 다루는 계층이 필요합니다.

다음처럼 기억하면 좋습니다.

`벡터 데이터베이스는 RAG에서 검색 단계의 실무형 저장소 역할을 한다.`

즉, 이 시스템의 역할은 모델을 대신하는 것이 아니라, 모델이 참고할 문서를 잘 찾아오도록 돕는 것입니다.

## 일반 데이터베이스와 무엇이 다른가

이 절에서는 엄밀 비교보다 역할 차이만 잡으면 충분합니다.

| 저장소 관점 | 중심 질문 |
| --- | --- |
| 일반 데이터베이스 | 정확히 일치하는 키, 필드, 조건을 어떻게 찾을까? |
| 벡터 데이터베이스 | 의미가 비슷한 항목을 어떻게 가깝게 찾을까? |

물론 실제 서비스에서는 두 종류를 같이 쓰기도 합니다. 예를 들어:

- 사용자 ID나 날짜 필터는 일반 필드 검색
- 의미가 비슷한 문서 찾기는 벡터 검색

처럼 결합될 수 있습니다.

## 벡터 데이터베이스도 만능은 아니다

이 점을 같이 넣어야 `벡터 데이터베이스를 붙였다`는 사실과 `검색 품질 문제가 자동으로 해결됐다`는 판단을 섞지 않게 됩니다.

벡터 데이터베이스가 있다고 해서:

- 항상 가장 관련된 문서를 찾는 것
- 오래된 문서를 자동으로 배제하는 것
- 잘못 쪼개진 문서를 스스로 고치는 것

이 자동으로 해결되지는 않습니다.

즉, 벡터 저장 구조는 중요하지만, 문서를 어떻게 나누는지, 메타데이터를 어떻게 붙이는지, 어떤 임베딩 모델을 쓰는지도 여전히 중요합니다.

## 아주 단순하게 그리면

```mermaid
flowchart TD
  A["text chunk"]
  B["embedding vector"]
  C["vector database"]
  D["nearest matching chunks"]

  A --> B
  B --> C
  C --> D
```

이 도식의 핵심은 텍스트가 먼저 벡터로 바뀌고, 검색은 그 벡터 저장소에서 일어난다는 점입니다.

## 사례로 보기

### 사례 1. 사내 위키 검색

사내 위키에서 사용자가 `퇴사 전에 회사 노트북을 어디에 반납하나요?`라고 묻는 장면을 생각해 보겠습니다. 사람이 키워드 검색만 쓰면 먼저 `노트북 반납`이란 표현이 그대로 들어간 문서를 찾게 됩니다. 하지만 실제 문서 제목은 `오프보딩 절차`, `자산 회수 안내`, `퇴사 체크리스트`처럼 다를 수 있고, 핵심 문장은 본문 안의 `IT 자산은 보안팀 데스크로 회수한다`일 수 있습니다. 이때 질문에는 `반납`이 있고 문서에는 `회수`만 있어도, 업무 흐름은 사실상 같습니다. 여기서 바뀌는 점은 `같은 단어가 있나`를 보던 기준에서 `의미가 같은 문단이 후보로 올라오는가`를 보는 기준으로 이동한다는 것입니다. 벡터 데이터베이스는 질문과 문서 조각을 의미 기반 벡터로 저장해 이런 표현 차이를 넘어서 관련 문단을 후보로 올리기 쉽게 만듭니다. 그래서 이 사례에서 확인해야 할 결과는 `반납`이란 단어가 없어도 `회수` 문단이 실제 후보로 올라오는가입니다.

### 사례 2. 제품 매뉴얼 검색

제품 매뉴얼에서 사용자가 `설정을 처음 상태로 되돌리고 싶어요`라고 묻는다고 해 봅시다. 사람이 문자열 검색만 쓰면 `처음 상태`, `되돌리기` 같은 표현이 들어간 문서부터 찾으려 합니다. 하지만 실제 매뉴얼은 `공장 초기화`, `설정 복원`, `리셋 후 재부팅`처럼 다른 용어를 섞어 쓸 수 있고, 메뉴 경로는 본문 표 한 칸에만 들어 있을 수 있습니다. 예를 들어 검색은 개요 문단만 찾고 실제 버튼 순서가 적힌 문단을 놓칠 수 있습니다. 여기서 바뀌는 점은 `표현이 비슷한가`를 보던 기준에서 `실제로 필요한 절차 문단이 함께 후보로 올라오는가`를 보는 기준으로 이동한다는 것입니다. 벡터 데이터베이스는 이런 문서 조각을 의미가 가까운 위치에 저장해 표현 차이가 있어도 관련 후보를 더 고르게 모읍니다. 그래서 이 사례에서 확인해야 할 결과는 개요 설명보다 실제 버튼 순서가 적힌 문단이 함께 후보로 올라오는가입니다.

### 사례 3. 개발 문서 지원

개발자가 `요청 제한이 걸리면 잠깐 기다렸다 다시 보내는 옵션이 있나요?`라고 묻는다고 해 봅시다. 사람은 함수 이름이나 옵션명을 정확히 알아야 검색이 될 것이라고 먼저 생각할 수 있습니다. 하지만 질문에는 정확한 이름이 없고, 실제로는 retry나 backoff 설명이 들어 있는 API 문단을 찾아야 할 수 있습니다. 예를 들어 문서에는 `exponential backoff`와 `max_retries`만 적혀 있는데, 질문은 `잠깐 기다렸다 다시 보내기`처럼 완전히 풀어 쓸 수 있습니다. 키워드 검색만 쓰면 이름이 없는 질문에서 관련 문단이 후보에 올라오지 않을 수 있습니다. 여기서 바뀌는 점은 `정확한 옵션명을 아는가`를 보던 기준에서 `의미가 가까운 API 설명을 후보로 찾는가`를 보는 기준으로 이동한다는 것입니다. 벡터 데이터베이스는 이런 질문과 문서 조각을 의미 기반으로 가깝게 저장해 관련 API 설명을 더 잘 끌어올립니다. 그래서 이 사례에서 확인해야 할 결과는 정확한 옵션명을 몰라도 retry나 backoff 문단이 실제 후보로 올라오는가입니다.

세 사례를 회수 기준으로 다시 정리하면 다음과 같습니다.

| 상황 | 문자열 검색만으로는 놓치기 쉬운 것 | 벡터 검색이 회수하려는 것 |
| --- | --- | --- |
| 사내 위키 검색 | `반납`과 `회수`처럼 표현이 다른 동일 업무 문단 | 의미가 같은 오프보딩 절차 문단 |
| 제품 매뉴얼 검색 | 개요 설명 뒤에 숨은 실제 버튼 순서 문단 | 절차 수행에 필요한 핵심 단계 문단 |
| 개발 문서 지원 | 질문에 이름이 없는 retry/backoff 관련 API 설명 | 의미가 가까운 옵션·동작 설명 문단 |

같은 내용을 저장 구조 관점으로 다시 보면 다음처럼 읽을 수 있습니다.

```mermaid
flowchart LR
  A["text chunk"]
  B["embedding vector"]
  C["metadata<br/>source / category / version"]
  D["vector database record"]
  E["retrieval payload<br/>text + metadata"]

  A --> D
  B --> D
  C --> D
  D --> E
```

핵심은 `벡터만 따로 저장`이 아니라, 검색 뒤에 생성 단계가 바로 다시 쓸 수 있게 텍스트와 메타데이터까지 연결된 레코드로 다룬다는 점입니다.

## 실행 가능한 Python 예제로 보기

이번 예제의 목표는 실제 벡터 데이터베이스 엔진 전체를 구현하는 것이 아니라, `벡터`, `원문`, `메타데이터`가 함께 저장되고, 질문 벡터와의 유사도로 다시 꺼내 쓰인다는 점을 눈으로 확인하는 것입니다. 이번에는 환불 정책, 설정 메뉴, SDK 제한 처리처럼 다른 질문 벡터를 한 번에 돌려, 같은 저장 구조가 질문에 따라 다른 조각과 메타데이터를 다시 꺼내고, 그 결과가 생성 단계용 payload로 어떻게 넘어가는지까지 보겠습니다.

문제 상황:

- 문서 조각들은 숫자 벡터만이 아니라 원문과 출처 정보를 함께 가져야 함
- 질문이 들어오면 질문 벡터와 가까운 조각을 다시 찾아야 함
- 검색 후에는 원문 텍스트와 메타데이터를 함께 생성 단계에 넘겨야 함
- 따라서 `무엇이 top-1인가`뿐 아니라 `어떤 출처와 범주가 같이 따라오는가`도 중요함

입력:

- 세 개의 문서 조각
- 각 조각의 임베딩 벡터
- 질문 벡터 여러 개

출력:

- 질문별 유사도 점수
- 질문별 상위 후보 문서 조각
- 검색 후 다시 꺼내 쓰는 원문과 메타데이터
- 질문별 1위 후보의 출처와 범주
- 생성 단계로 넘길 retrieval payload

먼저 이 절에서 확인할 점을 표로 잡으면 다음과 같습니다.

| 점검 항목 | 왜 필요한가 |
| --- | --- |
| top-1 후보가 기대 범주와 맞는가 | 벡터 검색이 질문 의도를 제대로 회수했는지 확인 |
| 반환 결과에 원문이 포함되는가 | 생성 단계가 실제 문장을 다시 붙일 수 있어야 해서 |
| 반환 결과에 메타데이터가 포함되는가 | 출처 표기, 날짜 필터, 버전 필터에 필요해서 |
| 질문마다 payload가 달라지는가 | 같은 저장 구조가 질문별 근거 반환 계층으로 동작하는지 확인 |

문제 상황:

- 벡터 저장소는 비슷한 문장만 찾는 것이 아니라 원문과 메타데이터까지 함께 반환해야 RAG에 바로 쓸 수 있다

입력(input):

위에 정리한 문서 레코드, 임베딩, 질문 벡터를 사용합니다.

확인할 개념:

- 벡터 데이터베이스는 유사한 문장뿐 아니라 원문과 메타데이터를 함께 반환해야 RAG 근거 저장소로 쓸 수 있다

```python
import math

records = [
    {
        "id": "doc-001-chunk-02",
        "text": "환불 요청 처리 기한이 14일로 변경되었습니다.",
        "embedding": [0.92, 0.15, 0.08],
        "metadata": {"source": "policy_notice_2026_06_29", "category": "refund"},
    },
    {
        "id": "doc-002-chunk-01",
        "text": "자동 저장은 환경설정 > 편집 메뉴에서 끌 수 있습니다.",
        "embedding": [0.12, 0.88, 0.14],
        "metadata": {"source": "manual_v3", "category": "settings"},
    },
    {
        "id": "doc-003-chunk-03",
        "text": "요청 제한이 걸리면 exponential backoff를 사용하세요.",
        "embedding": [0.21, 0.18, 0.93],
        "metadata": {"source": "sdk_guide_v2", "category": "api"},
    },
]

query_vectors = [
    {
        "name": "refund_question",
        "vector": [0.95, 0.10, 0.05],
        "expected_category": "refund",
    },
    {
        "name": "settings_question",
        "vector": [0.10, 0.93, 0.11],
        "expected_category": "settings",
    },
    {
        "name": "api_limit_question",
        "vector": [0.19, 0.16, 0.96],
        "expected_category": "api",
    },
]


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)


reports = []

for query in query_vectors:
    scored = []
    for record in records:
        score = cosine_similarity(query["vector"], record["embedding"])
        scored.append((score, record))

    scored.sort(key=lambda item: item[0], reverse=True)
    top_matches = scored[:2]

    retrieval_payload = [
        {
            "text": record["text"],
            "source": record["metadata"]["source"],
            "category": record["metadata"]["category"],
        }
        for score, record in top_matches
    ]

    reports.append(
        {
            "query_name": query["name"],
            "query_vector": query["vector"],
            "expected_category": query["expected_category"],
            "top_matches": [
                {
                    "score": round(score, 4),
                    "id": record["id"],
                    "text": record["text"],
                    "metadata": record["metadata"],
                }
                for score, record in top_matches
            ],
            "top1_summary": {
                "source": top_matches[0][1]["metadata"]["source"],
                "category": top_matches[0][1]["metadata"]["category"],
            },
            "retrieval_payload": retrieval_payload,
            "inspection": {
                "top1_category_ok": top_matches[0][1]["metadata"]["category"] == query["expected_category"],
                "payload_has_text": all("text" in item for item in retrieval_payload),
                "payload_has_metadata": all("source" in item and "category" in item for item in retrieval_payload),
                "payload_count": len(retrieval_payload),
            },
        }
    )

summary = {
    "top1_category_match_count": sum(report["inspection"]["top1_category_ok"] for report in reports),
    "payload_has_text_count": sum(report["inspection"]["payload_has_text"] for report in reports),
    "payload_has_metadata_count": sum(report["inspection"]["payload_has_metadata"] for report in reports),
    "top1_category_match_ratio": round(
        sum(report["inspection"]["top1_category_ok"] for report in reports) / len(reports),
        2,
    ),
    "payload_has_text_ratio": round(
        sum(report["inspection"]["payload_has_text"] for report in reports) / len(reports),
        2,
    ),
    "payload_has_metadata_ratio": round(
        sum(report["inspection"]["payload_has_metadata"] for report in reports) / len(reports),
        2,
    ),
}

print("[summary]")
print(summary)
print()

for report in reports:
    print("=" * 80)
    print("[query]")
    print(report["query_name"], report["query_vector"])
    print("[top matches]")
    for item in report["top_matches"]:
        print(item)
    print("[top1 summary]")
    print(report["top1_summary"])
    print("[retrieval payload]")
    print(report["retrieval_payload"])
    print("[inspection]")
    print(report["inspection"])
```

실행 결과 예시는 다음처럼 읽을 수 있습니다.

```text
[summary]
{'top1_category_match_count': 3, 'payload_has_text_count': 3, 'payload_has_metadata_count': 3, 'top1_category_match_ratio': 1.0, 'payload_has_text_ratio': 1.0, 'payload_has_metadata_ratio': 1.0}

================================================================================
[query]
refund_question [0.95, 0.1, 0.05]
[top matches]
{'score': 0.9978, 'id': 'doc-001-chunk-02', 'text': '환불 요청 처리 기한이 14일로 변경되었습니다.', 'metadata': {'source': 'policy_notice_2026_06_29', 'category': 'refund'}}
{'score': 0.2845, 'id': 'doc-003-chunk-03', 'text': '요청 제한이 걸리면 exponential backoff를 사용하세요.', 'metadata': {'source': 'sdk_guide_v2', 'category': 'api'}}
[top1 summary]
{'source': 'policy_notice_2026_06_29', 'category': 'refund'}
[retrieval payload]
[{'text': '환불 요청 처리 기한이 14일로 변경되었습니다.', 'source': 'policy_notice_2026_06_29', 'category': 'refund'}, {'text': '요청 제한이 걸리면 exponential backoff를 사용하세요.', 'source': 'sdk_guide_v2', 'category': 'api'}]
[inspection]
{'top1_category_ok': True, 'payload_has_text': True, 'payload_has_metadata': True, 'payload_count': 2}
================================================================================
[query]
settings_question [0.1, 0.93, 0.11]
[top matches]
{'score': 0.9988, 'id': 'doc-002-chunk-01', 'text': '자동 저장은 환경설정 > 편집 메뉴에서 끌 수 있습니다.', 'metadata': {'source': 'manual_v3', 'category': 'settings'}}
{'score': 0.3181, 'id': 'doc-003-chunk-03', 'text': '요청 제한이 걸리면 exponential backoff를 사용하세요.', 'metadata': {'source': 'sdk_guide_v2', 'category': 'api'}}
[top1 summary]
{'source': 'manual_v3', 'category': 'settings'}
[retrieval payload]
[{'text': '자동 저장은 환경설정 > 편집 메뉴에서 끌 수 있습니다.', 'source': 'manual_v3', 'category': 'settings'}, {'text': '요청 제한이 걸리면 exponential backoff를 사용하세요.', 'source': 'sdk_guide_v2', 'category': 'api'}]
[inspection]
{'top1_category_ok': True, 'payload_has_text': True, 'payload_has_metadata': True, 'payload_count': 2}
================================================================================
[query]
api_limit_question [0.19, 0.16, 0.96]
[top matches]
{'score': 0.9994, 'id': 'doc-003-chunk-03', 'text': '요청 제한이 걸리면 exponential backoff를 사용하세요.', 'metadata': {'source': 'sdk_guide_v2', 'category': 'api'}}
{'score': 0.3342, 'id': 'doc-002-chunk-01', 'text': '자동 저장은 환경설정 > 편집 메뉴에서 끌 수 있습니다.', 'metadata': {'source': 'manual_v3', 'category': 'settings'}}
[top1 summary]
{'source': 'sdk_guide_v2', 'category': 'api'}
[retrieval payload]
[{'text': '요청 제한이 걸리면 exponential backoff를 사용하세요.', 'source': 'sdk_guide_v2', 'category': 'api'}, {'text': '자동 저장은 환경설정 > 편집 메뉴에서 끌 수 있습니다.', 'source': 'manual_v3', 'category': 'settings'}]
[inspection]
{'top1_category_ok': True, 'payload_has_text': True, 'payload_has_metadata': True, 'payload_count': 2}
```

이 결과에서 먼저 봐야 할 것은 `top1_category_match_count`가 3이고, `payload_has_text_count`, `payload_has_metadata_count`도 모두 3이라는 점입니다. 즉, 벡터 데이터베이스는 가까운 숫자 항목 하나만 돌려주는 것이 아니라, 질문별로 맞는 범주의 조각을 top-1로 올리고, 생성 단계가 바로 쓸 수 있는 원문과 메타데이터를 함께 payload로 돌려주는 계층으로 읽어야 합니다.

그래서 이 예제에서 확인해야 할 결과는 두 가지입니다.

- 임베딩 숫자만 저장하는 것이 아니라, 검색 뒤에 생성 단계가 다시 사용할 원문 텍스트와 메타데이터까지 함께 저장하고 꺼낸다.
- 같은 저장 구조라도 질문 벡터가 달라지면 상위 조각, 출처, 범주가 함께 바뀌므로, 벡터 데이터베이스는 단순 숫자 저장소가 아니라 `질문별 근거 반환 계층`이다.

이 예제에서 독자가 직접 해 볼 수 있는 조정은 다음과 같습니다.

- `query_vectors` 안의 한 질문 벡터를 설정 관련 값에 더 가깝게 바꿔 상위 문서가 어떻게 바뀌는지 보기
- `query_vectors`에 새로운 질문 벡터를 추가해 다른 범주가 top-1로 올라오는지 보기
- `records`에 같은 환불 주제 조각을 더 넣어 top-k 후보 묶음이 어떻게 바뀌는지 보기
- `metadata`에 날짜나 버전을 더 넣고, 검색 후 필터 기준으로 어떻게 쓸지 상상해 보기

## 이 예제를 저장 구조 관점으로 다시 보면

앞의 예제는 벡터 데이터베이스를 구현하는 코드가 아니라, `비슷한 벡터를 찾는다`는 말 뒤에 실제로는 원문과 메타데이터까지 함께 저장하고 다시 꺼내는 계층이 있다는 점을 보여 주는 최소 장면입니다. 여기서 읽어야 할 핵심은 임베딩 숫자만으로 끝나지 않고, 검색 이후 답변 단계에 다시 쓸 정보를 함께 보존해야 한다는 점입니다. 그리고 같은 저장 구조가 질문마다 다른 출처와 범주를 다시 돌려준다는 점도 함께 중요합니다.

## 여기까지를 한 줄로 묶으면

벡터 데이터베이스는 숫자 벡터만 모아 두는 곳이 아니라, 질문과 가까운 문서 조각을 다시 찾고 그 문장과 출처 정보를 함께 생성 단계로 넘겨주는 검색 저장 계층입니다.

임베딩과 벡터 검색 자체는 LLM 이전에도 중요했습니다. 하지만 생성형 AI 서비스가 널리 퍼지면서, 이 기술은 `문서를 찾아 답변에 붙이는 구조`의 핵심 계층으로 다시 주목받게 되었습니다.

커리큘럼 관점에서 이 절이 중요한 이유는 다음과 같습니다.

- 임베딩을 추상적 수학 개념에서 서비스 저장 구조로 연결하고
- 다음 절의 인덱스와 검색 품질 문제를 읽을 준비를 시키며
- 바로 앞의 P5-10.1, P5-10.2 RAG 흐름을 실제 저장 계층으로 다시 묶어 읽게 합니다.

여기서 잡은 관점은 다음 구간으로도 그대로 이어집니다.

- P5-11.2 인덱스와 검색 품질: 검색 속도와 후보 품질을 함께 읽는 기준
- P5-12.1 도구 사용, P5-13.1 에이전트 구조: 검색 기반 기능이 전체 시스템 안에서 어디에 놓이는지 보는 기준
- P6-5.1 문서 기반 RAG 챗봇 목표, P6-5.2 검색 품질과 답변 검증, P6-6.1 agent의 기본 구조: 검색 기반 기능과 도구 연결 기능을 실제 설계로 옮길 때 재사용하는 기준

## 다음 절과의 연결

여기까지 오면 다음 질문이 남습니다.

- 비슷한 벡터를 빠르게 찾는 일은 어떻게 가능한가?
- 왜 검색 속도와 검색 정확도 사이에 균형 문제가 생기는가?

이 질문은 P5-11.2 인덱스(index)와 검색 품질로 이어집니다.

## 이 절에서 기억할 관점

- 벡터 데이터베이스는 임베딩 벡터와 원문, 메타데이터를 함께 저장하고 검색하는 시스템입니다.
- RAG에서는 질문과 가까운 문서 조각을 빠르게 다시 찾는 검색 단계의 실무형 저장소 역할을 합니다.
- 일반 키워드 중심 저장소와 달리, 표현이 달라도 의미가 가까운 문서 조각을 후보로 올리는 유사도 검색에 강점을 둡니다.
- 하지만 문서 분할, 메타데이터, 임베딩 모델 선택 문제를 대신 해결하지는 않습니다.

## 체크리스트

- 벡터 데이터베이스를 입문 수준에서 설명할 수 있는가?
- 무엇이 저장되고 무엇이 반환되는지 말할 수 있는가?
- 왜 RAG에서 이 구조가 자주 등장하는지 설명할 수 있는가?
- 왜 다음 절에서 인덱스와 검색 품질을 봐야 하는지 말할 수 있는가?

## 출처와 참고 자료

- Jeffrey Pennington et al., 임베딩과 의미 벡터 관련 기초 자료, 확인 날짜: 2026-06-29.
- 관련 벡터 검색 및 ANN 교육 자료, 확인 날짜: 2026-06-29.
- OpenAI, 임베딩 및 검색 관련 공식 문서, 확인 날짜: 2026-06-29.
