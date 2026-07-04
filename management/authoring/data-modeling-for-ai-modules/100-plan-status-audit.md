# 데이터 모델링 모듈 계획 상태 점검

## 목적

이 문서는 `data-modeling-for-ai-modules`의 핵심 계획 문서와 현재 워크트리 상태를 대조해, 무엇이 이미 준비되었고 무엇이 조건부 후속 작업으로 남아 있는지 한 번에 확인하기 위해 만든다.

여기서의 목적은 새 계획을 더 만드는 것이 아니라, 기존 계획이 실제 어떤 문서와 어떤 검토 로그로 이어졌는지 추적 가능하게 고정하는 것이다.

## 점검 기준

이번 점검은 다음 문서를 기준으로 한다.

- `10-next-writing-actions.md`
- `15-note-integration-priority-map.md`
- `16-next-source-editing-queue.md`
- `21-docs-insertion-asset-map.md`
- `43-common-vocabulary-and-usage-map.md`
- `45-overstatement-guard-sentences.md`
- `49-manuscript-insertion-prep-checklist.md`
- `50-reference-handling-and-manuscript-prep-log.md`
- `25-next-docs-editing-queue.md`
- `51-section-level-review-sequence.md`
- `52-section-review-sequence-log.md`

## 계획 항목별 상태

### 1. 공통 어휘 고정

상태:

- 완료

현재 근거:

- `43-common-vocabulary-and-usage-map.md`에 권장 표현, 피할 표현, 연결 문장, 치환 가이드가 정리되어 있다.
- `17`부터 `20`, `47`, `48`의 노트 검토 로그에서 공통 어휘 정리 기준이 참조본에 반영된 상태를 추적할 수 있다.
- Part 2, Part 3, Part 6 순차 검토 로그 `53` 이후에서 이 어휘가 실제 본문 보정 기준으로 재사용되었다.

남은 후속 작업:

- 새 본문 확장 위치가 생길 때 현재 어휘와 충돌하는 표현이 다시 나타나는지만 점검하면 된다.

### 2. 공통 표 세트 만들기

상태:

- 완료

현재 근거:

- `11-common-example-table-set.md`에 표 세트 4종과 도입/경계 문장이 정리되어 있다.
- `49-manuscript-insertion-prep-checklist.md`가 이 표 세트를 반영 묶음 1부터 4까지의 필수 자산으로 직접 호출한다.

남은 후속 작업:

- 실제 새 Section 확장 시 어떤 표를 어느 위치에 붙일지 개별 판단만 남아 있다.

### 3. 공통 Python 예제 세트 만들기

상태:

- 완료

현재 근거:

- `13-common-python-example-plan.md`에 예제별 질문, 입력, 출력 포인트가 정리되어 있다.
- `14-python-example-draft-snippets.md`에 코드, 예상 출력, 해석 문장 초안이 정리되어 있다.
- `49-manuscript-insertion-prep-checklist.md`가 예제 1부터 4를 각 반영 묶음에 연결한다.

남은 후속 작업:

- 새 본문 확장 위치가 생길 때 현재 예제 중 어떤 버전을 삽입할지 결정하면 된다.

### 4. Part별 삽입 후보 문단 만들기

상태:

- 완료

현재 근거:

- `12-part-draft-paragraphs.md`에 Part 1, Part 2, Part 3, Part 6 후보 문단과 자산 연결이 정리되어 있다.
- `49-manuscript-insertion-prep-checklist.md`가 각 반영 묶음에서 필요한 Part 후보 문단을 직접 호출한다.

남은 후속 작업:

- 새 본문 확장 위치가 구체화될 때 실제 삽입 여부를 다시 고르면 된다.

### 5. 과장 방지 문장 세트 만들기

상태:

- 완료

현재 근거:

- `45-overstatement-guard-sentences.md`에 핵심 문장 세트, 쓰기 좋은 위치, 선택 기준, 피해야 할 문장이 정리되어 있다.
- Part 3, Part 6 순차 검토 로그 `58` 이후에서 이 경계 문장을 본문에 반복 반영한 근거가 누적되어 있다.

남은 후속 작업:

- 이후 새 본문이나 회고 문장이 추가될 때 같은 문장 세트를 계속 호출하면 된다.

## 원고 반영 준비 상태

### 노트 통합 우선순위와 참조 전환

상태:

- 완료

현재 근거:

- `15-note-integration-priority-map.md`가 `01`부터 `10`까지의 우선 연결 순서를 정리한다.
- `50-reference-handling-and-manuscript-prep-log.md`가 참조 노트를 직접 수정하지 않고, `data-modeling-for-ai-modules` 쪽 자산과 체크리스트로 전환한 이유를 남긴다.
- `16-next-source-editing-queue.md`와 `99-source-queue-status-refresh-log.md`가 참조 큐를 `재개 조건 기반` 상태로 다시 고정한다.

남은 후속 작업:

- 새 본문 확장 위치가 생길 때만 참조 라운드를 다시 연다.

### 실제 삽입 자산 지도

상태:

- 준비 완료

현재 근거:

- `21-docs-insertion-asset-map.md`가 공통 도입 문단, 표, Python 예제, 경계 문장의 우선 삽입 후보를 Part 2, Part 3, Part 6 파일에 연결한다.
- `52-section-review-sequence-log.md`가 자산 지도만으로는 부족해 실제 Section별 검토 순서 문서가 필요해졌던 이유를 설명한다.

남은 후속 작업:

- 삽입 후보 위치는 새 본문 확장이나 재개 라운드가 생길 때 다시 호출하면 된다.

### 반영 묶음 1부터 4

상태:

- 준비 완료

현재 근거:

- `49-manuscript-insertion-prep-checklist.md`에 각 반영 묶음별 필요 자산과 사전 확인 질문이 정리되어 있다.
- `51-section-level-review-sequence.md`가 이 묶음을 실제 Section 검토 순서와 연결한다.

남은 후속 작업:

- 새 본문 확장 위치가 생기면, 어떤 묶음을 다시 호출할지 판단하는 일만 남아 있다.

### Part 2, Part 3, Part 6 순차 검토

상태:

- 1차 라운드 완료

현재 근거:

- `51-section-level-review-sequence.md`의 `현재 진행 상태`
- `25-next-docs-editing-queue.md`의 완료 이력
- 파일별 검토 로그 `53`부터 `96`
- 상태 정리 로그 `97`, `98`

남은 후속 작업:

- 새 본문 확장 위치가 생기거나, 공통 어휘 충돌/과장 표현이 다시 보일 때만 다음 라운드를 연다.

## 참조 노트 관리 상태

### `brewing-shot-ai-notes` 참조 정리

상태:

- 1차 참조 라운드 완료

현재 근거:

- `17-notes-01-02-review-log.md`
- `18-notes-03-05-review-log.md`
- `19-notes-06-08-review-log.md`
- `20-notes-09-10-review-log.md`
- `47-notes-01-02-refresh-log.md`
- `48-note-02-problem-framing-commit-log.md`
- `16-next-source-editing-queue.md`의 현재 상태 및 재개 후보 메모
- `99-source-queue-status-refresh-log.md`

남은 후속 작업:

- 참조 라운드는 새 본문 확장 위치, 공통 어휘 충돌, 자산 세분화 필요가 생길 때만 재개한다.

## 지금 시점의 실제 다음 일

현재 기준으로 바로 해야 하는 일은 `docs/`를 더 넓게 다시 읽는 것이 아니라 다음 둘 중 하나다.

1. 새 본문 확장 위치가 생기면 `49`, `51`, `25`를 기준으로 해당 묶음을 다시 연다.
2. 관리 문서 압축이나 역할 정리가 더 필요하다고 판단되면 `README`, 큐 문서, 상태 로그를 정리한다.

## 누락 점검

이번 점검 기준 문서 가운데 현재 상태 문서에서 직접 추적되는 항목은 다음과 같다.

- `10`: 공통 어휘, 표, Python 예제, Part별 문단, 과장 방지 문장 준비
- `15`, `16`, `50`: 참조 노트 우선순위와 비수정 원칙, 재개 조건
- `21`, `49`, `51`, `52`: 실제 삽입 자산 지도, 반영 묶음, Section 순차 검토 기준
- `25`: 완료 이력과 다음 재개 후보
- `43`, `45`: 공통 어휘와 과장 방지 문장 기준

현재 판단으로는 위 계획 축 가운데 `문서상 근거가 아직 연결되지 않은 항목`은 남아 있지 않다. 남은 일은 미처 시작하지 못한 계획 수행이라기보다, `새 본문 확장`이나 `재개 조건`이 생겼을 때 어떤 문서를 다시 호출할지 유지하는 관리 작업이다.

`01`부터 `16`까지 개별 계획 문서가 어떤 후속 문서와 이어졌는지는 `116-plan-traceability-matrix-01-16.md`에 별도로 정리했다.

## 비커밋 정책 확인

현재 워크트리에는 Part 2, Part 3, Part 6의 `docs/` 수정이 계속 남아 있으며, 이 상태는 사용자 지시와 저장소 규칙에 맞게 유지되고 있다. 본문은 커밋하지 않고, 관리 문서에서만 진행 상태와 판단 근거를 누적한다.

최근 사용자 지시까지 포함한 커밋 경계와 브랜치 기준은 `112-commit-boundary-and-branch-audit.md`에 따로 고정했다.

## 현재 결론

`data-modeling-for-ai-modules`의 핵심 계획 항목은 현재 워크트리 기준으로 한 차례 모두 준비되었고, Part 2, Part 3, Part 6 순차 검토와 참조 노트 정리도 1차 라운드까지 완료된 상태다. 지금 남아 있는 일은 `미완료 계획 수행`보다 `재개 조건이 생겼을 때 어느 계획을 다시 호출할지`를 정확히 유지하는 관리 작업에 가깝다.
