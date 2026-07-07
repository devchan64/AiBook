# 2026-07-08 Part 3 AGENTS Principles Review Report

검토 범위: `docs/parts/part-03/`

검토 기준:

- `AGENTS.md`의 작성 원칙
- `AGENTS.md`의 Section 경계 원칙
- 릴리즈노트 이슈는 이번 리포트에서 제외

## Findings

### [P1] `짧은 점검`, `언제 이 관점을 먼저 떠올려야 하는가`, `이 절은 … 문제로 다시 볼 수 있습니다`가 Part 3 전반에 반복되어 설명보다 메타 템플릿이 먼저 보인다

- AGENTS는 집필 진행 멘트와 메타 표지를 반복하기보다 문제 상황과 핵심 개념으로 바로 들어가라고 요구한다.
- 그런데 Part 3 본문은 다수 Section이 거의 같은 말미 구조를 공유하고, 본문 중간에도 `이 절은 … 문제로 다시 볼 수 있습니다`, `이 절에서 붙잡아야 할 문장은 다음과 같습니다` 같은 편집자형 문장을 반복한다.
- 대표 위치:
  - [docs/parts/part-03/chapter-01/section-01.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-01/section-01.md:88)
  - [docs/parts/part-03/chapter-05/section-04.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-05/section-04.md:103)
  - [docs/parts/part-03/chapter-08/section-03.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-08/section-03.md:85)
  - [docs/parts/part-03/chapter-09/section-04.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-09/section-04.md:128)
- `rg` 기준으로 `## 짧은 점검`과 `## 언제 이 관점을 먼저 떠올려야 하는가`가 Chapter 1~9 전반에 반복되고 있다.
- 이 패턴은 독자가 개념을 따라가기보다 `교안 단계`를 먼저 인식하게 만들어, AGENTS가 요구하는 직접 설명 원칙과 충돌한다.
- 수정 방향:
  - 공통 말미 템플릿을 기본 구조에서 빼고, 정말 필요한 대표 Section에만 제한한다.
  - `이 절은 … 문제로 다시 볼 수 있습니다`와 `이 절에서 붙잡아야 할 문장`은 실제 설명 문단으로 흡수한다.
  - 회고 질문은 일반 본문 안의 자연스러운 확인 문장으로 줄인다.

### [P1] `P3-7.3`이 Part 3의 기준선 설명을 넘어 Part 4의 `기준 모델` 개념을 독립적으로 설명해 Section 경계를 넘는다

- AGENTS는 현재 Section의 범위 안에서만 논의를 확장하고, 다른 Section이나 뒤 Part의 핵심 설명을 미리 작성하지 말라고 요구한다.
- 그런데 [P3-7.3](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-07/section-03.md:1)은 제목부터 `기준 모델`을 전면에 세우고, 비교 표와 근거 표, 외부 용어집 출처까지 동원해 Part 4 개념을 별도 주제로 설명한다.
- 특히 아래 구간은 `기준선`의 경계 표시를 넘어, `Part 4의 기준 모델이 무엇인가`를 독립적으로 정리하는 흐름이다.
  - 도입 정의: [section-03.md:6](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-07/section-03.md:6)
  - Part 4 개념 설명과 근거 연결: [section-03.md:31](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-07/section-03.md:31)
  - 상위 프레임 비교표: [section-03.md:57](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-07/section-03.md:57)
  - 근거 표와 출처: [section-03.md:82](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-07/section-03.md:82)
- 이 구성은 Part 3의 비교 구조 설명보다 `baseline이라는 단어의 두 뜻`을 정리하는 별도 미니 에세이에 가까워, Section 경계와 Part 경계를 함께 흐린다.
- 수정 방향:
  - 이 Section은 `기준선`이 무엇과 비교하는 기준인지에만 집중하고, `기준 모델`은 한두 문장 수준의 경계 표시만 남긴다.
  - Part 4의 benchmark/baseline model 설명과 외부 근거는 Part 4 대표 Section으로 이동한다.
  - 가능하면 제목도 Part 3 질문 안으로 다시 접는다.

### [P2] Part 마무리 페이지가 summary보다 설계 체크리스트와 뒤 Part 인계 메모를 과도하게 재전개해 요약 역할을 벗어난다

- AGENTS는 Part 마무리 페이지를 요약 역할로 두고, 같은 Part 안에서 상세 정의와 체크리스트 반복을 줄이라고 요구한다.
- 그러나 [docs/parts/part-03/summary.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/summary.md:10)는 요약을 넘어서 장문의 개념 목록, 오해 목록, 다음 Part 전 질문 목록, 상세 handoff 설명을 다시 크게 펼친다.
- 특히 아래 구간은 `마무리 요약`보다 `설계 점검 문서`에 더 가깝다.
  - `반드시 기억할 개념`: [summary.md:40](/Users/simchangbo/ws/AiBook/docs/parts/part-03/summary.md:40)
  - `오해하기 쉬운 지점`: [summary.md:89](/Users/simchangbo/ws/AiBook/docs/parts/part-03/summary.md:89)
  - `다음 Part로 넘어가기 전 질문`: [summary.md:127](/Users/simchangbo/ws/AiBook/docs/parts/part-03/summary.md:127)
  - Part 4·5 인계 재설명: [summary.md:166](/Users/simchangbo/ws/AiBook/docs/parts/part-03/summary.md:166)
- 이 구성은 summary를 다시 한 번 긴 운영 가이드처럼 읽히게 만들고, 본문에서 이미 다룬 질문을 중복 반복한다.
- 수정 방향:
  - summary는 `Part 3 spine`, `핵심 산출물`, `뒤 Part로 넘기는 최소 전제` 정도로 압축한다.
  - 장문 개념 목록과 질문 목록은 대표 항목만 남기고 나머지는 개념사전이나 중심 Section으로 회수한다.
  - Part 4·5 연결은 상세 인계 규칙이 아니라 한 문단 수준의 handoff 요약으로 줄인다.

## Residual Risks

- 이번 검토는 AGENTS 원칙 위반 여부에 집중했으며, 사실 근거의 충분성이나 외부 출처의 적합성 자체는 별도로 재검토하지 않았다.
- Part 3는 최근 재구성 직후라, 메타 템플릿을 줄이는 과정에서 일부 Section의 연결 문장을 함께 다시 다듬어야 할 가능성이 높다.
