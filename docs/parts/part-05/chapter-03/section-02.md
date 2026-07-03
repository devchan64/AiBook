# P5-3.2 attention과 context window

P5-3.1에서는 Transformer를 LLM 기준으로 다시 읽으며, 토큰이 임베딩을 거쳐 Transformer 블록을 통과한 뒤 다음 토큰 점수로 이어지는 흐름을 보았습니다. 이제 바로 다음 제약을 봐야 합니다.

Transformer가 이전 토큰을 참고할 수 있다면, 실제로는 어디까지 참고할 수 있는가?

이 절은 그 질문에 답합니다.

context window는 모델이 한 번의 계산 안에서 참고할 수 있는 토큰 범위이며, attention은 그 범위 안에서 어떤 토큰이 더 중요한지 계산하는 구조다.

## 이 절의 범위

이 절은 다음 질문에 답합니다.

- attention과 context window는 어떤 관계인가?
- 왜 `모든 이전 토큰을 본다`는 말에도 실제 한계가 붙는가?
- context window는 왜 비용, 품질, 서비스 구조에 영향을 주는가?

이 절에서는 다음 내용을 깊게 다루지 않습니다.

- RoPE, ALiBi 같은 위치 표현 세부 비교
- KV cache 최적화
- 장문맥 전용 아키텍처의 세부 구현

이 절은 `입력 범위 제약 축`으로 읽으면 충분합니다.

| 지금 이 절에서 읽는 것 | 뒤 Chapter나 뒤 Part로 넘기는 것 |
| --- | --- |
| 모델이 한 번의 계산에서 어디까지 입력으로 볼 수 있는가 | 그 제약을 실제 retrieval, 요약, 운영 정책으로 어떻게 풀어내는가 |
| attention이 그 범위 안에서만 중요도를 계산한다는 점 | 긴 문맥 전용 아키텍처와 서빙 최적화가 어떤 구현 차이를 만드는가 |

이 항목들은 같은 장의 P5-3.3 보충학습에서 `왜 긴 문맥을 다루기 어렵고 어떤 보강 장치가 붙는가`라는 수준으로 다시 설명합니다. 긴 문맥이 실제 서비스 구조와 RAG 설계에 미치는 영향은 P5-10.1, P5-10.2, P5-16.1에서도 다시 이어집니다.

이 절에서는 `문맥을 다 본다`는 표현을 너무 크게 해석하지 않고, 실제 서비스에서 왜 문맥 길이 관리가 중요한지 설명합니다.

## 이 절의 목표

- context window를 `모델이 한 번에 참고할 수 있는 토큰 범위`로 설명할 수 있습니다.
- attention이 그 범위 안에서 관련도를 계산한다는 점을 설명할 수 있습니다.
- context window가 길이 제한, 비용, 지연 시간과 왜 연결되는지 말할 수 있습니다.
- 이후 RAG와 긴 문서 처리 설명으로 자연스럽게 넘어갈 수 있습니다.

## 이 절을 읽는 순서

이 절은 다음 순서로 읽으면 충분합니다.

1. 먼저 context window가 `어디까지 입력으로 들어올 수 있는가`를 제한한다는 점을 봅니다.
2. 그 다음 attention이 그 제한된 범위 안에서만 관련도를 계산한다는 점을 구분합니다.
3. 이어서 왜 이 길이 제한이 실제 서비스에서 `무엇을 남길 것인가`라는 선택 문제로 바뀌는지 읽습니다.
4. 마지막에 왜 이 문제가 RAG, 대화 요약, 코드 어시스턴트 문맥 선택으로 이어지는지 연결합니다.

## context window는 무엇을 뜻하나

context window는 모델이 한 번의 입력으로 받을 수 있는 토큰 길이 범위입니다.

예를 들어 어떤 모델이 8k tokens를 지원한다면, 시스템 메시지, 사용자 입력, 대화 기록, 검색 결과, 도구 출력까지 합쳐 그 범위 안에 들어와야 합니다.

다음처럼 이해하면 좋습니다.

`문맥을 많이 넣을수록 좋을 것 같지만, 실제로는 토큰 길이 제한 안에서 무엇을 남기고 무엇을 줄일지 결정해야 한다.`

이 지점에서 중요한 것은 `많이 참고한다`와 `무한히 참고한다`를 구분하는 일입니다. LLM은 입력 안에 들어온 토큰을 넓게 활용할 수 있지만, 그 입력 자체는 항상 한정되어 있습니다.

## attention은 범위 안의 관련도를 계산한다

이제 attention을 이 제약 위에 올려 보면 관계가 더 분명해집니다. attention은 토큰 간 관련도를 계산하는 구조이지만, 그 계산은 무한한 과거 전체가 아니라 현재 입력에 들어와 있는 토큰 범위 안에서만 이루어집니다.

즉:

- context window는 `무엇까지 볼 수 있는가`를 제한하고
- attention은 그 안에서 `무엇을 더 중요하게 볼 것인가`를 계산합니다

이 둘을 섞으면 안 됩니다.

더 안전한 설명은 다음과 같습니다.

`context window는 입력 범위 제한에 가깝고, attention은 그 안의 선택 규칙에 가깝다.`

## 왜 이 제약이 바로 서비스 문제로 이어지나

context window는 단순 숫자 제한이 아닙니다. 실제로는 입력을 어떻게 구성할지 결정하게 만드는 제약이며, 곧바로 다음 문제를 만듭니다.

- 긴 문서를 그대로 다 넣지 못할 수 있다
- 오래된 대화 기록을 계속 누적하면 앞부분이 밀릴 수 있다
- 검색 결과를 너무 많이 넣으면 비용이 커지고 핵심이 흐려질 수 있다
- 도구 출력이 길면 정작 중요한 사용자 질문이 뒤로 밀릴 수 있다

즉, context window는 모델 성능뿐 아니라 `서비스 설계`의 문제이기도 합니다.

## 긴 문맥이 항상 더 좋은가

긴 context window는 분명 유리한 점이 있습니다.

- 더 많은 배경 문서를 넣을 수 있고
- 긴 코드 파일이나 긴 계약서를 한 번에 다루기 쉬워지며
- 대화 맥락을 오래 유지하기 쉬워집니다

하지만 항상 무조건 더 좋은 것은 아닙니다.

- 불필요한 문맥도 함께 늘어날 수 있고
- 관련 없는 정보가 attention을 분산시킬 수 있으며
- 비용과 지연 시간(latency)이 커질 수 있습니다

따라서 실무에서는 단순히 `길면 좋다`보다 `중요한 문맥을 어떻게 잘 고를 것인가`가 더 중요해집니다.

## 그래서 실제 설계 질문은 무엇인가

여기까지를 한 줄로 묶으면, 실제 설계 질문은 `얼마나 길게 넣을 수 있는가` 하나로 끝나지 않습니다.

- 무엇을 먼저 남길 것인가
- 무엇은 그대로 두고 무엇은 요약할 것인가
- 무엇이 현재 질문과 직접 연결되는가

즉, context window 문제는 길이 경쟁이 아니라 `입력 선택과 압축의 기준`을 세우는 문제이기도 합니다. 이 관점을 잡아야 뒤에서 RAG, 대화 요약, 에이전트 문맥 관리가 왜 모두 비슷한 설계 문제로 묶이는지 자연스럽게 읽을 수 있습니다.

## 그래서 왜 RAG와 연결되는가

RAG(retrieval-augmented generation)는 바로 이 문제와 연결됩니다.

긴 문서 전체를 넣는 대신:

- 관련 문서 조각만 검색하고
- 필요한 부분만 잘라 넣어
- 제한된 context window 안에서 근거를 더 효율적으로 사용하려는 구조이기 때문입니다

즉, context window의 존재는 RAG가 왜 필요한지 설명하는 중요한 배경입니다.

여기서 읽어야 할 핵심은 `attention이 강하니 문서를 전부 넣으면 된다`가 아니라, `윈도우 안에 남길 근거를 먼저 고르고 그 안에서 attention이 작동한다`는 순서입니다.

## 아주 단순하게 그리면

```mermaid
flowchart TD
  A["all possible prior information"]
  B["selected tokens inside context window"]
  C["attention over selected tokens"]
  D["next-token prediction"]

  A --> B
  B --> C
  C --> D
```

이 도식의 핵심은 다음입니다.

- 전체 정보가 다 들어오는 것이 아니라
- 먼저 윈도우 안에 들어온 정보가 있고
- attention은 그 안에서 계산된다는 점입니다

## 사례로 다시 묶어 보기

아래 도식은 이 절의 세 사례를 `얼마나 많이 넣는가`보다 `제한된 창 안에 무엇을 우선 남길 것인가`라는 공통 질문으로 다시 묶은 것입니다.

```mermaid
flowchart TD
  A["same context-window question"]
  B["long report<br/>which sections must survive?"]
  C["code assistant<br/>which files are directly relevant now?"]
  D["chatbot memory<br/>which state must remain visible?"]

  A --> B
  A --> C
  A --> D
```

이 도식에서 확인해야 할 점은 과업이 달라도 핵심 제약이 같다는 것입니다. 모두 `전부 넣는가`보다 `중요한 문맥을 먼저 남기는가`가 더 중요하며, attention은 그 뒤에 남은 범위 안에서만 계산됩니다.

### 사례 1. 긴 문서 요약

사용자가 100페이지 보고서를 한 번에 넣고 `핵심만 다섯 줄로 정리해 달라`고 요청할 수 있습니다. 사람은 처음에 `긴 문서를 다 넣으면 더 정확하겠지`라고 생각하기 쉽습니다. 하지만 문맥 윈도우가 한정되어 있으면 모델은 문서 전체를 그대로 다 넣어 읽지 못합니다. 예를 들어 앞부분의 배경 설명과 뒤쪽의 결론을 모두 남기고 싶어도, 중간 표와 부록까지 전부 넣으면 정작 `최종 권고안`이 적힌 마지막 절이 잘려 나갈 수 있습니다. 그러면 요약은 그럴듯해 보여도 가장 중요한 결론 한 줄이 빠질 수 있습니다. 여기서 바뀌는 점은 `많이 넣으면 더 정확한가`를 보던 기준에서 `제한된 범위 안에서 핵심 절이 실제로 보존되는가`를 보는 기준으로 이동한다는 것입니다. 그래서 중요한 절을 먼저 고르거나, 장별로 나누어 요약한 뒤 다시 합치는 설계가 필요해집니다. 그래서 이 사례에서 확인해야 할 결과는 문서를 많이 넣는 것보다 핵심 절을 고른 쪽이 실제 결론 보존에 더 유리한가입니다.

### 사례 2. 코드 도우미

큰 코드베이스에서 버그를 고칠 때 사용자는 `저장소 전체를 보고 원인을 찾아 달라`고 기대할 수 있습니다. 사람도 처음에는 전체를 다 보여 주면 더 잘 고칠 것 같다고 느낄 수 있습니다. 하지만 실제로는 모든 파일을 한 번에 넣기 어렵기 때문에, 현재 파일, 관련 함수, 최근 에러 로그, 실패한 테스트 결과를 우선 선택해야 합니다. 예를 들어 로그인 오류를 고치는데 디자인 자산 파일과 오래된 문서까지 함께 넣는다면, 정작 인증 미들웨어와 세션 설정 파일이 잘리고 핵심 원인 후보를 놓칠 수 있습니다. 즉, 문맥 관리란 단순 길이 제한이 아니라 `무엇을 먼저 보여 줄지`를 정하는 선택 문제이기도 합니다. 여기서 바뀌는 점은 `전체를 더 많이 보여 주는가`를 보던 기준에서 `현재 오류와 직접 연결된 문맥이 우선 남는가`를 보는 기준으로 이동한다는 것입니다. 그래서 이 사례에서 확인해야 할 결과는 정보량을 늘리는 것보다 현재 질문과 직접 연결된 파일을 남긴 쪽이 실제 원인 후보를 더 잘 보존하는가입니다.

### 사례 3. 대화형 챗봇

고객 지원 챗봇에서 대화가 길어지면 초반의 주문번호, 정책 설명, 사용자의 추가 질문이 계속 쌓입니다. 사람은 일단 다 남겨 두면 가장 안전하다고 느끼기 쉽지만, 이 기록을 전부 그대로 유지하면 문맥이 금방 길어지고 반대로 너무 많이 지우면 중요한 조건을 잃어버릴 수 있습니다. 예를 들어 초반에 나온 주문번호와 환불 예외 조건은 끝까지 중요하지만, 중간의 반복 인사나 이미 해결된 질문은 그대로 유지할 필요가 적을 수 있습니다. 반대로 주문번호까지 요약 과정에서 빠뜨리면, 뒤 답변이 맞는 정책을 말해도 다른 주문 건을 기준으로 설명하는 오류가 생길 수 있습니다. 여기서 바뀌는 점은 `대화를 많이 남기는가`를 보던 기준에서 `핵심 상태가 실제로 오래 유지되는가`를 보는 기준으로 이동한다는 것입니다. 그래서 어떤 메시지는 그대로 남기고, 어떤 메시지는 짧게 요약해 보존할지 결정하는 일이 실제 설계의 핵심이 됩니다. 그래서 이 사례에서 확인해야 할 결과는 반복 인사보다 주문번호와 예외 조건 같은 핵심 상태가 실제로 더 오래 보존되는가입니다.

세 사례를 context window 관리 관점으로 다시 묶으면 다음과 같습니다.

| 상황 | 많이 넣는다고 바로 좋아지지 않는 것 | 제한 안에서 먼저 남겨야 하는 것 |
| --- | --- | --- |
| 긴 문서 요약 | 부록과 주변 설명까지 전부 유지하는 것 | 최종 권고안과 핵심 절 |
| 코드 도우미 | 저장소 전체를 한 번에 넣는 것 | 현재 오류와 직접 연결된 파일·로그 |
| 대화형 챗봇 | 모든 대화 기록을 그대로 보존하는 것 | 주문번호, 예외 조건 같은 핵심 상태 |

## 실행 가능한 Python 예제로 확인하기

이번 예제의 목표는 `길이 제한이 있을 때 무엇을 우선 남길 것인가`를 더 분명하게 보는 것입니다. 이번에는 단순 개수 제한이 아니라 `토큰 예산`을 두고, 입력 순서대로 그냥 넣는 방식과 중요도 기준으로 다시 고르는 방식을 비교하겠습니다. 여기에 `현재 질문과 얼마나 직접 연결되는가`를 흉내 내는 간단한 relevance 점수도 붙여, context window 안에 무엇이 남느냐가 attention이 실제로 볼 수 있는 단서와 어떻게 연결되는지도 함께 보겠습니다.

입력:

- 여러 개의 문맥 항목
- 각 항목의 토큰 길이와 우선순위
- 최대 토큰 예산

출력:

- 입력 순서대로 넣었을 때 남는 항목
- 중요도 기준으로 다시 골랐을 때 남는 항목
- 두 방식에서 탈락한 항목과 총 사용 토큰
- 두 방식에서 핵심 상태가 실제로 얼마나 보존되었는지
- 두 방식에서 질문과 직접 연결된 항목이 얼마나 남는지
- 선택된 항목 안에서의 간단한 relevance 순위

문제 상황:

- context budget이 부족할 때는 입력 순서대로 자를지, 중요도 기준으로 다시 고를지에 따라 남는 정보가 달라진다

입력(input):

위에 정리한 context item 목록과 토큰 예산을 사용합니다.

확인할 개념:

- context budget이 부족할 때는 어떤 정보를 남기고 버리느냐에 따라 최종 답변에 쓸 수 있는 근거가 달라진다

```python
context_items = [
    {
        "name": "system instruction",
        "tokens": 18,
        "priority": 100,
        "content": "Follow policy and explain the cause clearly.",
    },
    {
        "name": "older chat history",
        "tokens": 30,
        "priority": 40,
        "content": "Earlier small talk and unrelated setup questions.",
    },
    {
        "name": "repeated greeting",
        "tokens": 8,
        "priority": 5,
        "content": "Hello again thank you hello again.",
    },
    {
        "name": "user question",
        "tokens": 12,
        "priority": 95,
        "content": "Why did login fail after the deploy?",
    },
    {
        "name": "current error log",
        "tokens": 22,
        "priority": 90,
        "content": "Login failed because session token signature mismatch after deploy.",
    },
    {
        "name": "related function code",
        "tokens": 20,
        "priority": 88,
        "content": "verify_session_token compares signature and rejects mismatch.",
    },
]

token_budget = 60
must_keep = {"system instruction", "user question", "current error log"}
query_keywords = {"login", "fail", "deploy", "token", "signature", "mismatch"}


def select_in_original_order(items, budget):
    selected = []
    used = 0
    for item in items:
        if used + item["tokens"] <= budget:
            selected.append(item)
            used += item["tokens"]
    dropped = [item for item in items if item not in selected]
    return selected, dropped, used


def select_by_priority(items, budget):
    ranked = sorted(items, key=lambda item: item["priority"], reverse=True)
    selected = []
    used = 0
    for item in ranked:
        if used + item["tokens"] <= budget:
            selected.append(item)
            used += item["tokens"]
    dropped = [item for item in ranked if item not in selected]
    return selected, dropped, used


naive_selected, naive_dropped, naive_used = select_in_original_order(context_items, token_budget)
priority_selected, priority_dropped, priority_used = select_by_priority(context_items, token_budget)


def coverage(selected, must_keep_names):
    selected_names = {item["name"] for item in selected}
    kept = sorted(selected_names & must_keep_names)
    missing = sorted(must_keep_names - selected_names)
    return kept, missing


def relevance_ranking(selected, keywords):
    scored = []
    for item in selected:
        words = set(item["content"].lower().replace(".", "").split())
        score = len(words & keywords)
        scored.append((score, item["name"]))
    return sorted(scored, reverse=True)

print("[naive original-order selection]")
for item in naive_selected:
    print("-", item["name"], "| tokens =", item["tokens"], "| priority =", item["priority"])
print("used_tokens =", naive_used)
print("dropped =", [item["name"] for item in naive_dropped])
naive_kept, naive_missing = coverage(naive_selected, must_keep)
print("must_keep_kept =", naive_kept)
print("must_keep_missing =", naive_missing)
print("relevance_ranking =", relevance_ranking(naive_selected, query_keywords))
print()

print("[priority-based selection]")
for item in priority_selected:
    print("-", item["name"], "| tokens =", item["tokens"], "| priority =", item["priority"])
print("used_tokens =", priority_used)
print("dropped =", [item["name"] for item in priority_dropped])
priority_kept, priority_missing = coverage(priority_selected, must_keep)
print("must_keep_kept =", priority_kept)
print("must_keep_missing =", priority_missing)
print("relevance_ranking =", relevance_ranking(priority_selected, query_keywords))
```

실행 결과 예시는 다음처럼 읽을 수 있습니다.

```text
[naive original-order selection]
- system instruction | tokens = 18 | priority = 100
- older chat history | tokens = 30 | priority = 40
- repeated greeting | tokens = 8 | priority = 5
used_tokens = 56
dropped = ['user question', 'current error log', 'related function code']
must_keep_kept = ['system instruction']
must_keep_missing = ['current error log', 'user question']
relevance_ranking = [(0, 'system instruction'), (0, 'repeated greeting'), (0, 'older chat history')]

[priority-based selection]
- system instruction | tokens = 18 | priority = 100
- user question | tokens = 12 | priority = 95
- current error log | tokens = 22 | priority = 90
- repeated greeting | tokens = 8 | priority = 5
used_tokens = 60
dropped = ['related function code', 'older chat history']
must_keep_kept = ['current error log', 'system instruction', 'user question']
must_keep_missing = []
relevance_ranking = [(5, 'current error log'), (3, 'user question'), (0, 'system instruction'), (0, 'repeated greeting')]
```

이 예제에서 읽어야 할 핵심은 다음입니다.

- 같은 토큰 예산이어도 입력 순서대로 그냥 넣으면 `older chat history`와 `repeated greeting`이 자리를 차지해, 정작 `user question`과 `current error log`가 잘릴 수 있습니다.
- 중요도 기준으로 다시 고르면 현재 질문과 직접 연결된 항목이 먼저 살아남고, 오래된 기록이나 반복 인사는 뒤로 밀립니다.
- naive 선택에서는 attention이 볼 수 있는 범위 안에 질문·오류 단서 자체가 없으므로, relevance 순위를 매겨도 전부 0점에 가깝습니다.
- priority 선택에서는 `current error log`와 `user question`이 윈도우 안에 함께 들어와, attention이 실제로 참고할 만한 단서가 남습니다.
- context window 관리에서 중요한 것은 `얼마나 많이 넣었는가`보다 `예산 안에서 핵심 상태를 실제로 살렸는가`입니다.
- 우선순위 선택 뒤에 예산이 조금 남으면 낮은 우선순위 항목이 일부 들어올 수 있지만, 그보다 먼저 `필수 상태가 전부 살아남았는가`를 확인하는 편이 더 중요합니다.
- 그래서 문맥 선택 로직을 볼 때는 총 토큰 수뿐 아니라 `주문번호`, `현재 질문`, `최신 오류 로그` 같은 필수 상태가 실제로 남았는지를 함께 점검해야 합니다.

## 이 예제를 입력 선택 관점으로 다시 보면

앞의 예제는 긴 문맥 처리를 구현하는 코드가 아니라, `무엇을 더 넣을 수 있는가`보다 `무엇을 남기고 무엇을 덜어낼 것인가`가 실제 설계 문제라는 점을 가장 짧게 보여 주는 장면입니다. 여기서 읽어야 할 핵심은 context window가 단순 길이 숫자가 아니라, 토큰 예산 안에서 입력 우선순위를 다시 정하게 만드는 제약이라는 점입니다. 그리고 attention은 그 뒤에 남아 있는 항목들 사이에서만 관련도를 계산하므로, 애초에 핵심 단서가 윈도우 밖으로 밀리면 attention이 아무리 좋아도 그 단서를 참고할 수 없습니다. RAG, 대화 요약, 코드 어시스턴트 문맥 선택이 모두 결국 이 문제를 다른 형태로 풀고 있다고 보면 연결이 자연스럽습니다.

초기 언어 모델에서는 이렇게 긴 문맥 관리 문제가 지금처럼 실무 전면에 드러나지 않았습니다. 하지만 Transformer와 LLM이 긴 입력을 다루는 범용 구조가 되면서, 이제 문맥 길이 관리 자체가 중요한 설계 주제가 되었습니다.

커리큘럼 관점에서 이 절에서 확인해야 할 결과는 바로 앞의 P5-3.1 Transformer 구조를 실제 사용 제약과 연결해, 이후 RAG, prompt 설계, tool use, agent loop에서 왜 입력 선택이 중요해지는지 설명할 수 있게 되는가입니다. 이 절이 필요한 이유는 다음과 같습니다.

- Transformer 구조를 실제 사용 제약과 연결해야 하기 때문입니다.
- 이후 RAG, prompt 설계, tool use, agent loop에서 왜 입력 선택이 중요한지 설명해야 하기 때문입니다.
- `모델이 다 기억한다`는 오해를 줄여야 하기 때문입니다.

## 다음 장과의 연결

여기까지 오면 이제 Transformer 구조 위에서 갈라지는 두 흐름을 봐야 합니다.

- 이전 토큰을 바탕으로 다음 토큰을 생성하는 GPT 계열
- 그 생성 구조가 왜 사용자 경험을 크게 바꾸었는가

가까운 본류는 P5-4.1 GPT 계열의 위치입니다. 비교 배경은 뒤 배경 축에서 다시 보면 충분합니다.

## 이 절에서 기억할 관점

- context window는 모델이 한 번에 참고할 수 있는 토큰 범위입니다.
- attention은 그 범위 안에서 무엇이 중요한지 계산합니다.
- 길이가 길어질수록 항상 좋은 것이 아니라, 선택과 압축이 더 중요해질 수 있습니다.
- 이 절은 이후 RAG와 서비스 설계 설명의 기초입니다.

## 체크리스트

- context window를 입문 수준에서 설명할 수 있는가?
- attention과 context window의 역할 차이를 구분할 수 있는가?
- 왜 문맥 길이가 비용과 서비스 설계에 영향을 주는지 설명할 수 있는가?
- 왜 이 절이 RAG와 연결되는지 말할 수 있는가?

## 출처와 참고 자료

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, 확인 날짜: 2026-06-29.
- Colin Raffel et al., `Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer`, JMLR, 2020, 확인 날짜: 2026-06-29.
- OpenAI API Docs, context window와 입력 길이 관련 설명, 확인 날짜: 2026-06-29. [https://platform.openai.com/docs](https://platform.openai.com/docs){: target="_blank" rel="noopener noreferrer" }
