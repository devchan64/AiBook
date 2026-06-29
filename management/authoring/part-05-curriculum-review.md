# Part 5 커리큘럼 재검토 메모

## 검토 목적

- Part 5가 `LLM과 생성형 AI를 이해하기 위한 파트`라는 목적에 맞게 전개되는지 다시 점검한다.
- 현재 섹션 순서가 Part 1 수준의 반복 설명에서 멈추는 구간을 만드는지 확인한다.
- `개념 이해`, `실무 구조 이해`, `작은 구현`까지 이어지는 학습 흐름으로 재배치 기준을 정리한다.

## 현재 Part 5 목적과 완료 기준

- [docs/parts/part-05/index.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/index.md:3) 는 Part 5를 `Transformer 이후의 흐름`, `RAG`, `도구 사용`, `에이전트`, `평가`, `운영`까지 다루는 파트로 정의한다.
- 같은 문서의 완료 기준은 [index.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/index.md:20) 부터 [index.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/index.md:23) 까지 제시되어 있으며, 마지막 기준은 `모델 API를 사용해 작은 생성형 AI 기능을 구현할 수 있다`이다.

## 최근 반영 사항

- [docs/parts/part-05/chapter-05/section-01.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/chapter-05/section-01.md:36) 에서 BERT 약어 설명, 인텐트 분류 사례, 더 나은 예제를 추가해 `왜 읽고 분류하는 모델인가`를 더 분명히 했다.
- [docs/parts/part-05/chapter-09/section-02.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/chapter-09/section-02.md:1) 에서 LoRA 도입부를 `효율적 조정이 왜 필요한가`에서 출발하도록 보강했다.
- [docs/parts/part-05/chapter-09/section-03.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/chapter-09/section-03.md:1) 보충학습을 추가해 LoRA, adapter, QLoRA의 차이를 별도로 회수했다.
- [docs/parts/part-05/chapter-19/section-01.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/chapter-19/section-01.md:1), [section-02.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/chapter-19/section-02.md:1) 에서 `통합 미니 실습` 장을 추가해 요청, 검색, 출력, 기록을 한 흐름으로 묶는 최소 실습을 넣었다.

이 변경들은 개별 절의 이해도는 높였지만, Part 5 전체의 순서 문제를 해결한 것은 아니다. 아래 판단은 여전히 유효하되, `개별 절 품질`과 `파트 구조`를 구분해서 읽어야 한다.

## 핵심 판단

### 1. 현재 Part 5는 여전히 `개념 설명 비중이 큰 파트`이지만, `작은 구현으로 닫히는 파트`라는 약점은 일부 보완되었다

- 완료 기준에는 구현이 포함되어 있었고, 이 문제를 줄이기 위해 [docs/parts/part-05/chapter-19/section-01.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/chapter-19/section-01.md:1) 과 [section-02.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/chapter-19/section-02.md:1) 에 통합 미니 실습을 추가했다.
- 이로써 `개념 설명만 하다가 끝난다`는 충돌은 약해졌지만, 여전히 실제 상용 API 사용 예나 더 현실적인 품질 비교 실습은 Part 6 쪽으로 남아 있다.
- 따라서 현재 상태는 `직접 충돌`에서 `부분 보완`으로 옮겨 갔다고 보는 편이 맞다.

### 2. 초반부가 너무 길게 전제 설명을 반복해, LLM 본류가 늦게 시작된다

- [docs/parts/part-05/chapter-03/section-01.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/chapter-03/section-01.md:37) 부터 [section-01.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/chapter-03/section-01.md:144) 까지는 언어 모델 역사, 임베딩, RNN, Attention, Transformer, 사전학습을 다시 긴 흐름으로 훑는다.
- 이어서 [docs/parts/part-05/chapter-04/section-01.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/chapter-04/section-01.md:1) 은 제목 자체가 `Transformer 구조 복습`이다.
- 이런 배치는 `Part 4에서 Transformer를 보고 Part 5에서 LLM을 이해한다`기보다, `이전 파트 요약을 다시 끝까지 읽고 난 뒤에야 LLM 본론으로 들어간다`는 인상을 만든다.
- LLM 이해의 중심축인 `GPT 계열`, `다음 토큰 예측`, `생성 과정`, `지시 튜닝`이 실제로는 [docs/parts/part-05/chapter-06/section-01.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/chapter-06/section-01.md:1), [docs/parts/part-05/chapter-08/section-01.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/chapter-08/section-01.md:1), [docs/parts/part-05/chapter-10/section-01.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/chapter-10/section-01.md:1) 에서야 본격화된다.

### 3. BERT 축의 비중이 현재 Part 목적에 비해 크다

- Part 5 목적은 `LLM과 생성형 AI` 이해인데, [docs/parts/part-05/chapter-05/section-01.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/chapter-05/section-01.md:1) 과 [docs/parts/part-05/chapter-05/section-02.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/chapter-05/section-02.md:1) 는 BERT 계열과 이해 중심 태스크에 두 절을 사용한다.
- [section-02.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/chapter-05/section-02.md:54) 부터 [section-02.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/chapter-05/section-02.md:126) 까지는 분류, 문장쌍 판단, 검색, 임베딩을 길게 풀어 설명한다.
- 이 내용은 `생성형 AI 본류`라기보다 `검색·임베딩 보조 축`에 가깝다.
- 현재처럼 GPT 본류 앞에 독립 장으로 크게 두면, 학습 초점이 `생성형 AI 구조 이해`보다 `NLP 일반론 복습`으로 이동한다.
- 다만 [P5-5.1](/Users/simchangbo/ws/AiBook/docs/parts/part-05/chapter-05/section-01.md:127) 의 사례와 예제는 이미 보강되어, `보조 축으로 둘 때도 왜 필요한가`는 이전보다 분명해졌다.

### 4. Part 1 또는 이전 파트의 감각을 다시 꺼내고 끝나는 문장이 반복된다

- [docs/parts/part-05/chapter-08/section-02.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/chapter-08/section-02.md:77) 는 temperature 설명에서 `Part 1에서도 한 번 조심해서 다뤘다`고 직접 언급한다.
- [docs/parts/part-05/chapter-04/section-01.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/chapter-04/section-01.md:36) 는 `Part 4의 Transformer와 Part 5의 Transformer`를 다시 구분하는 데 상당한 분량을 쓴다.
- 이런 문장들이 모두 잘못은 아니지만, 초반 여러 장에서 반복되면 `새 파트가 독립적으로 전진한다`는 느낌보다 `이전 파트 복습을 다시 끝까지 한다`는 느낌이 강해진다.

### 5. 서비스 구조 파트는 비교적 자연스럽지만, 앞단 LLM 핵심 이해가 늦어져 효과가 약해진다

- [docs/parts/part-05/chapter-12/section-01.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/chapter-12/section-01.md:1), [docs/parts/part-05/chapter-14/section-01.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/chapter-14/section-01.md:1), [docs/parts/part-05/chapter-15/section-01.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/chapter-15/section-01.md:1), [docs/parts/part-05/chapter-16/section-01.md](/Users/simchangbo/ws/AiBook/docs/parts/part-05/chapter-16/section-01.md:1) 의 흐름은 `프롬프트 -> RAG -> tool use -> agent -> MCP`로 비교적 잘 이어진다.
- 다만 이 서비스 구조가 힘을 가지려면 독자가 먼저 `LLM은 왜 다음 토큰 예측 기반인데도 지시를 따르고, 왜 RAG와 도구가 붙는가`를 명확히 이해해야 한다.
- 현재는 그 핵심 설명이 늦게 등장해, 뒤 절들이 `LLM 서비스 일반론`처럼 읽힐 위험이 있다.

## 재배치 원칙

### 원칙 1. Part 5의 첫 본류는 `LLM 핵심 메커니즘`이어야 한다

- 토큰과 토큰화
- Transformer를 LLM 관점에서 읽는 최소 구조
- GPT 계열과 다음 토큰 예측
- 생성 과정과 decoding 감각
- 사전학습, 지시 튜닝, 정렬

이 묶음이 먼저 닫혀야 한다.

### 원칙 2. BERT와 임베딩은 `본류`가 아니라 `보조 축`으로 위치를 조정한다

- BERT 계열은 GPT와 대비를 위해 한 번은 필요하다.
- 하지만 `생성형 AI 이해`의 첫 번째 계단은 아니다.
- 임베딩, 검색, 벡터 데이터베이스와 연결되는 맥락 안에서 더 짧게 요약하거나, 보충학습 또는 뒤쪽 보조 장으로 이동하는 편이 적합하다.

### 원칙 3. 각 장은 `현재 장의 중심 질문`을 앞으로 밀어야 한다

- 역사 정리 장은 `LLM 본론에 들어가기 전 최소 지도`까지만 허용한다.
- `Part 1에서 봤다`, `Part 4에서 복습했다`는 문장은 연결 확인 수준까지만 쓰고, 새 장의 분량 대부분을 차지하면 안 된다.

### 원칙 4. 파트의 끝은 `운영 일반론`만이 아니라 `작은 구현 또는 통합 실습`으로 닫혀야 한다

- Part 목적과 완료 기준을 맞추려면 `모델 API`, `프롬프트`, `검색 또는 도구`, `간단한 평가`를 묶은 작은 기능 구현 장이 필요하다.
- 구현 규모가 너무 크면 별도 Part로 보내되, 최소한 `이 파트에서 배운 개념이 실제로 어떻게 한 요청 흐름으로 연결되는가`는 보여 주어야 한다.

## 권장 순서

### A안. 본편 재배치

1. 토큰(token)과 토큰화(tokenization)
2. Transformer를 LLM 관점에서 다시 읽기
3. GPT 계열의 위치
4. 다음 토큰 예측(next-token prediction)
5. 생성 과정의 직관
6. 사전학습과 스케일
7. 지시 튜닝과 정렬
8. 프롬프트 엔지니어링과 한계
9. RAG와 검색 결합
10. 임베딩, 벡터 데이터베이스, 인덱스
11. 도구 사용과 함수 호출
12. 에이전트, MCP, 하네스
13. 평가와 운영
14. 작은 생성형 AI 기능 구현 또는 통합 실습

### B안. 보조 축 분리

- `P5-3.1 LLM 발전사의 큰 흐름`
- `P5-3.2 직접 계보와 주변 근거`
- `P5-5.1 BERT 계열의 위치`
- `P5-5.2 이해 중심 태스크`

이 네 절은 다음 둘 중 하나로 재배치하는 편이 낫다.

- 본편 안에서는 짧은 `배경 정리 장`으로 압축한다.
- 또는 `보충학습: 생성형 AI 이전 NLP 흐름과 encoder 계열`로 묶는다.

## 학습목표 타입 재분류 제안

Part 5의 학습목표는 한 종류가 아니다. 이후 분량 조절을 위해 다음 타입으로 나누는 편이 좋다.

| 타입 | 중심 질문 | 현재 해당 예 |
| --- | --- | --- |
| 구조 이해형 | LLM은 어떤 구조로 동작하는가 | 토큰, Transformer, GPT, next-token |
| 생성 메커니즘 이해형 | 왜 생성이 가능한가 | 생성 과정, temperature, instruction tuning |
| 근거 연결형 | 왜 외부 문서와 도구가 필요한가 | RAG, vector DB, tool use |
| 실행 환경 이해형 | 왜 agent, MCP, harness가 필요한가 | agent, MCP, harness |
| 운영 판단형 | 품질과 실패를 어떻게 읽는가 | evaluation, 운영 제약, 실패 대응 |
| 통합 실습형 | 실제 요청 흐름을 어떻게 구현하는가 | 현재 비어 있음 |

현재 문제는 `통합 실습형`이 비어 있고, `배경 이해형`과 `보조 축 설명`의 비중이 앞쪽에서 과하다는 점이다.

## 우선 수정 대상

### 우선순위 높음

- Chapter 3, 5의 분량 축소 또는 보충학습 이동
- Chapter 4, 6, 8, 10을 더 앞쪽 본류로 재배치
- index의 완료 기준과 실제 장 구성을 다시 맞추기

### 우선순위 중간

- `복습`, `Part 1에서도`, `앞에서 봤듯` 같은 연결 문장을 줄이고 현재 질문 중심 문장으로 교체
- 임베딩 장의 일부를 RAG/벡터 검색 장과 더 밀접하게 재배치
- Chapter 9는 현재처럼 `P5-9.2 실무 감각 + P5-9.3 보충학습` 구조를 유지하되, 이후 본편 재배치 시 `파인튜닝 뒤의 심화 축`으로 남기는 방안을 우선 검토

## 현재 기준의 다음 업데이트 순서

1. Part 5 끝에 `통합 실습 장`을 추가할지, Part 6 시작으로 넘길지 먼저 결정한다.
2. Chapter 3과 Chapter 5를 본편 축소 또는 보충학습 전환 관점에서 다시 편집한다.
3. Chapter 4, 6, 8, 10을 앞세우는 새 Part 5 순서를 management 메모와 실제 목차에 함께 반영한다.
4. 이후 index의 `다룰 내용`과 `완료 기준`을 새 구조에 맞춰 다시 쓴다.

### 우선순위 낮음

- 역사·계보 예제의 Python 비중 축소 검토
- Chapter 17, 18의 운영 설명을 통합 실습 회고와 더 직접 연결

## 결론

현재 Part 5는 `LLM과 생성형 AI의 핵심 구조를 배운 뒤 서비스 구조와 운영으로 확장하는 파트`라기보다, `기초 복습 + NLP 배경 + 서비스 구조 설명`이 한 파트 안에 길게 병렬 배치된 상태에 가깝다.

핵심 수정 방향은 다음 한 줄로 정리할 수 있다.

`LLM 본류를 앞당기고, BERT/역사 축은 보조화하며, 마지막은 작은 구현으로 닫는다.`
