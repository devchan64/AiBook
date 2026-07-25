# 개념사전 작성 규칙

작성일: 2026-07-24

## 목적과 범위

- 개념사전은 책 본문에서 반복 등장하는 핵심 개념을 다시 찾게 하는 독자용 참조 원고다.
- 개념사전은 본문을 대체하는 요약집이 아니라, 대표 표제어, 핵심 뜻, 대표 설명 위치, 재등장 위치를 압축해 연결하는 기준 원고다.
- 개념사전은 개인적 표현과 즉흥적 비유가 본문 전체에 흩어지지 않도록, 검증된 일반화 용어를 고정하는 장치다.
- 이 문서는 개념사전의 판단 기준과 작업 순서만 다룬다.
- 언어별 표제어 탐색, 인덱스 필드, 용량 관리는 `management/glossary-indexes/README.md`를 따른다.
- 원칙 문서인 이 파일은 별도 리비전노트를 두지 않고 문서 자체를 직접 갱신한다.

## 파일 위치

- 개념사전 공개 진입 원고: `docs/reference/concept-glossary.md`
- 단어별 개념사전 원고: `docs/reference/concept-glossary-terms/<english-slug>.<lang>.md`
  - 이 디렉터리는 단어별 항목 파일을 모아 두는 영어 기준 slug 디렉터리다.
- 한국어 자음별 색인 원고: `docs/reference/concept-glossary-parts/*.md`
- 영어 알파벳별 색인 원고: `docs/reference/concept-glossary.en.md`, `docs/reference/concept-glossary-alpha/*.en.md`
- 중국어 병음별 색인 원고: `docs/reference/concept-glossary.zh.md`, `docs/reference/concept-glossary-pinyin/*.zh.md`, `docs/reference/concept-glossary-zh-index.zh.md`
- 언어별 보조 인덱스:
  - `management/glossary-indexes/concept-glossary-index.ko.md`
  - `management/glossary-indexes/concept-glossary-index.en.md`
  - `management/glossary-indexes/concept-glossary-index.zh.md`

## 단어별 원고와 색인 조립 원칙

- 개념사전 항목 본문은 원칙적으로 단어별 파일 하나에 둔다. 자음별, 알파벳별, 병음별 파일에 항목 본문을 직접 누적하지 않는다.
- 단어별 파일명은 언어별 표제어가 아니라 영어 기준 용어를 kebab-case slug로 만든다.
  - 예: `git.ko.md`, `git.en.md`, `git.zh.md`
  - 예: `gradient-descent.ko.md`, `gradient-descent.en.md`, `gradient-descent.zh.md`
  - 예: `ann-approximate-nearest-neighbor.ko.md`, `ann-approximate-nearest-neighbor.en.md`, `ann-approximate-nearest-neighbor.zh.md`
- 영어 기준 용어가 바뀌면 파일명 변경이 링크와 검사에 영향을 주므로, 먼저 언어별 보조 인덱스에서 기존 slug와 새 slug의 관계를 확인한다.
- 각 언어별 공개 색인 구조는 유지한다. 한국어는 자음별, 영어는 알파벳별, 중국어는 병음별 색인을 유지하되, 색인 파일은 단어별 원고를 `pymdownx.snippets`로 include해 페이지를 만든다.
- MkDocs snippets 기준 경로는 `docs`이므로 include 경로는 `reference/concept-glossary-terms/<english-slug>.<lang>.md` 형식을 쓴다.
- 단어별 파일 안의 앵커는 영어 slug를 기준으로 둔다. 언어별 공개 색인에서 같은 단어 파일을 include하더라도 본문 링크와 검사 스크립트가 같은 기준으로 추적할 수 있어야 한다.
- 단어별 파일은 Section 파일처럼 독립적으로 검사할 수 있어야 한다. 항목 하나의 `Section ID`, `Version`, `Core/중심 Section`, `Appears/등장 Section` 대응을 파일 단위로 확인할 수 있게 유지한다.
- 색인 파일은 정렬, include 순서, 짧은 안내 문구만 맡는다. 뜻, 중요성, 관련 개념 같은 본문 필드는 단어별 파일에만 둔다.
- 임시 전환 기간에는 기존 자음별, 알파벳별, 병음별 파일에 직접 작성된 항목이 남아 있을 수 있다. 새 항목과 대규모 보강은 단어별 파일 구조를 우선 적용하고, 기존 직접 작성 항목은 이동 대상으로 본다.

## 핵심 원칙

- 개념사전 항목은 독자가 읽을 수 있는 문장으로 쓴다. 관리 메모, 검토 로그, 근거 분석을 개념사전 항목 안에 누적하지 않는다.
- 항목은 본문 내용을 그대로 복제하지 않고, 반복되는 개념의 핵심 자리만 압축한다.
- 대표 표제어와 핵심 정의는 가능한 한 공식 문서, 표준 문서, 교과서, 학술 논문, 연구기관·교육기관 용어집 같은 외부 레퍼런스로 확인한다.
- 표준 용어로 확인되지 않은 개인적 표현, 임시 번역어, 특정 Section 안에서만 통하는 표현은 대표 표제어로 바로 고정하지 않는다.
- 같은 개념은 같은 대표 표제어와 일반화 용어로 부른다. 다른 표현이 필요하면 첫 등장 문장 안에서 대표 표제어와 연결한다.
- 같은 한국어 표면형이라도 영어 기준 개념이 다르면 표제어를 분리한다.
- 개인적 비유나 직관은 주 정의가 아니라 보조 설명으로만 쓴다.
- 개념사전 항목은 본문에서 실제로 쓰였거나 곧 반복 사용될 개념을 우선 정리한다.

## 대표 설명 위치

- 같은 Part 안에서 반복 등장하는 주요 개념은 먼저 대표 설명 위치를 정한다.
- 대표 설명 위치는 그 개념이 처음 충분한 맥락, 쉬운 예시, 오해 방지 설명과 함께 나오는 Section이다.
- 개념사전의 `중심 Section`은 대표 설명 위치 하나만 가리킨다.
- 다른 Section에서 같은 개념이 다시 중요하게 쓰이면 `등장 Section`으로만 추적한다.
- 뒤 Part에서 같은 개념이 새로운 문제 설계 층위나 운영 층위로 다시 핵심이 되더라도 `중심 Section`은 하나만 유지하고, 새 본문 위치는 `등장 Section`으로 연결한다.

## 작업 순서

### 새 항목을 만들 때

1. 본문에서 실제로 반복되는 표현을 모은다.
2. 같은 개념을 가리키는 표현과 서로 다른 개념을 가리키는 표현을 나눈다.
3. 영어권 표준 용어 또는 널리 쓰이는 학술·기술 용어를 외부 레퍼런스로 확인한다.
4. 영어 기준 용어로 파일 slug를 정하고, 필요한 언어별 단어 파일을 만든다.
5. 한국어 대표 표제어와 영어 병기, 영어 표제어, 중국어 표제어를 언어별로 정한다.
6. 대표 설명 위치를 정하고 `중심 Section`을 하나만 적는다.
7. 관련 언어별 색인 파일에 단어 파일 include를 추가한다.
8. 관련 언어별 보조 인덱스를 갱신한다. 세부 기준은 `management/glossary-indexes/README.md`를 따른다.
9. 본문 설명이 부족하면 개념사전만 늘리지 말고 해당 Section 보강을 먼저 검토한다.

### 기존 항목을 바꿀 때

1. 기존 대표 표제어, 영어 병기, `중심 Section`, `등장 Section`을 확인한다.
2. 표제어·정의·대표 설명 위치 변경이 본문과 충돌하지 않는지 확인한다.
3. 표제어를 합치거나 나눌 때는 한국어 표면형보다 영어 기준 개념을 먼저 본다.
4. 영어 기준 slug가 달라지는지 확인한다. slug가 바뀌면 단어별 파일명, 언어별 색인 include, 본문 링크, 보조 인덱스를 함께 갱신한다.
5. 대표 설명 위치를 옮겼다면 관련 본문, 개념사전, 관련 Section 릴리즈노트를 함께 갱신한다.
6. 개념사전 자체의 전용 릴리즈노트 파일은 만들지 않고 `Version`만 갱신한다.

### 본문에서 다시 연결할 때

- 같은 Part 안에서 이미 대표 설명 위치가 있는 개념은 후속 Section에서 상세 정의를 반복하지 않는다.
- 현재 질문에 필요한 최소 연결만 남기거나 개념사전 해당 표제어 앵커로 연결한다.
- 같은 용어를 개념사전으로 직접 링크하는 위치는 기본적으로 한 Section 안에서 1회만 둔다.
- 개념사전 링크는 가능하면 페이지 전체가 아니라 표제어별 세부 앵커를 사용한다.

## 항목 구조

각 단어별 원고 파일은 다음 정보를 기본으로 포함한다.

```md
### 모델(model, 모형)

- 뜻: 현실 전체를 그대로 복사한 것이 아니라, 목적에 맞게 줄여 만든 계산용 모형입니다.
- 왜 중요한가: ...
- 함께 볼 개념: `입력(input)`, `출력(output)`
- 중심 Section: `P1-4.1`
- 등장 Section: `P1-14.1`, `P1-14.3`
```

규칙:

- 한 파일에는 원칙적으로 하나의 대표 표제어만 둔다.
- 항목 제목 수준은 색인 파일에 include될 때의 문서 구조를 고려해 `###`를 기본으로 한다.
- 항목 파일 안에는 자음·알파벳·병음 색인용 제목을 따로 넣지 않는다.
- `중심 Section`은 하나만 적는다.
- `등장 Section`에는 대표 설명 위치를 반복하지 않고, 실제 재등장 위치만 적는다.
- Section은 파일 경로가 아니라 `P1-4.1` 같은 `Section ID`로 적는다.
- 뜻이 다른 개념을 하나의 표제어 안에 억지로 병렬 배치하지 않는다.
- 표현만 다른 동의어는 별도 항목으로 만들지 말고 대표 항목 안에서 함께 설명한다.

색인 파일에서 항목을 불러올 때는 다음 형식을 쓴다.

```md
--8<-- "reference/concept-glossary-terms/model.ko.md"
```

규칙:

- include 대상 파일은 항상 `docs/reference/concept-glossary-terms/` 아래의 단어별 원고 파일이어야 한다.
- `docs/reference/concept-glossary-parts/`, `docs/reference/concept-glossary-alpha/`, `docs/reference/concept-glossary-pinyin/` 파일끼리는 서로 include하지 않는다.
- 언어별 색인 파일은 해당 언어의 단어별 원고 파일을 include하고, 정의 원고를 색인 파일에 직접 복제하지 않는다.
- include 경로를 바꿨다면 MkDocs 빌드에서 snippet 경로 오류가 나지 않는지 확인한다.

## 정렬과 중복

- 항목 본문은 단어별 파일에 둔다. `docs/reference/concept-glossary.md`와 언어별 색인 파일은 소개와 include 목록만 유지한다.
- 새 항목은 영어 기준 slug로 단어별 파일을 만들고, 각 언어 색인의 정렬 기준에 맞는 파일에 include한다.
- 한국어 자음별 파일 안에서는 한국어 표제어 기준 가나다순 include 순서를 유지한다.
- 영어 알파벳별 파일 안에서는 영어 표제어 기준 알파벳순 include 순서를 유지한다.
- 중국어 병음별 파일 안에서는 중국어 표제어의 병음 기준 include 순서를 유지한다.
- 영어판 개념사전은 영문 독자가 한국어 개념사전 페이지로 되돌아가지 않도록 알파벳별 영문 전용 페이지에서 단어별 영문 원고를 include한다. 각 영어 표제어 링크는 `docs/reference/concept-glossary-alpha/*.en.md`의 대응 앵커로 연결한다.
- 영어판 개념사전 항목은 영어 독자 기준으로 작성한다. 항목 본문에는 `Korean term:` 행, 한국어 표제어 병기, 한국어 설명 문장을 넣지 않는다.
- 영어판 개념사전의 `Related concepts`도 영어 표제어만 쓴다. `과적합(overfitting)`처럼 한국어 표기와 영어 표기를 함께 넣지 않는다.
- 한국어 개념사전의 `뜻`, `왜 중요한가`, `함께 볼 개념`, `중심 Section`, `등장 Section` 구조를 영문 개념사전에도 대응시키되, `Meaning`, `Why it matters`, `Related concepts`, `Core Section`, `Appears in`으로 영어화한다.
- 영어판 개념사전 항목이 아직 충분히 번역되지 않았더라도 한국어 자음별 개념사전으로 되돌려 링크하지 않는다. 해당 영어 단어 파일을 보강 대상으로 남긴다.
- 중국어판 개념사전도 영문 개념사전과 같은 원칙으로 운영한다. 중국어 독자가 한국어 개념사전 페이지로 되돌아가지 않도록 병음별 중국어 전용 페이지에서 단어별 중국어 원고를 include한다. 각 중국어 표제어 링크는 `docs/reference/concept-glossary-pinyin/*.zh.md` 또는 중국어 전용 개념사전 항목 페이지의 대응 앵커로 연결한다.
- 중국어판 개념사전은 단순 탐색 색인이나 한국어 항목으로 보내는 중간 페이지가 아니라 중국어 독자용 직접 본문을 조립한 페이지여야 한다.
- 중국어판 개념사전의 `Section ID`와 `Version`은 대응 한국어 항목과 추적 가능하게 유지한다. 중국어 번역만 보강한 경우에는 원문 기준 `Version`을 임의로 올리지 않고, 필요하면 관리 메모나 공통 릴리즈노트에 중국어판 보강 사실을 남긴다.
- 중국어판 개념사전 항목은 중국어 독자 기준으로 작성한다. 항목 본문에는 한국어 표제어 병기나 한국어 설명 문장을 넣지 않는다.
- 중국어판 개념사전의 관련 개념은 중국어 표제어를 우선 쓰고, 필요한 경우에만 영어 원어를 짧게 병기한다. 한국어 표기와 중국어·영어 표기를 함께 나열하지 않는다.
- 한국어 개념사전의 `뜻`, `왜 중요한가`, `함께 볼 개념`, `중심 Section`, `등장 Section` 구조를 중국어 개념사전에도 대응시키되, 중국어 필드명으로 자연스럽게 옮긴다.
- 중국어판 개념사전 항목이 아직 충분히 번역되지 않았더라도 한국어 자음별 개념사전으로 되돌려 링크하지 않는다. 해당 중국어 단어 파일을 보강 대상으로 남긴다.
- 표제어는 기본적으로 한글 표제어 기준 가나다순으로 정렬한다.
- 영어 원어는 표제어 괄호 안에 병기한다.
- 영문 약어가 더 널리 쓰이는 경우에도 가능한 한 한글 표제어를 먼저 세운다. 다만 책 본문에서 약어가 중심 용어라면 실제 표제어 문자열을 기준으로 정렬한다.
- 새 항목을 추가하기 전에는 기존 개념사전과 언어별 인덱스에서 같은 뜻의 표제어가 이미 있는지 확인한다.

권장 구조:

```text
docs/reference/
  concept-glossary.md
  concept-glossary.en.md
  concept-glossary.zh.md
  concept-glossary-terms/
    README.md
    model.ko.md
    model.en.md
    model.zh.md
    parameter-function.ko.md
    parameter-model.ko.md
  concept-glossary-parts/
    05-mieum.md
  concept-glossary-alpha/
    m.en.md
    p.en.md
  concept-glossary-pinyin/
    m.zh.md
```

## 외부 레퍼런스와 근거 기록

- 대표 표제어, 영어 병기, 핵심 정의를 바꿀 때는 표준화된 외부 레퍼런스를 확인한다.
- 서로 다른 레퍼런스가 다른 용어를 쓰면 한쪽을 바로 표준으로 단정하지 않고, 어느 맥락에서 어떤 표현이 쓰이는지 비교한다.
- 개념사전 항목 본문에는 레퍼런스 목록을 반복해서 붙이지 않는다.
- 검증 근거는 관련 Section의 `출처와 참고 자료` 또는 언어별 인덱스의 짧은 `검증 레퍼런스`로 추적한다.
- 외부 레퍼런스가 없는 임시 표현은 `검증 필요`로 두고, 대표 표제어가 아니라 본문 안의 작업 가설이나 보조 설명으로 제한한다.

## 함께 볼 문서

- `management/glossary-indexes/README.md`: 언어별 인덱스 형식과 용량 관리
- `management/guidelines/manuscript-writing-workflow.md`: 본문 작성, 후속 Section 축약, Section 경계
- `management/guidelines/section-metadata-guidelines.md`: `Section ID`, `Version`, 릴리즈노트 예외
- `management/release-notes/sections/README.md`: 관련 Section 릴리즈노트 형식
