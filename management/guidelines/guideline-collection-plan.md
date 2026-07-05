# 가이드라인 수집 준비안

## 목적

`management/authoring` 아래에 있는 문서 중에서 `책 원고 세부 작성 전에 다시 확인하는 기준 문서`를 추려, 이후 `management/guidelines`로 모을 준비를 한다.

여기서 말하는 가이드라인은 다음 성격을 가진 문서다.

- 책 원고 집필이나 편집 전에 확인하는 기준
- 차트, 예시, 보충학습, 체크리스트처럼 특정 작업 흐름에서 반복 참조하는 문서
- 조사 결과 자체보다 `어떻게 판단할 것인가`를 적은 문서

반대로 다음은 우선 이동 대상이 아니다.

- 저장소 전체 운영 규칙
- 커리큘럼 조사 문서
- 개별 챕터 분석 메모
- 근거 검토 메모
- 일회성 감사 기록

## 1차 후보 분류

### A. 저장소 규칙 원문

이 문서들은 가이드라인으로 보지 않고, 저장소 규칙 원문으로 별도 유지한다.

- `AGENTS.md`

판단:

- 저장소 전체 규칙 원문이다.
- 책 원고 세부 작성 규칙만 담은 문서가 아니다.
- 현재는 저장소 루트에 두는 편이 더 자연스럽다.
- `guidelines` 수집 대상에서는 제외한다.

### B. 원고 세부 작성 가이드 후보

이 문서들은 `guidelines`로 모으기 가장 쉬운 후보다.

- `management/authoring/chart-guidelines.md`
- `management/authoring/rules-and-guidelines-summary.md`

판단:

- 반복 참조 빈도가 높다.
- 저장소 운영 규칙보다 본문 작성과 시각화 작업에 직접 연결된다.
- 이후 `writing`, `charts`, `workflow` 같은 하위 묶음으로 나눌 수 있다.

### C. 작업 큐 문서

이 문서들은 가이드라인으로 보지 않고, `part별 작업 큐`로 분리해 다룬다.

- `management/authoring/part-01-open-checklist.md`
- `management/authoring/part-02-open-checklist.md`
- `management/authoring/part-03-open-checklist.md`
- `management/authoring/part-04-open-checklist.md`
- `management/authoring/part-05-open-checklist.md`
- `management/authoring/part-06-open-checklist.md`
- `management/authoring/part-07-open-checklist.md`

판단:

- 진행 상태와 미완료 항목을 관리하는 문서다.
- 반복 참조하는 기준 문서라기보다 현재 남은 작업 목록에 가깝다.
- `guidelines` 수집 대상에서는 제외한다.

### D. 이동 보류 문서

이 문서들은 기준 일부를 담고 있어도 현재는 `분석 메모`나 `조사/설계 문서` 성격이 더 강하다.

- `management/authoring/ai-intro-curriculum-survey.md`
- `management/authoring/table-of-contents.md`
- `management/authoring/section-paragraph-structure-analysis.md`
- `management/authoring/part-quality-analysis.md`
- `management/authoring/part-quality-next-round-plan.md`
- `management/authoring/part-02-detailed-quality-analysis.md`
- `management/authoring/part-05-detailed-quality-analysis.md`
- `management/authoring/part-06-detailed-quality-analysis.md`
- `management/authoring/evidence-analysis-disposal-audit.md`
- `management/authoring/chapter-04-domain-review.md`
- `management/authoring/chapter-04-reference-candidates.md`

판단:

- 반복 참조용 기준이라기보다 특정 시점의 판단 기록이다.
- `guidelines`로 옮기면 오히려 규칙 문서와 분석 메모가 섞일 수 있다.

## 추천 구조 초안

실제 수집을 진행한다면 우선 다음 구조를 검토한다.

```text
management/guidelines/
  README.md
  guideline-collection-plan.md
  writing/
  charts/
```

### writing

- 집필 규칙 요약
- 예시 보강 기준
- 보충학습 분리 기준

현재 후보:

- `rules-and-guidelines-summary.md`

### charts

- 도식 작성 기준

현재 후보:

- `chart-guidelines.md`

## 실제 이동 전 확인 질문

1. 이 문서는 `책 원고 세부 판단 기준`인가, `판단 기록`인가
2. 지금도 반복 참조하는가, 아니면 특정 작업이 끝나면 효용이 사라지는가
3. 저장소 규칙인가, 원고 작성 가이드인가, 진행 체크리스트인가
4. 이동 후 더 찾기 쉬워지는가, 아니면 `authoring` 맥락이 약해지는가
5. 다른 문서의 상대 경로나 설명 문구를 함께 고쳐야 하는가

## 다음 단계 제안

1. `guidelines` 안에 `writing`, `charts`, `checklists` 하위 디렉터리를 먼저 만들지 결정한다.
2. `rules-and-guidelines-summary.md`, `chart-guidelines.md`부터 이동 후보로 검토한다.
3. `part-XX-open-checklist.md`는 가이드라인이 아니라 작업 큐로 유지한다.
4. `AGENTS.md`는 이동 대상이 아니라 저장소 규칙 원문으로 유지한다.
