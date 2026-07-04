# 데이터 모델링 모듈 기준 Section별 검토 순서

## 목적

이 문서는 현재 수정 상태로 남아 있는 `docs/` 원고를, `49-manuscript-insertion-prep-checklist.md`의 반영 묶음 기준으로 어떤 순서로 다시 읽고 판단할지 정리한다.

핵심은 `무작정 파일 순서`가 아니라 `같은 자산 묶음을 재사용할 수 있는 Section끼리` 검토 순서를 묶는 데 있다.

## 기본 원칙

- 이 문서는 실제 원고 수정을 즉시 강제하지 않는다.
- 먼저 `어느 묶음의 자산을 어느 Section들에 다시 적용할지`를 고정한다.
- 이미 수정된 Section이라도, 현재 중심 질문과 반영 묶음이 어긋나면 다시 읽는다.
- 커밋 정책은 유지한다. `docs/` 수정은 검토와 편집을 진행하더라도 따로 커밋하지 않는다.

## 검토 묶음 A. 샘플 단위와 원시 시계열

반영 묶음:

- `49-manuscript-insertion-prep-checklist.md`의 반영 묶음 1
- 필요 자산: `43`, `11`의 표 세트 1, `14`의 예제 1, `12`의 Part 1 후보 문단

우선 검토 Section:

- `docs/parts/part-02/chapter-12/section-01.md`
- `docs/parts/part-02/chapter-13/section-01.md`

검토 질문:

- 원시 시계열의 한 행과 동작 1회가 분명히 구분되는가
- 샘플 1건이라는 말이 표나 예제 없이 추상적으로 남지 않는가
- 원시 로그가 곧바로 모델 입력처럼 읽히지 않는가

## 검토 묶음 B. 동작 1회 요약 행과 특징

반영 묶음:

- `49-manuscript-insertion-prep-checklist.md`의 반영 묶음 2
- 필요 자산: `11`의 표 세트 2, `14`의 예제 2, `12`의 Part 2/3 후보 문단

우선 검토 Section:

- `docs/parts/part-03/chapter-07/section-01.md`
- `docs/parts/part-03/chapter-08/section-01.md`
- `docs/parts/part-03/chapter-08/section-02.md`

검토 질문:

- 요약 행이 단순 집계값이 아니라 비교 가능한 표현으로 소개되는가
- 특징이 문제 정의와 해석 가능성을 함께 담는다는 점이 보이는가
- 평균만으로 구조를 다 설명하지 못한다는 경계가 들어가는가

## 검토 묶음 C. 최근 구간과 기준선 비교

반영 묶음:

- `49-manuscript-insertion-prep-checklist.md`의 반영 묶음 3
- 필요 자산: `11`의 표 세트 3, `14`의 예제 3, `45`의 경계 문장

우선 검토 Section:

- `docs/parts/part-03/chapter-09/section-02.md`
- `docs/parts/part-03/chapter-10/section-02.md`
- `docs/parts/part-03/chapter-11/section-01.md`
- `docs/parts/part-03/chapter-11/section-02.md`
- `docs/parts/part-03/chapter-12/section-01.md`
- `docs/parts/part-03/chapter-12/section-02.md`
- `docs/parts/part-06/chapter-01/section-01.md`
- `docs/parts/part-06/chapter-01/section-02.md`

검토 질문:

- 최근 구간과 기준선이 무엇을 비교하는지 문맥 안에서 스스로 설명되는가
- 차이값을 변화 신호로 읽고 원인 확정과 분리하는가
- 경고가 검토 우선순위 신호라는 점이 문단 끝까지 유지되는가

## 검토 묶음 D. 같은 평균, 다른 패턴

반영 묶음:

- `49-manuscript-insertion-prep-checklist.md`의 반영 묶음 4
- 필요 자산: `11`의 표 세트 4, `14`의 예제 4, `45`의 평균 관련 경계 문장

우선 검토 Section:

- `docs/parts/part-03/chapter-13/section-01.md`
- `docs/parts/part-03/chapter-13/section-02.md`
- `docs/parts/part-03/chapter-14/section-01.md`
- `docs/parts/part-03/chapter-14/section-02.md`
- `docs/parts/part-03/chapter-15/section-01.md`
- `docs/parts/part-03/chapter-15/section-02.md`
- `docs/parts/part-03/chapter-15/section-03.md`
- `docs/parts/part-03/chapter-16/section-01.md`
- `docs/parts/part-03/chapter-16/section-02.md`

검토 질문:

- 모델 비교가 점수 차이만의 문제가 아니라 패턴 해석 차이와 연결되는가
- 같은 평균이라도 실패 양상이 다를 수 있다는 관점이 살아 있는가
- baseline 비교와 대표 오류 사례가 함께 읽히는가

## 검토 묶음 E. 표본 수, 반복성, 경고 해석

반영 묶음:

- `45-overstatement-guard-sentences.md`
- `43-common-vocabulary-and-usage-map.md`의 `경고`, `검토 필요`, `변화 신호`

우선 검토 Section:

- `docs/parts/part-03/chapter-17/section-01.md`
- `docs/parts/part-03/chapter-17/section-02.md`
- `docs/parts/part-03/chapter-18/section-01.md`
- `docs/parts/part-03/chapter-18/section-02.md`
- `docs/parts/part-03/chapter-19/section-01.md`
- `docs/parts/part-03/chapter-19/section-02.md`
- `docs/parts/part-03/chapter-19/section-03.md`
- `docs/parts/part-03/chapter-19/section-04.md`
- `docs/parts/part-03/index.md`
- `docs/parts/part-03/summary.md`
- `docs/parts/part-06/chapter-02/section-01.md`
- `docs/parts/part-06/chapter-02/section-02.md`
- `docs/parts/part-06/chapter-03/section-01.md`
- `docs/parts/part-06/chapter-03/section-02.md`
- `docs/parts/part-06/chapter-04/section-01.md`
- `docs/parts/part-06/chapter-04/section-02.md`
- `docs/parts/part-06/chapter-05/section-01.md`
- `docs/parts/part-06/chapter-05/section-02.md`
- `docs/parts/part-06/chapter-06/section-01.md`
- `docs/parts/part-06/chapter-06/section-02.md`
- `docs/parts/part-06/chapter-07/section-01.md`
- `docs/parts/part-06/chapter-07/section-02.md`

검토 질문:

- 적은 표본에서 해석을 보수적으로 해야 한다는 경계가 유지되는가
- 경고와 진단, 실패 기록과 원인 확정이 섞이지 않는가
- 개선 기록이 다음 질문과 연결되는가

## 실제 진행 순서

1. Part 2에서 샘플 단위와 요약 구조를 다시 맞춘다.
2. Part 3 초반에서 특징과 입력 표현 설계를 맞춘다.
3. Part 3 평가 축과 Part 6 초입에서 기준선 비교와 경고 문장을 맞춘다.
4. Part 3 모델 비교 축에서 `같은 평균, 다른 패턴` 관점을 반복 점검한다.
5. Part 3 후반과 Part 6 회고 축에서 표본 수, 반복성, 경고 해석 언어를 끝까지 맞춘다.

## 현재 진행 상태

현재 워크트리 기준으로 위 5단계에 들어 있던 Part 2, Part 3, Part 6 대상 Section의 1차 순차 검토는 한 번 완료했다.

- Part 2 대상: `chapter-12/section-01`, `chapter-13/section-01`
- Part 3 대상: 묶음 B부터 E에 포함된 Section과 `part-03/index.md`, `part-03/summary.md`
- Part 6 대상: `chapter-01/section-01`부터 `chapter-07/section-02`까지 묶음 C와 E에 포함된 전체 Section

이 완료 상태는 `53`부터 `97`까지의 검토 로그와 큐 갱신 로그에서 이어서 추적한다.

다음 라운드에서 이 순서를 다시 열 조건은 다음과 같이 둔다.

- 새 본문 확장 위치가 생겨 같은 자산 묶음을 다시 호출해야 할 때
- 기존 문장이 과장되거나 현재 공통 어휘와 충돌하는 사례가 새로 발견될 때
- 관리 문서 압축 또는 역할 재정리가 필요해 완료 범위를 다시 묶어야 할 때

## 현재 결론

다음 `docs/` 검토 라운드는 개별 파일을 흩어지게 읽기보다, 이 문서의 묶음 순서대로 같은 자산과 같은 경계 문장을 재사용하는 방식으로 진행하는 편이 가장 안정적이다. 다만 현재 라운드는 한 번 닫힌 상태로 보고, 위 재개 조건이 생길 때 다시 여는 편이 맞다.
