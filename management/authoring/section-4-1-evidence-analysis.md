# 4.1 근거 분석: 모델(model, 모형)이라는 말에 익숙해지기

이 문서는 `docs/chapters/chapter-04/section-01.md`의 근거 연결을 검토한 관리 메모입니다.

원문 확인 규칙에 따라 내려받은 자료를 우선 사용했습니다. `.tmp/`의 원문 파일은 근거 검토용이며 저장소에 커밋하지 않습니다.

## 확인한 자료

| 자료 | 로컬 확인 | 본문 반영 역할 |
| --- | --- | --- |
| Stanford Encyclopedia of Philosophy, `Models in Science` | `.tmp/section-4-1-evidence/sep-models-science.html` | 과학 모델이 세계의 선택된 부분이나 측면을 대표한다는 설명, 축소 모형도 특정 측면에서만 충실하다는 설명 |
| Online Etymology Dictionary, `model` | `.tmp/section-4-1-evidence/etymonline-model.html` | `model`의 일반 의미가 축척된 유사물, 설계와 연결된다는 용어 배경 |
| Google for Developers, `Supervised Learning` | `.tmp/section-2-1-labeling-evidence/google-ml-terminology.html` | 지도학습에서 라벨이 붙은 예시를 통해 features와 label의 관계를 학습한다는 설명 |
| Google for Developers, `Machine Learning Glossary` | `.tmp/section-4-1-evidence/google-ml-glossary.html` | 학습된 모델, 추론, 특징과 라벨 관계 학습 등 용어 확인 |

## 핵심 근거 연결

| 본문 주장 | 근거 | 반영 판단 |
| --- | --- | --- |
| `model`은 축소 표현, 본, 설계의 의미와 연결된다 | Online Etymology Dictionary는 `model`의 초기 의미를 축척된 유사물과 건축 설계로 설명함 | 유지. 한국어 독자를 위해 `모형` 비유로 일반화 |
| AI 모델은 현실 전체가 아니라 목적에 맞게 줄인 계산용 모형으로 설명할 수 있다 | SEP `Models in Science`는 많은 과학 모델이 세계의 선택된 부분이나 측면을 대표한다고 설명하고, 축소 모형도 모든 면에서 완전히 충실할 수 없다고 설명함 | 유지. 엄밀한 수학 정의가 아니라 도입용 설명임을 명시 |
| 모델은 대상, 목적, 단순화, 한계를 함께 보아야 한다 | SEP의 선택된 부분/측면, 축소 모형의 제한적 충실성 설명에서 일반화 | 유지. 4.1의 핵심 일반화 축으로 사용 |
| 머신러닝 모델은 입력을 처리해 출력을 반환하는 계산 구조로 설명할 수 있다 | Google ML Glossary는 모델을 입력 데이터를 처리해 출력을 반환하는 수학적 구성물, 예측에 필요한 구조와 파라미터의 묶음으로 설명함 | 유지. 본문에서는 `계산용 모형`으로 쉽게 풀어 씀 |
| 학습 기반 모델은 데이터 사례를 통해 내부 기준과 값을 조정한다 | Google 자료는 라벨이 붙은 예시를 모델에 제공해 features와 label의 관계를 배우게 한다고 설명하고, training을 파라미터를 조정하는 과정으로 설명함 | 유지. 파라미터 상세는 4.3과 Part 3으로 보냄 |
| 모델 출력은 현실의 최종 행동이나 해결과 다르다 | 모델과 시스템의 역할 구분에 따른 저자적 일반화 | 유지. AI 과대평가를 막는 도입 관점 |

## 섹션 구성 검토

| 검토 항목 | 판단 |
| --- | --- |
| 4.1의 역할 | 모델이라는 말을 처음 받아들이기 위한 도입 섹션으로 유지 |
| 4.2와의 경계 | 입력, 출력, 데이터의 상세 설명은 4.2로 넘김. 4.1에서는 질문 목록 수준만 유지 |
| 4.3과의 경계 | 특징, 표현, 파라미터의 정의와 수학적 설명은 4.3으로 넘김 |
| 4.4와의 경계 | 좋은 문제 정의와 평가 지표의 관계는 4.4로 넘김 |
| 일반화 문장 | `모델은 어떤 대상을 어떤 목적을 위해 단순화한 계산용 표현이며, 그 단순화 때문에 유용하지만 동시에 한계를 가진다`로 정리 |

## 주의한 표현

- 4.1은 모델을 수학적으로 정의하지 않습니다. `모델 = 목적에 맞게 줄여 만든 계산용 모형`이라는 도입용 설명만 사용합니다.
- `모형` 비유는 이해를 돕기 위한 표현이며, 머신러닝 모델이 물리적 축소 모형과 같다는 뜻은 아닙니다.
- 사람의 판단과 모델의 계산을 비교하지만, 모델이 사람처럼 이해한다고 말하지 않습니다.
- `내부 기준`은 입문용 표현입니다. Google 용어집의 파라미터, 구조 설명과 연결되지만, 세부 정의는 4.3에서 다룹니다.
- 특징(feature), 표현(representation), 파라미터(parameter)는 4.3에서 다룹니다.

## 출처

- Google for Developers, [Supervised Learning](https://developers.google.com/machine-learning/intro-to-ml/supervised), 확인 날짜: 2026-06-22.
- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary/), 확인 날짜: 2026-06-22.
- Stanford Encyclopedia of Philosophy, Roman Frigg and Stephan Hartmann, [Models in Science](https://plato.stanford.edu/entries/models-science/), 최초 공개: 2006-02-27, 주요 개정: 2025-04-02, 확인 날짜: 2026-06-22.
- Online Etymology Dictionary, Douglas Harper, [model](https://www.etymonline.com/word/model), 확인 날짜: 2026-06-22.
