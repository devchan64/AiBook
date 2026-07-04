# 현재 커밋 패키지 감사

## 목적

이 문서는 현재 워크트리 기준으로 `이번 커밋에 실제로 담을 수 있는 변경 묶음`을 고정하기 위해 만든다.

이미 `112-commit-boundary-and-branch-audit.md`가 일반 경계를 설명하고 있으므로, 여기서는 그 경계를 현재 상태에 다시 대입해 `지금 무엇을 스테이징해야 하는가`만 더 구체적으로 적는다.

## 현재 기준 상태

- 현재 브랜치: `dev`
- `docs/` 아래 책원고는 다수 수정 상태다.
- `management/authoring/brewing-shot-ai-notes/02-problem-framing-from-shot-to-dataset.md`는 현재 `git status --short`에 나타나지 않는다.
- `management/authoring/data-modeling-for-ai-modules/` 아래에는 수정본과 신규 파일이 함께 존재한다.

## 현재 커밋 가능 묶음

이번 워크트리 기준으로 실제 커밋 가능 묶음은 아래처럼 읽는 편이 맞다.

### 1. 포함 가능

- `management/authoring/data-modeling-for-ai-modules/` 아래 관리 문서 변경

이 묶음은 현재 목표의 다음 요구를 직접 뒷받침한다.

- 책원고 편집 순차 검토 상태 관리
- 계획 근거 문서화
- 다음 재개 조건과 커밋 경계 추적

### 2. 현재는 포함할 것이 없는 예외 파일

- `management/authoring/brewing-shot-ai-notes/02-problem-framing-from-shot-to-dataset.md`

이 파일은 정책상 예외적 커밋 대상이 맞지만, 현재 수정 상태가 아니므로 `이번 커밋 패키지`에는 실제 내용이 없다.

즉 `커밋 대상 자격이 있다`와 `지금 커밋에 들어갈 변경이 있다`는 구분해서 읽어야 한다.

### 3. 반드시 제외

- `docs/` 아래 책원고 전체

이 묶음은 현재 워크트리에서 계속 수정 상태로 남아 있어도, 이번 커밋에서는 제외해야 한다.

## 스테이징 해석

현재 상태에서는 `docs/`를 한 줄이라도 함께 올리지 않는 것이 가장 중요하다.

따라서 이번 커밋은 사실상 다음 의미를 가진다.

- 원고 본문 변경은 워크트리에 유지
- 관리 문서 기준과 상태 감사만 커밋

이 해석은 `완료된 책원고 본문은 커밋하지 않는다`는 현재 목표와도 직접 맞는다.

## 관련 근거 문서

- `105-goal-requirements-audit.md`
- `112-commit-boundary-and-branch-audit.md`
- `122-precompletion-evidence-audit.md`
- `126-trigger-response-matrix.md`

## 현재 결론

현재 워크트리에서 다음 커밋은 `data-modeling-for-ai-modules` 관리 문서 묶음만 대상으로 잡는 편이 맞다. `docs/`는 계속 비커밋 상태로 남기고, 노트 `02`는 이후 실제 수정이 다시 생길 때만 예외 파일로 함께 다룬다.
