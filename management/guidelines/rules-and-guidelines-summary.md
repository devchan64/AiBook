# 집필 규칙·가이드라인 요약

작성일: 2026-07-01

이 문서는 저장소의 집필 규칙을 빠르게 다시 잡기 위한 운영용 요약입니다. 기준 원문은 `AGENTS.md`와 `management/guidelines/` 아래 문서이며, 실제 수정 전에는 필요한 원문을 다시 확인하는 것을 원칙으로 합니다.

## 기준 문서 맵

이 저장소의 문서는 성격이 다릅니다. 먼저 `규칙 원문`, 그다음 `작업형 가이드`, 마지막으로 `분석 메모`를 구분해서 읽는 것이 가장 효율적입니다.

### 1. 규칙 원문

이 문서들은 판단이 충돌할 때 우선권을 가집니다.

| 문서 | 역할 | 먼저 볼 때 |
| --- | --- | --- |
| `AGENTS.md` | 저장소 전체 규칙의 기준 원문 | 모든 작업 시작 전 |

### 2. 작업형 가이드

이 문서들은 특정 작업을 할 때 강하게 참고해야 하는 실행 기준입니다.

| 문서 | 역할 | 먼저 볼 때 |
| --- | --- | --- |
| `management/guidelines/manuscript-writing-workflow.md` | 원고 작성 세부 절차 | Part/Section 초안 작성, 초심자 보강, 사례 작성 전 |
| `management/guidelines/python-example-guidelines.md` | Python 예제 작성 기준 | Python 예제 추가·수정, 코드 블록 유지 여부 판단 전 |
| `AGENTS.md` | 초심자 설명·예시 보강 기준 | 새 Section 초안, 예시 보강, 보충학습 분리 판단 전 |
| `management/guidelines/chart-guidelines.md` | 차트·도식 작성과 검증 기준 | Mermaid, SVG, 차트 추가·수정 전 |
| `management/release-notes/sections/README.md` | Section 버전 코드와 릴리즈노트 관리 기준 | Section 수정, 번역본 동기화, 개정 이력 기록 전 |
| `management/authoring/part-XX-open-checklist.md` | Part별 미반영 작업 체크리스트 | 기존 메모 정리, 후속 작업 우선순위 점검 전 |

### 3. 보조 메모와 분석 문서

이 문서들은 규칙 원문이라기보다, 기존 원고를 정리하거나 후속 판단을 돕는 참고 자료입니다.

| 문서 | 역할 | 주로 볼 때 |
| --- | --- | --- |
| `management/authoring/author-notes.md` | 저자 관점 문장을 다듬기 위한 메모 | 머리말, 도입부, 관점 문장 정리 시 |
| `management/authoring/section-...-evidence-analysis.md` | 특정 Section의 근거 검토 메모 | 기존 절 수정, 근거 확인, 후속 설명 위치 판단 시 |

## 문서별 역할 분담

- `AGENTS.md`: 프로젝트 목적, 독자 기준, 문서 위치, Section 경계, Python 예제 원칙, 용어, 출처, 저작권, 배포, 빌드 검증까지 포함하는 최상위 규칙 문서입니다.
- `AGENTS.md`: 초심자가 막히는 지점을 현재 Section 안에서 풀지, `보충학습`으로 분리할지 판단하는 기준이 포함되어 있습니다.
- `management/guidelines/manuscript-writing-workflow.md`: Part/Section 작성, 초심자 보강, 사례 작성, Section 경계 같은 원고 작성 절차를 다루는 상세 문서입니다.
- `management/guidelines/python-example-guidelines.md`: Python 예제의 입력·출력 제시 방식, 금지 패턴, 초심자 점검 기준을 다루는 상세 문서입니다.
- `management/guidelines/chart-guidelines.md`: 차트의 표현 방식, Mermaid 우선 원칙, SVG 예외 조건, 레이아웃, 겹침 방지, 검증 기준까지 다루는 상세 문서입니다.
- `management/release-notes/sections/README.md`: Section 버전 코드, 수정일 기준 버전 갱신, 제목 앞 인덱스와 `Section ID`의 동일 규칙, Section별 릴리즈노트 파일 관리 방식을 다루는 운영 문서입니다.
- `management/release-notes/sections/README.md`: 앞으로 번역본이 생겼을 때도 `Section ID` 기준으로 대응 버전을 추적하는 운영 문서입니다.
- `management/guidelines/english-translation-guidelines.md`: 영어 번역 시 한국어 원문 대조, 공통 릴리즈노트 기록, `빈 줄 제외 라인 수 5% 미만` 검수 기준을 포함한 번역 운영 문서입니다.
- `management/guidelines/chinese-translation-guidelines.md`: 중국어 간체 번역 시 한국어 원문 대조, 공통 릴리즈노트 기록, `빈 줄 제외 라인 수 5% 미만` 검수 기준을 포함한 번역 운영 문서입니다.
- 원칙 문서와 가이드라인 문서는 별도 리비전노트를 두지 않고 문서 자체를 직접 갱신합니다.
- `author-notes.md`: 본문 규칙 문서가 아니라, 저자 관점 문장을 안전하게 일반화하기 위한 메모입니다. 사실 주장 근거 문서로 사용하지 않습니다.
- `section-...-evidence-analysis.md`: 개별 Section의 근거, 용어, 출처 충돌, 회수 위치를 기록하는 문서입니다. 전역 규칙은 아니지만, 해당 절 수정 시에는 실질적으로 가장 가까운 작업 메모입니다.
- `part-XX-open-checklist.md`: 이미 반영된 설명을 반복 저장하지 않고, 각 Part에서 아직 남은 작업만 추린 체크리스트입니다.

## 작업 유형별 참조 순서

### Section 본문을 새로 쓰거나 크게 고칠 때

1. `AGENTS.md`
2. `management/guidelines/manuscript-writing-workflow.md`
3. 필요하면 해당 `section-...-evidence-analysis.md`
4. 문단 재구성이 크면 `management/guidelines/manuscript-writing-workflow.md`의 문단 구조 점검 메모를 같이 본다.
5. Part 수준 후속 작업이 있으면 해당 `part-XX-open-checklist.md`
6. 실제로 수정한 Section이라면 `management/release-notes/sections/README.md`를 따라 버전 코드와 릴리즈노트도 함께 갱신한다.
7. 번역본이 아직 없더라도 릴리즈노트에 번역 반영 필요 여부를 남긴다.

### Python 예제를 넣거나 고칠 때

1. `AGENTS.md`의 Python 예제 원칙
2. `management/guidelines/python-example-guidelines.md`
3. 현재 Section의 중심 질문과 출력값 점검
4. 필요하면 `AGENTS.md`의 초심자 보강 기준으로 예제 보강 수준 판단

### 차트, Mermaid, SVG를 만들 때

1. `AGENTS.md`의 도식 원칙
2. `chart-guidelines.md`
3. 다국어 본문이면 Mermaid include 경로와 일반 SVG/파일 링크 경로를 구분해 다시 본다.

### 관점 문장, 머리말, 도입 문장을 다듬을 때

1. `AGENTS.md`의 기본 관점과 집필 태도
2. `author-notes.md`
3. 사실 주장이 섞이면 별도 근거 확인

## 노트 정리 원칙

- `section-...-evidence-analysis.md`에는 근거와 용어 판단, 현재 본문에서 아직 중요한 경계만 남깁니다.
- 이미 본문에 반영된 집필 메모나 끝난 작업 목록은 Section 메모에 계속 누적하지 않습니다.
- 후속 작업은 가능한 한 `part-XX-open-checklist.md`로 옮겨 Part 단위로 관리합니다.
- `review`, `plan`, `curriculum-review` 문서의 남은 항목을 Part 체크리스트로 옮겼다면 원본 문서는 삭제해도 됩니다.
- evidence 메모를 폐기할 때는 대응 원고 본문과 참고문헌 반영을 먼저 대조하고, 구조가 어긋나는 메모는 자동 폐기하지 않습니다.

## 핵심 리마인더

- 최상위 원칙은 `AGENTS.md`를 기준으로 다시 확인합니다. 이 문서는 원칙 원문을 재서술하지 않습니다.
- Section 경계, 권장 구조, 초심자 보강, 사례 작성, `보충학습` 분리 판단은 `manuscript-writing-workflow.md`를 기준으로 봅니다.
- 개념사전 항목 구조, `중심 Section`·`등장 Section`, 표제어 분리 기준은 `concept-glossary-guidelines.md`를 기준으로 봅니다.
- Python 예제 세부 규칙은 `python-example-guidelines.md`, 차트·도식 세부 규칙은 `chart-guidelines.md`를 기준으로 봅니다.
- 본문 Section를 실제로 수정했다면 `Version`과 릴리즈노트 갱신을 같은 작업 안에서 함께 확인합니다.

## 빠른 점검표

1. 이 작업의 기준 원문이 `AGENTS.md`인지, 작업형 가이드인지 먼저 구분했는가?
2. Section 본문 수정이라면 `manuscript-writing-workflow.md`와 릴리즈노트 가이드를 함께 열었는가?
3. 개념 위치, 대표 설명 위치, 개념사전 링크 판단이라면 `concept-glossary-guidelines.md`를 다시 확인했는가?
4. 예제, 차트, 번역처럼 전용 가이드가 있는 작업을 요약 문서만 보고 처리하고 있지는 않은가?
5. 끝난 판단을 메모 문서에 계속 누적하지 않고 체크리스트나 본문에 흡수했는가?

## 관련 문서

- `AGENTS.md`
- `management/guidelines/manuscript-writing-workflow.md`
- `management/guidelines/concept-glossary-guidelines.md`
- `management/guidelines/python-example-guidelines.md`
- `management/guidelines/chart-guidelines.md`
- `management/guidelines/english-translation-guidelines.md`
- `management/guidelines/chinese-translation-guidelines.md`
- `management/release-notes/sections/README.md`
