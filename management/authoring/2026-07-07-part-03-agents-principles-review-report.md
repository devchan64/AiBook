# 2026-07-07 Part 3 AGENTS Principles Review Report

검토 범위: `docs/parts/part-03/`

검토 기준:

- `AGENTS.md`의 작성 원칙
- `AGENTS.md`의 Section 경계 원칙
- 릴리즈노트 정합성 이슈는 이번 리포트에서 제외

## Findings

### [P1] `짧은 점검`과 `언제 이 관점을 먼저 떠올려야 하는가` 템플릿이 Part 3 전반에 반복되어, 설명보다 교안형 메타 구조가 먼저 드러난다

- AGENTS는 집필 진행 멘트와 메타 표지를 반복하기보다 문제 상황과 핵심 개념으로 바로 들어가라고 요구한다.
- 그런데 Part 3 본문은 매우 많은 Section이 동일한 말미 템플릿을 공유해, 설명 자체보다 `학습지형 형식`이 먼저 보인다.
- 대표 위치:
  - [docs/parts/part-03/chapter-01/section-01.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-01/section-01.md:86)
  - [docs/parts/part-03/chapter-05/section-04.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-05/section-04.md:109)
  - [docs/parts/part-03/chapter-07/section-03.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-07/section-03.md:53)
  - [docs/parts/part-03/chapter-09/section-04.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-09/section-04.md:136)
- 같은 패턴은 Chapter 1~9 전반에 걸쳐 반복되며, `rg` 기준으로 `## 짧은 점검`과 `## 언제 이 관점을 먼저 떠올려야 하는가`가 수십 곳에 남아 있다.
- 수정 방향:
  - 말미 템플릿을 기본 구조에서 빼고, 정말 필요한 일부 대표 Section에만 제한한다.
  - 점검 질문은 본문 문단 안의 자연스러운 회고 질문으로 흡수한다.
  - `언제 이 관점을 먼저 떠올려야 하는가`는 개념 재등장 위치가 실제로 혼동을 부르는 곳에만 남긴다.

### [P1] `P3-7.3`이 Part 4의 `기준 모델` 개념을 독립 주제로 세워, Part 3 Section 경계를 넘는다

- AGENTS는 현재 Section 범위 안에서만 논의를 확장하고, 다른 Part의 핵심 설명을 미리 작성하지 말라고 요구한다.
- 그런데 [P3-7.3](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-07/section-03.md:1)은 제목부터 `기준 모델`을 전면에 세우고, 표 두 개와 비교 서술을 통해 Part 4의 기준 모델 개념을 별도 소주제로 설명한다.
- 특히 아래 구간은 `Part 3의 기준선`을 설명하는 보조 언급을 넘어, `Part 4의 기준 모델이 무엇인가`를 독립적으로 정리하는 쪽으로 기울어 있다.
  - [docs/parts/part-03/chapter-07/section-03.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-07/section-03.md:6)
  - [docs/parts/part-03/chapter-07/section-03.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-07/section-03.md:23)
  - [docs/parts/part-03/chapter-07/section-03.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-07/section-03.md:31)
- 이 구조는 `기준선` Section 안에서 필요한 최소 경계 표시를 넘어서, 뒤 Part 핵심 개념을 Part 3에서 먼저 배우는 인상을 만든다.
- 수정 방향:
  - 이 Section을 `기준선`의 내부 경계 경고 한두 문단 수준으로 축소한다.
  - `기준 모델`의 정의와 쓰임은 Part 4 대표 Section에서만 중심 설명으로 남긴다.
  - 가능하면 제목도 `기준선은 무엇과 비교하는 기준인가`처럼 Part 3 질문 안으로 다시 접는다.

### [P2] Part 마무리 페이지가 요약보다 확장 체크리스트와 뒤 Part 인계 메모를 과도하게 펼쳐, summary 역할을 벗어난다

- AGENTS는 Part 마무리 페이지를 요약 역할로 두고, 같은 Part 안에서도 상세 정의와 체크리스트 반복을 줄이라고 요구한다.
- 그러나 [docs/parts/part-03/summary.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/summary.md:10)는 요약을 넘어서 장문의 개념 목록, 오해 목록, 다음 Part 전 질문 목록, 뒤 Part 설명을 대량으로 다시 펼친다.
- 특히 아래 구간은 `마무리 요약`보다 `설계 점검 문서`에 더 가깝다.
  - `반드시 기억할 개념`의 장문 목록: [summary.md:40](/Users/simchangbo/ws/AiBook/docs/parts/part-03/summary.md:40)
  - `오해하기 쉬운 지점`의 대량 나열: [summary.md:89](/Users/simchangbo/ws/AiBook/docs/parts/part-03/summary.md:89)
  - `다음 Part로 넘어가기 전 질문`의 장문 체크리스트: [summary.md:127](/Users/simchangbo/ws/AiBook/docs/parts/part-03/summary.md:127)
  - `Part 4`, `Part 5` 인계 설명의 재확장: [summary.md:166](/Users/simchangbo/ws/AiBook/docs/parts/part-03/summary.md:166)
- 이 구성은 요약 페이지를 다시 한 번 긴 운영 가이드처럼 읽히게 만들고, 본문에서 이미 다룬 질문을 중복 반복한다.
- 수정 방향:
  - summary는 `Part 3의 spine`, `남겨야 할 핵심 결과 구조`, `뒤 Part로 넘기는 최소 전제` 정도로 압축한다.
  - 장문의 개념 목록과 질문 목록은 대표 5~8개 수준으로 줄이거나 개념사전/대표 Section 링크로 회수한다.
  - Part 4·5 연결은 상세 인계 규칙이 아니라 한 문단 수준의 handoff 요약으로 축소한다.

## Residual Risks

- 이번 검토는 AGENTS 원칙 위반 여부에 집중했으며, 사실 근거의 충분성이나 외부 출처 품질은 별도로 재검토하지 않았다.
- Part 3는 최근 대규모 재구성 직후라, 현재 남아 있는 메타 템플릿을 줄이는 과정에서 다른 Section 간 연결 문장이 함께 흔들릴 가능성이 있다.
