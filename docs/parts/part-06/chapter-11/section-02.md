# P6-11.2 인덱스(index)와 검색 품질

> Section ID: `P6-11.2`
> Version: `v2026.07.12`

P6-11.1에서는 벡터 데이터베이스가 임베딩 벡터와 원문, 메타데이터를 함께 저장하고 검색 단계에서 실무형 저장소 역할을 한다는 점을 보았습니다. 이제 질문은 더 구체적이 됩니다.

비슷한 벡터를 빠르게 찾는 일은 왜 어렵고, 무엇을 포기하거나 조정해야 하는가?

이 절은 그 질문에 답합니다.

Part 6에서 `인덱스(index)`, `벡터 검색의 속도-정확도 균형`, `검색 구조가 품질에 미치는 영향`에 대한 첫 상세 설명은 이 절에서 잡습니다. 뒤 절에서는 현재 맥락에 필요한 최소 설명만 남기고, 검색 인덱스의 기본 뜻은 이 절과 개념사전을 기준으로 다시 연결합니다.

인덱스(index)는 검색 속도를 높이기 위한 구조이며, 벡터 검색에서는 보통 속도와 정확도 사이의 균형을 함께 고민하게 만든다.

## 이 절의 범위

이 절은 다음 질문에 답합니다.

- 왜 벡터를 하나씩 모두 비교하지 않는가?
- 인덱스는 검색에서 어떤 역할을 하는가?
- 검색 속도와 검색 품질은 왜 함께 조정해야 하는가?

이 절에서는 다음 내용을 깊게 다루지 않습니다.

- HNSW, IVF, PQ 수학 세부
- 특정 엔진 파라미터 튜닝
- 대규모 분산 검색 아키텍처

이 절은 인덱스를 `근사 검색을 위한 구조`로 읽는 데 집중하고, 이후 서비스 안에서 검색 외부 기능이 어떻게 확장되는지는 P6-12.1 도구 사용으로 이어집니다. 엔진별 수학과 분산 검색 아키텍처의 세부 구현은 현재 본편 범위 밖으로 둡니다.

이 절에서는 인덱스를 단순한 내부 기술명으로 넘기지 않고, `빠른 검색을 위해 근사(approximation)를 허용하는 구조`로 설명합니다.

지금 읽는 층위는 `검색 탐색 구조`입니다. 앞 절의 벡터 데이터베이스가 `무엇을 어떤 저장 구조에 담아 둘까`를 다뤘다면, 여기서는 `그 저장 구조 안에서 후보를 어떤 속도와 품질 균형으로 좁힐까`를 읽습니다. 바로 다음 P6-12.1에서는 질문이 다시 커져, `문서를 찾는 것`을 넘어 `무엇을 실제로 조회하거나 실행할까`로 이동합니다.

인덱스는 `후보를 빠르게 줄이는 구조`로 읽고, 그 다음에 어떤 층위가 더 붙는지까지 이어서 보면 됩니다.

| 지금 단계의 관점 | 바로 다음에 이어질 질문 | 뒤에서 본격적으로 다시 읽는 위치 |
| --- | --- | --- |
| 벡터 데이터베이스 | 검색 후보를 어떤 저장 구조에 다시 꺼내 쓸 것인가? | P6-11.1 |
| 인덱스(index) | 그 후보를 어떤 속도와 품질 균형으로 좁힐 것인가? | P6-11.2 |
| 도구 사용(tool use) | 문서 검색을 넘어서 무엇을 실제로 조회하거나 실행할 것인가? | P6-12.1, P6-12.2 |

이 절은 Part 6에서 `검색 인덱스(index)`를 대표로 설명하는 Section입니다. `빨리 찾는 내부 기술`이라는 인상을 `속도와 검색 품질을 함께 조정하는 탐색 구조`로 바꾸는 기준선을 여기서 세웁니다.

즉, 지금 장의 핵심은 `무엇을 저장할까`에서 `그 저장 구조를 어떤 속도와 품질로 탐색할까`로 관점이 바뀌는 데 있습니다. 바로 다음 장에서는 이 탐색을 넘어 무엇을 실제로 조회하거나 실행할지로 질문이 커집니다.

## 이 절의 목표

- 인덱스의 역할을 입문 수준에서 설명할 수 있습니다.
- 정확히 찾는 검색과 빠르게 찾는 검색의 차이를 말할 수 있습니다.
- 벡터 검색 품질을 속도와 분리해서 볼 수 없다는 점을 설명할 수 있습니다.
- 다음 장의 도구 사용과 서비스 구조 설명으로 이어질 준비를 할 수 있습니다.

## 이 절을 읽는 순서

이 절은 다음 순서로 읽으면 흐름이 잘 잡힙니다.

1. 먼저 `왜 모든 벡터를 다 비교하지 않나`와 `인덱스는 무엇을 하나`를 읽고, 인덱스가 전체 비교를 줄이기 위한 탐색 구조라는 점을 잡습니다.
2. 그다음 `왜 속도와 정확도가 함께 걸리나`, `검색 품질은 무엇으로 흔들리나`, `왜 RAG 품질과 직접 연결되나`를 읽으면서 속도와 후보 품질을 따로 떼어 볼 수 없다는 점을 확인합니다.
3. 마지막으로 사례와 Python 예제를 보면서, 실제 운영에서는 지연 시간만이 아니라 `top-k 포함률`, `top-1 정합률`, `버전 정합성`을 같이 봐야 한다는 점을 확인합니다.

## 왜 모든 벡터를 다 비교하지 않나

가장 단순한 방법은 질문 벡터와 저장된 모든 벡터를 하나씩 비교하는 것입니다. 하지만 문서 수가 많아지면 이 방식은 매우 느려질 수 있습니다.

예를 들어:

- 문서가 수백 개면 가능할 수 있지만
- 문서가 수십만, 수백만 개면
- 모든 벡터를 매번 다 비교하는 비용이 커집니다

그래서 실무에서는 `정확히 다 비교하는 방법` 대신 `가까울 것 같은 후보를 빠르게 좁히는 방법`이 중요해집니다. 이때 인덱스가 등장합니다.

## 인덱스는 무엇을 하나

인덱스는 다음처럼 이해할 수 있습니다.

`인덱스는 전체를 처음부터 끝까지 다 보지 않고, 가까울 가능성이 높은 후보를 더 빨리 찾도록 돕는 탐색 구조다.`

즉, 인덱스는 검색 속도를 높이기 위한 `길 찾기 구조`에 가깝습니다.

이 점은 일반 데이터베이스 인덱스와도 닮아 있지만, 벡터 검색에서는 `의미가 가까운 항목`을 찾기 위한 방식이라는 점이 다릅니다.

## 왜 속도와 정확도가 함께 걸리나

여기서 중요한 개념이 `근사 검색(approximate search)`입니다.

벡터 검색에서는 보통:

- 아주 정확하지만 느린 방식
- 조금 덜 정확할 수 있지만 빠른 방식

사이에서 균형을 잡습니다.

`벡터 검색 인덱스는 보통 가장 완벽한 답 하나를 항상 찾는 구조보다, 충분히 좋은 후보를 빠르게 찾는 구조에 가깝다.`

## 검색 품질은 무엇으로 흔들리나

검색 품질은 단순히 인덱스 종류만으로 정해지지 않습니다. 다음 요소가 함께 영향을 줍니다.

- 임베딩 품질
- 문서 조각(chunk) 크기
- 메타데이터 필터
- 인덱스 설정
- top-k 개수

즉, 검색 품질 문제는 `저장 구조`, `문서 준비`, `검색 전략`이 함께 만드는 문제입니다.

## 왜 RAG 품질과 직접 연결되나

RAG는 검색 결과를 생성에 붙입니다. 따라서 검색 품질이 낮으면 생성은 잘해도 시작점이 흔들립니다.

예를 들어:

- 관련 없는 문서를 가져오면 답이 엉뚱해지고
- 덜 중요한 문서가 먼저 오면 핵심이 빠질 수 있으며
- 오래된 문서가 섞이면 최신성 문제가 다시 생길 수 있습니다

즉, 벡터 검색 품질을 볼 때는 `얼마나 빨리 찾는가`보다 `정말 필요한 문서가 후보 안에 들어왔는가`를 먼저 확인해야 하고, 이것이 곧 RAG 답변 품질의 상한을 결정합니다.

## 아주 단순하게 그리면

```mermaid
--8<-- "assets/part-06/chapter-11/p6-c11-s02-diagram-01-ko.mmd"
```

이 도식의 핵심은 인덱스가 `답변 생성`을 직접 하는 것이 아니라, `검색 후보를 빠르게 좁히는 역할`을 한다는 점입니다.

## 사례 및 예시

### 사례 1. 사내 문서 검색 속도

사내 위키 문서가 수백 개일 때는 검색이 빨랐는데, 수만 개로 늘자 갑자기 느려졌다고 해 봅시다. 직관적으로는 `검색이 조금 늦네` 정도로만 느끼기 쉽습니다. 하지만 운영 단계에서는 답변 지연이 곧 사용자 이탈로 이어집니다. 예를 들어 휴가 규정 질문 하나에 후보 문서를 고르는 데 4초가 더 걸리면, 뒤 생성 단계가 같아도 사용자는 챗봇 전체가 느리다고 느끼게 됩니다. 이 시점부터 문제는 단순히 문서가 많아졌다는 사실이 아니라, 많은 문서 중 후보를 얼마나 빨리 줄일 수 있는가입니다. 여기서 바뀌는 점은 `문서 수가 늘었는가`를 보던 기준에서 `핵심 후보 압축 시간이 실제 대기 시간 안에 남는가`를 보는 기준으로 이동한다는 것입니다. 인덱스 구조와 검색 전략은 바로 이 후보 압축 속도를 바꾸는 핵심 장치가 됩니다. 그래서 이 사례에서 확인해야 할 결과는 문서 수가 늘어난 뒤에도 핵심 후보를 줄이는 시간이 실제 서비스 대기 시간 안에 남는가입니다.

### 사례 2. 매뉴얼 답변 품질

제품 매뉴얼에서 정확한 설정 문단 하나를 찾아야 하는데, 검색을 너무 빠르게 만들려고 근사 설정을 강하게 준다고 해 봅시다. 사람은 응답 시간이 빨라지면 검색이 더 좋아졌다고 느끼기 쉽습니다. 하지만 그러면 응답 시간은 줄어들 수 있어도, 정작 가장 중요한 문단이 후보에서 빠져 답변 품질이 바로 흔들릴 수 있습니다. 예를 들어 `자동 저장 끄기` 질문에 설정 개요 문단만 잡히고 실제 메뉴 경로 문단이 빠지면, 답변은 `설정에서 바꾸세요` 수준으로 끝나 실제 사용자는 여전히 버튼 위치를 찾지 못할 수 있습니다. 반대로 항상 가장 엄격한 검색만 쓰면 관련 문단은 잘 찾더라도 답이 너무 늦어집니다. 여기서 바뀌는 점은 `응답이 빨라졌는가`를 보던 기준에서 `핵심 문단이 후보에 남아 있는가`를 함께 보는 기준으로 이동한다는 것입니다. 즉, 운영자는 `빨라졌는가`만이 아니라 `빠르게 찾은 후보가 충분히 좋은가`를 함께 봐야 합니다. 그래서 이 사례에서 확인해야 할 결과는 응답 시간이 빨라져도 실제 핵심 문단이 후보에 남아 있는가입니다.

### 사례 3. 개발 문서 도우미

개발 문서 도우미가 비슷한 이름의 API 문서를 여러 개 가진 상태라고 해 봅시다. 사람은 최종 답만 보면 보통 `모델이 코드를 잘못 설명했다`고 먼저 느낍니다. 하지만 top-k 결과에 현재 버전 문서 대신 예전 버전 문서가 섞이면, 생성 단계는 그 후보를 바탕으로 꽤 자연스러운 답을 만들 수 있습니다. 예를 들어 2.x 버전 옵션을 묻는 질문에 1.x 문서가 후보 상단에 들어오면, 답변은 매끄러워도 바로 실행하면 에러가 나는 코드 예시가 나올 수 있습니다. 즉, 실제 시작점은 `후보 문서 묶음이 이미 어긋난 것`일 수 있습니다. 여기서 바뀌는 점은 `최종 답이 자연스러운가`를 보던 기준에서 `top-k 후보 안에 맞는 버전 문서가 들어왔는가`를 먼저 보는 기준으로 이동한다는 것입니다. 그래서 이 장면에서는 생성 평가와 별도로 검색 품질 평가가 필요합니다. 그래서 이 사례에서 확인해야 할 결과는 최종 답만 보기 전에 top-k 후보 안에 현재 버전 문서가 실제로 포함되어 있는가입니다.

세 사례를 속도·품질 균형 관점으로 다시 묶으면 다음과 같습니다.

| 상황 | 빨라 보이는 것만 보면 놓치는 것 | 함께 봐야 하는 검색 품질 기준 |
| --- | --- | --- |
| 사내 문서 검색 속도 | 전체 지연만 보고 후보 압축 실패를 놓침 | 핵심 후보를 서비스 시간 안에 남기는가 |
| 매뉴얼 답변 품질 | 응답 속도가 빨라져도 핵심 절차 문단이 빠질 수 있음 | 핵심 문단이 top-k 안에 남는가 |
| 개발 문서 도우미 | 자연스러운 최종 답 때문에 버전 후보 오류를 놓침 | 현재 버전 문서가 top-k 안에 포함되는가 |

같은 내용을 검색 타협 구조로 다시 보면 다음처럼 읽을 수 있습니다.

```mermaid
--8<-- "assets/part-06/chapter-11/p6-c11-s02-diagram-02-ko.mmd"
```

핵심은 `빠르다`와 `좋다`가 자동으로 같은 뜻이 아니라는 점입니다.

## 연습 및 예제

이번 예제의 목표는 인덱스 엔진 구현이 아니라, `더 빠른 검색 설정`과 `더 좋은 후보 회수`가 실제로 충돌할 수 있다는 점을 눈으로 확인하는 것입니다. 특히 한 질문만 보는 대신, 여러 질문에서 `top-k 안에 정답 문서가 남는 비율`, `top-1이 바로 맞는 비율`, `버전 정합성`을 함께 봐야 운영 판단이 더 정확해진다는 점을 확인하겠습니다.

문제 상황:

- 개발 문서 검색에서 현재 버전 문서가 꼭 top-k 안에 들어와야 함
- 빠른 설정은 지연 시간은 줄이지만 후보 일부를 놓칠 수 있음
- 느린 설정은 더 오래 걸리지만 중요한 후보를 더 잘 회수할 수 있음

입력:

- 여러 개의 질문
- 빠른 검색 설정과 엄격한 검색 설정의 후보 목록

출력:

- 질문별 지연 시간
- 질문별 top-k 후보
- 현재 버전 문서가 실제로 포함되었는지 여부
- 설정별 top-k 포함률과 top-1 정합률

먼저 이 예제에서 함께 볼 점검 항목은 다음과 같습니다.

| 점검 항목 | 왜 필요한가 |
| --- | --- |
| `target_in_top_k` | 생성 단계가 참고할 후보 안에 정답이 살아 있는지 확인 |
| `rank_of_target` | 정답이 너무 아래에 있어 생성이 놓치지 않는지 확인 |
| `top1_is_target` | 가장 먼저 붙는 문서가 맞는지 확인 |
| `top1_version_ok` | 비슷한 이름의 구버전 문서가 앞서 오지 않는지 확인 |

문제 상황:

- 검색기를 평가할 때는 단순 속도보다 정답 문서가 상위 후보 안에 실제로 들어오는지가 더 중요할 수 있다

입력(input):

위에 정리한 질문별 목표 문서와 fast/accurate 검색 결과를 사용합니다.

확인할 개념:

- 검색 품질 평가는 속도만이 아니라 정답 문서가 상위 후보 안에 실제로 들어오는지를 먼저 봐야 한다

```python
queries = [
    {
        "question": "2.x 버전에서 request timeout 옵션은 어디에 넣나요?",
        "target_doc": "sdk_v2_request_timeout",
        "fast": {
            "latency_ms": 24,
            "candidates": [
                "sdk_v1_timeout_guide",
                "sdk_v1_retry_notes",
                "sdk_general_networking",
            ],
        },
        "strict": {
            "latency_ms": 88,
            "candidates": [
                "sdk_v2_request_timeout",
                "sdk_v2_retry_and_backoff",
                "sdk_v1_timeout_guide",
            ],
        },
    },
    {
        "question": "2.x에서 retry backoff 기본값은 어디에 설명돼 있나요?",
        "target_doc": "sdk_v2_retry_and_backoff",
        "fast": {
            "latency_ms": 22,
            "candidates": [
                "sdk_v1_retry_notes",
                "sdk_general_networking",
                "sdk_v2_request_timeout",
            ],
        },
        "strict": {
            "latency_ms": 81,
            "candidates": [
                "sdk_v2_retry_and_backoff",
                "sdk_v2_request_timeout",
                "sdk_v1_retry_notes",
            ],
        },
    },
    {
        "question": "2.x 인증 토큰 갱신 흐름 문서는 어디를 봐야 하나요?",
        "target_doc": "sdk_v2_auth_refresh_flow",
        "fast": {
            "latency_ms": 25,
            "candidates": [
                "sdk_v1_auth_overview",
                "sdk_general_security",
                "sdk_v2_auth_refresh_flow",
            ],
        },
        "strict": {
            "latency_ms": 86,
            "candidates": [
                "sdk_v2_auth_refresh_flow",
                "sdk_general_security",
                "sdk_v1_auth_overview",
            ],
        },
    },
]

def inspect_search(result, target_doc):
    top1 = result["candidates"][0]
    return {
        "latency_ms": result["latency_ms"],
        "top_k": result["candidates"],
        "target_in_top_k": target_doc in result["candidates"],
        "rank_of_target": (
            result["candidates"].index(target_doc) + 1
            if target_doc in result["candidates"]
            else None
        ),
        "top1_is_target": top1 == target_doc,
        "top1_version_ok": top1.startswith("sdk_v2_"),
    }

def summarize_mode(queries, mode_name):
    reports = []
    hit_count = 0
    top1_hit_count = 0
    version_ok_count = 0
    total_latency = 0
    for item in queries:
        inspected = inspect_search(item[mode_name], item["target_doc"])
        reports.append((item["question"], inspected))
        hit_count += int(inspected["target_in_top_k"])
        top1_hit_count += int(inspected["top1_is_target"])
        version_ok_count += int(inspected["top1_version_ok"])
        total_latency += inspected["latency_ms"]
    hit_rate = round(hit_count / len(queries), 3)
    top1_hit_rate = round(top1_hit_count / len(queries), 3)
    version_ok_rate = round(version_ok_count / len(queries), 3)
    avg_latency = round(total_latency / len(queries), 1)
    return reports, hit_rate, top1_hit_rate, version_ok_rate, avg_latency

fast_reports, fast_hit_rate, fast_top1_hit_rate, fast_version_ok_rate, fast_avg_latency = summarize_mode(queries, "fast")
strict_reports, strict_hit_rate, strict_top1_hit_rate, strict_version_ok_rate, strict_avg_latency = summarize_mode(queries, "strict")

print("[fast search]")
for question, report in fast_reports:
    print("question =", question)
    print(report)
print("fast_hit_rate =", fast_hit_rate)
print("fast_top1_hit_rate =", fast_top1_hit_rate)
print("fast_top1_version_ok_rate =", fast_version_ok_rate)
print("fast_avg_latency_ms =", fast_avg_latency)
print("fast_latency_per_hit =", round(fast_avg_latency / fast_hit_rate, 1) if fast_hit_rate else None)

print("[strict search]")
for question, report in strict_reports:
    print("question =", question)
    print(report)
print("strict_hit_rate =", strict_hit_rate)
print("strict_top1_hit_rate =", strict_top1_hit_rate)
print("strict_top1_version_ok_rate =", strict_version_ok_rate)
print("strict_avg_latency_ms =", strict_avg_latency)
print("strict_latency_per_hit =", round(strict_avg_latency / strict_hit_rate, 1) if strict_hit_rate else None)
```

실행 결과 예시는 다음처럼 읽을 수 있습니다.

```text
[fast search]
question = 2.x 버전에서 request timeout 옵션은 어디에 넣나요?
{'latency_ms': 24, 'top_k': ['sdk_v1_timeout_guide', 'sdk_v1_retry_notes', 'sdk_general_networking'], 'target_in_top_k': False, 'rank_of_target': None, 'top1_is_target': False, 'top1_version_ok': False}
question = 2.x에서 retry backoff 기본값은 어디에 설명돼 있나요?
{'latency_ms': 22, 'top_k': ['sdk_v1_retry_notes', 'sdk_general_networking', 'sdk_v2_request_timeout'], 'target_in_top_k': False, 'rank_of_target': None, 'top1_is_target': False, 'top1_version_ok': False}
question = 2.x 인증 토큰 갱신 흐름 문서는 어디를 봐야 하나요?
{'latency_ms': 25, 'top_k': ['sdk_v1_auth_overview', 'sdk_general_security', 'sdk_v2_auth_refresh_flow'], 'target_in_top_k': True, 'rank_of_target': 3, 'top1_is_target': False, 'top1_version_ok': False}
fast_hit_rate = 0.333
fast_top1_hit_rate = 0.0
fast_top1_version_ok_rate = 0.0
fast_avg_latency_ms = 23.7
fast_latency_per_hit = 71.2
[strict search]
question = 2.x 버전에서 request timeout 옵션은 어디에 넣나요?
{'latency_ms': 88, 'top_k': ['sdk_v2_request_timeout', 'sdk_v2_retry_and_backoff', 'sdk_v1_timeout_guide'], 'target_in_top_k': True, 'rank_of_target': 1, 'top1_is_target': True, 'top1_version_ok': True}
question = 2.x에서 retry backoff 기본값은 어디에 설명돼 있나요?
{'latency_ms': 81, 'top_k': ['sdk_v2_retry_and_backoff', 'sdk_v2_request_timeout', 'sdk_v1_retry_notes'], 'target_in_top_k': True, 'rank_of_target': 1, 'top1_is_target': True, 'top1_version_ok': True}
question = 2.x 인증 토큰 갱신 흐름 문서는 어디를 봐야 하나요?
{'latency_ms': 86, 'top_k': ['sdk_v2_auth_refresh_flow', 'sdk_general_security', 'sdk_v1_auth_overview'], 'target_in_top_k': True, 'rank_of_target': 1, 'top1_is_target': True, 'top1_version_ok': True}
strict_hit_rate = 1.0
strict_top1_hit_rate = 1.0
strict_top1_version_ok_rate = 1.0
strict_avg_latency_ms = 85.0
strict_latency_per_hit = 85.0
```

이 예제에서 먼저 봐야 할 것은 `fast_avg_latency_ms = 23.7`이 매우 좋아 보여도 `fast_top1_hit_rate = 0.0`, `fast_top1_version_ok_rate = 0.0`이라는 점입니다. 즉, 빠른 설정은 지연 시간은 줄였지만, 가장 먼저 붙는 문서가 모두 구버전이어서 생성 단계 출발점이 이미 흔들립니다. 반대로 strict 설정은 느리지만 top-k 포함률, top-1 정합률, 버전 정합률이 모두 1.0입니다.

그래서 이 예제에서 확인해야 할 결과는 두 가지입니다.

- 더 빠른 검색 설정이 항상 더 좋은 검색을 뜻하지 않으며, 지연 시간과 함께 `정말 필요한 문서가 top-k 안에 들어왔는가`, `top-1이 맞는가`를 같이 읽어야 한다.
- 단일 질문에서는 우연히 통과해 보일 수 있어도, 여러 질문을 묶어 보면 `hit_rate`, `top1_hit_rate`, `version_ok_rate` 차이가 더 분명하게 드러난다.

이 예제에서 독자가 직접 해 볼 수 있는 조정은 다음과 같습니다.

- `target_doc`를 다른 문서로 바꿔 어떤 질문에서 빠른 설정이 더 큰 손실을 내는지 보기
- `queries[0]["fast"]["candidates"]`를 바꿔 비슷하지만 틀린 버전 문서가 얼마나 위험한지 확인하기
- `inspect_search`에 `recall_like_score`나 `top2_version_mix` 같은 항목을 추가해 자체 품질 지표를 넓혀 보기

속도와 품질 충돌을 운영 판단으로 다시 읽으면, 단일 지표만 보고 원인을 단정하면 안 된다는 점이 더 분명해집니다.

| 먼저 보인 신호 | 바로 검색 인덱스 층에서 확인할 것 | 왜 이것부터 봐야 하는가 |
| --- | --- | --- |
| 응답은 빨라졌는데 답변이 자주 빗나감 | `target_in_top_k`, `top1_hit_rate` | 생성 모델보다 먼저 검색 후보 자체가 흔들렸는지 확인해야 합니다. |
| top-k 안에는 정답이 들어오는데 최종 답이 틀림 | `rank_of_target`, chunk 구성, 생성 단계 사용 방식 | 검색은 통과했지만 생성이 핵심 후보를 제대로 쓰지 못했을 수 있습니다. |
| 비슷한 이름의 구버전 문서가 자주 섞임 | `top1_version_ok`, 메타데이터 필터, 버전 태그 | 속도 문제가 아니라 후보 정합성과 필터 설계 문제일 수 있습니다. |
| 특정 질문군에서만 검색이 약함 | 질문 유형별 hit rate, chunk 크기, 임베딩 표현 | 인덱스 전체보다 데이터 준비나 표현 문제가 더 큰 원인일 수 있습니다. |

## 이 예제를 검색 타협 관점으로 다시 보면

앞의 예제는 실제 인덱스를 구현하는 코드가 아니라, `더 빠른 검색`과 `더 나은 후보 회수`가 같은 목표가 아니라는 점을 가장 작은 비교표로 보여 주는 장면입니다. 예를 들어 `latency_ms`만 보고 빠른 설정을 택했는데 정작 핵심 문단이 후보에서 빠지면, 뒤 생성 단계는 매끄러워도 답변 품질은 바로 떨어질 수 있습니다. 여기서 중요한 것은 숫자 크기 자체보다, 검색에서는 속도와 품질을 함께 보고 어느 쪽을 더 우선할지 결정해야 한다는 점입니다. 또 운영자는 단일 성공 사례보다 여러 질문에서의 `top-k 포함률`을 함께 봐야, 우연한 성공과 실제 안정성을 구분할 수 있습니다.

## 여기까지를 한 줄로 묶으면

벡터 검색 인덱스는 검색을 빠르게 만들기 위한 구조이지만, 실제 운영에서는 지연 시간만이 아니라 `정답 후보가 top-k 안에 살아 있는가`를 함께 보지 않으면 좋은 설정을 고를 수 없습니다.

벡터 검색이 널리 쓰이면서, 검색 문제는 다시 `자료구조와 알고리즘`의 감각으로 돌아왔습니다. 하지만 LLM 서비스 문맥에서는 이것이 단순한 검색 엔진 문제가 아니라, 생성 품질과 사용자 경험에 직접 연결된다는 점이 더 중요합니다.

커리큘럼 관점에서 이 절이 중요한 이유는 다음과 같습니다.

- 벡터 데이터베이스를 단순 저장소가 아니라 탐색 구조와 함께 읽게 하고
- 이후 평가 장에서 검색 지표를 왜 별도로 봐야 하는지 준비시키며
- 서비스 구조에서 속도, 비용, 품질이 함께 얽힌다는 관점을 강화하기 때문입니다

## 체크리스트

| 상황 | 먼저 떠올릴 관점 | 왜 중요한가 |
| --- | --- | --- |
| 검색을 더 빠르게 만들었는데 답이 나빠진 것처럼 보일 때 | 속도와 품질의 균형 문제라는 점 | 후보를 빨리 줄이는 방식이 정답 후보를 놓치면 전체 응답 품질도 함께 떨어질 수 있습니다. |
| 모델이 아니라 검색 설정이 원인인지 의심해야 할 때 | 정답 문서가 top-k 안에 들어왔는지 먼저 확인해야 한다는 점 | 생성 모델이 잘못 답한 것처럼 보여도 실제로는 검색 단계에서 근거 문서를 회수하지 못했을 수 있습니다. |
| `빠른 검색`을 곧바로 `좋은 검색`으로 받아들이려 할 때 | 근사 탐색은 빠르지만 정답 후보를 일부 놓칠 수 있다는 점 | 인덱스 선택과 파라미터 조정은 속도뿐 아니라 회수 품질 관점에서 함께 판단해야 합니다. |

- 인덱스는 검색 속도를 높이기 위한 탐색 구조입니다.
- 벡터 검색에서는 속도와 정확도 사이의 균형을 함께 고민합니다.
- 검색 품질은 인덱스뿐 아니라 임베딩, chunking, 메타데이터 전략에도 영향을 받습니다.
- RAG 답변 품질은 검색 품질과 직접 연결됩니다.

- 인덱스를 `탐색 속도를 높이는 구조`로만이 아니라 `속도와 품질을 함께 좌우하는 탐색 구조`로 설명할 수 있어야 합니다.
- `top-k 안에 정답이 포함되는가`와 `1등 결과가 바로 정답인가`를 서로 다른 품질 지표로 구분할 수 있어야 합니다.
- 다음 장은 검색 저장 구조 설명의 연장이 아니라, 이렇게 줄인 후보를 바탕으로 실제 도구 호출과 외부 실행으로 넘어가는 단계라는 점을 잡고 있어야 합니다.

## 출처와 참고 자료

- Yu A. Malkov, D. A. Yashunin, [Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs](https://arxiv.org/abs/1603.09320){: target="_blank" rel="noopener noreferrer" }, arXiv, 2016, 확인 날짜: 2026-07-05.
- Jeff Johnson, Matthijs Douze, Herve Jegou, [Billion-scale similarity search with GPUs](https://arxiv.org/abs/1702.08734){: target="_blank" rel="noopener noreferrer" }, arXiv, 2017, 확인 날짜: 2026-07-05.
- OpenAI, [Vector embeddings](https://developers.openai.com/api/docs/guides/embeddings){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, 확인 날짜: 2026-07-05.
