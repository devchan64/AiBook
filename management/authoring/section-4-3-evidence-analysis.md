# 4.3 근거 분석: 특징(feature), 표현(representation), 파라미터(parameter)

이 문서는 `docs/chapters/chapter-04/section-03.md`의 근거 연결을 검토한 관리 메모입니다.

원문 확인 규칙에 따라 이미 내려받은 자료를 우선 사용했습니다. `.tmp/`의 원문 파일은 근거 검토용이며 저장소에 커밋하지 않습니다.

## 확인한 자료

| 자료 | 로컬 확인 | 본문 반영 역할 |
| --- | --- | --- |
| Google for Developers, `Machine Learning Glossary` | `.tmp/section-4-1-evidence/google-ml-glossary.html` | feature, label, representation, parameter, feature engineering 정의 확인 |
| Google for Developers, `Supervised Learning` | `.tmp/section-2-1-labeling-evidence/google-ml-terminology.html` | 라벨이 있는 예시를 통해 features와 label의 관계를 학습한다는 설명 |
| Stanford Encyclopedia of Philosophy, `Artificial Intelligence` | `.tmp/section-01-evidence/sep-ai.html` | feature vector representation, 표현 함수, 좋은 representation의 중요성 설명 |
| Bengio, Courville, Vincent, `Representation Learning: A Review and New Perspectives` | `.tmp/section-3-3-evidence-bengio-representation-learning.html` | 머신러닝 성공이 데이터 표현에 의존하고, 표현이 설명 요인을 드러내거나 숨길 수 있다는 설명 |

## 핵심 근거 연결

| 본문 주장 | 근거 | 반영 판단 |
| --- | --- | --- |
| 특징은 모델이 사용하는 입력 값이다 | Google ML Glossary는 feature를 머신러닝 모델의 input variable로 설명함 | 유지 |
| 라벨은 지도학습 예시의 답 또는 결과 부분이다 | Google ML Glossary는 label을 supervised ML에서 example의 answer/result 부분으로 설명함 | 본문에서는 4.2와 연결하는 보조 개념으로만 사용 |
| 표현은 데이터를 유용한 특징으로 매핑하는 과정으로 설명할 수 있다 | Google ML Glossary는 representation을 data를 useful features로 mapping하는 과정으로 설명함 | 유지하되 본문에서는 `계산하기 쉬운 형태로 바꾼 결과`로 쉽게 풀어 씀 |
| 표현 선택은 학습 문제의 난이도와 성능에 영향을 준다 | SEP AI 항목은 feature representation이 과제 난이도의 일부를 떠안을 수 있고, non-trivial problem에서 올바른 representation 선택이 중요하다고 설명함 | 유지 |
| 머신러닝 성공은 데이터 표현에 크게 의존한다 | Bengio et al. 리뷰는 성공이 data representation에 의존하고 표현이 설명 요인을 드러내거나 숨길 수 있다고 설명함 | 유지 |
| 파라미터는 학습 중 조정되는 내부 값이다 | Google ML Glossary는 parameter를 training 동안 모델이 배우는 weights와 biases로 설명함 | 유지. 본문에서는 `조정 가능한 내부 값`으로 일반화 |
| 가중치는 연결강도처럼 이해될 수 있는가 | Google ML Glossary는 neuron이 input value와 weight의 weighted sum을 계산한다고 설명하고, SEP AI 항목은 connectionist/neurocomputational approaches에서 dendrite에 해당하는 입력마다 numeric weight가 있다고 설명함 | 제한적으로 반영. `연결강도`는 신경망 이해를 돕는 비유로만 쓰고, 4.3의 일반 정의는 `출력 계산에 영향을 주는 내부 값`으로 유지 |
| LLM의 temperature는 모델 파라미터인가 | Google ML Glossary는 temperature를 모델 출력의 randomness를 조절하는 hyperparameter로 설명하고, parameter와 hyperparameter를 구분함 | 반영. `temperature`는 모델 내부에 학습되어 저장된 parameter가 아니라 생성/추론 시 조절하는 설정값으로 설명 |
| 인텐트 분석은 어디에 위치하는가 | Google ML Glossary는 natural language understanding을 사용자가 말하거나 입력한 것의 intentions를 결정하는 NLP의 하위 영역으로 설명함 | 반영. 인텐트는 모델 내부 파라미터가 아니라 입력을 업무 목적/라벨/중간 판단으로 해석하는 계층으로 설명 |

## 섹션 구성 검토

| 검토 항목 | 판단 |
| --- | --- |
| 4.2와의 경계 | 입력, 출력, 데이터 정의는 반복하지 않고, 그 입력이 모델 계산에 쓰이는 값으로 바뀌는 과정을 설명 |
| 3.3과의 경계 | 규칙 기반 접근과 표현 학습의 장단점 비교는 3.3에서 이미 다뤘으므로 4.3에서는 용어의 위치를 정리 |
| 4.4와의 경계 | 좋은 표현과 문제 정의의 관계를 암시하되, 평가 지표와 모델 선택은 4.4로 넘김 |
| AI 서비스 아키텍처와의 경계 | 인텐트 분석은 본문 핵심 흐름에서 분리해 `용어 경계 메모`로만 언급하고, 챗봇 구조와 도구 호출 흐름은 후속 장으로 넘김 |
| 모델 제작 절차와의 경계 | 4.3이 모델을 만드는 방법처럼 읽히지 않도록, 모델 계산을 읽기 위한 용어 정리로 범위를 명시 |
| 수학 난이도 | 선형 모델 수식은 Google 근거에 있지만 본문에서는 깊게 전개하지 않고 파라미터 직관만 사용 |

## 주의한 표현

- `특징`, `표현`, `파라미터`는 입문자가 구분해야 할 위치 개념으로 설명합니다.
- 학습된 표현이 항상 사람이 읽을 수 있는 의미 단위라고 단정하지 않습니다.
- 고객 문의 예시는 학습용 자체 예시입니다. 실제 서비스나 특정 조직의 라벨 체계가 아닙니다.
- 파라미터를 사람이 읽을 수 있는 IF-THEN 규칙처럼 설명하지 않습니다.
- `가중치`를 `연결강도`로 설명할 때는 신경망 계열의 직관적 비유로 제한하고, 4.3 전체가 신경망 설명으로 읽히지 않게 합니다.
- `temperature parameter`처럼 API나 도구 문맥에서 parameter라는 말이 쓰여도, 모델 내부 파라미터와 혼동하지 않도록 구분합니다.
- `인텐트(intent)`를 모델 내부 파라미터처럼 설명하지 않고, 자연어 입력을 업무 의도나 라벨로 해석한 결과로 제한합니다. 본문 핵심 흐름을 오염시키지 않도록 용어 경계 메모에서만 다룹니다.
- 4.3은 모델 제작법이나 학습 알고리즘 설명으로 읽히지 않도록 범위를 명시합니다.
- 딥러닝의 계층 표현, 임베딩, 역전파, 손실 함수는 Part 3과 Part 4에서 확장합니다.

## 본문에 넣지 않은 내용

- feature scaling, normalization, one-hot encoding, embedding의 세부 구현은 후속 절에서 다룹니다.
- 모델별 파라미터 구조와 학습 알고리즘은 Part 3에서 다룹니다.
- temperature, top-p, decoding strategy의 세부 동작은 LLM과 생성형 AI 장에서 다룹니다.
- 챗봇의 인텐트 라우팅, 슬롯 추출, 도구 호출 흐름은 AI 서비스 아키텍처 장에서 다룹니다.
- 딥러닝의 표현 학습 계층 구조는 Part 4에서 다룹니다.
- LLM 임베딩과 벡터 검색은 Part 5에서 다룹니다.

## 검증 필요

- `표현(representation)`을 한국어로 계속 `표현`이라고 둘지, `표현형`, `표현 벡터`, `내부 표현` 등과 어떻게 구분할지는 용어표에서 재검토합니다.
- `파라미터(parameter)`와 `하이퍼파라미터(hyperparameter)`의 구분은 Part 3에서 별도 근거와 함께 다룹니다.

## 출처

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary/), 확인 날짜: 2026-06-22.
- Google for Developers, [Supervised Learning](https://developers.google.com/machine-learning/intro-to-ml/supervised), 확인 날짜: 2026-06-22.
- Stanford Encyclopedia of Philosophy, Selmer Bringsjord and Naveen Sundar Govindarajulu, [Artificial Intelligence](https://plato.stanford.edu/entries/artificial-intelligence/), 2018-07-12, 확인 날짜: 2026-06-22.
- Yoshua Bengio, Aaron Courville, Pascal Vincent, [Representation Learning: A Review and New Perspectives](https://arxiv.org/abs/1206.5538), arXiv, 2012-06-24, 확인 날짜: 2026-06-22.
