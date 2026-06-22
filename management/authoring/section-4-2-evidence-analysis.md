# 4.2 근거 분석: 입력(input), 출력(output), 데이터(data)

이 문서는 `docs/chapters/chapter-04/section-02.md`의 근거 연결을 검토한 관리 메모입니다.

원문 확인 규칙에 따라 이미 내려받은 자료를 우선 사용했습니다. `.tmp/`의 원문 파일은 근거 검토용이며 저장소에 커밋하지 않습니다.

## 확인한 자료

| 자료 | 로컬 확인 | 본문 반영 역할 |
| --- | --- | --- |
| Stanford Encyclopedia of Philosophy, `Artificial Intelligence` | `.tmp/section-01-evidence/sep-ai.html` | 지능형 에이전트를 지각(percepts)과 행동(actions)의 함수로 보는 관점, 지도학습의 입력-출력 쌍 설명 |
| Google for Developers, `Supervised Learning` | `.tmp/section-2-1-labeling-evidence/google-ml-terminology.html` | 지도학습에서 예시(example), 특징(feature), 라벨(label), 특징과 라벨의 관계 학습, 라벨 없는 새 데이터에 대한 추론 설명 |

## 핵심 근거 연결

| 본문 주장 | 근거 | 반영 판단 |
| --- | --- | --- |
| AI 문제는 입력과 출력의 관계로 단순화해 볼 수 있다 | SEP AI 항목은 에이전트가 환경에서 percepts를 받고 actions를 수행하며, percept sequence를 action으로 매핑하는 함수 관점을 소개함 | 유지하되 모든 AI를 단순 함수로 환원한다고 과장하지 않음 |
| 지도학습에서는 입력과 정답 출력 쌍으로 문제를 볼 수 있다 | SEP AI 항목은 supervised learning의 training data가 input-output pairs 형태라고 설명함 | 4.2에서는 입문 수준으로만 사용 |
| 데이터는 사례(example)의 모음으로 설명할 수 있다 | Google 자료는 supervised learning의 examples가 features와 label을 포함한다고 설명함 | 유지 |
| 모델은 데이터에서 입력과 출력의 관계를 학습해 새 입력에 적용한다 | Google 자료는 라벨이 붙은 예시를 모델에 제공해 features와 label의 관계를 배우게 하고, 학습 후 라벨 없는 예시에 대한 추론을 수행한다고 설명함 | 유지. 본문에서는 `입력과 출력 사이의 관계를 조정한다`는 입문용 표현으로 일반화 |
| 출력 정의가 문제 성격을 바꾼다 | 분류, 회귀, 추천, 생성은 본문에서 예시로 일반화 | 유지하되 알고리즘 세부 설명은 후속 장으로 보냄 |
| 입력과 출력이 잘못 정의되면 모델 선택 이전에 문제가 생길 수 있다 | 근거 자료의 직접 인용이라기보다 모델링 관점의 저자적 일반화 | 유지. 4.4에서 문제 정의와 평가 지표로 확장 |
| 같은 업무 목표도 입력과 출력 정의에 따라 필요한 데이터가 달라진다 | 지도학습의 input-output pair 관점과 예시/라벨 구조를 바탕으로 한 저자적 일반화 | 유지. 고객 문의와 배송 예시는 자체 학습 예시로 사용 |

## 섹션 구성 검토

| 검토 항목 | 판단 |
| --- | --- |
| 글의 속도 | 기존 초안은 입력, 출력, 데이터를 빠르게 정의해 입문 독자가 따라가기 어려울 수 있었음 |
| 보강 방향 | 고객 문의 예시를 반복 사용해 넓은 현실 문제를 작은 모델링 과제로 좁히는 과정을 단계화 |
| 4.1과의 경계 | 모델/모형 자체의 개념 설명은 반복하지 않고, 4.2에서는 모델을 만들기 위한 입력·출력·데이터 정의에 집중 |
| 4.3과의 경계 | 특징(feature)과 라벨(label)을 언급하되, 상세 정의와 내부 표현 설명은 4.3으로 넘김 |
| 4.4와의 경계 | 문제 정의 실패 사례를 소개하되, 평가 지표와 모델 선택의 상세 논의는 4.4로 넘김 |

## 주의한 표현

- 4.2는 특징(feature), 표현(representation), 파라미터(parameter)의 세부 차이를 설명하지 않습니다. 이는 4.3의 범위입니다.
- 4.2는 문제 정의가 모델을 결정하는 방식과 평가 지표의 상세를 설명하지 않습니다. 이는 4.4와 Part 3의 범위입니다.
- 고객 문의, 배송, 날씨, 장애 탐지 예시는 학습용 자체 예시입니다. 특정 회사나 실제 서비스 운영 기준이 아닙니다.
- `환불`, `배송`, `교환`, `기타` 같은 라벨 체계도 설명용 예시입니다. 실제 업무에서는 조직의 정책, 처리 절차, 데이터 품질 검토에 따라 달라질 수 있습니다.
- `입력 -> 모델 -> 출력` 도식은 학습용 단순화입니다. 실제 AI 시스템에는 전처리, 후처리, 정책 규칙, 사람 검토, 로깅, 보안 절차가 함께 붙을 수 있습니다.
- `출력`은 항상 정답이라는 뜻이 아닙니다. 모델이 생성하거나 예측해야 하는 목표 값, 분류, 점수, 추천, 문장 등이 될 수 있습니다.

## 본문에 넣지 않은 내용

- 특징 공학(feature engineering)과 표현 학습(representation learning)은 4.3에서 다룹니다.
- 문제 정의와 평가 지표의 관계는 4.4와 Part 3에서 다룹니다.
- 데이터 분리, 검증, 과적합, 일반화는 Part 3에서 다룹니다.
- 개인정보, 보안, 저작권 문제는 Part 1의 윤리/보안 장과 별도 법·정책 장에서 다룹니다.

## 검증 필요

- `출력(output)`, `라벨(label)`, `타깃(target)`, `정답(ground truth)`의 한국어 용어 구분은 이후 용어표에서 다시 확인합니다.
- 생성형 AI에서 출력 정의와 평가 기준을 설명할 때는 별도 근거 자료가 필요합니다.

## 출처

- Stanford Encyclopedia of Philosophy, Selmer Bringsjord and Naveen Sundar Govindarajulu, [Artificial Intelligence](https://plato.stanford.edu/entries/artificial-intelligence/), 2018-07-12, 확인 날짜: 2026-06-22.
- Google for Developers, [Supervised Learning](https://developers.google.com/machine-learning/intro-to-ml/supervised), 확인 날짜: 2026-06-22.
