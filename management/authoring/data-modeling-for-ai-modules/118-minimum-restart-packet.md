# 최소 재개 패킷

## 목적

이 문서는 `data-modeling-for-ai-modules` 아래 문서가 많아진 현재 상태에서, 작업을 다시 열 때 반드시 먼저 봐야 하는 최소 문서 묶음을 다섯 개로 고정하기 위해 만든다.

전체 역할 지도와 세부 감사 문서는 계속 유지하되, 실제 재개 비용을 줄이기 위해 `지금 가장 먼저 필요한 문서`만 따로 압축한다.

## 최소 재개 패킷

재개 시에는 먼저 다음 다섯 문서만 본다.

1. `105-goal-requirements-audit.md`
2. `100-plan-status-audit.md`
3. `25-next-docs-editing-queue.md`
4. `51-section-level-review-sequence.md`
5. `112-commit-boundary-and-branch-audit.md`

## 각 문서의 역할

### 1. `105-goal-requirements-audit.md`

무엇을 확인하는가:

- 현재 목표 요구사항이 무엇인가
- 어떤 요구사항이 이미 근거 문서와 연결되었는가
- 어떤 작업이 조건부 후속 작업으로 남아 있는가

이 문서를 먼저 보는 이유:

- 재개 시점에 `무엇을 증명해야 하는가`를 가장 먼저 다시 고정해야 하기 때문이다.

### 2. `100-plan-status-audit.md`

무엇을 확인하는가:

- 핵심 계획 축이 어떤 문서와 연결되었는가
- 현재 상태가 `완료`, `준비 완료`, `1차 라운드 완료` 중 어디인가

이 문서를 두 번째로 보는 이유:

- 목표 요구사항 다음에는 실제 계획 수행 상태를 확인해야 하기 때문이다.

### 3. `25-next-docs-editing-queue.md`

무엇을 확인하는가:

- 실제 본문 검토 큐가 어디까지 왔는가
- 다음 라운드를 다시 열 조건이 무엇인가

이 문서를 세 번째로 보는 이유:

- 현재 상태를 확인한 뒤에는 실제 본문 작업 큐가 살아 있는지, 조건부 재개인지 판단해야 하기 때문이다.

### 4. `51-section-level-review-sequence.md`

무엇을 확인하는가:

- Part 2, Part 3, Part 6의 Section 단위 검토 구조
- 새 본문 확장 위치가 생겼을 때 어떤 묶음을 다시 열어야 하는가

이 문서를 네 번째로 보는 이유:

- `25`가 큐 상태를 보여 준다면, `51`은 실제 라운드 재개 구조를 보여 주기 때문이다.

### 5. `112-commit-boundary-and-branch-audit.md`

무엇을 확인하는가:

- 현재 브랜치가 `dev`인지
- `docs/` 본문을 커밋하면 안 된다는 경계
- `brewing-shot-ai-notes/02`만 예외적 커밋 대상이라는 점

이 문서를 다섯 번째로 보는 이유:

- 작업을 시작하기 전에 커밋 경계를 마지막으로 다시 고정해야 하기 때문이다.

## 이 다섯 문서만으로 판단할 수 있는 것

- 현재 목표의 범위
- 핵심 계획 축의 진행 상태
- 본문 순차 검토의 현재 위치
- 다음 라운드 재개 조건
- 커밋 금지 범위와 예외 커밋 범위

즉 재개 첫 단계의 운영 판단은 이 다섯 문서만으로도 가능하다.

## 그다음에 여는 조건부 보조 문서

### 새 본문 확장 위치가 생겼을 때

- `49-manuscript-insertion-prep-checklist.md`
- `21-docs-insertion-asset-map.md`
- `43-common-vocabulary-and-usage-map.md`
- `45-overstatement-guard-sentences.md`

### 현재 수정 범위와 로그 범위를 다시 대조해야 할 때

- `107-current-manuscript-scope-snapshot.md`
- `114-manuscript-scope-to-log-coverage-audit.md`

### 개별 계획 문서가 어디로 흡수되었는지 다시 확인해야 할 때

- `116-plan-traceability-matrix-01-16.md`

### 과거 판단 이유가 필요할 때

- `104-historical-log-reading-guide.md`
- 해당 라운드 로그 또는 파일별 검토 로그

### 완료 전 증거를 다시 최신화해야 할 때

- `122-precompletion-evidence-audit.md`
- `124-evidence-refresh-protocol.md`

### 재개 조건이 실제 사건으로 바뀌었을 때

- `126-trigger-response-matrix.md`

### 기준본 문서 집합만 빠르게 확인해야 할 때

- `128-canonical-doc-index.md`

## 사용 원칙

- 재개 첫 5분에는 이 문서와 다섯 개 핵심 문서만 본다.
- 핵심 다섯 문서만으로 충분히 판단되는 동안에는 보조 문서를 열지 않는다.
- 보조 문서는 `새 본문 확장`, `범위 대조`, `과거 판단 이유 확인` 같은 명시적 필요가 생겼을 때만 연다.

## 현재 결론

현재 이 디렉터리의 최소 재개 패킷은 `105 -> 100 -> 25 -> 51 -> 112`이며, 이 다섯 문서가 현재 작업을 다시 여는 가장 짧은 시작점이다.

운영 문서끼리의 역할 차이는 `120-operations-doc-overlap-audit.md`에 따로 정리했다.
