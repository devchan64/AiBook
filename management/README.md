# Management 문서 인덱스

작성일: 2026-07-05

이 디렉터리는 책 본문이 아닌 관리 문서를 모아 둔다. 목적은 `집필 워크플로우`, `근거 검토`, `파트별 작업 현황`, `Section 개정 이력`을 서로 다른 층위로 분리해 유지하는 것이다.

## 하위 디렉터리 역할

- `authoring/`: 집필 준비 메모, 진행 메타 소제목 감사 목록과 변경 제안서, Part별 오픈 체크리스트, 조사 결과, 근거 검토 메모를 둔다.
- `guidelines/`: 책 원고 세부 작성 규칙과 반복 워크플로우 문서를 둔다.
- `release-notes/`: 책 본문 문서의 릴리즈노트를 모아 두는 최상위 디렉터리다.
- `release-notes/sections/`: Section별 버전 코드 기준, 수정일 기준 개정 이력, 번역본 동기화 메모를 둔다.
- `tools/`: 번역 품질 리포트 생성처럼 집필·검수 작업을 돕는 보조 스크립트를 둔다.

P7-5.1~P7-5.2, P7-5.4와 P7-5.7 이후 Section별 개정 이력은 `release-notes/sections/part-07/`에서 각각 유지한다. 이번 세션과 공통 관리노트의 고유 실험 결론·공통 gate는 보조 문서인 [`authoring/part-07-p7-5-integrated-management-note.md`](authoring/part-07-p7-5-integrated-management-note.md)에 통합한다. `part-07-open-checklist.md`와 `part-07-section-analysis.md`는 별도 유지한다.

## 우선 확인 순서

### 1. 저장소 전체 규칙

- `../AGENTS.md`

### 2. 반복 작업용 가이드

- `guidelines/README.md`
- `guidelines/repository-management-guidelines.md`
- `guidelines/source-copyright-guidelines.md`
- `guidelines/section-learning-focus-guidelines.md`
- `guidelines/manuscript-writing-workflow.md`
- `guidelines/python-example-guidelines.md`
- `guidelines/english-translation-guidelines.md`
- `guidelines/chinese-translation-guidelines.md`
- `guidelines/chart-guidelines.md`
- `release-notes/README.md`
- `tools/README.md`

### 3. Section 버전과 번역 동기화

- `release-notes/sections/README.md`

### 4. 현재 원고 작업 현황

- `guidelines/section-learning-focus-guidelines.md`
- `authoring/progress-meta-heading-audit.md`
- `authoring/progress-meta-heading-proposal.md`
- `authoring/part-XX-open-checklist.md`

## 운영 원칙

- 작업 시작 기준은 `AGENTS.md`에 두고, 저장소 운영과 본문 수정 세부 기준은 `guidelines/` 아래 문서로 나누어 둔다.
- 반복 절차와 세부 체크 항목은 가능한 한 `guidelines/` 아래 워크플로우 문서로 내린다.
- Section별 개정 이력은 본문 파일 안에 길게 누적하지 않고 `release-notes/sections/`에서 관리한다.
- Section별 중심 학습 산출물 기준은 `guidelines/section-learning-focus-guidelines.md`에서 관리하고, 실제 항목은 Part별 체크포인트 노트에서 관리한다.
- 원칙 문서와 가이드라인 문서는 별도 리비전노트를 두지 않고 문서 자체를 직접 갱신한다.
- 번역본이 생겨도 개정 이력의 기준 키는 언어별 파일명이 아니라 `Section ID`로 유지한다.
- Section을 수정할 때는 가능하면 `본문 메타데이터의 Version 갱신 -> 대응 릴리즈노트 갱신 -> Part 체크리스트 메모 반영` 순서로 정리한다.
- 공개 본문 자산의 실제 저장소는 `docs/assets/` 하나로 본다. 자산 경로와 Mermaid 운영 규칙은 `guidelines/chart-guidelines.md`와 `../docs/assets/README.md`를 함께 기준으로 삼는다.
