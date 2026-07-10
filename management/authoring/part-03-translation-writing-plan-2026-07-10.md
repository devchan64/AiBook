# Part 3 번역문 작성 계획

작성일: 2026-07-10

## 목적

- 이 문서는 Part 3 데이터 모델링 본문을 영어판과 중국어 간체판으로 옮길 때의 작업 순서와 검수 기준을 정리한다.
- 목표는 `한국어 원문 구조 유지`, `Section ID / Version 정합성`, `공통 릴리즈노트 추적`, `라인 수 기반 누락 점검`, `언어별 내부 링크 품질`을 동시에 맞추는 것이다.

## 현재 기준선

- 한국어 원문 범위: `docs/parts/part-03/`
- 현재 Part 3 한국어 본문 수: 54개 Markdown
  - Part 시작 페이지 `index.md`
  - Part 마무리 페이지 `summary.md`
  - Chapter 1-9 Section 52개
- 현재 영어판 상태: `docs/en/parts/part-03/` 없음
- 현재 중국어 간체판 상태: `docs/zh/parts/part-03/` 없음

## 기본 원칙

- 번역 기준점은 항상 한국어 원문의 `Section ID`와 `Version`이다.
- 영어판과 중국어 간체판 모두 한국어 원문과 같은 제목 인덱스, `Section ID`, `Version`을 유지한다.
- 번역은 문장 치환이 아니라 `중심 질문`, `설명 범위`, `예시 역할`, `점검 질문`까지 같은 학습 책임을 옮기는 작업으로 본다.
- 한국어 원문에 없는 주장, 사례, 판단, 범위 확장을 번역본에 임의로 추가하지 않는다.
- 번역본만 별도 릴리즈노트를 만들지 않고, 기존 `management/release-notes/sections/part-03/` 공통 파일에 기록한다.

## 작업 범위

번역 대상은 다음 54개 문서 전체다.

1. `docs/parts/part-03/index.md`
2. `docs/parts/part-03/summary.md`
3. `docs/parts/part-03/chapter-01/section-01.md`부터 `chapter-09/section-13.md`까지의 모든 Section

언어별 출력 경로는 다음을 기준으로 한다.

- 영어판: `docs/en/parts/part-03/...`
- 중국어 간체판: `docs/zh/parts/part-03/...`

## 권장 순서

### 1. Part 뼈대 생성

- `docs/en/parts/part-03/`, `docs/zh/parts/part-03/` 디렉터리 구조를 한국어판과 같은 Chapter 단위로 만든다.
- `index.md`, `summary.md`를 먼저 만들어 Part 입구와 출구를 고정한다.
- `mkdocs.yml`의 영어/중국어 `nav`는 실제 파일이 생긴 뒤 연결한다.

### 2. Chapter 단위 번역

번역은 다음 5개 묶음으로 진행한다.

1. Chapter 1-2
2. Chapter 3-4
3. Chapter 5-6
4. Chapter 7-8
5. Chapter 9 + `summary.md`

이 순서를 쓰는 이유는 다음과 같다.

- Chapter 1-2는 Part 3의 문제 정의, 샘플 단위, 표 구조를 잡는 입구다.
- Chapter 3-6은 원시 로그, 특징, 기준선 비교, 세그먼트 표현처럼 번역 용어가 반복되는 본론 구간이다.
- Chapter 7-9는 표본 수, 반복성, Part 4 인계 전제를 설명하므로 앞 구간 용어가 정리된 뒤 번역하는 편이 안정적이다.

### 3. 언어 순서

각 묶음은 다음 순서를 기본으로 한다.

1. 한국어 원문 확인
2. 영어판 작성
3. 영어판 라인 수 / 링크 / 릴리즈노트 점검
4. 중국어 간체판 작성
5. 중국어 간체판 라인 수 / 링크 / 릴리즈노트 점검

영문 도식과 영문 자산은 가능한 한 공용 기준 원본으로 유지한다.

## 문서별 작업 절차

각 Section 또는 Part 페이지를 번역할 때는 아래 순서를 고정한다.

1. 한국어 원문의 `Section ID`, `Version`, 중심 질문을 확인한다.
2. 기존 번역본이 없으므로 새 파일을 생성한다.
3. 제목, `Section ID`, `Version` 두 줄을 먼저 맞춘다.
4. 표, 목록, 예시, Mermaid, 체크리스트를 한국어판과 같은 역할로 옮긴다.
5. 내부 링크는 가능한 한 같은 언어 경로를 먼저 연결한다.
6. 공통 릴리즈노트 파일에 번역 반영 상태와 `원문 기준 버전`을 기록한다.

## 검수 기준

- 영어판과 중국어 간체판 모두 한국어 원문 대비 `빈 줄 제외 라인 수 차이 5% 미만`을 기본 기준으로 삼는다.
- 5% 이상 차이가 나면 먼저 다음 가능성을 점검한다.
  - 설명 단계 누락
  - 표 / 목록 과축약
  - 사례 문단 생략
  - 체크리스트 / 회수 문단 누락
  - 링크 문장 누락
- 제목 개수(`##`, `###`)가 한국어 원문과 같은지도 함께 확인한다.
- `Version`이 같아도 번역본만 추가 수정을 했다면 릴리즈노트에 `언어별 추가 수정`으로 남긴다.

## 용어 운영 기준

- 영어판은 `representation`, `feature`, `baseline`, `split`, `evaluation`, `handoff`, `target`, `label` 같은 Part 3 핵심 용어를 일관되게 유지한다.
- 중국어 간체판은 한국어 원문의 뜻이 먼저 읽히도록 번역하되, 필요할 때만 영어 원어를 병기한다.
- `inference`, `prediction`, `generation`, `model`, `parameter`, `level`, `layer` 같은 다의어는 기존 가이드 기준대로 문맥을 분리한다.
- Part 3 특성상 `sample`, `raw log`, `aggregated table`, `feature`, `baseline model`, `review queue` 같은 기능어가 자주 나오므로, 각 Chapter 초반에서 번역어를 먼저 안정시킨다.

## 릴리즈노트 반영 기준

- 대응 파일: `management/release-notes/sections/part-03/P3-*.md`
- 각 번역 작업 시 최소한 다음 항목을 갱신한다.
  - `번역 동기화 메모`
  - `번역 반영 상태`
  - `원문 기준 버전`
- `index.md`, `summary.md`는 `P3-index.md`, `P3-summary.md` 릴리즈노트에서 함께 추적한다.

## 완료 판정 기준

Part 3 번역문 작성은 아래 조건을 모두 만족할 때 완료로 본다.

- 영어판 `docs/en/parts/part-03/`에 한국어 원문 대응 54개 파일이 모두 존재한다.
- 중국어 간체판 `docs/zh/parts/part-03/`에 한국어 원문 대응 54개 파일이 모두 존재한다.
- 각 파일의 `Section ID`, 제목 인덱스, `Version`이 한국어 원문과 맞는다.
- 각 파일의 `빈 줄 제외 라인 수 차이`가 기본적으로 5% 미만이거나, 예외 사유가 명시되어 있다.
- 공통 릴리즈노트에 영어판 / 중국어 간체판 반영 상태가 기록되어 있다.
- 영어 / 중국어 `nav`가 실제 존재 파일만 가리킨다.

## 바로 다음 작업

1. `docs/en/parts/part-03/`와 `docs/zh/parts/part-03/` 디렉터리 뼈대를 만든다.
2. `index.md`, `summary.md`, Chapter 1-2를 첫 번역 묶음으로 진행한다.
3. 첫 묶음 완료 후 라인 수 비교 리포트를 간단히 남겨 용어 기준이 안정적인지 점검한다.
