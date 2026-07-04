# 현재 본문 범위 스냅샷

## 목적

이 문서는 현재 워크트리에서 `docs/` 아래 어떤 본문 파일들이 `data-modeling-for-ai-modules` 관점의 순차 검토 범위에 포함되어 있는지 스냅샷처럼 고정한다.

상태 문서와 큐 문서는 완료 범위와 재개 조건을 설명하지만, 실제 수정 상태 파일 목록 자체를 한눈에 보여 주지는 않는다. 이 문서는 그 빈칸을 메우기 위한 현재 범위 기록이다.

## 기준 시점

- 현재 워크트리의 `git status --short docs/parts/part-02 docs/parts/part-03 docs/parts/part-06`
- `25-next-docs-editing-queue.md`
- `51-section-level-review-sequence.md`

## 현재 수정 상태 본문 범위

### Part 2

- `docs/parts/part-02/chapter-12/section-01.md`
- `docs/parts/part-02/chapter-13/section-01.md`

대응 검토 로그:

- `53-p2-12-1-review-log.md`
- `54-p2-13-1-review-log.md`

### Part 3

- `docs/parts/part-03/chapter-07/section-01.md`
- `docs/parts/part-03/chapter-08/section-01.md`
- `docs/parts/part-03/chapter-08/section-02.md`
- `docs/parts/part-03/chapter-09/section-02.md`
- `docs/parts/part-03/chapter-10/section-02.md`
- `docs/parts/part-03/chapter-11/section-01.md`
- `docs/parts/part-03/chapter-11/section-02.md`
- `docs/parts/part-03/chapter-12/section-01.md`
- `docs/parts/part-03/chapter-12/section-02.md`
- `docs/parts/part-03/chapter-13/section-01.md`
- `docs/parts/part-03/chapter-13/section-02.md`
- `docs/parts/part-03/chapter-14/section-01.md`
- `docs/parts/part-03/chapter-14/section-02.md`
- `docs/parts/part-03/chapter-15/section-01.md`
- `docs/parts/part-03/chapter-15/section-02.md`
- `docs/parts/part-03/chapter-15/section-03.md`
- `docs/parts/part-03/chapter-16/section-01.md`
- `docs/parts/part-03/chapter-16/section-02.md`
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

대응 검토 로그:

- `55`부터 `84`까지의 Part 3 검토 로그

### Part 6

- `docs/parts/part-06/chapter-01/section-01.md`
- `docs/parts/part-06/chapter-01/section-02.md`
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

대응 검토 로그:

- `64`, `65`
- `85`부터 `96`까지의 Part 6 검토 로그

## 이 범위를 어떻게 읽는가

- 이 목록은 `현재 비커밋 상태의 본문 범위`를 보여 준다.
- 이 목록이 곧바로 `지금 당장 다시 편집해야 할 파일 순서`를 뜻하지는 않는다.
- 실제 재개 순서는 `106-current-working-set-guide.md`를 먼저 따른다.

## 재개 시 확인 순서

1. `105-goal-requirements-audit.md`
2. `100-plan-status-audit.md`
3. `25-next-docs-editing-queue.md`
4. `51-section-level-review-sequence.md`
5. 이 문서에서 실제 수정 상태 파일 범위를 확인한다

## 비커밋 정책 확인

이 문서에 적힌 본문 파일들은 현재 수정 상태로 남아 있으며, 사용자 지시와 저장소 규칙에 따라 커밋하지 않는다.

현재 범위와 파일별 검토 로그의 수적 일치 여부는 `114-manuscript-scope-to-log-coverage-audit.md`에 따로 고정했다.

## 현재 결론

현재 `data-modeling-for-ai-modules` 관점의 비커밋 본문 범위는 Part 2의 2개 파일, Part 3의 핵심 Section과 Part 시작/마무리, Part 6의 chapter 01부터 07까지 전체 Section으로 고정되어 있다. 이후 재개 시에는 이 목록을 실제 워크트리 범위 확인용으로 쓰고, 편집 순서는 최신 큐 문서에서 다시 판단하는 편이 맞다.
