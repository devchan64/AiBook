# P3-3.1 근거 검토 메모

## 대상 섹션

- `docs/parts/part-03/chapter-03/section-01.md`
- 주제: 휴리스틱(heuristic)이 필요한 이유

## 확인한 근거

### Stanford Encyclopedia of Philosophy, Bounded Rationality

- URL: https://plato.stanford.edu/entries/bounded-rationality/
- 확인 날짜: 2026-06-25
- 활용 내용:
  - Herbert Simon의 제한된 합리성(bounded rationality)이 완전한 합리성 가정 대신 정보 접근과 계산 능력의 제약을 가진 주체의 합리성을 다루는 관점임을 확인했습니다.
  - 머신러닝 실무에서 모든 후보를 완전히 계산하지 못하고, 제한된 시간과 계산 자원 안에서 검증 가능한 선택을 해야 한다는 설명에 반영했습니다.

### Russell and Norvig, Artificial Intelligence: A Modern Approach

- URL: https://aima.cs.berkeley.edu/
- 확인 날짜: 2026-06-25
- 활용 내용:
  - AI 개론에서 탐색(search), 최적화(optimization), 강화학습(reinforcement learning), 확률 추론 등 여러 주제를 함께 다루는 대표 교재임을 확인했습니다.
  - 휴리스틱을 AI의 탐색과 문제 해결에서 후보를 줄이고 계산을 현실화하는 관점으로 연결했습니다.

### Pearl, Heuristics: Intelligent Search Strategies for Computer Problem Solving

- 자료: Judea Pearl, `Heuristics: Intelligent Search Strategies for Computer Problem Solving`, Addison-Wesley, 1984.
- 확인 날짜: 2026-06-25
- 활용 내용:
  - AI 문맥에서 휴리스틱이 지능적 탐색 전략과 연결되는 고전적 주제임을 확인했습니다.
  - 본문에서는 고전 탐색 알고리즘을 깊게 설명하지 않고, 머신러닝 실무의 후보 축소와 검증 흐름으로 일반화했습니다.

## 반영 판단

- Part 3 이후는 초심자를 기준으로 작성해야 하므로, 휴리스틱의 역사와 철학을 길게 설명하지 않고 고객 이탈 예측 예시로 시작했습니다.
- 휴리스틱을 `정답`, `최적해`, `대충 찍기`로 단정하지 않고 `검증 가능한 작업 가설`로 정리했습니다.
- P3-3.2는 모델 선택을 다룰 예정이므로, 이번 섹션에서는 모델 선택 세부 기준을 자세히 쓰지 않았습니다.

## 주의할 표현

- 휴리스틱이 항상 빠르고 좋은 결과를 낸다고 말하지 않습니다.
- 휴리스틱을 알고리즘과 같은 말로 쓰지 않습니다.
- 휴리스틱을 검증 없이 반복되는 개인 습관으로 정당화하지 않습니다.
- 실무 예시는 이해를 돕기 위한 자체 예시이며 특정 산업의 표준 절차로 단정하지 않습니다.
