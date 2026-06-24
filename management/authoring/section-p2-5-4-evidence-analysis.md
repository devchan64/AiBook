# P2-5.4 근거 분석: 확률과 통계를 작은 데이터로 확인하기

## Section 목적

P2-5.4는 P2-5.1부터 P2-5.3까지의 확률과 통계 입문 개념을 작은 데이터와 코드로 확인하는 실습형 절이다.

중심 질문:

```text
평균, 중위값, 분산, 표본 평균은 작은 데이터와 코드에서 어떤 모양으로 확인되는가?
```

## 확인한 근거

### NumPy Developers, numpy.mean

- URL: https://numpy.org/doc/stable/reference/generated/numpy.mean.html
- 로컬 파일: `.tmp/section-p2-5-4-evidence/numpy-mean.html`
- 확인 날짜: 2026-06-24

검토 내용:

- NumPy의 평균 계산 함수 `numpy.mean` 문서를 확인했다.
- 본문에는 `np.mean(data)`로 작은 배열의 평균을 계산하는 예제만 반영했다.

### NumPy Developers, numpy.var

- URL: https://numpy.org/doc/stable/reference/generated/numpy.var.html
- 로컬 파일: `.tmp/section-p2-5-4-evidence/numpy-var.html`
- 확인 날짜: 2026-06-24

검토 내용:

- NumPy의 분산 계산 함수 `numpy.var`와 `ddof` 인자를 확인했다.
- 본문에는 `np.var(data)`와 `np.var(data, ddof=1)`의 차이를 “데이터를 전체로 볼 것인가, 표본으로 볼 것인가”라는 입문 수준 설명으로 반영했다.

### NumPy Developers, numpy.median

- URL: https://numpy.org/doc/stable/reference/generated/numpy.median.html
- 로컬 파일: `.tmp/section-p2-5-4-evidence/numpy-median.html`
- 확인 날짜: 2026-06-24

검토 내용:

- NumPy의 중위값 계산 함수 `numpy.median` 문서를 확인했다.
- 본문에는 극단값이 있는 작은 데이터에서 평균과 중위값이 다르게 보일 수 있다는 입문 예제로 반영했다.

### OpenStax, Introductory Statistics, 1.2 Data, Sampling, and Variation in Data and Sampling

- URL: https://openstax.org/books/introductory-statistics/pages/1-2-data-sampling-and-variation-in-data-and-sampling
- 로컬 파일: `.tmp/section-p2-5-4-evidence/openstax-intro-stats-1-2-sampling.html`
- 확인 날짜: 2026-06-24

검토 내용:

- 데이터, 표본, 표본추출 변동의 기본 개념을 확인했다.
- 본문에는 표본을 바꾸면 표본 평균이 달라질 수 있다는 실습 예제로만 반영했다.

## 표현 정리

본문에 사용한 안전한 표현:

```text
코드 출력은 판단의 끝이 아니라 해석의 시작이다.
```

피한 표현:

```text
NumPy 결과가 나오면 통계 해석도 완료된다.
표본 평균은 전체 평균과 같다.
분산이 크면 데이터가 나쁘다.
```

계산 결과와 데이터 해석을 분리했다. 평균, 중위값, 분산을 코드로 확인하되, 표본 대표성과 수집 방식은 별도로 검토해야 한다는 관점을 유지했다.

## 자체 제작 자료

이 절에는 자체 제작 SVG 차트와 예제 코드 파일을 추가했다.

| 파일 | 목적 |
| --- | --- |
| `docs/assets/part-02/chapter-05/small-data-statistics-check.svg` | 작은 데이터에서 원자료, 중심, 퍼짐, 표본 추정을 구분해 확인하는 흐름을 보여 준다. |
| `docs/assets/part-02/chapter-05/p2_5_4_small_statistics.py` | 본문에 나온 평균, 분산, 표본 평균 예제를 한 번에 실행한다. |

외부 차트나 외부 코드를 복제하지 않았다.

## Section 경계

이 절에서 다룬 내용:

- 작은 데이터 배열 만들기
- 평균 계산
- 중위값 계산
- 극단값이 평균에 주는 영향
- 평균 중심화
- 제곱 편차와 분산
- 모집단 분산과 표본 분산의 계산 설정 차이
- 표본이 달라질 때 표본 평균이 달라지는 예
- 코드 출력값과 통계 해석의 구분

이 절에서 다루지 않은 내용:

- 정규분포
- 표준편차의 엄밀한 유도
- 표준오차
- 신뢰구간
- 가설검정
- 확률 시뮬레이션

이 내용은 이후 통계 심화, 머신러닝 평가, 데이터 분석 실습에서 다루는 것이 적절하다.
