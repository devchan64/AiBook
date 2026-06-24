# P2-6.2 근거 분석: 손실 함수와 목적 함수

## Section 목적

P2-6.2는 최적화 알고리즘을 설명하기 전에, 모델 학습에서 “무엇을 줄이거나 키우는가”를 표현하는 기준을 소개하는 절이다.

중심 질문:

```text
모델의 틀림을 어떤 숫자로 만들고, 그 숫자를 학습 기준으로 어떻게 묶는가?
```

편집 흐름:

```text
예측과 실제값의 차이
-> 손실 함수
-> 여러 샘플의 평균 손실
-> 목적 함수
-> 평가 지표와의 구분
-> 경사하강법으로 연결
```

## 확인한 근거

### Ian Goodfellow, Yoshua Bengio, Aaron Courville, Deep Learning, Chapter 5

- URL: https://www.deeplearningbook.org/contents/ml.html
- 로컬 파일: `.tmp/section-p2-6-2-evidence/deeplearningbook-ml.html`
- 확인 날짜: 2026-06-24

검토 내용:

- 모델 예측과 실제값의 차이를 평균 제곱 오차(mean squared error)로 측정하는 예시를 확인했다.
- 머신러닝 알고리즘이 비용 함수(cost function) 또는 성능 기준을 최소화하는 최적화 문제로 읽힐 수 있음을 확인했다.
- 본문에는 딥러닝 세부 이론, 가능도(maximum likelihood), 정규화 수식은 반영하지 않고, “예측의 틀림을 숫자로 만들고 줄인다”는 입문 설명으로 일반화했다.

### scikit-learn developers, Metrics and scoring

- URL: https://scikit-learn.org/stable/modules/model_evaluation.html
- 로컬 파일: `.tmp/section-p2-6-2-evidence/sklearn-model-evaluation.html`
- 확인 날짜: 2026-06-24

검토 내용:

- scikit-learn 문서에서 scoring function이 예측값과 실제값 사이의 거리를 측정하는 방식, 그리고 어떤 경우에는 training loss와 evaluation metric으로 모두 쓰일 수 있음을 확인했다.
- 평균 제곱 오차(mean squared error, MSE)의 정의와 수식을 확인했다.
- 본문에는 API 사용법을 반영하지 않고, 손실 함수와 평가 지표가 같을 수도 있고 다를 수도 있다는 경계 설명에 반영했다.

### PyTorch documentation, Loss functions

- URL: https://pytorch.org/docs/stable/nn.html#loss-functions
- 로컬 파일: `.tmp/section-p2-6-2-evidence/pytorch-loss-functions.html`
- 확인 날짜: 2026-06-24

검토 내용:

- 다운로드된 파일이 문서 본문 확인에 충분하지 않은 리다이렉트성 HTML로 확인되어 본문 근거로 사용하지 않았다.
- 손실 함수 목록의 존재는 알려져 있지만, 이번 절의 주장을 뒷받침하는 주요 근거에서는 제외했다.

## 표현 정리

본문에 사용한 안전한 표현:

```text
손실 함수는 예측의 틀림을 숫자로 바꾸는 함수다.
```

```text
목적 함수는 학습이 실제로 줄이거나 키우려는 전체 기준이다.
```

```text
손실 함수와 평가 지표는 같을 수도 있고 다를 수도 있다.
```

피한 표현:

```text
손실이 낮으면 항상 좋은 모델이다.
모든 모델은 평균 제곱 오차로 학습한다.
목적 함수와 손실 함수는 항상 같은 말이다.
평가 지표는 학습 손실과 반드시 같아야 한다.
```

## 자체 제작 차트

이 절에는 설명용 SVG 차트 1개를 자체 제작해 추가했다.

| 파일 | 목적 |
| --- | --- |
| `docs/assets/part-02/chapter-06/loss-objective-flow.svg` | 모델 예측과 실제값의 차이를 손실로 계산하고, 여러 샘플의 손실을 목적 함수로 묶는 흐름을 보여 준다. |

외부 도표를 복제하지 않았다.

## Section 경계

이 절에서 다룬 내용:

- 손실 함수(loss function)의 기본 직관
- 실제값 \(y\)와 예측값 \(\hat{y}\)
- 제곱 오차(squared error)
- 평균 제곱 오차(mean squared error, MSE)
- 손실 함수와 목적 함수(objective function)의 입문적 구분
- 손실 함수와 평가 지표(metric)의 경계

이 절에서 다루지 않은 내용:

- 회귀, 분류, 생성 문제별 손실 함수 세부 목록
- 교차 엔트로피의 확률적 해석
- 정규화와 구조적 위험 최소화
- 손실 곡면과 비볼록 최적화
- 경사하강법의 업데이트 공식

이 내용은 P2-6.3과 이후 머신러닝, 딥러닝 파트에서 다루는 것이 적절하다.
