# Guideline Release Note

- Document ID: `GUIDE-concept-glossary-guidelines`
- Source File: `management/authoring/concept-glossary-guidelines.md`

### v2026.07.07-6

- 변경 이유: 개념사전의 `등장 Section`이 단순 보조 필드로만 읽히면, 실제 재등장 위치 누락이나 잘못된 Section ID 표기를 체계적으로 관측하기 어렵다는 기준을 규칙 문서에 더 분명히 적어 둘 필요가 생겼다.
- 문서 반영: 레포 전역 원칙과 개념사전 작성 규칙에 `등장 Section`을 `목록`으로 유지하고, 대표 설명 위치와 실제 재등장 위치를 구분하며, 위치 표기 오류와 누락을 관측하는 용도로도 사용한다는 문장을 추가했다. 또한 오표기나 누락을 발견하면 개념사전 항목과 관련 본문, 릴리즈노트를 함께 바로잡는 기준을 명시했다.
- 번역 동기화 메모: 향후 다국어 원고가 생기면 `appearance-section list`를 canonical trace field로 유지하고, missing or wrong Section IDs도 같은 `Section ID` 기준으로 함께 바로잡아야 한다.
- 번역 반영 상태: 번역본 없음
- 관련 자산: `AGENTS.md`, `docs/reference/concept-glossary.md`
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-5

- 변경 이유: 개념사전이 한국어 표면형만으로 읽히면 서로 다른 영어 개념이 섞일 수 있고, 본문 초반 신규 용어를 개념사전에 연결하는 방식도 항목별 직접 앵커와 1회 링크 기준까지 문서화할 필요가 생겼다.
- 문서 반영: 기본 원칙과 정렬 규칙에 `한국어+영어 병기`, `같은 한국어 표면형이라도 영어 개념이 다르면 표제어 분리`, `동음이의어·다의어 오류 관찰 기준`을 추가했다. 또한 본문 연결 규칙을 새로 두어, Part 초반 대표 Section에서는 신규 핵심 개념을 묶어 소개하고 개념사전의 개별 앵커로 연결하며, 같은 Section 안에서는 직접 링크를 1회만 두는 기준을 명시했다.
- 번역 동기화 메모: 향후 다국어 원고가 생기면 Korean surface form split, English-term disambiguation, early grouped glossary block, per-term anchor linking 원칙도 같은 `Section ID` 기준으로 유지해야 한다.
- 번역 반영 상태: 번역본 없음
- 관련 자산: `docs/reference/concept-glossary.md`, `docs/parts/part-01/chapter-01/section-01.md`, `AGENTS.md`
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-4

- 변경 이유: 대표 설명 위치 원칙은 있었지만, 실제 본문 작업에서는 같은 Part 안 후속 Section가 다시 사전식 표나 비교 표를 만들지 말고 개념사전 링크로 돌아가야 한다는 기준을 더 명확히 적어 둘 필요가 생겼다.
- 문서 반영: 같은 Part 안에서는 새로운 핵심 개념을 최초 1회만 충분히 설명하고, 이후 Section는 기본적으로 개념사전 링크로 연결하며, 새 Part에서 다시 핵심이 되면 그 Part 첫 등장 Section에서만 다시 정리할 수 있다는 규칙으로 정리했다.
- 번역 동기화 메모: 향후 다국어 원고가 생기면 same-part single detailed explanation, glossary-link follow-up, new-part reintroduction 원칙도 같은 `Section ID` 기준으로 유지해야 한다.
- 번역 반영 상태: 번역본 없음
- 관련 자산: `AGENTS.md`, `management/guidelines/writing/manuscript-writing-workflow.md`, `docs/reference/concept-glossary.md`
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-3

- 변경 이유: 개념사전 항목을 점검하니 `중심 Section`에 여러 Section를 쉼표로 나열한 항목이 많이 남아 있어, 대표 Section를 하나만 두려던 원칙과 실제 산출물이 어긋나고 있었다.
- 문서 반영: `중심 Section`은 대표 설명 위치 하나만 적고, 뒤 Part나 후속 Section의 재설명은 `등장 Section`으로만 추적한다는 규칙을 명시했다. 대표 Section를 하나로 잡기 어렵다면 표제어를 좁히거나 분리하는 판단 기준도 함께 추가했다.
- 번역 동기화 메모: 향후 다국어 개념사전이 생기면 `중심 Section` 단일값 원칙과 `등장 Section` 분리 원칙도 같은 `Section ID` 기준으로 유지해야 한다.
- 번역 반영 상태: 번역본 없음
- 관련 자산: `docs/reference/concept-glossary.md`
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-2

- 변경 이유: Part 5 후반 개념사전을 다시 정리하면서 `학습 모드`, `평가 모드`, `temperature`, `top-k`처럼 계산 상태나 출력 선택 기준을 설명하는 모드·설정값도 대표 설명 위치와 후속 재등장을 추적해야 할 필요가 분명해졌다.
- 문서 반영: 업데이트 원칙에 모드·설정값도 같은 Part 안에서 반복되면 개념사전 후보로 올린다는 기준을 추가했다.
- 번역 동기화 메모: 향후 다국어 원고가 생기면 mode, setting, decoding 관련 표제어도 같은 `Section ID` 기준으로 중심과 재등장 위치를 함께 유지해야 한다.
- 번역 반영 상태: 번역본 없음
- 관련 자산: `docs/reference/concept-glossary.md`, `docs/parts/part-05/chapter-06/section-02.md`, `docs/parts/part-05/chapter-15/section-02.md`
- 원문 기준 버전: `v2026.07.07`

### v2026.07.07-1

- 변경 이유: Part 7 본문을 순차 정리하면서 같은 Part 안에서 최초 1회만 길게 설명하고 이후 여러 Section에서 평가·운영 기록으로 다시 쓰이는 개념을 개념사전 후보로 올리는 기준을 규칙 문서에도 더 분명히 적어 둘 필요가 생겼다.
- 문서 반영: 업데이트 원칙에 Part 7형 개념 후보 기준을 추가하고, `기준선`, `회고`, `권한`, `어휘 밖(OOV)`, `토큰 커버리지` 같은 평가·운영 개념도 대표 설명 위치와 후속 재등장 기준으로 개념사전에 올릴 수 있다는 예시를 보강했다.
- 번역 동기화 메모: 향후 다국어 원고가 생기면 Part 7형 평가·운영 표제어의 후보 선정 기준과 대표 Section 연결 원칙도 같은 `Section ID` 기준으로 유지해야 한다.
- 번역 반영 상태: 번역본 없음
- 관련 자산: `docs/reference/concept-glossary.md`, `docs/parts/part-07/chapter-04/section-02.md`, `docs/parts/part-07/chapter-06/section-02.md`
- 원문 기준 버전: `v2026.07.07`

### v2026.07.06-5

- 변경 이유: 개념사전 규칙 문서에서 `중심 Section`이라는 필드명이 산출물 정의의 `대표 Section`과 같은 뜻이라는 점을 더 분명히 적어 둘 필요가 생겼다.
- 문서 반영: 대표 설명 위치 원칙과 Section 표기 규칙에 `중심 Section`이 곧 대표 Section를 적는 필드라는 설명을 추가했다.
- 번역 동기화 메모: 향후 다국어 원고가 생기면 `central section`과 `representative section` 대응을 같은 용어 규칙으로 유지해야 한다.
- 번역 반영 상태: 번역본 없음
- 관련 자산: `docs/reference/concept-glossary.md`
- 원문 기준 버전: `v2026.07.06`

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

### v2026.07.06-4

- 변경 이유: Part 3 리팩터링을 반영하면서 기존 기초 개념이 뒤 Part에서 문제 설계 층위로 다시 충분히 설명될 수 있다는 점과, `용어 | 아주 짧은 뜻 | 이 절에서의 역할` 형식의 용어 재소개 표가 한 Section 안에서 중복 복제되지 않도록 막는 기준을 규칙 문서에 명시할 필요가 생겼다.
- 문서 반영: 뒤 Part에서 같은 개념이 새로운 설계·운영 층위로 다시 충분히 설명되면 `중심 Section` 또는 `등장 Section`으로 확장 연결할 수 있다는 원칙을 추가했다. 또한 `용어 재소개 표`는 대표 정의를 복제하지 않으며, 한 Section 안에서 같은 형식을 여러 번 반복하지 않고 필요하면 기존 표를 확장하거나 일반 문단·예시 표로 풀도록 규칙을 보강했다.
- 번역 동기화 메모: 향후 다국어 원고가 생기면 확장된 `중심/등장 Section` 규칙과 용어 재소개 표의 단일 사용 원칙도 같은 `Section ID` 기준으로 함께 맞춰야 한다.
- 번역 반영 상태: 번역본 없음
- 관련 자산: `docs/reference/concept-glossary.md`, `management/authoring/concept-glossary-guidelines.md`
- 원문 기준 버전: `v2026.07.06`
