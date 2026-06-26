# P3-6.3 계획 검토: 보충학습 - 사이트 신뢰성 엔지니어링에서 매트릭스(metrics)를 읽는 법

## 목적

이 메모는 Part 3 Chapter 6 뒤에 넣을 보충학습 후보를 준비하기 위한 계획 문서다.

사용자 의도는 `평가 지표(metric)`를 머신러닝 모델의 내부 평가에만 가두지 않고, 실제 서비스 운영에서 숫자가 어떻게 읽히는지도 연결하는 것이다. 다만 이 절은 SRE 입문서 전체가 아니라, 머신러닝 평가 지표 장을 읽은 독자가 `운영 지표는 또 다른 층위의 metric`이라는 점을 이해하게 만드는 보충학습이어야 한다.

특히 SRE는 `metric`이라는 말을 이미 SW 엔지니어가 익숙하게 접하는 영역이기 때문에, 머신러닝 평가 지표를 설명할 때 좋은 연결 다리로 쓸 수 있다. latency, error rate, availability, throughput 같은 운영 매트릭스를 읽어 본 사람은 `accuracy`, `precision`, `recall`도 결국 `무엇을 중요하게 측정할 것인가`의 문제로 더 빠르게 받아들일 수 있다.

## 제안 위치

- Part 3. 머신러닝
- Chapter 6. 평가 지표
- Section 후보: `P3-6.3 보충학습: 사이트 신뢰성 엔지니어링에서 매트릭스(metrics)를 읽는 법`

이 위치가 적절한 이유:

1. P3-6.1은 평가 지표가 왜 여러 개인지 설명한다.
2. P3-6.2는 문제 유형별로 지표를 나누어 본다.
3. 그 뒤 보충학습으로 `서비스 운영에서는 또 어떤 숫자를 읽는가`를 붙이면, 모델 평가와 서비스 운영을 구분하면서 연결할 수 있다.

## 이 절의 중심 질문

- 모델이 잘 맞는 것과 서비스가 잘 운영되는 것은 왜 다른가?
- 머신러닝 평가 지표(metric)와 운영 매트릭스(metrics)는 무엇이 다른가?
- SRE는 어떤 숫자를 보고 시스템을 판단하는가?
- SLI(service level indicator), SLO(service level objective), SLA(service level agreement)는 어떤 관계인가?
- 왜 운영에서는 평균(mean) 하나보다 분포(distribution), 지연 시간(latency), 오류율(error rate), 가용성(availability), 포화도(saturation)를 같이 보는가?

## 도메인 경계

이 절은 다음을 다룬다.

- 머신러닝 평가 지표와 운영 지표의 층위 구분
- SRE에서 숫자를 읽는 대표 관점
- SLI, SLO, 에러 버짓(error budget)의 입문적 의미
- 지연 시간(latency), 오류율(error rate), 트래픽(traffic), 포화도(saturation) 같은 대표 운영 지표의 직관
- AI 서비스 운영에서 모델 metric과 시스템 metric이 동시에 필요하다는 연결

이 절은 다음을 깊게 다루지 않는다.

- 쿠버네티스(Kubernetes) 운영 실무
- Prometheus, Grafana, OpenTelemetry 도구 사용법
- 알림 정책(alert policy) 세부 튜닝
- Incident management 전체 절차
- 분산 추적(tracing), 로그(logging), 프로파일링(profiling)의 구현 상세
- AI 관측가능성(observability) 제품 비교

## P3-6.1, P3-6.2와의 경계

### P3-6.1과의 경계

- P3-6.1은 `정확도, 정밀도, 재현율`처럼 모델 결과를 읽는 기준을 설명한다.
- P3-6.3은 `서비스 지연 시간, 오류율, 가용성`처럼 시스템 동작을 읽는 기준을 설명한다.
- 둘 다 숫자를 읽지만, 대상이 다르다.

### P3-6.2와의 경계

- P3-6.2는 분류, 회귀, 군집화 등 문제 유형에 따라 어떤 평가 기준이 적절한지 다룬다.
- P3-6.3은 모델 종류가 아니라 서비스 운영 관점의 매트릭스를 다룬다.

## 초심자용 핵심 문장 후보

- `모델 metric은 예측이 얼마나 맞는지에 가깝고, SRE metric은 서비스가 얼마나 버티는지에 가깝다.`
- `좋은 모델이 있어도 느리거나 자주 실패하는 서비스는 좋은 서비스가 아니다.`
- `운영에서는 평균 점수 하나보다, 실패율과 느린 꼬리 구간(tail)을 함께 본다.`
- `머신러닝 평가는 모델 품질 질문에 답하고, SRE 평가는 서비스 신뢰성 질문에 답한다.`
- `SRE metrics는 SW 엔지니어가 머신러닝 metric을 낯설지 않게 받아들이도록 돕는 가까운 비유가 될 수 있다.`

## 예시 방향

### 예시 1. 챗봇 서비스

- 모델 평가:
  - 정답률, 재현율, 사용자 만족도, hallucination rate
- 운영 평가:
  - p95 latency
  - error rate
  - timeout 비율
  - availability

핵심 메시지:

- 답변 품질이 좋아도 8초씩 걸리면 서비스 문제다.
- 지연 시간은 낮아도 잘못된 답이 많으면 모델 문제다.
- 둘은 서로 다른 metric 층위다.

### 예시 2. 스팸 분류 API

- 모델 평가:
  - precision, recall, F1
- 운영 평가:
  - 처리량(request throughput)
  - 실패율
  - 평균 및 p95 응답 시간
  - 배포 후 오류 증가 여부

핵심 메시지:

- 분류 성능이 높아도 장애가 잦으면 운영 품질이 낮다.
- 운영 지표가 좋더라도 스팸을 놓치면 제품 목표를 달성하지 못한다.

## 도식 후보

### 도식 1. 두 층위의 metric

```text
user request
  -> model output quality metrics
  -> service runtime metrics
  -> product decision
```

의도:

- 모델 평가와 서비스 운영 평가가 병렬로 존재함을 보여 준다.

### 도식 2. SLI -> SLO -> error budget

```text
measured behavior -> chosen indicator -> target objective -> remaining risk budget
```

의도:

- SRE 용어가 단절된 약어 암기가 아니라, 운영 판단 구조라는 점을 보여 준다.

## 근거 후보

우선순위가 높은 근거 후보:

1. Google SRE Book, `Monitoring Distributed Systems`
   - The Four Golden Signals
   - latency, traffic, errors, saturation
2. Google SRE Book 또는 Workbook의 SLI/SLO 관련 장
   - service level indicator
   - service level objective
   - error budget
3. 필요하면 OpenAI/Anthropic 운영 문서가 아니라, 일반적이고 오래 가는 SRE 표준 관점 위주로 유지

## 작성 시 주의

- 이 절은 머신러닝 책의 보충학습이다. SRE 입문서를 대신하면 범위가 무너진다.
- `metric`이라는 같은 단어가 모델 평가와 운영 평가에서 다르게 쓰인다는 점을 먼저 분리해야 한다.
- SRE를 단순 비유로만 소비하지 않는다. 비슷한 점은 `측정과 판단 기준`이고, 다른 점은 `무엇을 측정하는가`라는 사실을 분명히 둔다.
- DevOps, observability, monitoring, tracing, alerting을 한 절에 다 밀어 넣지 않는다.
- `SRE = 운영팀 도구 모음`처럼 오해되지 않게 한다.
- AI 서비스와 연결할 때도 현재 제품 사례보다 일반 구조를 우선한다.

## 다음 작업 후보

1. 공식 SRE 자료에서 SLI/SLO/error budget, four golden signals 근거 수집
2. P3-6.3의 도메인 경계 확정
3. 초심자용 예시 2개 선정
4. Mermaid 도식 초안 작성
5. 본문 초안 작성 후 P3-6.1, P3-6.2와 중복 점검
