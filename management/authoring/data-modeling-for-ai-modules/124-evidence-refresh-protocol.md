# 증거 갱신 프로토콜

## 목적

이 문서는 `122-precompletion-evidence-audit.md`에 적힌 증거를 다음 재개 시점에 어떤 순서로 다시 갱신해야 하는지 고정하기 위해 만든다.

증거 문서는 시간이 지나면 오래될 수 있으므로, 종료 판단이나 재개 판단 전에 `무엇부터 다시 확인할 것인가`를 짧게 정리해 둔다.

## 언제 이 문서를 쓰는가

- `122-precompletion-evidence-audit.md`를 다시 검토할 때
- 목표 종료 가능성을 다시 점검할 때
- 며칠 뒤 재개해 현재 상태가 바뀌었는지 다시 확인할 때

## 갱신 순서

### 1. 브랜치 확인

명령:

- `git branch --show-current`

확인할 것:

- 현재 브랜치가 계속 `dev`인지

갱신 대상 문서:

- `112-commit-boundary-and-branch-audit.md`
- `122-precompletion-evidence-audit.md`

### 2. 워크트리 상태 확인

명령:

- `git status --short docs management/authoring/data-modeling-for-ai-modules management/authoring/brewing-shot-ai-notes/02-problem-framing-from-shot-to-dataset.md`

확인할 것:

- `docs/` 본문 수정이 계속 비커밋 상태인지
- 관리 문서가 어떤 범위까지 누적되었는지
- `brewing-shot-ai-notes/02`가 현재 별도 수정 상태인지 아닌지

갱신 대상 문서:

- `105-goal-requirements-audit.md`
- `112-commit-boundary-and-branch-audit.md`
- `122-precompletion-evidence-audit.md`

### 3. 본문 범위와 로그 커버리지 확인

먼저 볼 문서:

- `107-current-manuscript-scope-snapshot.md`
- `114-manuscript-scope-to-log-coverage-audit.md`

추가 확인:

- `git status --short docs`

확인할 것:

- 수정 본문 수가 여전히 현재 로그 범위와 맞는지
- 새 본문 확장 파일이 생겼는지

갱신 대상 문서:

- `107-current-manuscript-scope-snapshot.md`
- `114-manuscript-scope-to-log-coverage-audit.md`
- 필요하면 새 파일별 검토 로그

### 4. 계획 연결 상태 확인

먼저 볼 문서:

- `100-plan-status-audit.md`
- `116-plan-traceability-matrix-01-16.md`

확인할 것:

- 기존 계획 축 가운데 새로 열린 항목이 있는지
- 새 본문 확장 위치가 기존 계획 축 어디에 걸리는지

갱신 대상 문서:

- `100-plan-status-audit.md`
- `116-plan-traceability-matrix-01-16.md`
- 필요하면 해당 계획 로그 문서

### 5. 운영 문서 최신성 확인

먼저 볼 문서:

- `118-minimum-restart-packet.md`
- `120-operations-doc-overlap-audit.md`

확인할 것:

- 최소 재개 패킷의 핵심 문서 구성이 여전히 맞는지
- 운영 문서 역할 분리가 여전히 유효한지

갱신 대상 문서:

- `118-minimum-restart-packet.md`
- `120-operations-doc-overlap-audit.md`
- 필요하면 `106`, `109`

## 갱신 후 마지막 반영 문서

위 확인이 끝나면 마지막으로 다음 두 문서를 갱신한다.

- `105-goal-requirements-audit.md`
- `122-precompletion-evidence-audit.md`

이유:

- `105`는 요구사항 판정 기준본이고,
- `122`는 현재 명령 출력까지 포함한 완료 전 증거 기준본이기 때문이다.

## 사용 원칙

- 상태가 조금이라도 바뀌었으면 `122`의 직접 관찰 결과를 그대로 재사용하지 않는다.
- `118`은 재개 시작점이고, `124`는 재개 후 증거 갱신 순서다.
- 사건별 대응 경로를 고를 때는 `126-trigger-response-matrix.md`를 먼저 참고한다.
- `105`와 `122`는 항상 가장 마지막에 다시 정렬한다.

## 현재 결론

현재 증거 체계는 `118`로 시작해 현재 상태를 잡고, `124` 순서로 증거를 갱신한 뒤, 마지막에 `105`와 `122`를 다시 맞추는 구조로 운영하는 편이 가장 안정적이다.
