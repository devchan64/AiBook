# Management 문서 인덱스

작성일: 2026-07-05

이 디렉터리는 책 본문이 아닌 관리 문서를 모아 둔다. 목적은 `집필 워크플로우`, `근거 검토`, `파트별 작업 현황`, `Section 개정 이력`을 서로 다른 층위로 분리해 유지하는 것이다.

## 하위 디렉터리 역할

- `authoring/`: 집필 준비 메모, Part별 오픈 체크리스트, 조사 결과, 근거 검토 메모를 둔다.
- `guidelines/`: 책 원고 세부 작성 규칙과 반복 워크플로우 문서를 둔다.
- `release-notes/`: 저장소의 릴리즈노트를 모아 두는 최상위 디렉터리다.
- `release-notes/sections/`: Section별 버전 코드 기준, 수정일 기준 개정 이력, 번역본 동기화 메모를 둔다.
- `release-notes/guidelines/`: 개념사전, 소개 페이지, 목차, Part 시작/요약 페이지 같은 관리 문서의 개정 이력을 둔다.

## 우선 확인 순서

### 1. 저장소 전체 규칙

- `../AGENTS.md`

### 2. 반복 작업용 가이드

- `guidelines/README.md`
- `guidelines/writing/manuscript-writing-workflow.md`
- `guidelines/charts/chart-guidelines.md`
- `release-notes/README.md`

### 3. Section 버전과 번역 동기화

- `release-notes/sections/README.md`
- `release-notes/guidelines/README.md`

### 4. 현재 원고 작업 현황

- `authoring/part-XX-open-checklist.md`

## 운영 원칙

- 본문 수정 규칙의 기준 원문은 `AGENTS.md`에 둔다.
- 반복 절차와 세부 체크 항목은 가능한 한 `guidelines/` 아래 워크플로우 문서로 내린다.
- Section별 개정 이력은 본문 파일 안에 길게 누적하지 않고 `release-notes/sections/`에서 관리한다.
- 가이드라인과 관리 문서의 개정 이력은 `release-notes/guidelines/`에서 관리한다.
- 번역본이 생겨도 개정 이력의 기준 키는 언어별 파일명이 아니라 `Section ID`로 유지한다.
- Section을 수정할 때는 가능하면 `본문 메타데이터의 Version 갱신 -> 대응 릴리즈노트 갱신 -> Part 체크리스트 메모 반영` 순서로 정리한다.
