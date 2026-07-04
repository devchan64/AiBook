# 데이터 모델링 모듈의 실제 원고 삽입 자산 지도

## 목적

이 문서는 `data-modeling-for-ai-modules`와 `brewing-shot-ai-notes`에서 정리한 내용을 실제 `docs/` 원고 파일에 어떤 자산으로 연결할지 고정한다.

여기서 말하는 자산은 다음 네 종류다.

- 공통 도입 문단
- 공통 표
- 공통 Python 예제
- 공통 경계 문장

## 기본 원칙

- 본문 파일은 아직 커밋하지 않는다.
- 먼저 어떤 자산을 어디에 넣을지 관리 문서에서 고정한다.
- 같은 사례를 모든 Section에 길게 반복하지 않는다.
- 각 Section은 현재 중심 질문에 필요한 자산만 짧게 호출한다.

## 우선 연결 대상 본문 파일

현재 우선 연결 대상으로 보는 파일은 다음과 같다.

- `docs/parts/part-02/chapter-12/section-01.md`
- `docs/parts/part-02/chapter-13/section-01.md`
- `docs/parts/part-03/chapter-07/section-01.md`
- `docs/parts/part-06/chapter-01/section-01.md`

이 파일들은 이미 사례 일반화 방향으로 일부 수정된 곳이므로, 공통 자산을 넣기 좋은 출발점이다.

## 자산 1. 공통 도입 문단

출처:

- `12-part-draft-paragraphs.md`

### Part 2용 도입

핵심 역할:

- 원시 시계열 여러 행을 동작 1회 요약 행으로 바꾸는 이유를 설명한다.

우선 삽입 후보:

- `docs/parts/part-02/chapter-12/section-01.md`

### Part 3용 도입

핵심 역할:

- 특징이 단순 계산값이 아니라 입력 표현 설계라는 점을 설명한다.

우선 삽입 후보:

- `docs/parts/part-03/chapter-07/section-01.md`

### Part 6용 도입

핵심 역할:

- 프로젝트에서 최근 구간과 기준선 비교 리포트가 왜 필요한지 설명한다.

우선 삽입 후보:

- `docs/parts/part-06/chapter-01/section-01.md`

## 자산 2. 공통 표 세트

출처:

- `11-common-example-table-set.md`

### 표 세트 A. 원시 시계열 예제

핵심 질문:

- 한 행은 무엇이고, 여러 행이 어떻게 동작 1회를 이루는가

우선 삽입 후보:

- `docs/parts/part-02/chapter-12/section-01.md`

### 표 세트 B. 동작 1회 요약 표

핵심 질문:

- 여러 행을 하나의 분석용 샘플로 바꾸면 어떤 열이 생기는가

우선 삽입 후보:

- `docs/parts/part-02/chapter-12/section-01.md`
- `docs/parts/part-03/chapter-07/section-01.md`

### 표 세트 C. 최근 구간과 기준선 비교 표

핵심 질문:

- 절대값이 아니라 비교 프레임으로 읽는다는 것은 무엇인가

우선 삽입 후보:

- `docs/parts/part-03/chapter-07/section-01.md`
- `docs/parts/part-06/chapter-01/section-01.md`

### 표 세트 D. 같은 평균, 다른 패턴 비교 표

핵심 질문:

- 평균이 같아도 패턴이 다를 수 있다는 점을 어떻게 보여 줄 것인가

우선 삽입 후보:

- `docs/parts/part-02/chapter-13/section-01.md`
- `docs/parts/part-03/chapter-07/section-01.md`

## 자산 3. 공통 Python 예제

출처:

- `13-common-python-example-plan.md`
- `14-python-example-draft-snippets.md`

### 예제 A. 원시 로그를 동작 1회로 묶기

우선 삽입 후보:

- `docs/parts/part-02/chapter-12/section-01.md`

### 예제 B. 동작 1회 요약 특징 만들기

우선 삽입 후보:

- `docs/parts/part-02/chapter-12/section-01.md`
- `docs/parts/part-03/chapter-07/section-01.md`

### 예제 C. 최근 구간과 기준선 비교하기

우선 삽입 후보:

- `docs/parts/part-03/chapter-07/section-01.md`
- `docs/parts/part-06/chapter-01/section-01.md`

### 예제 D. 같은 평균, 다른 패턴 비교하기

우선 삽입 후보:

- `docs/parts/part-02/chapter-13/section-01.md`

## 자산 4. 공통 경계 문장

출처:

- `10-next-writing-actions.md`

반복 사용 후보:

- 변화는 관찰되지만 원인은 아직 확정되지 않았다.
- 경고는 검토 우선순위를 올리기 위한 신호다.
- 적은 표본에서는 해석을 보수적으로 해야 한다.
- 같은 평균이라도 패턴은 다를 수 있다.

이 문장들은 다음 위치에서 특히 유용하다.

- Part 3 평가/기준선 비교 설명
- Part 6 프로젝트 결과 해석

## 실제 편집 순서 제안

1. `docs/parts/part-02/chapter-12/section-01.md`에 표 세트 A, B와 예제 A, B 후보를 반영한다.
2. `docs/parts/part-02/chapter-13/section-01.md`에 표 세트 D와 예제 D 후보를 반영한다.
3. `docs/parts/part-03/chapter-07/section-01.md`에 표 세트 B, C와 예제 B, C, 경계 문장을 반영한다.
4. `docs/parts/part-06/chapter-01/section-01.md`에 표 세트 C와 예제 C, 결과 해석 문장을 반영한다.

## 현재 결론

관리 노트 단계에서 준비한 공통 문단, 표, Python 예제는 이제 실제 `docs/` 파일 기준으로 삽입 후보 위치까지 연결되었다. 다음 단계는 이 지도를 따라 본문을 비커밋 상태로 순차 편집하며, 각 Section의 중심 질문에 맞는 최소 자산만 넣는 것이다.
