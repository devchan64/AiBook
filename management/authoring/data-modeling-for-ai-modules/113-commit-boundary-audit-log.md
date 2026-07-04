# 커밋 경계 감사 로그

## 목적

이 문서는 `112-commit-boundary-and-branch-audit.md`를 추가한 이유를 기록한다.

## 추가 이유

- 기존 상태 문서에는 `docs/ 비커밋` 원칙은 있었지만, 최근 사용자 지시까지 포함한 `예외 커밋 파일` 경계가 한 문서에 고정돼 있지 않았다.
- 특히 `brewing-shot-ai-notes/02-problem-framing-from-shot-to-dataset.md`는 예외적으로 커밋 대상이고, `docs/`는 수정되어도 커밋하면 안 되는 상태라 구분 문서가 필요해졌다.
- 앞으로 커밋 전 범위 점검 시 이 문서를 먼저 보면 `수정 가능`, `참조 전용`, `비커밋 유지`, `예외적 커밋 대상`을 혼동하지 않게 된다.

## 연결 문서

- `48-note-02-problem-framing-commit-log.md`
- `105-goal-requirements-audit.md`
- `109-active-thread-handoff.md`
- `112-commit-boundary-and-branch-audit.md`

## 현재 결론

이 로그는 최근 사용자 지시를 운영 규칙으로 승격해, 이후 커밋 범위 판단을 더 짧고 안전하게 만들기 위해 추가했다.
