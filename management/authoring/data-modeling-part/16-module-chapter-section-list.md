# 데이터 모델링 Part 모듈·챕터·섹션 목록

## 목적

이 문서는 `Part 3 데이터 모델링`을 재학습용 커리큘럼 관점에서 `모듈 -> 챕터 -> 섹션` 구조로 다시 정리한 기준표다.

기존 문서가 Chapter와 Section의 설계를 설명했다면, 이 문서는 다음 판단을 더 쉽게 하도록 만든다.

- 독자가 어떤 학습 묶음을 순서대로 밟는가
- 각 Chapter가 어느 모듈에 속하는가
- 각 Section이 무엇을 고정한 뒤 다음 Chapter로 넘기는가
- 실제 집필과 `docs/parts/part-03/` 배치에서 어떤 단위로 작업할 것인가

## 구성 원칙

- 모듈은 `재학습자가 회복해야 할 판단 단위`를 기준으로 나눈다.
- Chapter는 모듈 안에서 하나의 핵심 질문 묶음을 맡는다.
- Section은 Chapter의 중심 질문을 실제 원고 단위로 푼다.
- 모듈 이름은 대학 커리큘럼 용어를 그대로 복사하지 않고, 현재 책의 사례 흐름으로 다시 쓴다.

## 처음 보는 독자를 위한 순서 원칙

- 처음에는 `feature engineering`, `inference`, `baseline` 같은 이름보다 `지금 무엇을 정하는 단계인가`가 먼저 보여야 한다.
- 독자가 아직 모르는 용어로 다음 용어를 설명하지 않는다.
- 먼저 `행이 무엇인가`, `표가 무엇을 뜻하는가`를 고정한 뒤에야 feature와 비교 구조로 넘어간다.
- 비교 구조가 아직 없을 때는 경고, 이상, 원인 같은 결론형 표현을 앞세우지 않는다.
- 예측 문제는 가장 뒤에서 다룬다. 처음 보는 독자에게는 `무엇을 예측할 것인가`보다 `무엇을 한 건으로 볼 것인가`가 먼저다.

## 전체 모듈 목록

| 모듈 | 역할 | 포함 Chapter | 외부 커리큘럼과의 연결 |
| --- | --- | --- | --- |
| Module 1. 역할 지도 | 데이터 모델링이 데이터 생애주기 어디에 놓이는지 고정 | Chapter 1 | problem framing, data lifecycle |
| Module 2. 데이터셋 환상 깨기 | 원천데이터와 데이터셋의 차이를 먼저 납득시킴 | Chapter 2 | dataset construction, analysis-ready table |
| Module 3. 샘플 정의 | 한 행과 한 샘플의 차이를 고정 | Chapter 3 | sample unit, data representation |
| Module 4. 표 구조 변환 | 원시 로그를 분석 가능한 표로 바꾸는 흐름 고정 | Chapter 4 | data wrangling, analysis-ready table |
| Module 5. 특징 설계 | feature를 표현 설계로 이해하게 함 | Chapter 5 | feature engineering, representation |
| Module 6. 비교 구조 읽기 | 기준선 비교 구조를 먼저 읽게 함 | Chapter 6 | baseline comparison, analysis table |
| Module 7. 해석 경계 | 보수적 해석과 불확실성 경계를 고정 | Chapter 7 | sampling, inference, uncertainty |
| Module 8. 문제 유형 구분 | 경고, 검토, 예측 문제를 나눔 | Chapter 8 | problem framing, operational labels |
| Module 9. 머신러닝 handoff | Part 4가 이어받을 전제를 정리 | Chapter 9 | classification/regression handoff |

## 모듈별 상세 목록

### Module 1. 역할 지도

- 목표: 데이터 모델링을 DB 설계나 전처리 하위 절로 축소하지 않게 한다.
- 포함 Chapter:
  - Chapter 1. 데이터 모델링은 데이터 생애주기 어디에 놓이는가
- 포함 Section:
  - Section 1. 저장 구조와 분석 구조는 어떻게 다른가
  - Section 2. 데이터 생애주기에서 샘플, 특징, 기준선, 출력 구조 보기
- 이 모듈이 끝나면:
  - 독자는 데이터 모델링이 `저장 -> 분석 -> 학습` 사이에서 어떤 역할을 하는지 설명할 수 있어야 한다.
  - 뒤 Chapter에서 나오는 sample, feature, baseline이 왜 같은 흐름에 묶이는지 이해해야 한다.

### Module 2. 데이터셋 환상 깨기

- 목표: 처음 보는 독자가 눈앞의 표를 곧바로 데이터셋처럼 읽는 습관을 먼저 흔든다.
- 포함 Chapter:
  - Chapter 2. 데이터셋은 처음부터 주어지지 않는다
- 포함 Section:
  - Section 1. 원천데이터를 처음 보면 왜 바로 모델을 떠올리게 되는가
  - Section 2. 데이터셋은 주어진 표가 아니라 다시 만든 구조다
- 이 모듈이 끝나면:
  - 원천데이터와 데이터셋이 처음부터 같은 것이 아니라는 점을 설명할 수 있어야 한다.
  - 왜 데이터 모델링을 배우지 않으면 모델 이름부터 먼저 떠올리게 되는지 이해해야 한다.

### Module 3. 샘플 정의

- 목표: `한 행이 곧 샘플 1건`이라는 자동 가정을 깨고, 샘플 단위를 먼저 정하게 한다.
- 포함 Chapter:
  - Chapter 3. 샘플 단위를 어떻게 정하는가
- 포함 Section:
  - Section 1. 행 하나가 뜻하는 것은 무엇인가
  - Section 2. 측정값과 샘플을 혼동하면 왜 문제가 생기는가
- 이 모듈이 끝나면:
  - 측정값 표, 동작 단위 표, 최근 구간 표, 기준선 표를 구분할 수 있어야 한다.
  - feature, label, evaluation unit이 샘플 단위에 기대고 있음을 설명할 수 있어야 한다.

### Module 4. 표 구조 변환

- 목표: 원시 로그, 요약 표, 집계 표를 서로 다른 층위의 표로 이해하게 한다.
- 포함 Chapter:
  - Chapter 4. 원시 로그를 요약 표로 바꾸는 법
- 포함 Section:
  - Section 1. 원시 로그, 요약 표, 집계 표의 차이
  - Section 2. 같은 평균, 다른 패턴을 어떻게 드러내는가
- 이 모듈이 끝나면:
  - 원시 로그가 곧바로 데이터셋이 아니라는 점을 설명할 수 있어야 한다.
  - 같은 평균이라도 다른 패턴을 가진 동작을 요약 표에서 어떻게 드러내는지 말할 수 있어야 한다.

### Module 5. 특징 설계

- 목표: feature를 열 선택이 아니라 표현 설계로 이해하게 한다.
- 포함 Chapter:
  - Chapter 5. 특징과 중간 표현을 설계하는 법
- 포함 Section:
  - Section 1. 평균, 기울기, 변동성은 왜 특징이 되는가
  - Section 2. 세그먼트 표현과 토큰화된 표현은 어디까지 쓸 수 있는가
- 이 모듈이 끝나면:
  - 왜 어떤 요약값은 feature가 되고 어떤 값은 아직 설명력이 약한지 말할 수 있어야 한다.
  - 설명 가능한 표현과 과장된 표현의 경계를 구분할 수 있어야 한다.

### Module 6. 비교 구조 읽기

- 목표: 기준선 비교표와 차이 열을 읽는 순서를 먼저 고정한다.
- 포함 Chapter:
  - Chapter 6. 기준선 비교 구조를 읽는 법
- 포함 Section:
  - Section 1. 기준선은 왜 데이터 모델링의 일부인가
  - Section 2. 최근 구간과 기준선 비교표는 어떻게 읽는가
- 이 모듈이 끝나면:
  - 최근 구간, 기준선, 차이값이 왜 같은 비교 구조에 속하는지 설명할 수 있어야 한다.
  - 비교표의 열을 어떤 순서로 읽어야 오해가 줄어드는지 말할 수 있어야 한다.

### Module 7. 해석 경계

- 목표: 변화 신호를 곧바로 원인 확정처럼 읽지 않게 한다.
- 포함 Chapter:
  - Chapter 7. 표본 수와 반복성은 어떻게 읽는가
- 포함 Section:
  - Section 1. 표본 수가 적을 때 무엇을 말하지 말아야 하는가
  - Section 2. 변화 신호와 통계적 보수성을 왜 함께 봐야 하는가
- 이 모듈이 끝나면:
  - 적은 표본과 낮은 반복성 앞에서 왜 해석을 보수적으로 해야 하는지 말할 수 있어야 한다.
  - 변화는 관찰되지만 원인은 아직 확정되지 않았다는 문장을 자연스럽게 이해해야 한다.

### Module 8. 문제 유형 구분

- 목표: 비교 리포트, 검토 큐, 예측 문제의 경계를 정리한다.
- 포함 Chapter:
  - Chapter 8. 어떤 문제를 예측 문제로 만들 것인가
- 포함 Section:
  - Section 1. 경고, 검토 후보, 라벨 예측을 어떻게 구분하는가
  - Section 2. 어떤 운영 문제는 왜 비교 리포트로 남겨야 하는가
- 이 모듈이 끝나면:
  - 어떤 문제는 아직 분류기가 아니라 검토 우선순위 문제라는 점을 설명할 수 있어야 한다.
  - 예측 문제로 밀어 넣지 않는 편이 더 정직한 운영 문제를 구분할 수 있어야 한다.

### Module 9. 머신러닝 handoff

- 목표: Part 4가 이어받을 feature, target, split, evaluation 전제를 정리한다.
- 포함 Chapter:
  - Chapter 9. 머신러닝 Part로 무엇을 넘길 것인가
- 포함 Section:
  - Section 1. Part 4가 이어받을 feature와 target의 전제
  - Section 2. split, baseline, evaluation으로 넘어가기 전 확인할 것
- 이 모듈이 끝나면:
  - 머신러닝 Part가 이어받을 feature, target, split, evaluation의 전제를 명확히 말할 수 있어야 한다.

## 모듈 기준 집필 우선순위

1. Module 1. 역할 지도
2. Module 2. 데이터셋 환상 깨기
3. Module 3. 샘플 정의
4. Module 4. 표 구조 변환
5. Module 5. 특징 설계
6. Module 6. 비교 구조 읽기
7. Module 7. 해석 경계
8. Module 8. 문제 유형 구분
9. Module 9. 머신러닝 handoff

이 순서는 독자용 학습 순서다. 집필 실무에서는 Module 2와 Module 3의 표와 Python 예제를 먼저 만들어도 되지만, 최종 커리큘럼 설명은 위 순서를 기준으로 고정한다.

초심자 기준에서 이 순서가 읽히는 이유는 다음과 같다.

- Module 1은 전체 지도를 먼저 줘서 뒤에 나올 용어가 공중에 뜨지 않게 한다.
- Module 2는 `눈앞의 표가 곧바로 데이터셋은 아니다`라는 직관을 먼저 만들어 초반 속도를 늦춘다.
- Module 3은 가장 자주 생기는 오해인 `한 행 = 샘플 1건`을 먼저 바로잡는다.
- Module 4는 원시 로그와 분석용 표의 차이를 보여 줘서 데이터 정리가 왜 필요한지 납득시키기 쉽다.
- Module 5는 그 다음에야 feature를 `설계된 표현`으로 받아들일 준비가 된다.
- Module 6은 비교 구조를 먼저 읽게 해서 기준선 표가 낯선 표가 되지 않게 한다.
- Module 7은 그 뒤에야 보수적 해석을 말해도 무엇을 두고 보수적으로 말하는지 이해할 수 있다.
- Module 8은 앞선 구조를 다 본 뒤에야 `비교 리포트`, `검토 큐`, `예측 문제`의 차이를 무리 없이 받아들일 수 있다.
- Module 9는 마지막에야 머신러닝 Part로 넘길 전제를 정리해 모델 이름이 너무 빨리 튀어나오지 않게 한다.

반대로 이 순서를 어기면 초심자는 다음처럼 막히기 쉽다.

- feature를 열 이름 정도로 오해한다.
- baseline을 모델 평가 용어로만 읽는다.
- 경고를 원인 확정처럼 읽는다.
- 예측 문제를 너무 일찍 세워 라벨이 없는 상황을 설명하지 못한다.

## docs 배치 대응표

| 모듈 | docs 경로 |
| --- | --- |
| Module 1 | `docs/parts/part-03/chapter-01/section-01.md`, `section-02.md` |
| Module 2 | `docs/parts/part-03/chapter-02/section-01.md`, `section-02.md` |
| Module 3 | `docs/parts/part-03/chapter-03/section-01.md`, `section-02.md` |
| Module 4 | `docs/parts/part-03/chapter-04/section-01.md`, `section-02.md` |
| Module 5 | `docs/parts/part-03/chapter-05/section-01.md`, `section-02.md` |
| Module 6 | `docs/parts/part-03/chapter-06/section-01.md`, `section-02.md` |
| Module 7 | `docs/parts/part-03/chapter-07/section-01.md`, `section-02.md` |
| Module 8 | `docs/parts/part-03/chapter-08/section-01.md`, `section-02.md` |
| Module 9 | `docs/parts/part-03/chapter-09/section-01.md`, `section-02.md` |

## 현재 결론

Part 3 데이터 모델링은 9개 모듈, 9개 Chapter, 18개 Section으로 운영하는 편이 더 안정적이다. 이 구조는 외부 커리큘럼의 반복 항목을 흡수하면서도, 현재 책이 사용하는 `자동으로 실행되는 동작 1회와 그 원천 시계열` 사례 흐름을 유지하고 초심자 부담을 더 고르게 나눌 수 있다.
