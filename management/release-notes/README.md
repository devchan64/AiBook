# 릴리즈노트 인덱스

작성일: 2026-07-06

이 디렉터리는 이 저장소의 릴리즈노트를 한곳에 모아 관리한다. 기존 `section-release-notes/`는 Section 본문 개정 이력만 다루는 이름이었기 때문에, Section 본문과 가이드라인·관리 문서의 개정 이력을 함께 보관하는 현재 구조와 범위가 맞지 않았다. 그래서 최상위 이름을 `release-notes/`로 바꾸고, 성격에 따라 하위 묶음으로 나누어 정리한다.

## 구조

- `sections/`
  - 책 본문 Section, Part 개요, Part 마무리 페이지의 개정 이력을 둔다.
  - Section ID와 본문 경로를 기준으로 번역 동기화와 버전 추적을 수행한다.
- `guidelines/`
  - 개념사전 원고, 개념사전 규칙, 소개 페이지, Part 시작/마무리 페이지, 목차 같은 관리 문서와 가이드라인 문서의 개정 이력을 둔다.

## 현재 집계

### Section 릴리즈노트

총 284개 파일을 Part별로 나누어 관리한다.

| 묶음 | 파일 수 |
| --- | ---: |
| `sections/part-01/` | 57 |
| `sections/part-02/` | 62 |
| `sections/part-03/` | 22 |
| `sections/part-04/` | 49 |
| `sections/part-05/` | 35 |
| `sections/part-06/` | 44 |
| `sections/part-07/` | 15 |

추가 공통 문서:

- `sections/README.md`
- `sections/section-release-note-template.md`

### 가이드라인·관리 문서 릴리즈노트

총 7개 파일을 문서 단위로 관리한다.

| 파일 | 대상 문서 |
| --- | --- |
| `guidelines/concept-glossary.md` | `docs/reference/concept-glossary.md` |
| `guidelines/concept-glossary-guidelines.md` | `management/authoring/concept-glossary-guidelines.md` |
| `guidelines/index-page.md` | `docs/index.md` |
| `guidelines/part-01-index.md` | `docs/parts/part-01/index.md` |
| `guidelines/part-01-summary.md` | `docs/parts/part-01/summary.md` |
| `guidelines/part-02-index.md` | `docs/parts/part-02/index.md` |
| `guidelines/table-of-contents.md` | `docs/book/table-of-contents.md` |

## 운영 원칙

- Section 본문을 수정할 때는 `sections/README.md`의 규칙을 따른다.
- 관리 문서나 가이드라인 문서를 수정할 때는 대응 릴리즈노트를 `guidelines/` 아래에서 함께 갱신한다.
- 새 릴리즈노트를 추가할 때는 먼저 `sections/`와 `guidelines/` 중 어느 묶음에 속하는지 결정한다.
- 경로만 바뀌고 문서 성격이 바뀌지 않은 경우에도, 릴리즈노트 위치와 관련 문서 참조는 같은 작업 안에서 함께 정리한다.
