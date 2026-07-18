# Section 릴리즈노트 파일 관리

작성일: 2026-07-05

이 디렉터리는 `management/release-notes/` 아래에서 책 본문 문서의 릴리즈노트 파일만 관리한다. 여기서 책 본문 문서는 Section 본문, Part 시작/마무리 페이지, 그리고 `docs/index.md`, `docs/book/table-of-contents.md` 같은 공개 진입 문서를 뜻한다.

본문의 `Section ID`, 제목 앞 인덱스, `Version` 같은 메타데이터 관리 규칙은 `../../guidelines/section-metadata-guidelines.md`를 따른다. 이 디렉터리의 파일은 책 본문 문서용 `Section Release Note`로만 관리하며, 별도의 체인지로그를 따로 두지 않는다.

## 기본 원칙

- 릴리즈노트는 Section별 변경 이력과 Part 진입/마무리 페이지 개정 이력을 남겨 이후 회고, 검토, 번역 동기화에 재사용할 수 있게 한다.
- 다국어 본문이 생겼을 때도 같은 릴리즈노트에서 원문과 번역본의 대응 상태를 추적한다.
- 같은 날의 여러 수정 사항은 릴리즈노트에서 `### vYYYY.MM.DD` 한 항목으로 통합해 기록한다.

## 릴리즈노트 파일 위치

- 파일은 `management/release-notes/sections/part-XX/` 아래에 둔다.
- 파일명은 기본적으로 `Px-y.z.md` 형식을 사용한다.
- Part 시작 페이지와 Part 마무리 페이지는 각각 `Px-index.md`, `Px-summary.md` 형식을 사용한다.
- Part 바깥의 공개 진입 문서는 별도 하위 폴더를 두고 관리할 수 있다. 현재 소개 페이지와 독자용 목차 설명 페이지는 `book/` 아래에서 관리한다.
- 예:
  - `management/release-notes/sections/part-05/P5-11.1.md`
  - `management/release-notes/sections/part-06/P6-15.2.md`
  - `management/release-notes/sections/part-06/P6-index.md`
  - `management/release-notes/sections/part-07/P7-summary.md`

## 릴리즈노트 항목 형식

릴리즈노트 파일 상단에는 식별용 고정 항목만 남긴다.

- Section ID
- 대응 본문 경로

릴리즈노트의 버전별 개정 내용은 각 `### vYYYY.MM.DD` 항목에만 기록한다. 같은 날짜에 여러 차례 수정했더라도 버전 항목은 하나만 유지하고, 변경 이유와 본문 반영 내용을 그 한 항목 안에서 통합 정리한다. 각 버전 항목에는 다음을 우선 남긴다.

- 변경 이유
- 본문 반영 내용
- 번역 동기화 메모
- 번역 반영 상태
- 관련 자산
- 원문 기준 버전

세부 형식과 표기 순서는 같은 디렉터리의 `section-release-note-template.md`를 따른다.

## 릴리즈노트 파일 작업 순서

1. 대응하는 `part-XX/Section ID.md` 릴리즈노트 파일을 찾거나 새로 만든다.
2. 파일 상단 식별 항목의 `Section ID`와 대응 본문 경로를 확인한다.
3. 최신 `### vYYYY.MM.DD` 항목을 갱신하거나 새로 만든다.
4. 변경 이유, 본문 반영 내용, 번역 동기화 메모, 번역 반영 상태, 관련 자산, 원문 기준 버전을 필요한 범위에서 기록한다.
5. 같은 날짜에 여러 차례 수정했다면 버전 항목을 추가로 만들지 않고 최신 날짜 항목 안에 통합한다.

## Part 디렉터리 운영

- Part별 하위 폴더는 `part-01`, `part-02`처럼 현재 책의 Part 번호와 일치시킨다.
- 새 Part에서 처음 Section 릴리즈노트를 만들 때는 해당 Part 폴더를 먼저 만든다.
- Part 시작 페이지와 Part 마무리 페이지도 현재 기본 릴리즈노트 대상에 포함한다.
- 개요/마무리 페이지는 `Section ID` 대신 `P6-index`, `P6-summary`처럼 Part 단위 식별자를 사용해 추적한다.

## 공개 진입 문서 운영

- `docs/index.md`와 `docs/book/table-of-contents.md` 같은 공개 진입 문서도 릴리즈노트 대상에 포함한다.
- 대응 릴리즈노트 파일은 `management/release-notes/sections/book/` 아래에 둔다.
- 영어판과 다른 언어판이 추가되어도 같은 `Section ID`를 유지하고 공통 릴리즈노트에서 추적한다.

## 번역본 대응 원칙

- 릴리즈노트에는 다음을 구분해 남긴다.
  - 원문 기준 버전
  - 번역 반영 상태
  - 번역만 따로 손본 부분
- 공용 자산 수정 여부도 함께 남긴다.
- 번역본을 아직 만들지 않았더라도, 나중에 번역 동기화를 판단할 수 있게 `번역 동기화 메모`는 비워 두지 않고 최소 판단을 남긴다.
