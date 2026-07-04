# 데이터 모델링 Part Chapter·Section 세부 설계안

## 목적

이 문서는 `03-part-outline-draft.md`의 Chapter 초안을 실제 집필 단위에 더 가깝게 세분화하기 위해 만든다.

## Chapter 1. 데이터 모델링은 무엇을 다루는가

### Section 1. 저장 구조와 문제 표현 구조는 어떻게 다른가

- 중심 질문: 데이터 모델링은 왜 DB 스키마 설명으로 끝나지 않는가
- 꼭 들어갈 것: 저장 구조, 분석 구조, 학습 구조의 차이
- 예시: 같은 원천데이터를 저장용 테이블과 분석용 샘플 표로 다르게 읽는 장면

### Section 2. 샘플, 특징, 기준선, 출력 구조를 한눈에 보기

- 중심 질문: 이 Part에서 앞으로 반복할 핵심 구성요소는 무엇인가
- 꼭 들어갈 것: sample, feature, baseline, output structure 한눈에 보는 표
- 예시: 동작 1회 사례를 한 줄 지도처럼 요약한 그림

## Chapter 2. 샘플 단위를 어떻게 정하는가

### Section 1. 행 하나가 뜻하는 것은 무엇인가

- 중심 질문: 한 행은 측정값인가, 동작 1회인가, 집계 구간인가
- 꼭 들어갈 것: row meaning, sample unit, event vs measurement
- 예시: 같은 원천데이터를 서로 다른 행 의미로 읽은 표 3개

### Section 2. 측정값과 샘플을 혼동하면 왜 문제가 생기는가

- 중심 질문: 샘플 단위가 흔들리면 어떤 후속 개념이 같이 흔들리는가
- 꼭 들어갈 것: feature 의미, label 의미, evaluation unit이 함께 흔들리는 문제
- 예시: 측정값 기준과 동작 기준을 섞었을 때 생기는 오해

Chapter 2의 공통 자산:

- `14-shared-assets-and-guards.md`의 행 의미 비교표
- `14-shared-assets-and-guards.md`의 샘플 단위 Python 예제
- `14-shared-assets-and-guards.md`의 `자동으로 실행되는 동작 1회`, `샘플 1건`, `원시 시계열`

## Chapter 3. 원시 로그를 요약 표로 바꾸는 법

### Section 1. 원시 로그, 요약 표, 집계 표의 차이

- 중심 질문: 왜 원시 시계열은 바로 데이터셋이 아닌가
- 꼭 들어갈 것: raw log, summarized row, aggregated window의 차이
- 예시: 센서 시계열 일부와 동작 1회 요약 행 비교

### Section 2. 같은 평균, 다른 패턴을 어떻게 드러내는가

- 중심 질문: 평균만 같다고 같은 동작이라고 볼 수 있는가
- 꼭 들어갈 것: pattern difference, segment summary, trend shape
- 예시: 평균은 같지만 초반/후반 흐름이 다른 두 동작

Chapter 3의 공통 자산:

- `14-shared-assets-and-guards.md`의 요약 표와 비교 표
- `14-shared-assets-and-guards.md`의 동작 요약 Python 예제
- `14-shared-assets-and-guards.md`의 `같은 평균이라도 패턴은 다를 수 있다`

## Chapter 4. 특징과 중간 표현을 설계하는 법

### Section 1. 평균, 기울기, 변동성은 왜 특징이 되는가

- 중심 질문: 어떤 요약값이 왜 feature가 되는가
- 꼭 들어갈 것: mean, slope, variance, rate of change
- 예시: 같은 원시 로그에서 서로 다른 특징 세트를 만드는 장면

### Section 2. 세그먼트 표현과 토큰화된 표현은 어디까지 쓸 수 있는가

- 중심 질문: 구간 표현과 토큰화는 어떤 장점이 있고 어디서 과장되기 쉬운가
- 꼭 들어갈 것: segment code, tokenized pattern, explainability boundary
- 예시: 상승/유지/하강 구간을 기호로 요약한 사례

Chapter 4의 공통 자산:

- `14-shared-assets-and-guards.md`의 특징 생성 예제
- `14-shared-assets-and-guards.md`의 `특징`, `동작 1회 요약 행`
- `14-shared-assets-and-guards.md`의 요약 행 관련 경계 문장

## Chapter 5. 기준선 비교와 변화 해석

### Section 1. 기준선은 왜 데이터 모델링의 일부인가

- 중심 질문: 기준선은 평가 절의 부록이 아니라 왜 표현 설계에 포함되는가
- 꼭 들어갈 것: recent window, baseline window, comparison columns
- 예시: 최근 20건과 기준선 200건 비교표

### Section 2. 변화 신호와 원인 확정을 왜 분리해야 하는가

- 중심 질문: 기준선 이탈을 바로 진단으로 읽으면 왜 위험한가
- 꼭 들어갈 것: alert candidate, review-needed, cause not confirmed
- 예시: 반복 변화는 보이지만 원인은 아직 모르는 리포트 문장

Chapter 5의 공통 자산:

- `14-shared-assets-and-guards.md`의 최근 구간 vs 기준선 표
- `14-shared-assets-and-guards.md`의 기준선 비교 예제
- `14-shared-assets-and-guards.md`의 `기준선`, `변화 신호`, `경고`, `검토 필요`
- `14-shared-assets-and-guards.md`의 경계 문장 전체

## Chapter 6. 표본 수, 반복성, 라벨, 문제 유형

### Section 1. 표본 수와 반복성은 왜 해석의 일부인가

- 중심 질문: 표본 수가 적을 때 어떤 결론을 보류해야 하는가
- 꼭 들어갈 것: sample size, repeatability, false alarm risk
- 예시: 2건 변화와 40건 반복 변화의 해석 차이

### Section 2. 경고, 검토 후보, 라벨 예측을 어떻게 구분하는가

- 중심 질문: 어떤 문제는 왜 분류기가 아니라 검토 후보 생성이 더 맞는가
- 꼭 들어갈 것: alert, review queue, label scarcity, prediction target boundary
- 예시: 확정 라벨이 부족한 상황에서 비교 리포트가 더 현실적인 이유

Chapter 6의 공통 자산:

- `03-part-outline-draft.md`의 추가 학습 축과 문제 유형 구분
- `14-shared-assets-and-guards.md`의 `적은 표본에서는 해석을 보수적으로 해야 한다`
- `15-manuscript-application-checklist.md`의 반영 체크리스트

## 집필 순서 제안

가장 먼저 쓰기 좋은 순서는 다음과 같다.

1. Chapter 2
2. Chapter 3
3. Chapter 5
4. Chapter 4
5. Chapter 6
6. Chapter 1

이 순서는 개념 정의보다 사례와 데이터 흐름을 먼저 붙잡고, 그 다음 전체 정의를 더 또렷하게 다듬는 방식이다.

## 현재 결론

이 Part는 `샘플 단위 -> 요약 구조 -> 특징 -> 기준선 -> 해석 경계`를 따라 Section 단위까지 자연스럽게 쪼갤 수 있는 상태다.
