# 가이드라인 인덱스

이 디렉터리는 `AGENTS.md`의 전역 원칙을 실제 작업으로 옮길 때 다시 여는 작업별 가이드라인을 모아 둔다.

저장소 전체 운영 원칙은 `../../AGENTS.md`에 남기고, 이 문서는 어떤 기준 문서를 먼저 열어야 하는지 빠르게 찾는 통합 인덱스로 사용한다. 세부 절차, 예외 규칙, 반복 체크 항목은 개별 가이드라인 문서에서 관리한다.

## 문서 경계

- `../../AGENTS.md`는 저장소의 핵심 원칙, 문서 위치, 브랜치와 배포 기준, 작업 전 확인할 가이드라인 인덱스를 맡는다.
- `../README.md`는 `authoring/`, `guidelines/`, `release-notes/`의 역할 분담을 빠르게 찾는 관리 문서 인덱스를 맡는다.
- `management/guidelines/README.md`는 이 폴더에 둘 문서와 두지 않을 문서의 경계, 작업 유형별 참조 순서를 맡는다.
- 개별 가이드라인 문서는 특정 워크플로우를 실제로 수행할 때 필요한 세부 절차, 예외, 검증 기준을 맡는다.
- `../release-notes/sections/README.md`는 Section 단위 릴리즈노트 파일 위치, 파일명, 항목 형식을 맡는다.
- `../authoring/`은 저자 관점 메모, Part 체크포인트, Section별 근거 분석처럼 특정 집필 판단을 돕는 보조 자료를 맡는다.
- 원칙 문서와 가이드라인 문서는 별도 리비전노트를 두지 않고 문서 자체를 직접 갱신한다.

## 포함 기준

다음 성격의 문서는 이 폴더에 둔다.

- 원고 작성, 수정, 번역, 도식화처럼 반복되는 작업의 실행 기준
- 차트, 그래프, 도식 작성 기준
- Python 예제 작성 기준
- 개념사전 작성과 표제 관리 기준
- Section 메타데이터 관리 기준
- 특정 작업 흐름별 세부 워크플로우 규칙

다음 성격의 문서는 이 폴더에 두지 않는다.

- 저장소 전체 운영 규칙
- Part별 작업 큐 문서
- 커리큘럼 조사 문서
- 개별 챕터 분석 메모
- 근거 검토 메모
- 일회성 감사 기록

## 기준 문서 맵

| 문서 | 역할 | 먼저 볼 때 |
| --- | --- | --- |
| `../../AGENTS.md` | 저장소 핵심 원칙과 전역 작업 기준 | 모든 작업 시작 전 |
| `manuscript-writing-workflow.md` | 원고 작성 세부 절차 | Part/Section 초안 작성, 초심자 보강, 사례 작성 전 |
| `concept-glossary-guidelines.md` | 개념사전 작성 기준 | 개념사전 항목 추가·수정, 중심 Section과 등장 Section 정리 전 |
| `section-metadata-guidelines.md` | Section 메타데이터 관리 기준 | Section ID, 제목 앞 인덱스, Version, 릴리즈노트 연결 확인 전 |
| `python-example-guidelines.md` | Python 예제 작성 기준 | Python 예제 추가·수정, 코드 블록 유지 여부 판단 전 |
| `chart-guidelines.md` | 차트·도식 작성과 검증 기준 | Mermaid, SVG, 차트 추가·수정 전 |
| `english-translation-guidelines.md` | 영어 번역 운영 기준 | 영어판 Section 작성, 다국어 링크 정리, 공통 릴리즈노트 반영 전 |
| `chinese-translation-guidelines.md` | 중국어 간체 번역 운영 기준 | 중국어 간체판 Section 작성, 다국어 링크 정리, 공통 릴리즈노트 반영 전 |
| `../release-notes/sections/README.md` | 릴리즈노트 파일 관리 기준 | 릴리즈노트 파일 위치와 항목 형식 확인 전 |
| `../authoring/part-XX-open-checklist.md` | Part별 중심선 체크포인트 노트 | 목차 기준 중심 주제 정리, Part 흐름 점검 전 |

## 작업 유형별 참조 순서

### Section 본문을 새로 쓰거나 크게 고칠 때

1. `../../AGENTS.md`로 전역 원칙과 적용 범위를 확인한다.
2. `section-metadata-guidelines.md`로 `Section ID`, 제목 앞 인덱스, `Version`, 대응 릴리즈노트 파일을 먼저 확인한다.
3. 실제 작업 순서는 `manuscript-writing-workflow.md`의 `원고 작성·수정 작업 순서`를 따른다.
4. 릴리즈노트 파일 위치와 항목 형식은 `../release-notes/sections/README.md`를 따른다.

### Python 예제를 넣거나 고칠 때

1. `python-example-guidelines.md`
2. 필요하면 `manuscript-writing-workflow.md`의 예제 연결 규칙
3. 현재 Section의 중심 질문과 출력값 점검

### 차트, Mermaid, SVG를 만들 때

1. `chart-guidelines.md`
2. 필요하면 `manuscript-writing-workflow.md`의 시각 형식 연결 규칙
3. 다국어 본문이면 Mermaid include 경로와 일반 SVG/파일 링크 경로를 구분해 다시 본다.

### 관점 문장, 머리말, 도입 문장을 다듬을 때

1. `../../AGENTS.md`의 기본 관점과 집필 태도
2. `../authoring/author-notes.md`
3. 사실 주장이 섞이면 별도 근거 확인

### 개념사전 표제와 본문 링크를 정리할 때

1. `concept-glossary-guidelines.md`의 등재·제외 기준과 표제 정리 절차를 먼저 확인한다.
2. 단어별 원고, 언어별 공개 색인, 통합 인덱스가 같은 slug와 의미 범위를 가리키는지 확인한다.
3. 완료된 실행 기록을 새 기준처럼 재사용하지 않고, 반복 운영 기준은 가이드라인에 남긴다.

## 노트 정리 원칙

- `section-...-evidence-analysis.md`에는 근거와 용어 판단, 현재 본문에서 아직 중요한 경계만 남긴다.
- 이미 본문에 반영된 집필 메모나 끝난 작업 목록은 Section 메모에 계속 누적하지 않는다.
- Part 수준 메모는 가능한 한 `part-XX-open-checklist.md`에서 목차 기준 중심 주제만 유지하고, 순차 점검 기록은 별도 운영 문서로 누적하지 않는다.
- 오픈체크리스트는 작업 상태표가 아니라 Part 원고가 유지해야 할 중심선 문서로 관리한다.
- 오래된 개편 전 Section ID는 현재 목차 기준 체크포인트 안에 직접 남기지 않는다. 필요한 경우 현재 체크포인트가 아니라 아카이브 회수 메모나 별도 리포트에서만 언급한다.
- 책 전체 중심 직관은 별도 장문 보관 메모에 계속 의존하지 않고, 원고 점검 기준으로 쓸 내용만 해당 `part-XX-open-checklist.md`의 짧은 중심축 문장으로 흡수한다.
- `review`, `plan`, `curriculum-review` 문서의 남은 항목을 정리할 때도 Part 체크포인트 노트에는 작업 로그 대신 중심 주제와 구조 판단만 남긴다.
- evidence 메모를 폐기할 때는 대응 원고 본문과 참고문헌 반영을 먼저 대조하고, 구조가 어긋나는 메모는 자동 폐기하지 않는다.

## 빠른 점검표

1. 이 작업의 기준 원문이 `AGENTS.md`인지, 작업형 가이드인지 먼저 구분했는가?
2. Section 본문 수정이라면 `manuscript-writing-workflow.md`와 `section-metadata-guidelines.md`를 함께 열었는가?
3. 개념 위치, 대표 설명 위치, 개념사전 링크 판단이라면 `concept-glossary-guidelines.md`를 다시 확인했는가?
4. 표제어·영어 기준 용어·번역어 대응만 빠르게 확인하면 되는 작업이라면 언어별 공개 개념사전과 단어별 원고를 먼저 확인했는가?
5. 표제 정리 작업에서 일회성 실행 기록의 후보 목록을 새 기준처럼 쓰지 않고, 가이드라인의 역할 분류와 등재·제외 기준으로 재판정했는가?
6. 예제, 차트, 번역처럼 전용 가이드가 있는 작업을 요약 문서만 보고 처리하고 있지는 않은가?
7. 끝난 판단을 메모 문서에 계속 누적하지 않고 체크리스트나 본문에 흡수했는가?

## 문서 목록

- `chart-guidelines.md`
- `chinese-translation-guidelines.md`
- `concept-glossary-guidelines.md`
- `english-translation-guidelines.md`
- `manuscript-writing-workflow.md`
- `python-example-guidelines.md`
- `section-metadata-guidelines.md`
- `../release-notes/sections/README.md`
- `../../AGENTS.md`
