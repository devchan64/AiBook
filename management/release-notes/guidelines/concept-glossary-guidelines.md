# Guideline Release Note

- Document ID: `GUIDE-concept-glossary-guidelines`
- Source File: `management/authoring/concept-glossary-guidelines.md`

### v2026.07.06

- 변경 이유: 책 본문을 순차 보강하는 과정에서 개념을 빠르게 다시 찾고 중복 없이 정리할 수 있는 원고형 개념사전과 그 작성 규칙이 필요해졌다.
- 문서 반영: 개념사전 원고 위치, 가나다순 정렬, 항목 구조, Section ID 표기, 중복 방지, 본문과의 관계, 업데이트 원칙을 담은 `concept-glossary-guidelines.md`를 새로 만들었다.
- 번역 동기화 메모: 향후 다국어 원고가 생기면 개념사전 표제어 기준, 원어 병기, Section ID 연결 규칙을 언어별 원고에도 대응시켜야 한다.
- 번역 반영 상태: 번역본 없음
- 관련 자산: `docs/reference/concept-glossary.md`
- 원문 기준 버전: `v2026.07.06`
- 추가 정리: 같은 Part 안에서 주요 개념의 상세 설명은 가능한 한 한 Section에만 두고, 개념사전은 그 대표 설명 위치를 다시 찾게 하는 색인 역할을 맡는 원칙을 함께 명시했다.

### v2026.07.06-2

- 변경 이유: Part 2 본문을 순차 개정하면서 실제로 사용한 `대표 설명 위치`, `후속 Section 최소 연결`, `용어 재소개 표` 원칙을 규칙 문서에도 더 명확히 맞출 필요가 생겼다.
- 문서 반영: 같은 Part 안에서 주요 개념의 상세 설명은 가능한 한 최초 1회만 본문에 충분히 두고, 이후 Section는 대표 설명 위치 문단과 최소 연결만 남기며, 개념사전의 `중심 Section`이 그 위치를 가리키도록 규칙을 보강했다.
- 번역 동기화 메모: 향후 다국어 원고가 생기면 대표 설명 위치 문단, 용어 재소개 표, `중심 Section` 연결 규칙을 같은 `Section ID` 기준으로 함께 맞춰야 한다.
- 번역 반영 상태: 번역본 없음
- 관련 자산: `docs/reference/concept-glossary.md`, `management/authoring/2026-07-06-part-concept-detail-dedup-report.md`
- 원문 기준 버전: `v2026.07.06`

### v2026.07.06-3

- 변경 이유: 개념사전이 대표 설명 위치만 가리키면 실제로 어느 Section에서 다시 등장하는지 추적하기 어려워, `중심 Section`과 별도로 `등장 Section` 필드를 도입할 필요가 생겼다.
- 문서 반영: 개념사전 항목 구조에 `등장 Section`을 추가하고, `중심 Section`은 대표 설명 위치, `등장 Section`은 후속 재등장 위치를 추적하는 보조 필드라는 규칙을 명시했다. 이미 순차 보강이 끝난 항목도 이후 수정 시 함께 채운다는 업데이트 기준을 추가했다.
- 번역 동기화 메모: 향후 다국어 원고가 생기면 `중심 Section`과 `등장 Section`의 역할 구분과 `Section ID` 표기 방식을 같은 기준으로 맞춰야 한다.
- 번역 반영 상태: 번역본 없음
- 관련 자산: `docs/reference/concept-glossary.md`
- 원문 기준 버전: `v2026.07.06`
