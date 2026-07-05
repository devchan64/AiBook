# 데이터 모델링 Part Chapter·Section 세부 설계안

## 목적

이 문서는 `03-part-outline-draft.md`의 Chapter 초안을 실제 집필 단위에 더 가깝게 세분화하기 위해 만든다.

## 설계 원칙

- 재학습 독자가 `도구 이름`보다 `판단 순서`를 먼저 회복하게 한다.
- 외부 커리큘럼의 `wrangling`, `feature engineering`, `sampling`, `inference`를 현재 책의 사례 흐름으로 다시 배치한다.
- 각 Chapter는 뒤 Chapter가 기대는 전제를 하나씩 고정한다.

## 초심자 읽기 원칙

- Chapter 1에서는 전체 지도를 먼저 주되, 아직 세부 용어를 많이 늘리지 않는다.
- Chapter 2에서 먼저 `지금 보고 있는 것이 왜 곧바로 데이터셋이 아닌가`를 납득시킨다.
- Chapter 3과 Chapter 4에서 `행`, `표`, `샘플`의 뜻을 눈에 보이게 만든 뒤 Chapter 5로 넘어간다.
- Chapter 5보다 먼저 Chapter 6을 읽지 않게 한다. 특징이 무엇인지 모르면 기준선 비교표의 열도 제대로 읽기 어렵기 때문이다.
- Chapter 7은 기준선 비교 다음에 둔다. 무엇을 비교했는지 본 뒤에야 무엇을 말하면 안 되는지 이해할 수 있기 때문이다.
- Chapter 8과 Chapter 9는 가장 뒤에 둔다. 문제 유형과 예측 대상을 너무 일찍 꺼내면 초심자는 데이터 구조보다 모델 이름에 먼저 끌려간다.

## Chapter 1. 데이터 모델링은 데이터 생애주기 어디에 놓이는가

### Section 1. 저장 구조와 분석 구조는 어떻게 다른가

- 중심 질문: 데이터 모델링은 왜 DB 스키마 설명으로 끝나지 않는가
- 꼭 들어갈 것: 저장 구조, 분석 구조, 학습 구조의 차이
- 예시: 같은 원천데이터를 저장용 테이블과 분석용 샘플 표로 다르게 읽는 장면

### Section 2. 데이터 생애주기에서 샘플, 특징, 기준선, 출력 구조 보기

- 중심 질문: 이 Part에서 앞으로 반복할 핵심 구성요소는 무엇이며, 어디서 통계와 머신러닝으로 넘어가는가
- 꼭 들어갈 것: sample, feature, baseline, output structure 한눈에 보는 표
- 예시: 동작 1회 사례를 한 줄 지도처럼 요약한 그림

## Chapter 2. 데이터셋은 처음부터 주어지지 않는다

### Section 1. 원천데이터를 처음 보면 왜 바로 모델을 떠올리게 되는가

- 중심 질문: 초심자는 왜 눈앞의 표를 바로 데이터셋처럼 읽게 되는가
- 꼭 들어갈 것: raw data illusion, dataset illusion, model-first mistake
- 예시: 시계열 표를 보자마자 분류기부터 떠올리는 장면

### Section 2. 데이터셋은 주어진 표가 아니라 다시 만든 구조다

- 중심 질문: 데이터셋을 만든다는 말은 실제로 무엇을 다시 정한다는 뜻인가
- 꼭 들어갈 것: row meaning, table purpose, analysis-ready structure
- 예시: 같은 원천데이터를 서로 다른 표로 다시 만드는 장면

## Chapter 3. 샘플 단위를 어떻게 정하는가

### Section 1. 행 하나가 뜻하는 것은 무엇인가

- 중심 질문: 한 행은 측정값인가, 동작 1회인가, 집계 구간인가
- 꼭 들어갈 것: row meaning, sample unit, event vs measurement
- 예시: 같은 원천데이터를 서로 다른 행 의미로 읽은 표 3개

### Section 2. 측정값과 샘플을 혼동하면 왜 문제가 생기는가

- 중심 질문: 샘플 단위가 흔들리면 어떤 후속 개념이 같이 흔들리는가
- 꼭 들어갈 것: feature 의미, label 의미, evaluation unit이 함께 흔들리는 문제
- 예시: 측정값 기준과 동작 기준을 섞었을 때 생기는 오해

Chapter 3의 공통 자산:

- `14-shared-assets-and-guards.md`의 행 의미 비교표
- `14-shared-assets-and-guards.md`의 샘플 단위 Python 예제
- `14-shared-assets-and-guards.md`의 `자동으로 실행되는 동작 1회`, `샘플 1건`, `원시 시계열`

## Chapter 4. 원시 로그를 요약 표로 바꾸는 법

### Section 1. 원시 로그, 요약 표, 집계 표의 차이

- 중심 질문: 왜 원시 시계열은 바로 데이터셋이 아닌가
- 꼭 들어갈 것: raw log, summarized row, aggregated window의 차이
- 예시: 센서 시계열 일부와 동작 1회 요약 행 비교

### Section 2. 같은 평균, 다른 패턴을 어떻게 드러내는가

- 중심 질문: 평균만 같다고 같은 동작이라고 볼 수 있는가
- 꼭 들어갈 것: pattern difference, segment summary, trend shape
- 예시: 평균은 같지만 초반/후반 흐름이 다른 두 동작

Chapter 4의 공통 자산:

- `14-shared-assets-and-guards.md`의 요약 표와 비교 표
- `14-shared-assets-and-guards.md`의 동작 요약 Python 예제
- `14-shared-assets-and-guards.md`의 `같은 평균이라도 패턴은 다를 수 있다`

## Chapter 5. 특징과 중간 표현을 설계하는 법

### Section 1. 평균, 기울기, 변동성은 왜 특징이 되는가

- 중심 질문: 어떤 요약값이 왜 feature가 되는가
- 꼭 들어갈 것: mean, slope, variance, rate of change
- 예시: 같은 원시 로그에서 서로 다른 특징 세트를 만드는 장면

### Section 2. 세그먼트 표현과 토큰화된 표현은 어디까지 쓸 수 있는가

- 중심 질문: 구간 표현과 토큰화는 어떤 장점이 있고 어디서 과장되기 쉬운가
- 꼭 들어갈 것: segment code, tokenized pattern, explainability boundary
- 예시: 상승/유지/하강 구간을 기호로 요약한 사례

Chapter 5의 공통 자산:

- `14-shared-assets-and-guards.md`의 특징 생성 예제
- `14-shared-assets-and-guards.md`의 `특징`, `동작 1회 요약 행`
- `14-shared-assets-and-guards.md`의 요약 행 관련 경계 문장

## Chapter 6. 기준선 비교 구조를 읽는 법

### Section 1. 기준선은 왜 데이터 모델링의 일부인가

- 중심 질문: 기준선은 평가 절의 부록이 아니라 왜 표현 설계에 포함되는가
- 꼭 들어갈 것: recent window, baseline window, comparison columns
- 예시: 최근 20건과 기준선 200건 비교표

### Section 2. 최근 구간과 기준선 비교표는 어떻게 읽는가

- 중심 질문: 차이값과 비교 열은 어떤 순서로 읽어야 오해가 줄어드는가
- 꼭 들어갈 것: comparison columns, deltas, recent window, baseline window
- 예시: 최근 20건과 기준선 200건 비교표를 줄 단위로 읽는 장면

Chapter 6의 공통 자산:

- `14-shared-assets-and-guards.md`의 최근 구간 vs 기준선 표
- `14-shared-assets-and-guards.md`의 기준선 비교 예제
- `14-shared-assets-and-guards.md`의 `기준선`, `변화 신호`

## Chapter 7. 표본 수와 반복성은 어떻게 읽는가

### Section 1. 표본 수가 적을 때 무엇을 말하지 말아야 하는가

- 중심 질문: 적은 표본 앞에서 어떤 결론을 보류해야 하는가
- 꼭 들어갈 것: sample size, repeatability, false alarm risk
- 예시: 2건 변화와 40건 반복 변화가 같은 강도의 결론을 주지 않는 장면

### Section 2. 변화 신호와 통계적 보수성을 왜 함께 봐야 하는가

- 중심 질문: 변화 신호를 곧바로 원인 확정처럼 읽으면 왜 위험한가
- 꼭 들어갈 것: alert candidate, review-needed, cause not confirmed, uncertainty boundary
- 예시: 변화는 보이지만 원인은 아직 모르는 리포트 문장

Chapter 7의 공통 자산:

- `14-shared-assets-and-guards.md`의 `경고`, `검토 필요`
- `14-shared-assets-and-guards.md`의 경계 문장 전체
- `15-manuscript-application-checklist.md`의 표본 수 관련 점검 질문

## Chapter 8. 어떤 문제를 예측 문제로 만들 것인가

### Section 1. 경고, 검토 후보, 라벨 예측을 어떻게 구분하는가

- 중심 질문: 어떤 문제는 왜 분류기가 아니라 검토 후보 생성이 더 맞는가
- 꼭 들어갈 것: alert, review queue, label scarcity, prediction target boundary
- 예시: 확정 라벨이 부족한 상황에서 비교 리포트가 더 현실적인 이유

### Section 2. 어떤 운영 문제는 왜 비교 리포트로 남겨야 하는가

- 중심 질문: 예측 문제로 밀어 넣지 않는 편이 더 정직한 경우는 언제인가
- 꼭 들어갈 것: report-first workflow, operational boundary, label scarcity
- 예시: 같은 표에서 비교 리포트 문제와 지도학습 문제를 나눠 보는 장면

Chapter 8의 공통 자산:

- `03-part-outline-draft.md`의 문제 유형 구분
- `15-manuscript-application-checklist.md`의 반영 체크리스트

## Chapter 9. 머신러닝 Part로 무엇을 넘길 것인가

### Section 1. Part 4가 이어받을 feature와 target의 전제

- 중심 질문: 머신러닝 Part가 시작되기 전에 무엇이 이미 정리되어 있어야 하는가
- 꼭 들어갈 것: feature/target boundary, label candidate, prediction target
- 예시: 같은 데이터 구조에서 어떤 열이 feature이고 어떤 열이 target 후보인지 정리한 표

### Section 2. split, baseline, evaluation으로 넘어가기 전 확인할 것

- 중심 질문: split과 evaluation을 설명하기 전에 어떤 전제를 다시 확인해야 하는가
- 꼭 들어갈 것: train-validation-test handoff, baseline vs evaluation, unit consistency
- 예시: 샘플 단위가 흔들리면 split도 흔들리는 장면

Chapter 9의 공통 자산:

- `docs/parts/part-03/summary.md`와 `docs/parts/part-03/chapter-09/`에 반영된 Part 4 handoff 문장
- `15-manuscript-application-checklist.md`의 공통 점검 질문

## 보충학습 후보

- sampling과 bootstrap의 직관
- variance와 repeatability를 읽는 기초
- classification target과 operational label의 차이
- baseline model과 baseline window의 용어 구분

## 집필 순서 제안

가장 먼저 쓰기 좋은 순서는 다음과 같다.

1. Chapter 1
2. Chapter 2
3. Chapter 3
4. Chapter 4
5. Chapter 5
6. Chapter 6
7. Chapter 7
8. Chapter 8
9. Chapter 9

이 순서는 교육용 전개 기준이다. 집필 실무에서는 Chapter 3과 Chapter 4의 표·예제를 먼저 만들어도 되지만, 독자용 목차 전개는 `역할 지도 -> 데이터셋 환상 깨기 -> 샘플 -> 표 -> 특징 -> 기준선 비교 -> 해석 경계 -> 문제 유형 -> handoff` 순서가 더 안정적이다.

초심자에게 특히 중요한 것은 `용어를 뒤에서 설명할 수 있는 순서`가 아니라 `앞에서 생긴 질문이 다음 Chapter에서 자연스럽게 회수되는 순서`다. 현재 전개는 다음 질문 흐름을 유지한다.

1. 데이터 모델링은 왜 따로 배우는가
2. 왜 눈앞의 표가 곧바로 데이터셋처럼 보이는가
3. 한 행은 무엇을 뜻하는가
4. 원시 로그는 왜 바로 데이터셋이 아닌가
5. 무엇을 feature로 남길 것인가
6. 무엇과 비교해야 변화가 보이는가
7. 그 변화에서 어디까지 말할 수 있는가
8. 여기까지 본 뒤 무엇을 예측 문제로 만들 수 있는가
9. 머신러닝 Part는 무엇을 이어받는가

## 현재 결론

이 Part는 `역할 지도 -> 데이터셋 환상 깨기 -> 샘플 단위 -> 요약 구조 -> 특징 -> 기준선 비교 -> 해석 경계 -> 문제 유형 -> handoff`를 따라 Section 단위까지 자연스럽게 쪼갤 수 있는 상태다.
