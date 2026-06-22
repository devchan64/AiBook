# 5.3 근거 검토 메모

이 문서는 `docs/chapters/chapter-05/section-03.md`의 근거 연결과 표현 판단을 기록한 관리 메모입니다.

## 작성 목적

- 한국어 `추론`이 `inference`, `reasoning`, `prediction`, `statistical inference`, `generation`을 함께 덮어 읽히는 문제를 줄입니다.
- 5.2에서 길게 다루지 않은 용어 혼동을 5.3의 고유 영역으로 분리합니다.
- 앞으로 원고에서 `추론`을 단독 사용하지 않고 영어 병기를 유지하는 기준을 세웁니다.

## 사용 근거

| 자료 | 사용 위치 | 반영 내용 |
| --- | --- | --- |
| Google Machine Learning Glossary, `inference` 항목 | `inference`의 중심 의미 | 전통 ML에서는 학습된 모델을 라벨 없는 예시에 적용해 prediction을 만드는 과정, LLM에서는 프롬프트에 대한 response를 생성하는 과정으로 설명 |
| Google Machine Learning Glossary, `prediction` 항목 | `prediction` 구분 | prediction은 모델의 출력이며, 분류와 회귀에서 출력 형태가 달라질 수 있음을 반영 |
| Google Machine Learning Glossary, `weight` 항목 | 5.2와의 연결 | training은 이상적인 weight를 정하고 inference는 학습된 weight로 prediction을 만든다는 구분을 유지 |
| scikit-learn Glossary, `predict` 항목 | API 예시 | `predict`는 각 sample에 대해 prediction을 만들며, classifier/regressor에서는 fitting 때 사용한 target space의 값을 반환한다는 설명을 반영 |

## 판단한 표현

| 초안 표현 | 판단 | 반영 |
| --- | --- | --- |
| `inference = 추론` | 한국어 독자에게 reasoning과 혼동될 수 있음 | 첫 등장에서는 `inference(모델 실행)` 또는 `inference(모델 적용)` 병기 |
| `reasoning = 추론` | 논리적 사고 과정의 의미를 보존해야 함 | `reasoning(논리적 추론)`으로 병기 |
| `prediction = 예측` | 모델 출력이라는 점을 강조해야 함 | `prediction(예측, 모델 출력)`으로 설명 |
| `statistical inference = 통계적 추론` | 별도 통계학 영역과 혼동 가능 | 이 절에서는 짧게 구분하고, 세부 내용은 이후 수학/통계 기초에서 다루도록 제한 |
| `LLM이 reasoning한다` | 모델 능력 주장으로 커질 위험이 있음 | `reasoning처럼 보이는 텍스트를 생성할 수 있다`로 보수화 |

## 도메인 경계

| 섹션 | 맡는 역할 |
| --- | --- |
| 5.1 | 학습과 훈련의 차이, 학습이 모델 내부 값을 바꾸는 관점 |
| 5.2 | 훈련된 모델을 실행해 출력을 만드는 inference의 기본 흐름 |
| 5.3 | `inference=추론` 번역에서 생기는 한국어 용어 혼동 정리 |
| 이후 딥러닝 장 | forward pass, backpropagation, 확률 출력, 생성 알고리즘의 기술적 설명 |
| 이후 LLM 장 | LLM의 reasoning 표현, chain-of-thought, 평가와 한계 |

## 보수화한 주장

- “LLM은 reasoning한다”라고 단정하지 않았습니다.
- “inference가 reasoning과 같다”라고 쓰지 않았습니다.
- “한국어 추론의 사전적 정의”를 외부 사전 인용 없이 단정하지 않았습니다. 본문에서는 한국어 독자가 느낄 수 있는 일반적 혼동을 설명하는 수준으로 제한했습니다.
- 통계적 추론은 Google Glossary가 의미 차이를 언급한다는 점만 반영하고, 통계학 세부 정의는 확장하지 않았습니다.

## 확인한 원문 위치

- `.tmp/section-5-1-evidence/google-ml-glossary.html`
  - `inference`: 8438-8472행 부근
  - `prediction`: 12690-12735행 부근
  - `weight`: 17182-17208행 부근
- `.tmp/section-5-1-evidence/scikit-learn-glossary.html`
  - `predict`: 1824-1845행 부근

## 남은 검토 사항

- 한국어 `추론`의 사전적 정의를 본문에 넣을 경우 국립국어원 또는 표준국어대사전 등 공개 가능한 출처를 별도 확보해야 합니다.
- `reasoning`의 철학/논리학적 설명은 이 절의 범위를 넘습니다. 필요하면 별도 섹션에서 Stanford Encyclopedia of Philosophy 같은 자료를 기준으로 검토합니다.
- LLM의 reasoning 능력, chain-of-thought, self-consistency 등은 현재 절에서 다루지 않고 LLM 장에서 근거 기반으로 재검토합니다.
