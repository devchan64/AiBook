# P3-6.3 보충학습: 사이트 신뢰성 엔지니어링에서 매트릭스(metrics)를 읽는 법 - 근거 검토 메모

## 확인한 자료

1. Google SRE, `Service Level Objectives`
   - URL: https://sre.google/sre-book/service-level-objectives/
   - 확인 날짜: 2026-06-26
   - 사용 목적:
     - SLI(service level indicator), SLO(service level objective), SLA(service level agreement)의 구분 확인
     - 운영 metric이 단순 관측이 아니라 목표와 반응 구조까지 이어진다는 점 확인
     - 대표 SLI로 latency, error rate, throughput, availability가 자주 쓰인다는 점 확인

2. Google SRE, `Monitoring Distributed Systems`
   - URL: https://sre.google/sre-book/monitoring-distributed-systems/
   - 확인 날짜: 2026-06-26
   - 사용 목적:
     - monitoring, alert, dashboard의 기본 개념 확인
     - The Four Golden Signals: latency, traffic, errors, saturation 확인
     - 평균(mean)보다 분포와 tail latency가 중요할 수 있다는 설명 확인
     - paging은 단순 이상 징후가 아니라 인간 개입이 필요한 문제에 집중해야 한다는 운영 철학 확인

## 본문에 반영한 일반화

- 모델 metric과 운영 metric은 둘 다 측정과 판단의 기준이지만, 측정 대상이 다르다.
- 모델 metric은 예측 품질에 가깝고, 운영 metric은 서비스 신뢰성과 사용자 경험에 가깝다.
- SLI는 측정값, SLO는 목표값, SLA는 약속과 결과로 구분할 수 있다.
- error budget은 완벽을 강요하는 개념이 아니라, 허용 가능한 실패 범위를 관리하는 개념으로 설명할 수 있다.
- 운영에서는 평균 하나보다 percentile, tail latency, error rate 같은 분포적 관점이 중요할 수 있다.
- latency, traffic, errors, saturation은 사용자 대상 서비스 운영을 읽는 대표 신호로 설명할 수 있다.

## 절의 경계

- 이 절은 SRE 입문서를 대신하지 않는다.
- Prometheus, Grafana, OpenTelemetry, alert rule 구현법은 다루지 않는다.
- incident response, on-call, tracing, logging, profiling의 상세 절차는 다루지 않는다.
- AI observability 제품 비교나 운영 플랫폼 비교는 하지 않는다.

## 작성 판단 메모

- Chapter 6이 평가 지표를 다루므로, 보충학습으로 운영 metric을 붙이는 것이 모델 평가와 서비스 운영의 층위를 구분하는 데 도움이 된다.
- SRE는 SW 엔지니어가 익숙하게 접하는 metric 세계이므로, 머신러닝 metric을 낯설지 않게 연결하는 다리로 쓸 수 있다.
- 본문 예시는 특정 기업 성능 주장이나 특정 사건 분석이 아니라, 일반적인 서비스 운영 상황을 설명하는 수준으로 유지한다.
