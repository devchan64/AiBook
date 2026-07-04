# 현재 스레드 핸드오프

## 목적

이 문서는 현재 스레드의 작업 상태를 가장 짧게 이어받기 위한 운영용 인덱스다.

상세 근거는 다른 상태 문서에 남겨 두고, 여기서는 `어디서 시작할지`, `무엇을 지켜야 하는지`, `어떤 경우에 다시 본문 검토를 여는지`만 빠르게 보여 준다.

## 현재 상태 한 줄 요약

- `data-modeling-for-ai-modules`의 핵심 계획 축은 문서상 근거와 연결 완료
- Part 2, Part 3, Part 6 본문은 1차 순차 검토 완료
- `docs/` 본문은 비커밋 상태 유지
- 다음 작업은 `새 본문 확장 위치` 또는 `재개 조건`이 생길 때 다시 여는 구조

## 지금 바로 먼저 볼 문서

1. `105-goal-requirements-audit.md`
2. `100-plan-status-audit.md`
3. `25-next-docs-editing-queue.md`
4. `51-section-level-review-sequence.md`
5. `107-current-manuscript-scope-snapshot.md`
6. `112-commit-boundary-and-branch-audit.md`
7. `118-minimum-restart-packet.md`

## 운영 규칙

- 현재 브랜치: `dev`
- `docs/` 본문은 커밋하지 않는다.
- `brewing-shot-ai-notes/02-problem-framing-from-shot-to-dataset.md`만 예외적 커밋 대상으로 본다.
- `brewing-shot-ai-notes`는 참조본으로만 읽는다.
- 새 판단이 생기면 관리 문서 로그를 먼저 남긴다.

## 본문 검토를 다시 여는 조건

- 새 본문 확장 위치가 생겨 같은 자산 묶음을 다시 호출해야 할 때
- 기존 문장이 과장되거나 현재 공통 어휘와 충돌하는 사례가 새로 발견될 때
- 관리 문서 압축 또는 역할 재정리가 필요해 완료 범위를 다시 묶어야 할 때

## 자산 문서를 다시 볼 조건

실제 본문 확장이 필요해질 때만 다음 문서를 연다.

- `49-manuscript-insertion-prep-checklist.md`
- `21-docs-insertion-asset-map.md`
- `43-common-vocabulary-and-usage-map.md`
- `45-overstatement-guard-sentences.md`

## 과거 로그를 볼 때

- 당시 왜 그렇게 고쳤는지 보려면 `53` 이후 파일별 검토 로그
- 참조 노트 정리 이유를 보려면 `17`부터 `20`, `47`, `48`
- 상태 정렬 이유를 보려면 `97`부터 `108`

읽기 원칙은 `104-historical-log-reading-guide.md`를 따른다.

## 현재 결론

이 스레드는 `새 계획 작성` 단계가 아니라 `현재 상태와 재개 조건 유지` 단계에 있다. 지금 재개한다면 먼저 상태 문서와 큐를 확인하고, 새 본문 확장 조건이 생겼을 때만 자산 문서와 본문 검토 라운드를 다시 여는 편이 맞다.

가장 짧은 재개 시작점만 필요하면 `118-minimum-restart-packet.md`의 다섯 문서 패킷을 따른다.

`105`, `106`, `109`, `118`의 역할 차이는 `120-operations-doc-overlap-audit.md`를 기준으로 본다.
