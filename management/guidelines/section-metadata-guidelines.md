# Section 메타데이터 관리 가이드

작성일: 2026-07-18

이 문서는 책 본문 문서의 `Section ID`, 제목 앞 인덱스, `Version`, 릴리즈노트 연결 방식을 관리한다. 릴리즈노트 파일 자체의 위치와 항목 형식은 `../release-notes/sections/README.md`를 따른다. 다만 `docs/table-of-contents.md`와 `docs/reference/concept-glossary.md`는 `Section ID`와 `Version`만 유지하고, 별도 Section 릴리즈노트는 연결하지 않는다.

## 목적

- Section 단위 작업을 파일명이 아니라 `Section ID`로 추적한다.
- 본문 제목, 본문 메타데이터, 릴리즈노트 파일이 같은 단위를 가리키게 한다.
- 다국어 본문이 생겨도 원문과 번역본의 대응 관계를 같은 `Section ID`로 추적할 수 있게 한다.

## 언제 이 문서를 보는가

- Section 본문을 새로 만들거나 수정할 때
- Part 시작 페이지나 Part 마무리 페이지를 수정할 때
- `docs/index.md`, `docs/table-of-contents.md` 같은 공개 진입 문서를 수정할 때
- 번역본 작업 전에 원문과 번역본의 기준 키가 같은지 확인할 때
- 본문 수정에 대응하는 릴리즈노트 파일을 찾거나 만들 때

## 본문 메타데이터 원칙

- Section을 실제로 수정했다면 본문만 고치고 끝내지 않는다.
- 수정한 Section의 제목 바로 아래에는 다음 두 줄만 둔다.
  - `Section ID`
  - `Version`
- 버전 코드는 수정일 기준 `vYYYY.MM.DD` 형식을 사용한다.
- `Section ID`는 목차 인덱스와 같은 값을 사용한다. 예를 들어 `P5-11.1`처럼 본문 번호와 직접 대응해야 한다.
- Section 제목 앞 인덱스도 `Section ID`와 완전히 같은 값을 사용한다. 축약형 번호를 제목에 별도로 두지 않는다.
- Section의 날짜성 메타데이터는 `Version` 한 줄만 사용한다.
- `Last Updated` 같은 별도 수정일 메타데이터는 Section 본문에 두지 않는다.
- 같은 날 여러 번 수정해도 Section 본문 안의 버전 코드는 날짜 기준으로 유지한다.
- 본문을 수정했다면 가능한 한 같은 작업에서 릴리즈노트 파일도 함께 갱신한다.
- 릴리즈노트 파일 위치와 항목 형식은 `../release-notes/sections/README.md`를 따른다.
- 예외: `docs/table-of-contents.md`와 `docs/reference/concept-glossary.md`는 릴리즈노트 파일을 따로 두지 않는다.

## 본문 메타데이터 형식

Section 제목 바로 아래에 다음 형식을 둔다.

```md
> Section ID: `P5-11.1`
> Version: `v2026.07.05`
```

규칙:

- `Section ID`는 언어가 달라도 같은 개념 단위를 가리켜야 한다.
- 제목 앞 인덱스는 `Section ID`를 그대로 반복해야 하며, `P5-11.1`을 `11.1`처럼 줄여 쓰지 않는다.
- `Version`은 수정일 기준 버전이다.
- 날짜성 메타데이터는 `Version` 한 줄로만 관리한다.
- 번역본이 추가되더라도 이 두 값은 언어별 파일명보다 먼저 Section 단위의 기준 키로 취급한다.

## 작업 순서

1. 수정 대상 본문의 `Section ID`를 확인한다.
2. 제목 앞 인덱스와 제목 아래 `Section ID`가 같은 값인지 확인한다.
3. 본문 제목 아래 메타데이터의 `Version`을 수정일 기준으로 갱신한다.
4. 대응 릴리즈노트 파일을 갱신하거나 새로 만든다.
5. 변경 이유와 본문 반영 내용은 릴리즈노트 파일 관리 문서의 형식에 맞춰 남긴다.
6. 같은 작업에서 Part 체크포인트 노트를 함께 보면, 작업 로그를 누적하지 말고 목차 기준 중심 주제와 구조 판단만 유지한다.

`docs/table-of-contents.md`와 `docs/reference/concept-glossary.md`를 수정할 때는 위 4, 5단계를 적용하지 않는다. 이 경우에는 본문 메타데이터와 해당 문서 전용 가이드 정합성만 확인한다.

## 번역본 메타데이터 연결

- 번역본이 생기면 `Section ID`는 원문과 동일하게 유지한다.
- 기존 번역본이 있으면 대응 한국어 원문의 현재 `Version`과 번역본의 `Version`을 먼저 비교한다.
- 번역 반영 상태, 언어별 추가 수정, 번역 동기화 메모의 세부 작성 방식은 각 번역 가이드와 릴리즈노트 파일 관리 문서를 따른다.

## 공개 진입 문서와 Part 페이지

- Part 시작 페이지와 Part 마무리 페이지도 현재 기본 메타데이터 관리 대상에 포함한다.
- 개요/마무리 페이지는 `Section ID` 대신 `P6-index`, `P6-summary`처럼 Part 단위 식별자를 사용해 추적한다.
- `docs/index.md`와 `docs/table-of-contents.md` 같은 공개 진입 문서도 본문 메타데이터로 추적한다.
  - 소개 페이지: `BOOK-index`
  - 독자용 목차 설명 페이지: `BOOK-toc`
- `docs/index.md`는 대응 릴리즈노트 파일을 유지하지만, `docs/table-of-contents.md`는 별도 Section 릴리즈노트 파일을 만들지 않는다.
- `docs/reference/concept-glossary.md`는 공개 참조 문서로 추적하되, 대응 릴리즈노트 파일은 만들지 않는다.

## 지금부터의 적용 범위

- 이 규칙은 지금부터 수정하는 Section과 Part 시작/마무리 페이지부터 적용한다.
- 기존 본문 전체를 한 번에 소급 정리하지 않는다.
- 다만 이미 손대는 Section이나 Part 개요/마무리 페이지라면 버전 코드와 릴리즈노트를 함께 추가하는 것을 기본으로 한다.
- 독자용 목차와 개념사전은 같은 적용 범위 안에서도 예외로 두며, 버전 코드는 갱신하되 릴리즈노트는 추가하지 않는다.

## 함께 볼 문서

- `../../AGENTS.md`
- `manuscript-writing-workflow.md`
- `../release-notes/sections/README.md`
