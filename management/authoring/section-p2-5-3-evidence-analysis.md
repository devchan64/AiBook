# P2-5.3 근거 분석: 표본, 추정, 오차

## Section 목적

P2-5.3은 통계적 추론 전체를 다루는 절이 아니라, AI 학습자가 데이터셋을 현실 전체가 아닌 표본으로 이해하도록 돕는 절이다.

중심 질문:

```text
전체를 다 볼 수 없을 때, 일부 데이터로 무엇을 추정하고 어떤 오차를 인정해야 하는가?
```

## 확인한 근거

### OpenStax, Introductory Statistics, 1.2 Data, Sampling, and Variation in Data and Sampling

- URL: https://openstax.org/books/introductory-statistics/pages/1-2-data-sampling-and-variation-in-data-and-sampling
- 로컬 파일: `.tmp/section-p2-5-3-evidence/openstax-intro-stats-1-2-sampling.html`
- 확인 날짜: 2026-06-24

검토 내용:

- 데이터, 표본, 표본추출, 변동의 기본 개념을 확인했다.
- 본문에는 표본을 모집단에서 실제 관측한 일부로 설명하고, 표본이 달라지면 추정값도 달라질 수 있다는 관점으로 반영했다.

### OpenStax, Introductory Statistics, 7 Introduction

- URL: https://openstax.org/books/introductory-statistics/pages/7-introduction
- 로컬 파일: `.tmp/section-p2-5-3-evidence/openstax-intro-stats-7-introduction.html`
- 확인 날짜: 2026-06-24

검토 내용:

- 표본 평균과 관련된 표본분포(sampling distribution) 장의 도입을 확인했다.
- 본문에는 표본 통계량이 모집단 값을 추정하는 데 사용된다는 입문 설명만 반영했다.

### OpenStax, Introductory Statistics, 7.1 The Central Limit Theorem for Sample Means

- URL: https://openstax.org/books/introductory-statistics/pages/7-1-the-central-limit-theorem-for-sample-means-averages
- 로컬 파일: `.tmp/section-p2-5-3-evidence/openstax-intro-stats-7-1-clt-sample-means.html`
- 확인 날짜: 2026-06-24

검토 내용:

- 표본 평균의 분포와 중심극한정리 관련 설명을 확인했다.
- 이 Section에서는 중심극한정리를 설명하지 않고, 표본 평균이 달라질 수 있다는 직관의 배경 자료로만 사용했다.

## 표현 정리

본문에 사용한 안전한 표현:

```text
표본은 모집단 전체가 아니라 실제 관측한 일부이고, 추정값은 그 일부로 전체 값을 짐작한 결과다.
```

피한 표현:

```text
표본이 크면 항상 모집단을 완벽히 대표한다.
테스트 점수는 현실 성능을 증명한다.
오차는 단순히 실패를 뜻한다.
```

표본 수가 커도 수집 방식이 치우치면 편향이 생길 수 있고, 테스트 점수도 특정 표본에서 얻은 추정값이므로 단정하지 않았다.

## 자체 제작 차트

이 절에는 설명용 SVG 차트 3개와 Mermaid 도식 2개를 자체 제작해 추가했다. 외부 도표를 복제하지 않았고, `management/authoring/chart-guidelines.md`의 기준에 따라 차트 내부의 보이는 문구는 영어를 사용하고 한국어 설명은 본문에서 보조했다.

| 형식 | 목적 |
| --- | --- |
| Mermaid: `section-03.md` 본문 | 모집단, 표본, 데이터셋의 포함 관계와 정리 흐름을 보여 준다. |
| SVG: `docs/assets/part-02/chapter-05/population-sample-estimate.svg` | 모집단에서 표본을 뽑고 표본으로 추정값을 만드는 흐름을 보여 준다. |
| SVG: `docs/assets/part-02/chapter-05/estimate-error-gap.svg` | 추정값과 실제 값 사이의 차이를 오차로 보는 관점을 보여 준다. |
| SVG: `docs/assets/part-02/chapter-05/sampling-variation-vs-bias.svg` | 표본추출 변동과 표본 편향의 차이를 비교한다. |
| Mermaid: `section-03.md` 본문 | 현실 세계의 일부가 데이터셋이 되고, 다시 훈련/테스트 표본으로 나뉘는 흐름을 보여 준다. |

## Section 경계

이 절에서 다룬 내용:

- 모집단(population)과 표본(sample)의 구분
- 추정(estimation), 추정값(estimate), 오차(error)의 관계
- 통계의 모수(parameter)와 모델 파라미터(model parameter)의 용어 구분
- 표본추출 변동(sampling variation)
- 표본 편향(sampling bias)
- 데이터셋(dataset)을 수집된 표본이 구조화된 형태로 보는 관점
- 훈련 데이터와 테스트 데이터를 표본 관점으로 읽는 방법

이 절에서 다루지 않은 내용:

- 신뢰구간
- 가설검정
- 표준오차 계산
- 중심극한정리의 엄밀한 설명
- 교차검증의 실제 절차
- 편향-분산 트레이드오프

이 내용은 이후 통계 심화, 머신러닝 평가, 일반화 절에서 다루는 것이 적절하다.
