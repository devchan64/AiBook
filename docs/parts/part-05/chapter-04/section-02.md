# P5-4.2 attention과 context window

P5-4.1에서는 Transformer를 LLM 기준으로 다시 읽으며, 토큰이 임베딩을 거쳐 Transformer 블록을 통과한 뒤 다음 토큰 점수로 이어지는 흐름을 보았습니다. 이제 바로 다음 제약을 봐야 합니다.

Transformer가 이전 토큰을 참고할 수 있다면, 실제로는 어디까지 참고할 수 있는가?

이 절은 그 질문에 답합니다.

context window는 모델이 한 번의 계산 안에서 참고할 수 있는 토큰 범위이며, attention은 그 범위 안에서 어떤 토큰이 더 중요한지 계산하는 구조다.

## 이 절의 범위

이 절은 다음 질문에 답합니다.

- attention과 context window는 어떤 관계인가?
- 왜 `모든 이전 토큰을 본다`는 말에도 실제 한계가 붙는가?
- context window는 왜 비용, 품질, 서비스 구조에 영향을 주는가?

이 절은 다음 내용은 깊게 다루지 않습니다.

- RoPE, ALiBi 같은 위치 표현 세부 비교
- KV cache 최적화
- 장문맥 전용 아키텍처의 세부 구현

이 항목들은 같은 장의 P5-4.3 보충학습에서 `왜 긴 문맥을 다루기 어렵고 어떤 보강 장치가 붙는가`라는 수준으로 다시 설명합니다. 긴 문맥이 실제 서비스 구조와 RAG 설계에 미치는 영향은 P5-12.1, P5-12.2, P5-18.1에서도 다시 이어집니다.

이 절의 목적은 독자가 `문맥을 다 본다`는 표현을 너무 크게 해석하지 않게 하고, 실제 서비스에서 왜 문맥 길이 관리가 중요한지 설명하는 데 있습니다.

## 이 절의 목표

- context window를 `모델이 한 번에 참고할 수 있는 토큰 범위`로 설명할 수 있습니다.
- attention이 그 범위 안에서 관련도를 계산한다는 점을 설명할 수 있습니다.
- context window가 길이 제한, 비용, 지연 시간과 왜 연결되는지 말할 수 있습니다.
- 이후 RAG와 긴 문서 처리 설명으로 자연스럽게 넘어갈 수 있습니다.

## attention은 범위 안의 관련도를 계산한다

attention은 토큰 간 관련도를 계산하는 구조입니다. 하지만 이 계산은 무한한 과거 전체를 보는 것이 아니라, 현재 입력에 들어와 있는 토큰 범위 안에서 이루어집니다.

즉:

- attention은 `무엇을 더 볼 것인가`를 계산하고
- context window는 `무엇까지 볼 수 있는가`를 제한합니다

이 둘을 섞으면 안 됩니다.

더 안전한 설명은 다음과 같습니다.

`attention은 선택 규칙에 가깝고, context window는 입력 범위 제한에 가깝다.`

## context window는 무엇을 뜻하나

context window는 모델이 한 번의 입력으로 받을 수 있는 토큰 길이 범위입니다.

예를 들어 어떤 모델이 8k tokens를 지원한다면, 시스템 메시지, 사용자 입력, 대화 기록, 검색 결과, 도구 출력까지 합쳐 그 범위 안에 들어와야 합니다.

다음처럼 이해하면 좋습니다.

`문맥을 많이 넣을수록 좋을 것 같지만, 실제로는 토큰 길이 제한 안에서 무엇을 남기고 무엇을 줄일지 결정해야 한다.`

## 왜 길이 제한이 중요한가

context window는 단순 숫자 제한이 아닙니다. 실제로 다음 문제를 만듭니다.

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

## 왜 RAG와 연결되는가

RAG(retrieval-augmented generation)는 바로 이 문제와 연결됩니다.

긴 문서 전체를 넣는 대신:

- 관련 문서 조각만 검색하고
- 필요한 부분만 잘라 넣어
- 제한된 context window 안에서 근거를 더 효율적으로 사용하려는 구조이기 때문입니다

즉, context window의 존재는 RAG가 왜 필요한지 설명하는 중요한 배경입니다.

## 아주 단순하게 그리면

```mermaid
flowchart LR
  A["all possible prior information"]
  B["selected tokens inside context window"]
  C["attention over selected tokens"]
  D["next-token prediction"]

  A --> B --> C --> D
```

이 도식의 핵심은 다음입니다.

- 전체 정보가 다 들어오는 것이 아니라
- 먼저 윈도우 안에 들어온 정보가 있고
- attention은 그 안에서 계산된다는 점입니다

## 사례로 보기

### 사례 1. 긴 문서 요약

100페이지 문서를 그대로 넣기 어려우면, 중요한 절을 먼저 고르거나 요약 단위를 나눠야 합니다.

### 사례 2. 코드 도우미

큰 코드베이스 전체를 한 번에 넣을 수 없으므로, 현재 파일과 관련 함수, 에러 로그, 테스트 결과를 우선 선택해야 합니다.

### 사례 3. 대화형 챗봇

대화가 길어질수록 오래된 메시지가 계속 누적됩니다. 이때 어떤 대화 기록을 남기고 어떤 기록은 요약할지 결정해야 합니다.

## 작은 Python 예제로 보기

이번 예제의 목표는 실제 토크나이저 길이 계산이 아니라, 제한된 문맥 안에 일부 항목만 남긴다는 감각을 확인하는 것입니다.

입력:

- 여러 개의 문맥 항목
- 최대 개수 제한

출력:

- 윈도우 안에 남은 항목

```python
context_items = [
    "system instruction",
    "user question",
    "document chunk 1",
    "document chunk 2",
    "tool output",
    "older chat history",
]

max_items = 4
selected = context_items[:max_items]

print("selected_context =")
for item in selected:
    print("-", item)
```

실행 결과 예시는 다음처럼 읽을 수 있습니다.

```text
selected_context =
- system instruction
- user question
- document chunk 1
- document chunk 2
```

이 예제는 실제 토큰 길이 계산을 하지 않지만, `모든 정보를 다 넣지 못하므로 선택이 필요하다`는 핵심 감각을 보여 줍니다.

## 역사와 커리큘럼 관점

초기 언어 모델에서는 이렇게 긴 문맥 관리 문제가 지금처럼 실무 전면에 드러나지 않았습니다. 하지만 Transformer와 LLM이 긴 입력을 다루는 범용 구조가 되면서, 이제 문맥 길이 관리 자체가 중요한 설계 주제가 되었습니다.

커리큘럼 관점에서 이 절은 매우 중요합니다.

- Transformer 구조를 실제 사용 제약과 연결하고
- 이후 RAG, prompt 설계, tool use, agent loop에서 왜 입력 선택이 중요한지 설명하며
- `모델이 다 기억한다`는 오해를 줄이기 때문입니다

## 다음 장과의 연결

여기까지 오면 이제 Transformer 구조 위에서 갈라지는 두 흐름을 봐야 합니다.

- 입력 전체 문맥 표현에 강한 BERT 계열
- 다음 토큰 생성에 강한 GPT 계열

이 질문은 P5-5.1 BERT 계열의 위치로 이어집니다.

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
