# P2-6.1 근거 분석: 최적화는 무엇을 찾는가

## Section 목적

P2-6.1은 최적화 알고리즘을 설명하는 절이 아니라, AI 학습으로 들어가기 전 최적화 문제의 기본 형태를 소개하는 절이다.

중심 질문:

```text
최적화는 여러 후보 중 무엇을 기준으로 더 나은 값을 찾는 문제인가?
```

편집 흐름:

```text
흥미 유발 질문
-> 교과서식 정의
-> 후보, 기준, 제약
-> 업무와 역사적 배경
-> 최소화와 최대화
-> AI 학습과의 연결
```

## 확인한 근거

### Stephen Boyd, Lieven Vandenberghe, Convex Optimization

- URL: https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf
- 로컬 파일: `.tmp/section-p2-6-1-evidence/boyd-vandenberghe-convex-optimization.pdf`
- 확인 날짜: 2026-06-24

검토 내용:

- 최적화 문제를 목적 함수(objective function), 변수(variables), 제약(constraints)의 관점으로 다루는 고전적 교재 자료로 확인했다.
- 본문에는 교과서식 정의를 가볍게 유지하되, 엄밀한 수식이나 볼록성 조건을 반영하지 않고 후보, 기준, 제약의 입문 설명으로 일반화했다.

### SciPy Developers, Optimization and root finding

- URL: https://docs.scipy.org/doc/scipy/reference/optimize.html
- 로컬 파일: `.tmp/section-p2-6-1-evidence/scipy-optimize.html`
- 확인 날짜: 2026-06-24

검토 내용:

- SciPy의 `optimize` 문서에서 minimization, least squares, root finding 등 최적화와 관련된 계산 도구의 범위를 확인했다.
- 본문에는 코드 사용법을 반영하지 않고, 최적화가 계산 가능한 기준을 두고 값을 찾는 문제라는 관점의 보조 근거로 사용했다.

### Ian Goodfellow, Yoshua Bengio, Aaron Courville, Deep Learning, Chapter 8

- URL: https://www.deeplearningbook.org/contents/optimization.html
- 로컬 파일: `.tmp/section-p2-6-1-evidence/deeplearningbook-optimization.html`
- 확인 날짜: 2026-06-24

검토 내용:

- 딥러닝 학습에서 최적화가 모델 학습과 연결되는 장이라는 점을 확인했다.
- 본문에는 세부 알고리즘, 경사하강법, 일반화 논쟁을 반영하지 않고, “모델 파라미터를 조정해 기준을 개선한다”는 도입 설명으로만 반영했다.

### Gary Wolf, The Optimizer

- URL: https://www.wired.com/2001/12/dantzig
- 로컬 파일: `.tmp/section-p2-6-1-evidence/wired-dantzig-optimizer.html`
- 확인 날짜: 2026-06-24

검토 내용:

- George Dantzig의 simplex method가 물류, 일정, 생산 계획 등 실제 최적화 문제와 연결되어 설명되는 사례를 확인했다.
- Wired 기사는 학술 교재가 아니라 언론 기사이므로, 본문에는 역사적 분위기와 실제 업무 연결을 보여 주는 보조 근거로만 반영했다.
- 알고리즘의 정확한 역사와 수학적 설명은 Boyd, Vandenberghe 교재 및 별도 최적화 교재에서 다루는 것이 적절하다고 판단했다.

## 표현 정리

본문에 사용한 안전한 표현:

```text
최적화는 후보를 놓고, 기준에 따라 비교하고, 제약을 지키면서 더 나은 값을 찾는 문제다.
```

```text
최적화는 AI 전용 기술이라기보다, 기준과 제약 속에서 더 나은 값을 찾으려는 오래된 계산 사고가 AI 학습 안으로 들어온 것으로 이해할 수 있다.
```

피한 표현:

```text
최적화는 항상 전역 최적해를 찾는다.
최적이라는 말은 현실에서 완벽하다는 뜻이다.
AI 학습은 오직 경사하강법 하나로 설명된다.
```

최적화 결과는 후보 범위, 기준, 제약에 의존한다는 점을 명시했다.

## 자체 제작 차트

이 절에는 설명용 SVG 차트 1개를 자체 제작해 추가했다.

| 파일 | 목적 |
| --- | --- |
| `docs/assets/part-02/chapter-06/optimization-search-loop.svg` | 변수가 후보를 만들고, 목적 함수와 제약을 통해 후보를 평가한 뒤, 더 나은 허용 후보로 반복 이동하는 흐름을 보여 준다. |

외부 도표를 복제하지 않았다.

## Section 경계

이 절에서 다룬 내용:

- 최적화의 기본 직관
- 후보(candidate), 기준(criterion), 제약(constraint)
- 물류, 제조, 광고, 서비스 운영, 검색/추천, 머신러닝 업무 예시
- 선형계획법과 운영연구로 이어지는 짧은 역사적 배경
- 최소화(minimization), 최대화(maximization)
- 최적(optimal)이라는 표현의 제한
- AI 학습을 모델 파라미터 조정 문제로 읽는 입문 관점

이 절에서 다루지 않은 내용:

- 손실 함수의 종류
- 목적 함수의 수식 구성
- 경사하강법의 업데이트 공식
- 볼록 최적화의 수학적 조건
- 선형계획법, 제약 최적화 알고리즘

이 내용은 P2-6.2, P2-6.3 및 이후 머신러닝 학습 절에서 다루는 것이 적절하다.
