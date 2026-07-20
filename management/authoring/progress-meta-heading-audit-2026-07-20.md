# 진행 메타 제목 전수검사 리포트

작성일: 2026-07-20

## 검사 목적

`이 절의 범위`, `이 절의 목표`, `이 절을 읽는 순서`처럼 진행 방식을 제목으로 세우는 원고 구조가 본문에 얼마나 남아 있는지 확인한다.

검사 기준은 `management/guidelines/manuscript-writing-workflow.md`의 다음 원칙이다.

- 이전 Section과의 연결, 현재 Section의 경계, 다루지 않는 내용은 독립 소제목이나 진행 메타 블록으로 만들지 않는다.
- `이 절의 범위`, `이 절의 목표`, `이 절을 읽는 순서`, `이 보충학습의 범위`, `이 보충학습의 목표`처럼 진행 방식을 제목으로 세우지 않는다.
- 소제목은 독자가 지금 읽을 구체 개념, 오해, 비교 대상, 판단 기준을 바로 보게 해야 한다.

## 검사 범위

- 1차 검사 대상: `docs/parts/` 아래 공개 본문 Markdown
- 보조 검사 대상: `docs/table-of-contents.md`의 `읽는 순서` 표현
- 제외 대상: `AGENTS.md`, `management/guidelines/`의 규칙 설명 문장

## 검사 명령

1차 제목 위반 검색:

```sh
rg -n "^#{2,6} (이 절의 범위|이 절의 목표|이 절을 읽는 순서|이 보충학습의 범위|이 보충학습의 목표|이 보충학습을 읽는 순서|읽는 순서|먼저 읽는 순서|이 마무리를 읽는 순서)$" docs/parts
```

보조 표현 검색:

```sh
rg -n "읽는 순서|이 절의 목표" docs/parts docs/table-of-contents.md
```

## 전체 결과

1차 제목 위반은 총 339건이다.

| 제목 유형 | 건수 | 판단 |
| --- | ---: | --- |
| `이 절의 목표` | 201 | 직접 정비 대상 |
| `이 절의 범위` | 98 | 직접 정비 대상 |
| `이 보충학습의 목표` | 21 | 직접 정비 대상 |
| `이 보충학습의 범위` | 10 | 직접 정비 대상 |
| `이 절을 읽는 순서` | 5 | 우선 정비 대상 |
| `읽는 순서` | 1 | Part 시작 페이지 정비 대상 |
| `이 보충학습을 읽는 순서` | 1 | 우선 정비 대상 |
| `이 마무리를 읽는 순서` | 1 | Part 마무리 페이지 정비 대상 |
| `먼저 읽는 순서` | 1 | 우선 정비 대상 |

Part별 1차 제목 위반은 다음과 같다.

| Part | 건수 | 특징 |
| --- | ---: | --- |
| Part 1 | 62 | 초반 Section에 `이 절의 목표`가 넓게 남아 있고, 일부 Section에는 `이 절의 범위`도 함께 남아 있다. |
| Part 2 | 63 | `이 절의 목표` 중심으로 남아 있고, 보충학습 절의 목표 제목도 반복된다. |
| Part 3 | 1 | Part 시작 페이지의 `읽는 순서` 1건만 확인된다. |
| Part 4 | 121 | `이 절의 범위`와 `이 절의 목표`가 거의 쌍으로 남아 있고, 보충학습 범위/목표 제목도 많다. |
| Part 5 | 92 | `이 절의 범위`와 `이 절의 목표`가 쌍으로 남아 있으며, 일부 Section은 `읽는 순서`까지 3단 진행 메타 구조를 가진다. |
| Part 6 | 0 | 1차 제목 위반은 없다. 문장 안의 `읽는 순서` 표현은 보조 점검 대상이다. |
| Part 7 | 0 | 1차 제목 위반은 없다. |

## 확장 점검 결과

Section 본문 금지 문구와 별도로, Part 시작/마무리 페이지에도 진행 메타 성격의 제목이 18건 있다. Part 오버뷰는 Section 본문과 역할이 다르므로 즉시 위반으로 단정하지 않고, Part 시작/마무리 작성 기준과 함께 별도 판단한다.

확장 점검 명령:

```sh
rg -n "^#{2,6} (이 파트의 목표|이 파트에서 설명하는 범위와 설명하지 않을 범위|범위와 비범위|Part [0-9]+의 목적과 범위)$" docs/parts
```

| 파일 | 위치 | 현재 제목 |
| --- | ---: | --- |
| `docs/parts/part-01/index.md` | 40 | `이 파트의 목표` |
| `docs/parts/part-01/index.md` | 52 | `이 파트에서 설명하는 범위와 설명하지 않을 범위` |
| `docs/parts/part-01/summary.md` | 26 | `이 파트의 목표` |
| `docs/parts/part-01/summary.md` | 97 | `이 파트에서 설명하는 범위와 설명하지 않을 범위` |
| `docs/parts/part-02/index.md` | 74 | `이 파트의 목표` |
| `docs/parts/part-02/index.md` | 92 | `이 파트에서 설명하는 범위와 설명하지 않을 범위` |
| `docs/parts/part-02/summary.md` | 82 | `이 파트의 목표` |
| `docs/parts/part-02/summary.md` | 144 | `이 파트에서 설명하는 범위와 설명하지 않을 범위` |
| `docs/parts/part-03/index.md` | 78 | `범위와 비범위` |
| `docs/parts/part-04/index.md` | 45 | `이 파트의 목표` |
| `docs/parts/part-04/index.md` | 59 | `이 파트에서 설명하는 범위와 설명하지 않을 범위` |
| `docs/parts/part-04/summary.md` | 18 | `이 파트의 목표` |
| `docs/parts/part-04/summary.md` | 97 | `이 파트에서 설명하는 범위와 설명하지 않을 범위` |
| `docs/parts/part-05/index.md` | 108 | `이 파트에서 설명하는 범위와 설명하지 않을 범위` |
| `docs/parts/part-05/index.md` | 120 | `이 파트의 목표` |
| `docs/parts/part-06/index.md` | 98 | `Part 6의 목적과 범위` |
| `docs/parts/part-07/index.md` | 138 | `이 파트에서 설명하는 범위와 설명하지 않을 범위` |
| `docs/parts/part-07/summary.md` | 107 | `이 파트에서 설명하는 범위와 설명하지 않을 범위` |

## Part별 상세 집계

| Part | 제목 유형 | 건수 |
| --- | --- | ---: |
| Part 1 | `이 절의 범위` | 5 |
| Part 1 | `이 절의 목표` | 56 |
| Part 1 | `이 보충학습의 목표` | 1 |
| Part 2 | `이 절의 목표` | 53 |
| Part 2 | `이 보충학습의 목표` | 10 |
| Part 3 | `읽는 순서` | 1 |
| Part 4 | `이 절의 범위` | 51 |
| Part 4 | `이 절의 목표` | 51 |
| Part 4 | `이 절을 읽는 순서` | 2 |
| Part 4 | `이 보충학습의 범위` | 8 |
| Part 4 | `이 보충학습의 목표` | 8 |
| Part 4 | `먼저 읽는 순서` | 1 |
| Part 5 | `이 절의 범위` | 42 |
| Part 5 | `이 절의 목표` | 41 |
| Part 5 | `이 절을 읽는 순서` | 3 |
| Part 5 | `이 보충학습의 범위` | 2 |
| Part 5 | `이 보충학습의 목표` | 2 |
| Part 5 | `이 보충학습을 읽는 순서` | 1 |
| Part 5 | `이 마무리를 읽는 순서` | 1 |

## Chapter별 분포

Part 1:

| Chapter | 건수 |
| --- | ---: |
| chapter-01 | 6 |
| chapter-02 | 5 |
| chapter-03 | 3 |
| chapter-04 | 4 |
| chapter-05 | 3 |
| chapter-06 | 3 |
| chapter-07 | 4 |
| chapter-08 | 3 |
| chapter-09 | 3 |
| chapter-10 | 3 |
| chapter-11 | 3 |
| chapter-12 | 3 |
| chapter-13 | 4 |
| chapter-14 | 6 |
| chapter-15 | 3 |
| chapter-16 | 3 |
| chapter-17 | 3 |

Part 2:

| Chapter | 건수 |
| --- | ---: |
| chapter-01 | 2 |
| chapter-02 | 4 |
| chapter-03 | 6 |
| chapter-04 | 6 |
| chapter-05 | 5 |
| chapter-06 | 3 |
| chapter-07 | 9 |
| chapter-08 | 7 |
| chapter-09 | 4 |
| chapter-10 | 3 |
| chapter-11 | 4 |
| chapter-12 | 3 |
| chapter-13 | 3 |
| chapter-14 | 2 |
| chapter-15 | 2 |

Part 4:

| Chapter | 건수 |
| --- | ---: |
| chapter-01 | 4 |
| chapter-02 | 6 |
| chapter-03 | 4 |
| chapter-04 | 4 |
| chapter-05 | 4 |
| chapter-06 | 8 |
| chapter-07 | 8 |
| chapter-08 | 6 |
| chapter-09 | 6 |
| chapter-10 | 6 |
| chapter-11 | 10 |
| chapter-12 | 6 |
| chapter-13 | 5 |
| chapter-14 | 4 |
| chapter-15 | 8 |
| chapter-16 | 6 |
| chapter-17 | 8 |
| chapter-18 | 5 |
| chapter-19 | 13 |

Part 5:

| Chapter | 건수 |
| --- | ---: |
| chapter-01 | 4 |
| chapter-02 | 4 |
| chapter-03 | 12 |
| chapter-04 | 4 |
| chapter-05 | 4 |
| chapter-06 | 8 |
| chapter-07 | 16 |
| chapter-08 | 7 |
| chapter-09 | 4 |
| chapter-10 | 4 |
| chapter-11 | 8 |
| chapter-12 | 4 |
| chapter-13 | 6 |
| chapter-15 | 6 |
| summary.md | 1 |

## 우선 정비 대상

가장 먼저 정비할 대상은 `읽는 순서` 계열 제목이다. 건수는 적지만 가이드라인에서 금지한 진행 메타가 가장 노골적으로 드러난다.

| 파일 | 위치 | 현재 제목 |
| --- | ---: | --- |
| `docs/parts/part-02/chapter-01/section-01.md` | 157 | `Part 2에서 수학을 읽는 순서` |
| `docs/parts/part-03/index.md` | 60 | `읽는 순서` |
| `docs/parts/part-04/chapter-13/section-02.md` | 38 | `이 절을 읽는 순서` |
| `docs/parts/part-04/chapter-18/section-02.md` | 31 | `먼저 읽는 순서` |
| `docs/parts/part-04/chapter-19/section-03.md` | 34 | `이 절을 읽는 순서` |
| `docs/parts/part-05/summary.md` | 24 | `이 마무리를 읽는 순서` |
| `docs/parts/part-05/chapter-11/section-02.md` | 32 | `이 절을 읽는 순서` |
| `docs/parts/part-05/chapter-11/section-03.md` | 29 | `이 보충학습을 읽는 순서` |
| `docs/parts/part-05/chapter-15/section-01.md` | 43 | `이 절을 읽는 순서` |

## 후속 패치 진행 현황

2026-07-20 후속 패치에서는 Part 1의 시작 페이지, 마무리 페이지, Chapter 1~17 본문과 영어·중국어 간체 번역문을 함께 정리했다.

정리 기준은 최초 1차 검색어에 영어·중국어 간체 번역 제목까지 더한 확장 패턴이다.

```sh
rg -n "^#{2,6} (이 절의 범위|이 절의 목표|이 보충학습의 목표|이 보충학습의 범위|Scope of This Section|Goal of This Section|Goal of This Supplemental Section|Scope of This Supplement|Goal of This Supplement|How to Read This Section|본절 목표|本节目标|这一节的范围|这一节的目标|这篇补充学习的范围|这篇补充学习的目标|这一节的阅读顺序)$" docs/parts/part-01
```

현재 처리 완료 범위에서는 잔여 진행 메타 제목이 없다.

| 범위 | 처리 상태 | 잔여 건수 |
| --- | --- | ---: |
| `docs/parts/part-01/index.*.md` | 완료 | 0 |
| `docs/parts/part-01/summary.*.md` | 완료 | 0 |
| `docs/parts/part-01/chapter-01` | 완료 | 0 |
| `docs/parts/part-01/chapter-02` | 완료 | 0 |
| `docs/parts/part-01/chapter-03` | 완료 | 0 |
| `docs/parts/part-01/chapter-04` | 완료 | 0 |
| `docs/parts/part-01/chapter-05` | 완료 | 0 |
| `docs/parts/part-01/chapter-06` | 완료 | 0 |
| `docs/parts/part-01/chapter-07` | 완료 | 0 |
| `docs/parts/part-01/chapter-08` | 완료 | 0 |
| `docs/parts/part-01/chapter-09` | 완료 | 0 |
| `docs/parts/part-01/chapter-10` | 완료 | 0 |
| `docs/parts/part-01/chapter-11` | 완료 | 0 |
| `docs/parts/part-01/chapter-12` | 완료 | 0 |
| `docs/parts/part-01/chapter-13` | 완료 | 0 |
| `docs/parts/part-01/chapter-14` | 완료 | 0 |
| `docs/parts/part-01/chapter-15` | 완료 | 0 |
| `docs/parts/part-01/chapter-16` | 완료 | 0 |
| `docs/parts/part-01/chapter-17` | 완료 | 0 |

Part 1 전체에서 번역문까지 포함한 확장 패턴 잔여 제목은 0건이다.

추가 검증 결과, `docs/parts/part-01` 아래 177개 `Version` 표기는 모두 `v2026.07.20`이고, `management/release-notes/sections/part-01/`의 `P1-*.md` 59개 파일은 모두 `### v2026.07.20` 항목을 가진다.

2026-07-20 추가 패치에서는 Part 2의 시작 페이지, 마무리 페이지, Chapter 1~15 본문과 영어·중국어 간체 번역문을 함께 정리했다.

Part 2 정리 기준도 최초 1차 검색어에 영어·중국어 간체 번역 제목과 Part 시작/마무리 페이지의 진행 메타 성격 제목을 더한 확장 패턴이다.

```sh
rg -n "^#{2,6} (이 절의 범위|이 절의 목표|이 보충학습의 목표|이 보충학습의 범위|Scope of This Section|Goal of This Section|Goals of This Section|Goal of This Supplemental Section|Goals of This Supplemental Learning|Goals of This Supplementary Learning|Scope of This Supplement|Goal of This Supplement|Goals of This Supplement|How to Read This Section|Reading Order When You See the Phrase Vector Space|본절 목표|本节目标|本节的目标|本补充学习的目标|这节补充学习的目标|这一节的范围|这一节的目标|这篇补充学习的范围|这篇补充学习的目标|这一节的阅读顺序)$" docs/parts/part-02
```

Part 2 전체에서 번역문까지 포함한 확장 패턴 잔여 제목은 0건이다.

| 범위 | 처리 상태 | 잔여 건수 |
| --- | --- | ---: |
| `docs/parts/part-02/index.*.md` | 완료 | 0 |
| `docs/parts/part-02/summary.*.md` | 완료 | 0 |
| `docs/parts/part-02/chapter-01` | 완료 | 0 |
| `docs/parts/part-02/chapter-02` | 완료 | 0 |
| `docs/parts/part-02/chapter-03` | 완료 | 0 |
| `docs/parts/part-02/chapter-04` | 완료 | 0 |
| `docs/parts/part-02/chapter-05` | 완료 | 0 |
| `docs/parts/part-02/chapter-06` | 완료 | 0 |
| `docs/parts/part-02/chapter-07` | 완료 | 0 |
| `docs/parts/part-02/chapter-08` | 완료 | 0 |
| `docs/parts/part-02/chapter-09` | 완료 | 0 |
| `docs/parts/part-02/chapter-10` | 완료 | 0 |
| `docs/parts/part-02/chapter-11` | 완료 | 0 |
| `docs/parts/part-02/chapter-12` | 완료 | 0 |
| `docs/parts/part-02/chapter-13` | 완료 | 0 |
| `docs/parts/part-02/chapter-14` | 완료 | 0 |
| `docs/parts/part-02/chapter-15` | 완료 | 0 |

추가 검증 결과, `docs/parts/part-02` 아래 195개 `Version` 표기는 모두 `v2026.07.20`이고, `management/release-notes/sections/part-02/`의 `P2-*.md` 65개 파일은 모두 `### v2026.07.20` 항목을 가진다.

2026-07-20 추가 패치에서는 Part 3의 시작 페이지, 마무리 페이지, Chapter 1~9 본문과 영어·중국어 간체 번역문을 함께 점검했다.

Part 3의 최초 제목 위반은 시작 페이지의 `읽는 순서` 1건이었고, 번역문에는 `Reading Order`, `阅读顺序`가 같은 위치에 남아 있었다. 확장 점검 대상인 `범위와 비범위` 계열도 Part 시작 페이지 문맥에서 함께 정리했다.

```sh
rg -n "^#{2,6} (이 절의 범위|이 절의 목표|이 절을 읽는 순서|이 보충학습의 범위|이 보충학습의 목표|이 보충학습을 읽는 순서|읽는 순서|먼저 읽는 순서|이 마무리를 읽는 순서|Scope of This Section|Goal of This Section|Goals of This Section|Goal of This Supplemental Section|Goals of This Supplemental Learning|Goals of This Supplementary Learning|Scope of This Supplement|Goal of This Supplement|Goals of This Supplement|How to Read This Section|Reading Order|본절 목표|本节目标|本节的目标|本补充学习的目标|这节补充学习的目标|这一节的范围|这一节的目标|这篇补充学习的范围|这篇补充学习的目标|这一节的阅读顺序|阅读顺序)$" docs/parts/part-03
```

Part 3 전체에서 번역문까지 포함한 확장 패턴 잔여 제목은 0건이다.

| 범위 | 처리 상태 | 잔여 건수 |
| --- | --- | ---: |
| `docs/parts/part-03/index.*.md` | 완료 | 0 |
| `docs/parts/part-03/summary.*.md` | 점검 완료 | 0 |
| `docs/parts/part-03/chapter-01` | 점검 완료 | 0 |
| `docs/parts/part-03/chapter-02` | 점검 완료 | 0 |
| `docs/parts/part-03/chapter-03` | 점검 완료 | 0 |
| `docs/parts/part-03/chapter-04` | 점검 완료 | 0 |
| `docs/parts/part-03/chapter-05` | 점검 완료 | 0 |
| `docs/parts/part-03/chapter-06` | 점검 완료 | 0 |
| `docs/parts/part-03/chapter-07` | 점검 완료 | 0 |
| `docs/parts/part-03/chapter-08` | 점검 완료 | 0 |
| `docs/parts/part-03/chapter-09` | 점검 완료 | 0 |

추가 검증 결과, `docs/parts/part-03` 아래 162개 `Version` 표기는 모두 `v2026.07.20`이고, `management/release-notes/sections/part-03/`의 `P3-*.md` 54개 파일은 모두 `### v2026.07.20` 항목을 가진다.

2026-07-20 추가 패치에서는 Part 4의 시작 페이지, 마무리 페이지, Chapter 1~19 본문과 영어·중국어 간체 번역문을 함께 점검했다.

Part 4의 최초 제목 위반은 한국어 본문의 `이 절의 범위`, `이 절의 목표`, 보충학습의 범위·목표 제목, 일부 `읽는 순서` 계열 제목이 중심이었다. 번역문에는 영어 `Reading Order`, 중국어 `本节目标`, `阅读顺序`, `本补充学习的目标` 계열이 대응 위치에 남아 있었다. Part 시작·마무리 페이지의 `목적`, `목표`, `범위` 계열 제목도 Part 오버뷰 문맥에서 함께 정리했다.

```sh
rg -n "^#{2,6} (이 절의 범위|이 절의 목표|이 절을 읽는 순서|이 보충학습의 범위|이 보충학습의 목표|이 보충학습을 읽는 순서|읽는 순서|먼저 읽는 순서|이 마무리를 읽는 순서|이 파트의 목적|이 파트의 목표|이 파트에서 설명하는 범위와 설명하지 않을 범위|Purpose of This Part|Goals of This Part|Scope of This Section|Goal of This Section|Goals of This Section|Goal of This Supplemental Section|Goals of This Supplemental Learning|Goals of This Supplementary Learning|Scope of This Supplement|Goal of This Supplement|Goals of This Supplement|How to Read This Section|Reading Order|본절 목표|本节目标|本节的目标|本补充学习的目标|这节补充学习的目标|这一节的范围|这一节的目标|这篇补充学习的范围|这篇补充学习的目标|这一节的阅读顺序|阅读顺序|这一 Part 的目的|这一 Part 的目标)$" docs/parts/part-04
```

Part 4 전체에서 번역문까지 포함한 확장 패턴 잔여 제목은 0건이다.

| 범위 | 처리 상태 | 잔여 건수 |
| --- | --- | ---: |
| `docs/parts/part-04/index.*.md` | 완료 | 0 |
| `docs/parts/part-04/summary.*.md` | 완료 | 0 |
| `docs/parts/part-04/chapter-01` | 완료 | 0 |
| `docs/parts/part-04/chapter-02` | 완료 | 0 |
| `docs/parts/part-04/chapter-03` | 완료 | 0 |
| `docs/parts/part-04/chapter-04` | 완료 | 0 |
| `docs/parts/part-04/chapter-05` | 완료 | 0 |
| `docs/parts/part-04/chapter-06` | 완료 | 0 |
| `docs/parts/part-04/chapter-07` | 완료 | 0 |
| `docs/parts/part-04/chapter-08` | 완료 | 0 |
| `docs/parts/part-04/chapter-09` | 완료 | 0 |
| `docs/parts/part-04/chapter-10` | 완료 | 0 |
| `docs/parts/part-04/chapter-11` | 완료 | 0 |
| `docs/parts/part-04/chapter-12` | 완료 | 0 |
| `docs/parts/part-04/chapter-13` | 완료 | 0 |
| `docs/parts/part-04/chapter-14` | 완료 | 0 |
| `docs/parts/part-04/chapter-15` | 완료 | 0 |
| `docs/parts/part-04/chapter-16` | 완료 | 0 |
| `docs/parts/part-04/chapter-17` | 완료 | 0 |
| `docs/parts/part-04/chapter-18` | 완료 | 0 |
| `docs/parts/part-04/chapter-19` | 완료 | 0 |

추가 검증 결과, `docs/parts/part-04` 아래 183개 `Version` 표기는 모두 `v2026.07.20`이고, `management/release-notes/sections/part-04/`의 `P4-*.md` 61개 파일은 모두 `### v2026.07.20` 항목과 진행 메타 제목 정리 기록을 가진다.

아래 표는 최초 감사 당시 후속 정비 후보로 남긴 목록이다. 위 완료 기록이 있는 Part 4 항목은 2026-07-20 추가 패치에서 정리되었고, 남은 후속 판단에는 Part 5 항목과 문장 단위 보조 점검 대상만 사용한다.

`이 보충학습의 범위` 계열은 본문보다 별도 안내문처럼 굳기 쉬우므로, `어떤 오해를 바로잡는가`, `무엇을 구분하는가`, `어떤 연결을 복구하는가`가 드러나는 제목으로 바꾸는 것이 좋다.

| 파일 | 위치 | 현재 제목 |
| --- | ---: | --- |
| `docs/parts/part-04/chapter-06/section-03.md` | 10 | `이 보충학습의 범위` |
| `docs/parts/part-04/chapter-06/section-04.md` | 16 | `이 보충학습의 범위` |
| `docs/parts/part-04/chapter-07/section-03.md` | 10 | `이 보충학습의 범위` |
| `docs/parts/part-04/chapter-07/section-04.md` | 14 | `이 보충학습의 범위` |
| `docs/parts/part-04/chapter-08/section-03.md` | 12 | `이 보충학습의 범위` |
| `docs/parts/part-04/chapter-09/section-03.md` | 19 | `이 보충학습의 범위` |
| `docs/parts/part-04/chapter-10/section-03.md` | 17 | `이 보충학습의 범위` |
| `docs/parts/part-04/chapter-19/section-04.md` | 19 | `이 보충학습의 범위` |
| `docs/parts/part-05/chapter-11/section-03.md` | 12 | `이 보충학습의 범위` |
| `docs/parts/part-05/chapter-13/section-03.md` | 12 | `이 보충학습의 범위` |

## 보조 점검 대상

문장 안의 `읽는 순서` 표현은 모두 금지 대상은 아니다. 표나 도식을 실제로 해석하는 절차를 설명하는 경우는 남길 수 있다. 다만 다음 문장들은 진행 메타로 쓰였는지 다시 확인할 필요가 있다.

| 파일 | 위치 | 표현 |
| --- | ---: | --- |
| `docs/parts/part-02/chapter-03/section-02.md` | 50 | `즉 이 절의 목표는...` |
| `docs/parts/part-02/chapter-08/section-04.md` | 426 | `이 절에서는... 읽는 순서로 둡니다.` |
| `docs/parts/part-04/chapter-07/section-01.md` | 845 | `이 절의 목표는...` |
| `docs/parts/part-04/chapter-07/section-02.md` | 908 | `이 절의 목표는...` |
| `docs/parts/part-04/chapter-12/section-02.md` | 141 | `읽는 순서는 다음처럼...` |
| `docs/parts/part-04/chapter-12/section-03.md` | 146 | `즉, 이 절의 목표는...` |
| `docs/parts/part-04/chapter-15/section-02.md` | 303 | `이 절의 목표도 바로...` |
| `docs/parts/part-04/chapter-15/section-03.md` | 235 | `이 결과를 읽는 순서는...` |
| `docs/parts/part-04/chapter-15/section-04.md` | 281 | `이 결과를 읽는 순서는...` |
| `docs/parts/part-05/chapter-11/section-02.md` | 32 | 제목 위반과 함께 본문 흐름 재구성 필요 |

다음은 실제 표, 도식, 토큰, 문서 해석 순서를 설명하는 표현으로 보이며, 일괄 금지보다 문맥 유지 여부를 판단한다.

| 파일 | 위치 | 판단 |
| --- | ---: | --- |
| `docs/parts/part-02/chapter-05/section-02.md` | 75 | 차트 해석 순서라서 유지 가능성이 높다. |
| `docs/parts/part-03/chapter-02/section-02.md` | 41 | 표 열 해석 순서라서 유지 가능성이 높다. |
| `docs/parts/part-03/chapter-02/section-03.md` | 41 | 품질 점검 항목의 적용 순서라서 유지 가능성이 높다. |
| `docs/parts/part-03/chapter-07/section-02.md` | 6 | 비교표 해석 순서라서 유지 가능성이 높다. |
| `docs/parts/part-04/chapter-06/section-01.md` | 255 | 표의 열 이름으로 쓰여 유지 가능성이 높다. |
| `docs/parts/part-04/chapter-10/section-02.md` | 226 | 도식 해석 순서라서 유지 가능성이 높다. |
| `docs/parts/part-06/chapter-01/section-02.md` | 56 | 토큰화 결과 확인 순서라서 유지 가능성이 높다. |
| `docs/parts/part-06/chapter-01/section-05.md` | 65 | 도식 해석 순서라서 유지 가능성이 높다. |
| `docs/parts/part-06/chapter-13/section-02.md` | 225 | 사례 해석 제목이므로 진행 메타와 다르다. |
| `docs/table-of-contents.md` | 666 | 목차 설명 문장으로 진행 메타 제목이 아니다. |

## 정비 원칙

1. `이 절의 범위`와 `이 절의 목표`가 연속으로 있는 Section은 두 블록을 도입 문단 하나로 흡수한다.
2. 제목은 `무엇을 안내하는가`가 아니라 `무엇을 설명하는가`로 바꾼다.
3. `읽는 순서` 제목은 절차 제목으로 남기지 말고, 실제 대상의 구조가 드러나는 제목으로 바꾼다.
4. 보충학습 제목은 `범위/목표` 대신 오해, 구분, 연결 복구를 드러내는 제목으로 바꾼다.
5. 대량 정비는 Part 단위로 진행하고, Section 본문을 수정하면 `section-metadata-guidelines.md`에 따라 `Version`과 릴리즈노트 연결을 함께 확인한다.

## 권장 작업 순서

1. Part 5의 `읽는 순서` 5건과 보충학습 진행 메타 5건을 먼저 정비한다.
2. Part 4의 보충학습 범위/목표 제목과 `읽는 순서` 계열을 정비한다.
3. Part 4와 Part 5의 `이 절의 범위`/`이 절의 목표` 쌍을 Chapter 단위로 정비한다.
4. Part 1과 Part 2의 `이 절의 목표` 제목을 Chapter 단위로 정비한다.
5. Part 시작/마무리 페이지의 `읽는 순서`, `이 파트의 목표`, `범위와 비범위` 계열은 Part 오버뷰 가이드와 충돌하지 않는지 별도 판단한다.

## 후속 확인

정비 후에는 다음 명령이 0건에 가까워지는지 확인한다.

```sh
rg -n "^#{2,6} (이 절의 범위|이 절의 목표|이 절을 읽는 순서|이 보충학습의 범위|이 보충학습의 목표|이 보충학습을 읽는 순서|읽는 순서|먼저 읽는 순서|이 마무리를 읽는 순서)$" docs/parts
```

단, Part 시작/마무리 페이지의 오버뷰 구조는 Section 본문과 역할이 다르므로 일괄 삭제보다 별도 판단이 필요하다.
