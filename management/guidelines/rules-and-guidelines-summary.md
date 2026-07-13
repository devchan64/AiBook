# 집필 규칙·가이드라인 요약

작성일: 2026-07-01

이 문서는 저장소의 규칙을 `빠르게 다시 찾는 인덱스`입니다. 상세 규칙을 여기와 원문 문서에 중복해서 길게 유지하지 않는 것을 기본 원칙으로 합니다.

## 이 문서의 역할

- 어떤 작업에서 어떤 문서를 먼저 열어야 하는지 빠르게 안내합니다.
- `AGENTS.md`와 개별 가이드라인의 역할 경계를 짧게 정리합니다.
- 작업 중 자주 빠뜨리는 확인 포인트만 제한적으로 다시 적습니다.

이 문서는 다음을 하지 않습니다.

- `AGENTS.md`의 전역 규칙을 길게 다시 쓰지 않습니다.
- 개별 가이드라인의 세부 절차, 예외 규칙, 금지 패턴을 반복 저장하지 않습니다.
- 작업 메모나 분석 메모 역할을 대신하지 않습니다.

## 문서 역할 분담

### `AGENTS.md`

- 저장소 전역 규칙의 기준 원문입니다.
- 프로젝트 목적, 독자 기준, 문서 위치, 용어, 출처, 저작권, 배포, 빌드 검증 같은 공통 기준을 둡니다.
- 작업 중 놓치기 쉬운 `먼저 볼 문서` 포인트만 제한적으로 중첩합니다.

### `management/guidelines/*.md`

- 특정 작업을 실제로 수행할 때 다시 여는 세부 규칙 문서입니다.
- 예:
  - 원고 작성: `manuscript-writing-workflow.md`
  - Python 예제: `python-example-guidelines.md`
  - 차트·도식: `chart-guidelines.md`
  - 번역: `english-translation-guidelines.md`, `chinese-translation-guidelines.md`
  - 개념사전: `concept-glossary-guidelines.md`

### `management/release-notes/sections/README.md`

- Section 메타데이터, 버전 코드, 릴리즈노트 갱신 규칙의 원문입니다.
- Section 본문을 실제로 수정했다면 이 문서를 따라 같이 갱신합니다.

### `management/authoring/*.md`

- 작업 메모, 근거 검토, Part별 후속 작업 관리 문서입니다.
- 전역 규칙 문서가 아니라 현재 작업의 판단 보조 문서입니다.

## 중첩 허용 원칙

다음처럼 `작업 중 놓치기 쉬운 확인 포인트`만 중첩을 허용합니다.

- Section 수정 시 `Version`과 릴리즈노트를 함께 갱신해야 한다는 점
- Python 예제, 차트, 번역, 개념사전, 목차 변경은 전용 가이드를 먼저 열어야 한다는 점
- `main` 푸시는 배포라는 점

그 외의 세부 규칙은 가능하면 원문 한 곳에서만 관리합니다.

## 작업별 참조 순서

### Section 본문을 새로 쓰거나 크게 고칠 때

1. `AGENTS.md`
2. `management/guidelines/manuscript-writing-workflow.md`
3. 필요하면 해당 `management/authoring/section-...-evidence-analysis.md`
4. Section을 실제로 수정했다면 `management/release-notes/sections/README.md`

### Python 예제를 넣거나 고칠 때

1. `AGENTS.md`
2. `management/guidelines/python-example-guidelines.md`
3. 현재 예제가 `설명형`, `검증형`, `실험형` 중 무엇인지 먼저 구분
4. 필요하면 `management/guidelines/manuscript-writing-workflow.md`

### 차트, Mermaid, SVG를 만들 때

1. `AGENTS.md`
2. `management/guidelines/chart-guidelines.md`
3. 형식 선택이 먼저 필요하면 `표 / 플로우차트 / 좌표 차트 / 구조 다이어그램` 중 무엇이 맞는지 차트 가이드의 형식 선택 기준부터 확인

### 영어/중국어 번역을 다룰 때

1. `AGENTS.md`
2. 해당 번역 가이드라인
3. 원문 Section의 릴리즈노트

### 개념사전을 갱신할 때

1. `AGENTS.md`
2. `management/guidelines/concept-glossary-guidelines.md`

## 자주 빠뜨리는 확인 포인트

- Section 본문을 수정했으면 `Version`과 릴리즈노트를 같은 작업 안에서 함께 갱신합니다.
- 목차 구조를 바꾸면 `mkdocs.yml`과 독자용 목차 설명 문서를 함께 확인합니다.
- Python 예제는 세부 판단을 요약 문서가 아니라 Python 가이드 원문에서 확인합니다.
- 차트·도식은 언어 자산, 파일 위치, 레이아웃 기준을 차트 가이드 원문에서 확인합니다.
- `main` 푸시는 배포이므로, 명시적 지시가 없으면 기본 브랜치는 `dev`입니다.

## 빠른 시작 순서

1. 작업 시작: `AGENTS.md`
2. 작업 종류 확인: 해당 가이드라인 원문
3. 본문 수정이면: 릴리즈노트 가이드까지 함께 확인
4. 필요하면: `authoring` 메모와 Part 체크리스트 확인

## 관련 문서

- `AGENTS.md`
- `management/guidelines/README.md`
- `management/guidelines/manuscript-writing-workflow.md`
- `management/guidelines/python-example-guidelines.md`
- `management/guidelines/chart-guidelines.md`
- `management/guidelines/english-translation-guidelines.md`
- `management/guidelines/chinese-translation-guidelines.md`
- `management/guidelines/concept-glossary-guidelines.md`
- `management/release-notes/sections/README.md`
