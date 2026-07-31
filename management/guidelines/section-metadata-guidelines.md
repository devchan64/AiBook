# Section 메타데이터 관리 가이드

이 문서는 본문 파일을 `Section ID`와 `Version`으로 추적하는 규칙만 다룬다. Section의 학습 산출물은 `section-learning-focus-guidelines.md`, 본문 구성과 표현은 `manuscript-writing-workflow.md`, 릴리즈노트 파일 형식은 `../release-notes/sections/README.md`를 따른다.

## 목적

- Section 단위 작업을 파일명이 아니라 `Section ID`로 추적한다.
- 본문 제목, 제목 아래 메타데이터, 릴리즈노트 파일이 같은 단위를 가리키게 한다.
- 번역본이 생겨도 원문과 번역본의 대응 관계를 같은 `Section ID`로 유지한다.
- 릴리즈노트 예외 문서를 구분해 불필요한 관리 파일 생성을 막는다.

## 적용 대상

- `docs/parts/part-XX/chapter-YY/section-ZZ.md`
- `docs/parts/part-XX/index.md`
- `docs/parts/part-XX/summary.md`
- `docs/index.md`
- `docs/table-of-contents.md`
- `docs/reference/concept-glossary.md`

## 본문 메타데이터 형식

Section 제목 바로 아래에는 다음 두 줄만 둔다.

```md
> Section ID: `P5-11.1`
> Version: `v2026.07.05`
```

- `Section ID`는 제목 앞 인덱스와 같은 값을 사용한다.
- 제목 앞 인덱스는 `P5-11.1`처럼 전체 식별자를 쓰고, `11.1`처럼 줄이지 않는다.
- `Version`은 수정일 기준 `vYYYY.MM.DD` 형식을 사용한다.
- 날짜성 메타데이터는 `Version` 한 줄로만 관리한다.
- `Last Updated` 같은 별도 수정일 메타데이터는 Section 본문에 두지 않는다.

## 식별자 원칙

- 장별 본문 Section은 목차 인덱스와 같은 `Section ID`를 사용한다.
- Part 시작 페이지와 마무리 페이지는 각각 `P6-index`, `P6-summary` 같은 식별자를 사용한다.
- 소개 페이지는 `BOOK-index`를 사용한다.
- 독자용 목차 설명 페이지는 `BOOK-toc`를 사용한다.
- 번역본은 원문과 같은 `Section ID`를 유지한다.
- 한국어 원문 변경을 번역본에 반영하는 작업에서는 번역본 `Version`도 원문 기준 `Version`에 맞춘다.

## 릴리즈노트 연결

- 본문을 실제로 수정했다면 가능한 한 같은 작업에서 대응 릴리즈노트 파일도 갱신한다.
- 릴리즈노트 파일의 위치, 파일명, 항목 형식은 `../release-notes/sections/README.md`를 따른다.
- 번역 반영 상태, 언어별 추가 수정, 번역 동기화 메모는 각 번역 가이드와 릴리즈노트 파일 관리 문서를 따른다.
- 다음 문서는 메타데이터만 갱신하고 별도 Section 릴리즈노트 파일은 만들지 않는다.
  - `docs/table-of-contents.md`
  - `docs/reference/concept-glossary.md`

## 작업 순서

1. 수정 대상 본문의 `Section ID`를 확인한다.
2. 제목 앞 인덱스와 제목 아래 `Section ID`가 같은 값인지 확인한다.
3. 본문 제목 아래 `Version`을 수정일 기준으로 갱신한다.
4. 릴리즈노트 예외 문서가 아니라면 대응 릴리즈노트 파일을 갱신하거나 새로 만든다.
5. 변경 이유와 본문 반영 내용은 릴리즈노트 파일 관리 문서의 형식에 맞춰 남긴다.
6. Section의 중심 질문이나 학습 산출물이 바뀌었다면 `section-learning-focus-guidelines.md`를 별도로 확인한다.

## 적용 범위

- 이 규칙은 지금부터 수정하는 Section과 Part 시작/마무리 페이지부터 적용한다.
- 기존 본문 전체를 한 번에 소급 정리하지 않는다.
- 이미 손대는 Section이나 Part 개요/마무리 페이지라면 버전 코드와 릴리즈노트를 함께 확인한다.

## 함께 볼 문서

- `../../AGENTS.md`
- `section-learning-focus-guidelines.md`
- `manuscript-writing-workflow.md`
- `../release-notes/sections/README.md`
