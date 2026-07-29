# P6-3.2 정답이 아니라 후보를 만드는 가까운 벡터

> Section ID: `P6-3.2`
> Version: `v2026.07.26`

P6-3.1에서는 임베딩(embedding)을 토큰이나 문장을 벡터(vector)로 바꾸는 표현 방식이라고 설명했습니다. 이제 벡터를 만들었다면, 그다음에는 이 벡터를 어떻게 읽을지가 문제입니다.

임베딩 벡터가 만들어졌다면, 두 표현이 가깝다는 말은 실제로 무엇을 뜻하는가? 의미와 거리라는 표현은, 임베딩 공간에서 비슷한 쓰임의 표현을 서로 가까운 후보로 비교하려는 계산 관점을 뜻합니다.

여기서 가장 먼저 갈라야 할 것은 `가까운 후보`와 `맞는 근거`입니다. 거리(distance)와 유사도(similarity)는 후보를 먼저 좁히는 비교 기준이지, 그 후보가 곧 정답이거나 최신 근거라는 보장은 아닙니다.

## 벡터 후보 비교의 기준

의미와 거리를 처음 읽을 때는 아래 질문을 붙잡습니다.

- 벡터 공간에서 `가깝다`는 것은 어떤 뜻인가?
- 거리(distance)와 유사도(similarity)는 어떻게 다르게 읽을 수 있는가?
- 왜 가까운 벡터가 곧 정답이나 진실을 뜻하는 것은 아닌가?
- 이 관점이 검색, 추천, RAG와 어떻게 이어지는가?

의미와 거리는 `임베딩 벡터를 어떤 비교 기준으로 가까운 후보로 읽을 것인가`라는 질문으로 먼저 잡습니다. 임베딩 학습 흐름, 빠른 후보 탐색, 검색 시스템 안의 실제 사용은 이후 절에서 넓어지지만, 지금 필요한 기준은 검색과 추천의 기본 비교 감각입니다.

수식을 외우기보다, `임베딩 공간의 거리`를 실제 비교와 검색의 언어로 읽습니다.

P6-3.1의 임베딩 설명이 `표현을 벡터로 바꾸는가`를 다뤘다면, 여기서는 그렇게 만든 벡터를 어떤 기준으로 서로 가깝거나 멀다고 읽을지 다룹니다. 이 비교 기준은 이후 Transformer 내부 계산, RAG, 벡터 데이터베이스의 검색 후보 선정으로 질문이 더 커집니다.

따라서 핵심은 `벡터를 만들었다`에서 끝내지 않고, 그 벡터를 어떤 기준으로 비교해야 하는지까지 읽는 데 있습니다.

| 지금 단계의 초점 | 이어질 질문 | 다시 넓게 읽는 위치 |
| --- | --- | --- |
| 임베딩(embedding) | 텍스트나 문장을 어떤 벡터 표현으로 바꿀 것인가? | P6-3.1 |
| 의미와 거리 | 그 벡터들을 어떤 기준으로 가까운 후보로 비교할 것인가? | P6-3.2 |
| 검색과 RAG | 가까운 후보를 실제 문서 검색과 생성 결합에 어떻게 쓸 것인가? | P6-11.1, P6-11.2, P6-12.1, P6-12.2 |
| 추천과 후속 선택 | 가까운 후보를 어떤 맥락 기준으로 다시 걸러 최종 선택할 것인가? | P6-3.2의 사례와 서비스 맥락 전반 |

즉, 지금 장의 핵심은 `벡터를 만든다`에서 `그 벡터를 어떤 후보 비교 기준으로 읽는다`로 넘어가는 데 있습니다. 이 기준이 잡혀야 뒤에서 RAG와 벡터 검색을 읽을 때 가까운 문서 후보와 최종 답 근거를 섞지 않습니다.

## 가까운 후보와 맞는 근거의 구분

이 구분은 P6-3.1의 임베딩을 `벡터를 만든다`에서 `벡터를 비교한다`로 확장하고, 검색과 외부 지식 연결을 이해하는 핵심 기초가 됩니다. 이 절을 읽은 뒤에는 거리(distance)와 유사도(similarity)를 후보 비교 기준으로 설명하고, 가까운 벡터가 `비슷한 후보일 수 있음`과 `곧 정답은 아님`을 함께 말할 수 있어야 합니다.

## `가깝다`는 말은 무엇을 뜻하나

임베딩 벡터는 여러 숫자로 이루어진 표현입니다. 이 벡터들 사이에는 수학적으로 거리나 유사도를 정의할 수 있습니다.

다음처럼 이해할 수 있습니다.

- 거리가 짧다 -> 벡터가 서로 가깝다
- 유사도가 높다 -> 벡터가 더 비슷한 방향이나 위치를 가진다

이때 중요한 것은, 이 비교가 `문자열 비교`가 아니라 `학습된 표현 비교`라는 점입니다.

즉:

- 같은 단어가 없어도 비슷한 표현이 가까워질 수 있고
- 같은 단어가 있어도 맥락이 다르면 멀어질 수 있습니다

## 거리와 유사도는 어떻게 다른가

입문 단계에서는 둘을 너무 엄격하게 구분할 필요는 없습니다. 다만 읽는 방향은 다를 수 있습니다.

| 표현 | 독자 직관 |
| --- | --- |
| 거리(distance) | 얼마나 떨어져 있는가 |
| 유사도(similarity) | 얼마나 비슷한가 |

둘 다 `비교 기준`이라는 점은 같습니다.

실무에서는 검색 시스템이나 임베딩 모델에 따라 어떤 비교 함수를 쓰는지가 달라질 수 있습니다. 하지만 독자가 먼저 가져가야 할 것은 수식 이름이 아니라, 질문과 문서·상품·문장이 `무엇을 기준으로 서로 가깝다고 읽히는가`를 보는 관점입니다.

## 가까운 벡터는 왜 유용한가

가까운 벡터를 찾으면 다음과 같은 일이 가능해집니다.

- 비슷한 질문 찾기
- 관련 문서 후보 찾기
- 비슷한 상품 또는 콘텐츠 찾기
- 중복되거나 거의 같은 표현 찾기

즉, 임베딩 공간의 거리 개념은 Part 6 뒤쪽의 RAG, 벡터 데이터베이스(vector database), 추천(recommendation) 같은 주제로 자연스럽게 이어집니다.

## 가까운 벡터가 곧 정답은 아닌 이유

이 점을 먼저 잡아야 `가깝다`는 판단과 `맞다` 또는 `최신이다`라는 판단을 섞지 않게 됩니다.

`가까운 벡터`는 보통 `관련 가능성이 높은 후보`를 뜻하지, 정답이나 진실을 뜻하지는 않습니다.

다음과 같은 경우를 생각할 수 있습니다.

- 표현은 비슷하지만 사실이 틀린 문서
- 질문과 표면적으로 비슷하지만 필요한 맥락은 다른 문서
- 오래되어 최신성이 없는 문서
- 전문 분야에서는 일반 임베딩이 충분히 구분하지 못하는 문서

따라서 유사도 검색이나 RAG에서는 `가까운 후보를 찾는 단계`와 `그 후보가 실제로 맞는 근거인지 확인하는 단계`를 반드시 분리해서 봐야 합니다.

## 아주 단순하게 그리면

```mermaid
--8<-- "assets/part-06/chapter-03/p6-c03-s02-similarity-flow-ko.mmd"
```

이 도식에서 확인해야 할 결과는 `가까운 것 찾기`와 `그것을 최종 답으로 정리하기`가 서로 다른 단계이며, 검색이 맞아도 답변 정리는 별도 판단을 거친다는 점입니다.

도식을 읽을 때는 먼저 `1차 후보`와 `최종 확정`을 분리해서 보면 됩니다.

| 먼저 나눠 볼 것 | 왜 필요한가 |
| --- | --- |
| 가까운 후보를 고르는 단계 | 거리와 유사도가 하는 일을 먼저 고정하기 위해서입니다. |
| 후보를 열어 확인하는 단계 | 가까움이 곧 정답이 아니라는 점을 붙잡기 위해서입니다. |
| 최신성·예외 조건을 다시 보는 단계 | 뒤의 RAG와 검색 품질 설명으로 자연스럽게 이어지기 때문입니다. |

## 사례 및 예시

아래 도식은 이 절의 세 사례를 `무엇이 같은가`보다 `무엇을 먼저 가까운 후보로 올릴 것인가`라는 공통 질문으로 다시 묶은 것입니다.

```mermaid
--8<-- "assets/part-06/chapter-03/p6-c03-s02-similarity-use-cases-ko.mmd"
```

이 도식에서 확인해야 할 점은 과업이 달라도 `먼저 가까운 후보를 고른다`는 단계가 공통으로 들어간다는 것입니다. 다만 그 후보가 곧 정답이라는 뜻은 아니므로, 이후 검토와 정리 단계가 따로 필요합니다.

### 사례 1. 비슷한 질문 찾기

사용자가 도움말 창에 `프롬프트만으로 거짓말을 막을 수 있나요?`라고 묻는 장면을 떠올려 보겠습니다. 질문 속 단어가 문서 제목에 그대로 있어야 찾기 쉽다고 생각하면 `거짓말`이나 `막다` 같은 단어를 먼저 찾게 됩니다. 하지만 실제 지식베이스에는 `프롬프트의 한계와 사실성 보강 방법`처럼 더 기술적인 표현으로 정리된 문서만 있을 수 있습니다. 이때 키워드만 맞추면 관련 문서를 놓치고, 사용자는 `문서가 없나 보다`라고 오해할 수 있습니다.

여기서 바뀌는 기준은 단어 일치 여부를 넘어서, 두 문장이 실제로 같은 문제 장면을 가리키는지까지 비교하는 쪽입니다. 유사도 검색은 `거짓말을 막는다`와 `사실성을 보강한다`를 꽤 가까운 문제로 보고 그 문서를 후보로 올립니다.

여기서 바로잡아야 할 오해는 `같은 단어가 없으면 같은 질문도 아니다`라는 감각입니다. 이 사례에서 확인해야 할 결과는 질문 단어가 그대로 없더라도 같은 문제를 다루는 문서가 실제 후보로 올라오는가, 그리고 후보만 봐도 왜 그 문서가 같은 장면으로 묶였는지 설명할 수 있는가입니다.

이 사례에서 닫을 판단은 단순합니다. 거리 비교는 같은 문제 장면을 먼저 찾아 주지만, 후보 본문과 근거 확인은 여전히 별도 단계입니다.

### 사례 2. 문서 검색

사내 정책 문서 수백 개 중에서 `출장비 정산 마감일이 언제인가요?`를 묻는 상황을 생각해 보겠습니다. 제목을 먼저 기준으로 삼으면 `출장비`, `정산`, `마감일`이 제목에 모두 들어 있어야 바로 답이 나올 것처럼 느껴집니다. 하지만 실제 문서 구조에서는 제목이 `출장 운영 가이드`이고, 본문 중간 표에만 `매월 5영업일 이내 제출`과 `해외 출장 예외`가 들어 있을 수 있습니다. 제목만 맞는 문서 하나를 열어도 정작 핵심 문단을 놓치면 답은 여전히 늦거나 틀릴 수 있습니다.

여기서 바뀌는 기준은 문서 제목 하나를 고르는 것에서 끝나지 않고, 질문과 가장 가까운 문단 몇 개를 먼저 모으는 쪽으로 탐색 단위가 내려가는 데 있습니다. 유사도 검색은 질문과 가까운 문단 몇 개를 후보로 모으고, 그다음 LLM이 그 문단을 읽어 자연어 답변을 정리하게 만듭니다.

여기서 바로잡아야 할 오해는 `제목이 맞으면 문서도 곧 답이다`라는 기대입니다. 이 사례에서 확인해야 할 결과는 제목만 맞는 문서 하나가 아니라, 실제 마감일이 적힌 핵심 문단이 후보에 포함되는가, 그리고 예외 조항이 있는 문단도 함께 올라오는가입니다.

이 사례에서 닫을 판단은 제목 일치와 답 근거 확정을 분리하는 일입니다. 가까운 문단 후보를 먼저 모은 뒤, 실제 마감일과 예외 조항이 들어 있는지 다시 열어 확인해야 합니다.

### 사례 3. 추천 시스템

사용자가 입문용 선형대수 강의를 끝까지 봤고, 다음 강의를 추천해야 하는 상황을 생각해 보겠습니다. `입문용` 태그가 같으면 비슷한 강의일 것이라고 먼저 묶기 쉽습니다. 하지만 실제로는 하나는 칠판 수식 설명 위주이고, 다른 하나는 NumPy 실습 위주라서 학습 리듬이 꽤 다를 수 있습니다. 예를 들어 수식 설명 영상을 끝까지 본 사용자가 바로 코드 실습 중심 강의로 넘어가면 중도 이탈이 늘 수 있습니다. 즉, 같은 태그는 비슷한 소비 경험을 보장하지 않습니다.

여기서 바뀌는 기준은 태그 하나를 맞추는 것보다, 실제로 어떤 강의를 어떤 흐름으로 소비했는지를 함께 보는 쪽입니다. 시청 행동과 강의 특징을 함께 반영한 벡터 공간에서 가까운 항목을 찾으면, 단순 태그보다 실제 학습 흐름이 비슷한 후보를 더 자연스럽게 고를 수 있습니다.

여기서 바로잡아야 할 오해는 `라벨이 같으면 경험도 같다`는 감각입니다. 이 사례에서 확인해야 할 결과는 같은 태그보다 실제 학습 리듬이 비슷한 후보가 더 앞쪽에 모이는가, 그리고 그 후보 선택이 다음 학습 이탈 가능성까지 줄이는가입니다.

이 사례에서 닫을 판단도 같습니다. 가까운 추천 후보는 최종 선택이 아니라 후속 필터의 입력이므로, 난이도, 목표, 최신성 같은 조건을 다시 봐야 합니다.

세 사례를 후보 선정 관점으로 다시 묶으면 다음과 같습니다.

| 상황 | 사람 눈에 먼저 보이는 것 | 유사도 검색이 먼저 올리려는 후보 |
| --- | --- | --- |
| 비슷한 질문 찾기 | 같은 단어가 있는 질문 | 같은 문제를 다루는 질문 |
| 문서 검색 | 제목이 비슷한 문서 | 핵심 답이 들어 있는 문단 |
| 추천 시스템 | 같은 태그를 단 항목 | 실제 소비 흐름이 비슷한 항목 |

## 후보 선정과 정답 확정 구분하기

이 절을 읽은 뒤에는 아직 거리 함수를 자세히 몰라도, 아래처럼 `가까운 후보를 고르는 일`과 `최종 정답을 확정하는 일`을 먼저 갈라보는 예제를 따라갈 수 있습니다.

| 지금 보이는 결과 | 먼저 떠올리기 쉬운 오해 | 의미와 거리 관점에서 먼저 바꿔 물을 질문 |
| --- | --- | --- |
| 어떤 문서가 distance 1등이다 | 그 문서가 곧 최종 정답이라고 느끼기 쉽다 | 이 값은 1차 후보 순서인가, 최종 답 확정인가 |
| 두 후보가 모두 가깝게 나온다 | 1등만 보면 되고 나머지는 버려도 된다고 느끼기 쉽다 | top-k 후보를 실제 본문과 최신성 기준으로 다시 열어 봤는가 |
| 질문과 비슷한 문서가 올라왔다 | 비슷하면 사실도 맞겠지라고 느끼기 쉽다 | 관련성 외에 최신성, 예외, 사실 일치를 따로 확인했는가 |

이 표에서 중요한 것은 거리 점수를 외우는 일이 아닙니다. 먼저 필요한 것은 `후보 선정`과 `정답 확정`을 다른 단계로 읽는 일입니다.

여기서 자주 섞이는 단계도 바로 이 두 가지입니다.

- 가까운 후보를 찾으면 이미 답이 끝났다고 느끼기 쉽습니다.
- top-1 문서가 올라오면 나머지 후보는 의미 없다고 느끼기 쉽습니다.
- 관련성이 높으면 사실성도 자동으로 따라온다고 느끼기 쉽습니다.

하지만 뒤의 RAG, 검색 품질, 운영 제약 절을 읽으려면 `무엇을 먼저 후보로 올렸는가`와 `무엇을 최종 근거로 확정했는가`를 분리해서 볼 수 있어야 합니다.

## 연습 및 예제

이 연습의 목표는 `가까운 후보를 먼저 고른다`는 감각과 `가까움이 곧 정답은 아니다`라는 점을 구분해 보는 것입니다. 먼저 작은 수치 예시로 판단 자리를 잡고, 이어서 같은 구조를 두 가지 검색 신호로 확인합니다.

질문은 `출장비 정산 마감일이 언제인가요?`이고, 검색 시스템이 다음 세 후보를 올렸다고 가정합니다.

| 순위 | 후보 | 거리 | 업데이트 | 메모 |
| ---: | --- | ---: | --- | --- |
| 1 | `doc_A` | `0.02` | `2026-03` | 지난 분기 정책 |
| 2 | `doc_C` | `0.05` | `2026-06` | 최신 예외 조항 포함 |
| 3 | `doc_B` | `1.0` | `2025-12` | 다른 주제 |

이 표에서 거리값은 `질문과 가까운 후보를 먼저 세우는 신호`이고, 업데이트와 메모는 `최종 근거로 쓸 수 있는지 다시 확인해야 하는 신호`입니다.

여기서 `doc_A`가 거리 기준 1등이라는 사실은 `먼저 열어 볼 후보`를 뜻합니다. 그러나 `doc_A`는 지난 분기 정책이고, `doc_C`는 거리 기준 2등이어도 최신 예외 조항을 담고 있습니다. 따라서 거리 순위는 후보 선정 단계의 출력이고, 최종 근거 확정은 본문과 메타데이터를 다시 확인한 뒤에야 가능합니다.

## 검색 후보 판단에서 갈리는 것

이 절의 코드는 같은 문서 후보를 두 방식으로 세워 봅니다. 먼저 `TfidfVectorizer`로 문자 겹침에 가까운 재현 가능한 기준선을 만들고, 이어서 Ollama embedding 모델로 실제 임베딩 기반 후보 순위를 확인합니다. 두 출력의 순위는 달라질 수 있습니다. 그러나 읽어야 할 중심은 같습니다. `가까운 후보`, `검토할 후보 묶음`, `최종 근거`를 서로 다른 단계로 가르는 것입니다.

### 기본 예제. top-k 후보와 최종 근거 후보 분리하기

이 예제는 실제 임베딩 모델을 대신해 `TfidfVectorizer`를 작은 검색 모델처럼 사용합니다. 핵심은 검색 모델 종류가 아니라, 가까운 후보 순서와 최종 근거 후보가 다를 수 있음을 출력으로 확인하는 것입니다. 직접 조작할 값은 `query`, `top_k`, `min_similarity`입니다.

```python
# 가까운 후보 top-k와 최종 근거 후보를 분리해서 보는 예제입니다.
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

documents = [
    {
        "doc_id": "doc_A",
        "title": "출장비 정산 정책",
        "text": "출장비 정산 마감일과 제출 마감일은 매월 5영업일입니다. 지난 분기 기준입니다.",
        "current_version": False,
        "contains_exception": False,
    },
    {
        "doc_id": "doc_C",
        "title": "출장비 정산 최신 예외",
        "text": "해외 출장 예외 조건과 긴급 승인 예외 조건은 최신 공지 링크를 확인합니다.",
        "current_version": True,
        "contains_exception": True,
    },
    {
        "doc_id": "doc_B",
        "title": "회의실 예약",
        "text": "회의실 예약은 사내 캘린더에서 신청하고 장비 대여 여부를 함께 기록합니다.",
        "current_version": True,
        "contains_exception": False,
    },
]

# 조작 변수: query, top_k, min_similarity를 바꾸면 검토할 후보 묶음이 달라집니다.
query = "출장비 정산 마감일과 예외 조건은 무엇인가요?"
top_k = 3
min_similarity = 0.10

vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))
document_vectors = vectorizer.fit_transform([doc["text"] for doc in documents])
query_vector = vectorizer.transform([query])
similarities = cosine_similarity(query_vector, document_vectors)[0]

ranked = sorted(
    zip(documents, similarities),
    key=lambda item: item[1],
    reverse=True,
)[:top_k]

print("retrieved candidates:")
for rank, (doc, score) in enumerate(ranked, start=1):
    print(
        rank,
        doc["doc_id"],
        "similarity=", round(float(score), 3),
        "current=", doc["current_version"],
        "exception=", doc["contains_exception"],
    )

grounding_candidates = [
    doc["doc_id"]
    for doc, score in ranked
    if score >= min_similarity and doc["current_version"] and doc["contains_exception"]
]

print("grounding_candidates =", grounding_candidates)
```

실행 결과 예시는 다음처럼 읽을 수 있습니다.

```text
retrieved candidates:
1 doc_A similarity= 0.459 current= False exception= False
2 doc_C similarity= 0.408 current= True exception= True
3 doc_B similarity= 0.046 current= True exception= False
grounding_candidates = ['doc_C']
```

이 출력에서 `doc_A`는 유사도 기준 1등이지만 지난 분기 기준이고 예외 조건도 없습니다. 반대로 `doc_C`는 2등이지만 최신 문서이고 예외 조건을 담고 있으므로 최종 근거 후보가 됩니다. 즉, 가까운 후보를 먼저 찾는 일과 답변 근거로 확정하는 일은 서로 다른 단계입니다.

### 선택 예제. 로컬 임베딩 모델로 같은 후보 비교하기

Ollama가 설치되어 있고 `nomic-embed-text` 모델을 내려받은 환경이라면 같은 구조를 실제 임베딩 모델로도 확인할 수 있습니다. 이 선택 예제의 목적은 모델 성능을 비교하는 데 있지 않습니다. 문자열 겹침 기반 벡터화가 아니라, embedding 모델이 만든 벡터를 사용해 후보를 세워도 `가까운 후보`와 `최종 근거 후보`를 다시 분리해서 봐야 한다는 점을 확인하는 데 있습니다.

먼저 로컬 터미널에서 모델을 준비합니다.

```bash
ollama pull nomic-embed-text
```

그다음 아래 코드를 실행합니다. 이 코드는 Python 패키지 `ollama`를 사용합니다. 코드가 `Ollama embedding model is not ready.`를 출력하면 Ollama 서버가 꺼져 있거나, `nomic-embed-text` 모델이 아직 준비되지 않은 상태입니다.

```python
# Ollama의 로컬 embedding 모델로 top-k 후보와 최종 근거 후보를 다시 비교하는 선택 예제입니다.
from math import sqrt

import ollama

documents = [
    {
        "doc_id": "doc_A",
        "title": "출장비 정산 정책",
        "text": "출장비 정산 마감일과 제출 마감일은 매월 5영업일입니다. 지난 분기 기준입니다.",
        "current_version": False,
        "contains_exception": False,
    },
    {
        "doc_id": "doc_C",
        "title": "출장비 정산 최신 예외",
        "text": "해외 출장 예외 조건과 긴급 승인 예외 조건은 최신 공지 링크를 확인합니다.",
        "current_version": True,
        "contains_exception": True,
    },
    {
        "doc_id": "doc_B",
        "title": "회의실 예약",
        "text": "회의실 예약은 사내 캘린더에서 신청하고 장비 대여 여부를 함께 기록합니다.",
        "current_version": True,
        "contains_exception": False,
    },
]

# 조작 변수: query, top_k, min_similarity를 바꾸면 검색 후보와 근거 후보가 달라질 수 있습니다.
query = "출장비 정산 마감일과 예외 조건은 무엇인가요?"
top_k = 3
min_similarity = 0.25
model_name = "nomic-embed-text"

def embed(text: str) -> list[float]:
    return ollama.embed(model=model_name, input=text).embeddings[0]

def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sqrt(sum(x * x for x in a))
    norm_b = sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)

try:
    query_vector = embed(query)
    document_vectors = [embed(doc["text"]) for doc in documents]
except Exception as error:
    print("Ollama embedding model is not ready.")
    print(type(error).__name__, error)
    raise SystemExit

ranked = sorted(
    zip(documents, document_vectors),
    key=lambda item: cosine_similarity(query_vector, item[1]),
    reverse=True,
)[:top_k]

print("embedding candidates:")
for rank, (doc, vector) in enumerate(ranked, start=1):
    score = cosine_similarity(query_vector, vector)
    print(
        rank,
        doc["doc_id"],
        "similarity=", round(float(score), 3),
        "current=", doc["current_version"],
        "exception=", doc["contains_exception"],
    )

grounding_candidates = [
    doc["doc_id"]
    for doc, vector in ranked
    if (
        cosine_similarity(query_vector, vector) >= min_similarity
        and doc["current_version"]
        and doc["contains_exception"]
    )
]

print("grounding_candidates =", grounding_candidates)
```

실행 결과 예시는 다음처럼 나왔습니다.

```text
embedding candidates:
1 doc_C similarity= 0.85 current= True exception= True
2 doc_A similarity= 0.833 current= False exception= False
3 doc_B similarity= 0.813 current= True exception= False
grounding_candidates = ['doc_C']
```

이 선택 예제에서는 실제 embedding 모델이 `doc_C`를 1등으로 올렸습니다. 그러나 이것만으로 embedding 모델이 최종 답을 맞혔다고 읽으면 안 됩니다. `doc_A`와 `doc_B`도 높은 유사도로 함께 올라왔기 때문입니다. 짧은 문서 후보가 적게 들어 있는 예제에서는 넓은 의미의 업무 문서, 신청 절차, 정책 문장이 서로 가깝게 잡힐 수 있습니다. 실제 embedding 모델을 써도 가까움은 `후보 선정 신호`이지, 최신성과 예외 조건을 자동으로 보장하는 판정값이 아닙니다.

### 연습 1. 두 검색 신호의 순위 차이 읽기

두 실행 결과를 나란히 보면 같은 질문에서도 1등 후보가 달라집니다.

| 실행 방식 | 1등 후보 | 같이 읽어야 할 신호 |
| --- | --- | --- |
| `TfidfVectorizer` 기준선 | `doc_A` | 마감일 표현이 많이 겹치지만 `current_version=False`이고 예외 조건이 없다 |
| Ollama embedding 모델 | `doc_C` | 예외 조건 문서가 먼저 올라오지만 다른 후보도 높은 유사도로 함께 올라온다 |

먼저 스스로 답해 봅니다.

- `TfidfVectorizer`에서는 왜 `doc_A`가 먼저 올라왔는가?
- Ollama embedding 모델에서는 왜 `doc_C`가 먼저 올라올 수 있는가?
- 두 출력이 달라도 최종 근거를 확정하기 전에 공통으로 확인해야 할 것은 무엇인가?

해설: `TfidfVectorizer`는 문자 조각의 겹침을 강하게 봅니다. 그래서 `출장비`, `정산`, `마감일` 표현이 많이 겹치는 `doc_A`가 먼저 올라옵니다. Ollama embedding 모델은 문장 전체의 의미 관계를 더 넓게 보므로 `예외 조건`을 담은 `doc_C`를 먼저 올릴 수 있습니다. 하지만 두 방식 모두 최종 근거 확정 전에는 문서 본문, 최신성, 예외 조건을 다시 확인해야 합니다.

### 연습 2. 높은 유사도를 바로 믿지 않기

Ollama embedding 출력만 보면 세 후보의 유사도가 모두 높게 보입니다.

| 후보 | 유사도 | 현재 버전 | 예외 조건 |
| --- | ---: | --- | --- |
| `doc_C` | `0.850` | 예 | 예 |
| `doc_A` | `0.833` | 아니요 | 아니요 |
| `doc_B` | `0.813` | 예 | 아니요 |

먼저 스스로 답해 봅니다.

- `doc_B`의 유사도가 높게 나왔다고 최종 근거로 써도 되는가?
- `doc_A`의 유사도가 높게 나왔다고 지난 분기 정책을 답에 넣어도 되는가?
- 이 출력에서 최종 근거 후보를 `doc_C`로 좁히는 이유는 무엇인가?

해설: `doc_B`는 현재 버전이어도 질문의 핵심인 출장비 정산 예외 조건을 담지 않습니다. `doc_A`는 질문과 가까워도 지난 분기 정책입니다. 따라서 세 후보가 모두 가까워 보여도 최종 근거 후보는 `current_version=True`이고 `contains_exception=True`인 `doc_C`로 좁혀야 합니다. 이때 유사도는 후보를 버리거나 믿는 최종 판정이 아니라, 무엇을 먼저 열어 볼지 정하는 순서입니다.

### 연습 3. 다음 조치 고르기

다음 장면마다 `문서 본문 검토`, `최신성 확인`, `추가 검색`, `근거 후보 확정` 중 무엇을 먼저 해야 하는지 고르고 이유를 한 문장으로 적어 보세요.

| 장면 | 먼저 고를 조치 |
| --- | --- |
| top-1 문서는 질문과 가장 가깝지만 작년 정책만 담고 있다 | ? |
| top-3 후보는 모두 비슷하게 가까운데, 하나만 최신 공지 링크를 포함하고 있다 | ? |
| top-k 후보 전체가 질문과 거리가 멀고 핵심 단어도 거의 겹치지 않는다 | ? |
| top-1 후보는 그럴듯하지만 예외 조항 언급이 전혀 없다 | ? |

해설: 첫 장면은 최신성 확인이 먼저입니다. 가까운 후보라도 작년 정책만 담고 있으면 최종 근거가 될 수 없습니다. 둘째 장면은 문서 본문 검토와 최신성 확인을 함께 해야 합니다. top-k가 모두 가깝다면 거리 순서만 보지 말고 실제 공지 링크와 근거 문단을 열어 봐야 합니다. 셋째 장면은 추가 검색이 먼저입니다. 후보 전체가 멀고 핵심 단어도 겹치지 않으면 현재 검색 질의나 인덱스가 맞지 않을 수 있습니다. 넷째 장면은 문서 본문 검토가 먼저입니다. top-1 후보가 그럴듯해도 예외 조항이 없으면 답을 확정하기 어렵습니다. 네 장면 모두 핵심은 `가까운 후보 선정`과 `최종 근거 확정`을 분리해서 읽는 것입니다.

이 예시는 `가까운 벡터를 찾는다`는 말이 실제 서비스에서는 `답을 바로 확정한다`가 아니라 `먼저 검토할 후보를 순서대로 좁힌다`는 뜻임을 보여 줍니다. TF-IDF 기준선과 Ollama embedding 모델은 서로 다른 순위를 만들 수 있지만, 둘 다 최종 근거를 대신 확정해 주지는 않습니다. 그래서 이후 검색, RAG, 추천 절을 읽을 때도 핵심은 거리 계산 그 자체보다 `무엇을 후보로 올리고, 그다음 어떤 단계로 검토하는가`에 있습니다.

임베딩과 거리 개념은 통계적 언어 모델 이후의 표현 학습(representation learning) 흐름과 깊게 연결됩니다. 단어를 one-hot처럼 분리된 기호로만 다루는 대신, 벡터 공간 안에서 관계를 표현하려는 시도가 이후 검색과 생성 서비스 전반으로 확장되었습니다.

LLM 시대에는 이 관점이 더 중요해졌습니다.

- 모델 내부에서는 attention 계산으로 이어지고
- 서비스 바깥에서는 임베딩 검색과 RAG로 이어지기 때문입니다

## 체크리스트

- 거리와 유사도를 `후보 비교 기준`이라는 말로 설명할 수 있어야 합니다.
- 가장 가까운 벡터와 최종 정답을 분리해서 생각할 수 있어야 합니다.
- `비슷한 질문과 문서가 왜 함께 올라오는가`와 `가장 가까운 후보가 왜 항상 정답은 아닌가`를 각각 설명할 수 있어야 합니다.

## 출처와 참고 자료

- Tomas Mikolov et al., [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781){: target="_blank" rel="noopener noreferrer" }, arXiv, 2013, 확인 날짜: 2026-07-19. dense word vector와 유사 문맥 표현의 배경 근거로 사용했다.
- Tomas Mikolov et al., [Distributed Representations of Words and Phrases and their Compositionality](https://arxiv.org/abs/1310.4546){: target="_blank" rel="noopener noreferrer" }, arXiv, 2013, 확인 날짜: 2026-07-19. 단어와 구를 벡터 공간에서 비교 가능한 표현으로 다루는 배경 근거로 사용했다.
- Nils Reimers, Iryna Gurevych, [Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://arxiv.org/abs/1908.10084){: target="_blank" rel="noopener noreferrer" }, arXiv, 2019, 확인 날짜: 2026-07-19. 문장 임베딩을 cosine similarity로 비교해 semantic similarity search에 사용하는 설명의 근거로 사용했다.
- Daniel Jurafsky, James H. Martin, [Speech and Language Processing, 3rd ed. draft](https://web.stanford.edu/~jurafsky/slp3/){: target="_blank" rel="noopener noreferrer" }, online manuscript released January 6, 2026, 확인 날짜: 2026-07-19. 임베딩과 유사도 비교 설명의 일반 NLP 배경 근거로 사용했다.
- Ollama, [nomic-embed-text](https://registry.ollama.com/library/nomic-embed-text){: target="_blank" rel="noopener noreferrer" }, Ollama model registry, 확인 날짜: 2026-07-24. 로컬 embedding 모델을 사용한 선택 실행 예제의 모델 설명과 호출 방식 확인에 사용했다.
