# P2-5.2 근거 분석: 분포, 평균, 분산

## Section 목적

P2-5.2는 통계학 전체를 설명하는 절이 아니라, AI 학습자가 데이터 묶음을 읽기 위해 필요한 최소 통계 언어를 복구하는 절이다.

중심 질문:

```text
데이터 묶음의 모양, 중심, 퍼짐을 어떻게 읽을 것인가?
```

## 확인한 근거

### OpenStax, Introductory Statistics, 2.2 Histograms, Frequency Polygons, and Time Series Graphs

- URL: https://openstax.org/books/introductory-statistics/pages/2-2-histograms-frequency-polygons-and-time-series-graphs
- 로컬 파일: `.tmp/section-p2-5-2-evidence/openstax-intro-stats-2-2-histograms.html`
- 확인 날짜: 2026-06-24

검토 내용:

- 히스토그램(histogram)을 통해 데이터 값의 분포 형태를 시각화하는 흐름을 확인했다.
- 본문에는 히스토그램 자체의 작성법보다 “분포는 값들이 놓인 모양”이라는 입문 설명으로 반영했다.

### OpenStax, Introductory Statistics, 2.5 Measures of the Center of the Data

- URL: https://openstax.org/books/introductory-statistics/pages/2-5-measures-of-the-center-of-the-data
- 로컬 파일: `.tmp/section-p2-5-2-evidence/openstax-intro-stats-2-5-center.html`
- 확인 날짜: 2026-06-24

검토 내용:

- 평균(mean), 중앙값(median), 최빈값(mode)이 중심 경향을 나타내는 대표 도구라는 점을 확인했다.
- 이 Section의 목차는 평균을 중심으로 하므로 중앙값과 최빈값은 언급하지 않았다. 필요한 경우 이후 데이터 분석 절에서 다루는 것이 적절하다.

### OpenStax, Introductory Statistics, 2.7 Measures of the Spread of the Data

- URL: https://openstax.org/books/introductory-statistics/pages/2-7-measures-of-the-spread-of-the-data
- 로컬 파일: `.tmp/section-p2-5-2-evidence/openstax-intro-stats-2-7-spread.html`
- 확인 날짜: 2026-06-24

검토 내용:

- 범위(range), 분산(variance), 표준편차(standard deviation) 등 산포 측도의 기본 역할을 확인했다.
- 본문에는 분산을 “평균 주변의 퍼짐”으로 설명하고, 표준편차는 분산의 제곱근이라는 연결만 입문 수준으로 반영했다.

## 표현 정리

본문에 사용한 안전한 표현:

```text
분포는 값들이 놓인 모양이고, 평균은 중심을 요약하며, 분산은 중심 주변의 퍼짐을 요약한다.
```

피한 표현:

```text
평균은 데이터의 대표값으로 항상 충분하다.
분산이 작으면 좋은 데이터다.
데이터 분포와 확률분포는 같은 말이다.
```

평균과 분산은 목적과 데이터 문맥에 따라 다르게 해석되어야 하므로 좋고 나쁨으로 단정하지 않았다.

## 자체 제작 차트

이 절에는 설명용 SVG 차트 2개를 자체 제작해 추가했다. 외부 도표를 복제하지 않았고, `management/authoring/chart-guidelines.md`의 기준에 따라 차트 내부의 보이는 문구는 영어를 사용하고 한국어 설명은 본문에서 보조했다.

| 파일 | 목적 |
| --- | --- |
| `docs/assets/part-02/chapter-05/distribution-mean-variance-summary.svg` | 분포의 모양, 평균, 분산을 순서대로 읽는 관점을 보여 준다. |
| `docs/assets/part-02/chapter-05/same-mean-different-variance.svg` | 평균이 같아도 분산이 다르면 데이터의 성격이 달라질 수 있음을 보여 준다. |

## Section 경계

이 절에서 다룬 내용:

- 분포(distribution)를 값들이 놓인 모양으로 설명
- 데이터 분포(data distribution)와 확률분포(probability distribution)의 입문적 구분
- 평균(mean)의 정의와 시그마 표기 연결
- 평균만으로 부족한 이유
- 분산(variance)을 평균 주변의 퍼짐으로 설명
- 표준편차(standard deviation)의 최소 연결
- AI에서 평균 손실, 데이터 분포, 분포 이동으로 이어지는 예고

이 절에서 다루지 않은 내용:

- 정규분포의 성질
- 중앙값, 최빈값의 자세한 비교
- 공분산, 상관계수
- 표본분산과 모집단분산의 구분
- 통계적 추론과 신뢰구간

이 내용은 이후 통계 심화, 데이터 분석, 머신러닝 평가 절에서 다루는 것이 적절하다.
