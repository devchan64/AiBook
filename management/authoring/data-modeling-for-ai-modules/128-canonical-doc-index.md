# 기준본 문서 인덱스

## 목적

이 문서는 `data-modeling-for-ai-modules` 아래 문서들 가운데 현재 상태 판단, 재개 판단, 증거 갱신에 직접 쓰는 `기준본 문서`만 따로 묶기 위해 만든다.

문서 수가 많아진 현재 상태에서는 모든 문서가 같은 우선순위를 가지지 않는다. 이 문서는 `지금 판단에 직접 쓰는 문서`와 `설명용 보조 문서`를 구분하는 가장 짧은 인덱스다.

## 기준본 문서

### 1. 목표 기준본

- `105-goal-requirements-audit.md`

역할:

- 현재 목표 요구사항 분해
- 요구사항별 충족 상태와 조건부 후속 작업 판정

### 2. 계획 상태 기준본

- `100-plan-status-audit.md`

역할:

- 핵심 계획 축의 현재 연결 상태 판정
- 계획 누락 여부의 1차 기준

### 3. 본문 검토 큐 기준본

- `25-next-docs-editing-queue.md`
- `51-section-level-review-sequence.md`

역할:

- 현재 본문 순차 검토 위치
- 다음 라운드 재개 조건
- 자산 묶음 기준의 Section 검토 순서

### 4. 커밋 경계 기준본

- `112-commit-boundary-and-branch-audit.md`

역할:

- 현재 브랜치 기준
- `docs/` 비커밋 원칙
- 예외 커밋 파일 경계

### 5. 증거 기준본

- `122-precompletion-evidence-audit.md`
- `124-evidence-refresh-protocol.md`

역할:

- 현재 직접 증거 스냅샷
- 다음 시점의 증거 갱신 순서

### 6. 사건 대응 기준본

- `118-minimum-restart-packet.md`
- `126-trigger-response-matrix.md`

역할:

- 재개 시작점
- 트리거별 대응 경로

## 보조 문서

다음 문서들은 중요하지만, 현재 판단의 1차 기준본은 아니다.

- `106-current-working-set-guide.md`
- `109-active-thread-handoff.md`
- `110-document-role-map.md`
- `116-plan-traceability-matrix-01-16.md`
- `120-operations-doc-overlap-audit.md`
- `107-current-manuscript-scope-snapshot.md`
- `114-manuscript-scope-to-log-coverage-audit.md`
- `16-next-source-editing-queue.md`
- `99-source-queue-status-refresh-log.md`
- `132-readme-coverage-audit.md`
- `134-role-map-coverage-audit.md`
- `136-index-navigation-integrity-audit.md`

이 문서들은 특정 조건에서 기준본을 보강하거나 설명하는 역할을 맡는다.

## 가장 짧은 읽기 순서

### 현재 상태만 다시 판단할 때

1. `118-minimum-restart-packet.md`
2. `105-goal-requirements-audit.md`
3. `100-plan-status-audit.md`
4. `25-next-docs-editing-queue.md`
5. `51-section-level-review-sequence.md`
6. `112-commit-boundary-and-branch-audit.md`

### 완료 전 증거를 다시 맞출 때

1. `122-precompletion-evidence-audit.md`
2. `124-evidence-refresh-protocol.md`

### 사건이 생겼을 때

1. `126-trigger-response-matrix.md`

## 사용 원칙

- 기준본 문서만으로 현재 판단이 끝나면 보조 문서는 열지 않는다.
- 보조 문서는 기준본이 지시하는 조건에서만 연다.
- 인덱스가 바뀌면 `118`, `120`, `126`을 함께 다시 맞춘다.

## 현재 결론

현재 `data-modeling-for-ai-modules`의 기준본 구조는 `105`, `100`, `25`, `51`, `112`, `118`, `122`, `124`, `126`을 중심으로 읽고, 나머지는 보조 문서로 여는 방식이 가장 안정적이다.

이 기준본 집합의 상호 일관성 점검은 `130-canonical-doc-consistency-audit.md`에 따로 정리했다.
