# 2026-07-08 Part 3 AGENTS · 개념사전 가이드 점검 리포트

## 범위

- 기준 문서: `AGENTS.md`, `management/guidelines/concept-glossary-guidelines.md`
- 점검 대상: `docs/parts/part-03/`, `docs/reference/concept-glossary.md`
- 제외: 릴리즈노트 이슈

## Findings

### [P1] `P3-9.4` 도입부가 개념 설명보다 `이 절에서는` 메타 설명과 같은 표제어의 반복 직접 링크를 먼저 세운다

- 파일: [docs/parts/part-03/chapter-09/section-04.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-09/section-04.md:6)
- 근거:
  - 6행은 `[검토 후보 큐]`, `[비교 리포트]`, `[목표 라벨 후보]`를 한 문장에 모두 직접 링크하고, 바로 이어 `그래서 이 절에서는 ... 정리합니다`로 현재 절의 편집 의도를 먼저 설명합니다.
  - 8행은 같은 Section 도입부에서 `목표 라벨 후보(target candidate)`를 다시 직접 링크하며, 6행의 핵심 정의를 거의 한 번 더 반복합니다.
- 왜 문제인가:
  - AGENTS는 도입에서 `이 절에서는` 같은 집필 진행 멘트보다 문제 상황과 개념 설명을 우선하라고 요구합니다.
  - 개념사전 가이드는 같은 용어의 직접 링크를 한 Section 안에서 기본적으로 1회만 두고, 후속 문장에서는 반복 링크보다 일반 텍스트 연결을 우선하라고 요구합니다.

### [P2] `P3-4.2` 말미가 현재 개념 정리보다 `...문제로 다시 볼 수 있습니다` 템플릿으로 닫혀 본문을 다시 메타화한다

- 파일: [docs/parts/part-03/chapter-04/section-02.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-04/section-02.md:169)
- 근거:
  - 169행의 `이 절은 샘플 정의의 후속 주의사항이 아니라, ... 문제로 다시 볼 수 있습니다.`는 현재 절에서 이미 설명한 `단위 정합성`을 다시 편집자형 재프레이밍 문장으로 감쌉니다.
  - 바로 뒤 172행은 이미 같은 내용을 직접 진술형으로 마무리하고 있어, 169행 문장이 개념 진전을 추가하지 않습니다.
- 왜 문제인가:
  - AGENTS는 질문과 핵심 정의를 인용문이나 메타 문장으로 따로 세우기보다 일반 본문 안에서 자연스럽게 이어 쓰라고 요구합니다.
  - 이 문장은 새 이해를 더하기보다 `이 절을 어떻게 분류할 것인가`를 앞세워, 현재 절의 직접 설명을 한 번 더 끊습니다.

### [P2] Part 시작 페이지의 범위 설명이 여전히 `뒤 Part` 예고를 직접 호출해 오버뷰보다 인계 메모처럼 읽히는 구간이 남아 있다

- 파일: [docs/parts/part-03/index.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/index.md:96)
- 근거:
  - 96행은 `특정 머신러닝 알고리즘의 학습 방식 ... 복잡한 시계열 딥러닝 구조는 뒤 Part에서 다시 다룹니다.`라고 직접 예고합니다.
  - 98행도 `이 생략은 회피가 아니라 역할 분리`라고 덧붙여, 오버뷰 자체보다 배치 해설의 비중을 키웁니다.
- 왜 문제인가:
  - AGENTS는 Part 시작 페이지가 설계 메모보다 오버뷰 역할을 해야 한다고 요구합니다.
  - 현재 문장은 `Part 3에서 무엇을 배우는가`보다 `무엇을 아직 안 다루는가`와 뒤 Part 배치를 먼저 의식하게 만듭니다.

### [P2] 개념사전의 `비교 리포트(comparison report)` 항목이 Part 3 실제 재등장 범위를 아직 충분히 따라가지 못한다

- 파일: [docs/reference/concept-glossary.md](/Users/simchangbo/ws/AiBook/docs/reference/concept-glossary.md:773)
- 근거:
  - 본문 [docs/parts/part-03/chapter-09/section-04.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-09/section-04.md:6)에서는 `비교 리포트(comparison report)`를 `검토 후보 큐`, `목표 라벨 후보`와 함께 운영 메모가 구조화되는 출발 산출물로 직접 다시 호출합니다.
  - 그러나 `비교 리포트(comparison report)` 항목의 `등장 Section` 목록에는 이 재등장 위치가 반영되지 않은 상태입니다.
- 왜 문제인가:
  - 개념사전 가이드는 `등장 Section`을 실제 재등장 위치를 누적 추적하는 목록으로 유지하라고 요구합니다.
  - 대표 산출물 spine 중 하나인 `비교 리포트`의 재등장 위치가 빠지면, 독자가 어디서 다시 이 개념이 구조적으로 쓰이는지 추적하기 어려워집니다.
