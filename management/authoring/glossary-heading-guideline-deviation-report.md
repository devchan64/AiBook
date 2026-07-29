# 개념사전 표제 가이드라인 이탈 후보 리포트

작성일: 2026-07-29

## 검토 목적

`management/concept-glossary-integrated-index.md`와 `docs/reference/concept-glossary-terms/`의 단어별 원고를 기준으로, 개념사전 작성 규칙에서 벗어날 가능성이 있는 표제와 관련 개념 표현을 추적한다.

이 문서는 즉시 삭제 목록이 아니라 후속 정리 큐다. 실제 수정 전에는 각 항목의 중심 Section, 등장 Section, 공개 색인 include, 본문 링크를 다시 확인한다.

## 기준 문서

- 통합 인덱스: `management/concept-glossary-integrated-index.md`
- 단어별 원고: `docs/reference/concept-glossary-terms/`
- 적용 기준: `management/guidelines/concept-glossary-guidelines.md`
- 선행 검토: `management/authoring/part-01-07-glossary-heading-review.md`

## 판정 축

| 판정 축 | 확인 질문 | 기본 처리 |
| --- | --- | --- |
| 삭제된 표제 잔존 | 삭제·제외한 표제명이 관련 개념 필드에 남아 있는가 | 유지 표제 중심으로 교체 |
| 범위 재확장 | 한국어 표제는 좁혔는데 영어·중국어 표제가 단독 일반어로 다시 열리는가 | 제목과 첫 문장을 문맥 한정으로 동기화 |
| 일반어 우세 | 표준 개념보다 일반 사전적 의미, 작업 절차, 문서 형식, 도구 구성요소 이름이 앞서는가 | 새 표제 제외 또는 상위 표제 흡수 |
| 언어 대응 불일치 | 같은 slug의 한국어·영어·중국어 표제가 서로 다른 범위를 가리키는가 | 언어별 표제와 첫 정의를 같은 범위로 조정 |

## 상태 요약

| 그룹 | 범위 | 2026-07-29 상태 | 다음 처리 |
| --- | --- | --- | --- |
| A | 삭제·제외 표제명이 관련 개념에 남은 경우 | 완료 | 새 잔존 표현이 생기면 유지 표제 기준으로 교체 |
| B | 영어·중국어 표제가 한국어 문맥 한정 표제보다 넓어진 경우 | 완료 | slug 변경은 보류하고 제목·첫 문장 동기화 원칙 유지 |
| C | 표제 자체 재검토 대상 | 완료 | 8개 항목은 삭제하지 않고 문맥 한정 표제로 유지 |
| D | 다국어 항목 품질 점검 | 1차 검색 정리 완료 | 제목·본문 전체의 자연스러운 번역 품질은 별도 읽기 검토 |
| E | 본문 개념사전 링크 앵커 경고 후보 | 진행 중 | 남은 앵커 경고는 빈도순으로 1차 판정 후 흡수·추가·보류 결정 |

## 처리 기록

### A. 삭제·제외 표제 잔존 정리

`part-01-07-glossary-heading-review.md`에서 삭제 또는 표제 제외 흐름으로 정리한 표현이 관련 개념 필드에 남아 있던 사례를 정리했다.

대표 처리:

| 잔존 표현 유형 | 처리 방향 |
| --- | --- |
| `external resource`, `external tool`, `external system` | `retrieval`, `provenance`, `source data`, `tool use`, `trust boundary` 등 유지 표제로 교체 |
| `orchestration`, `service operation` | `permission`, `AI agent`, `accountability`, `privacy` 등 실제 관리 표제로 교체 |
| `dependency`, `planning`, `expression`, `tree`, `array` | 하위 설명 또는 유지 표제로 흡수 |
| 중국어 관련 개념의 영어-only 표현 | 중국어 표제어 우선 표기로 교체하고 필요한 경우 영어를 괄호 병기 |

### B. 표제 범위 재동기화

한국어 표제는 문맥 한정으로 좁혔지만 영어·중국어 표제가 단독 일반어처럼 남아 있던 항목을 제목과 첫 정의 중심으로 정리했다.

| slug | 정리 방향 |
| --- | --- |
| `state` | 에이전트/RL 상태 문맥으로 제한 |
| `event` | 확률 사건 문맥으로 제한 |
| `visualization` | 데이터 시각화 문맥으로 제한 |
| `metadata` | 문서 검색·검색 메타데이터 문맥으로 제한 |
| `permission` | 도구 실행 권한 문맥으로 제한 |
| `search` | 상태공간 탐색 문맥으로 제한 |
| `model-input`, `model-output` | 문제 정의와 모델링 계약 문맥으로 제한 |
| `model-score` | 모델 후보 점수·순위화 문맥으로 제한 |
| `evaluation-design` | 모델 평가 설계 문맥으로 제한 |
| `output-structure` | 모델링 출력 구조 문맥으로 제한 |

### C. 표제 자체 재검토

아래 항목은 삭제하지 않고 문맥 한정 표제로 유지한다. 단독 일반어로 다시 넓어지지 않도록 언어별 표제와 첫 정의를 함께 관리한다.

| slug | 유지 표제 | 재판정 |
| --- | --- | --- |
| `decision` | 업무 의사결정(decision) | 모델 점수와 실제 업무 행동을 분리하는 기준점 |
| `learning` | AI 학습(learning) | `learning`과 `training`을 구분하는 상위 기준점 |
| `license` | 자료 라이선스(license) | 저작권·출처 표시·자료 사용 조건을 구분하는 법·운영 기준점 |
| `retrieval` | RAG 검색(retrieval) | RAG 입력 근거 후보를 가져오는 단계 |
| `topology` | 위상(topology) | 표준 수학 용어로 유지하되, 원고에서는 표현 공간의 연결성·연속성 같은 구조를 가리키는 제한된 맥락에서 사용 |
| `response-generation` | LLM 응답 생성(response generation) | LLM inference의 자연어 출력 생성 문맥 |
| `software-regression` | AI 서비스 소프트웨어 회귀(software regression) | 모델·프롬프트·설정 변경 뒤 기존 품질 저하를 설명하는 검증 기준점 |
| `text-and-data-mining` | 학습 데이터 맥락의 텍스트·데이터 마이닝(text and data mining, TDM) | 학습 데이터와 저작권 논의의 법·정책 전문 용어 |

### D. 다국어 항목 1차 정리

검색으로 확인 가능한 직접 이탈 표현은 정리했다. 남은 작업은 표제 자체보다 제목·본문 전체의 자연스러운 번역 품질 검토다.

| 유형 | 2026-07-29 처리 | 남은 확인 |
| --- | --- | --- |
| 영어 파일에 한국어 본문이 남음 | 검색 기준 잔존 0건으로 정리 | 영어 독자 기준 문장 품질 읽기 검토 |
| 중국어 관련 개념에 영어 일반어가 직접 남음 | 중국어 표제어 우선 표기로 정리 | 약어·모델명 병기 방식의 일관성 확인 |
| Related concepts가 현재 표제와 맞지 않음 | 영어·중국어 관련 개념 필드의 직접 잔존 표현을 유지 표제 중심으로 교체 | 새로 생긴 표제와 미등재 후보의 적합성 확인 |

### E. 본문 링크 앵커 경고 1차 정리

Part 본문에서 `docs/reference/concept-glossary-parts/*.md`, `docs/reference/concept-glossary-alpha/*.en.md`, `docs/reference/concept-glossary-pinyin/*.zh.md`로 향하는 링크를 모아, 대상 언어별 색인이 실제로 include하는 단어별 원고의 앵커와 대조했다.

2026-07-29 기준으로 실제 앵커가 없는 한국어 본문 링크 후보는 351개였고, 즉시 수정 가능한 항목을 반영한 뒤 328개가 남았다. 같은 기준을 영어·중국어 본문까지 넓혀 다시 대조하면 759건, 191개 앵커 후보가 잡혔고, 언어별 색인 경로 오류 23건을 먼저 수정한 뒤 736건, 188개 앵커 후보가 남았다.

| 항목 | 처리 |
| --- | --- |
| `#glossary-sample` | Part 3의 `sample` 반복 문맥을 `샘플 단위(sample unit)`로 판정하고 `sample-unit` 단어별 원고 3개 언어에 호환 앵커 추가 |
| `#glossary-output-structure` | 한국어 Part 3 링크 경로를 실제 include 위치인 `05-mieum.md`로 수정 |
| `#glossary-score` | 한국어 Part 3 링크 경로를 실제 include 위치인 `05-mieum.md`로 수정 |
| `review-queue` | 운영 출력 구조 이름으로 판정해 `output-structure` 링크로 흡수 |
| `comparison-report` | 문서 산출물 이름으로 판정해 `output-structure` 링크로 흡수 |
| `comparison-table` | 표 형식 이름으로 판정해 `output-structure` 링크로 흡수 |
| `summary-table` | 표 형식 이름으로 판정해 `data-modeling` 링크로 흡수 |
| `training` | 일반어로 넓게 열리는 단독 링크를 `model-training` 표제로 흡수 |
| `random-forest` | 표준 모델 계열로 판정해 한·영·중 단어별 원고와 공개 색인 include 추가 |
| `bootstrap` | 통계·앙상블 문맥의 표준 용어로 판정해 한·영·중 단어별 원고와 공개 색인 include 추가 |
| `oob-score` | Random Forest 하위 평가 용어로 판정해 한·영·중 단어별 원고와 공개 색인 include 추가 |
| `optimizer` | 표준 딥러닝 학습 용어로 판정해 한·영·중 단어별 원고와 공개 색인 include 추가 |
| `data-modeling` 중국어 링크 | 실제 include 위치가 `d.zh.md`인데 본문 링크가 `s/`를 가리키던 7건을 `d/`로 수정 |
| `generalization` 중국어 링크 | 실제 include 위치가 `f.zh.md`인데 본문 링크가 `g/`를 가리키던 9건을 `f/`로 수정 |
| `activation-function` 중국어 링크 | 실제 include 위치가 `j.zh.md`인데 본문 링크가 `a/`를 가리키던 7건을 `j/`로 수정 |

남은 고빈도 후보의 1차 판정은 다음 순서로 처리한다. 표준 개념처럼 보이더라도 기존 상위 표제 안에서 충분히 관리할 수 있으면 새 단어별 원고를 만들지 않는다.

| 후보 앵커 | 건수 | 1차 판정 | 우선 대응 |
| --- | ---: | --- | --- |
| `#glossary-row` | 12 | 하위 설명 | `sample-unit`, `data-modeling`, `data-structure` 중 문맥별 흡수 |
| `#glossary-evidence-strength` | 12 | 문맥 한정 개념 후보 | `interpretation-boundary` 또는 `evaluation-design` 흡수 우선, 독립 표제는 보류 |
| `#validation` | 9 | 일반어 우세 | `model-validation`, `validation-data`, `evaluation-design`로 분해 |
| `#error-case` | 9 | 작업·분석 산출물 | `model-validation` 또는 `error-cost` 하위 설명으로 흡수 |
| `#support-vector-machine` | 9 | 표준 모델 계열 | 기존 `kernel`, `decision-boundary`, `margin` 흡수로 충분한지 확인 후 등재 보류 |
| `#feature-scale` | 9 | 하위 설명 | `standardization`, `feature`, `distance` 문맥으로 흡수 |
| `#feature-importance` | 9 | 문맥 한정 개념 후보 | `random-forest` 하위 설명으로 우선 흡수 |
| `#glossary-policy-rule` | 9 | 문맥 한정 개념 후보 | `decision`, `model-output`, `AI agent` 중 문맥별 흡수 |
| `#glossary-evaluation` | 9 | 일반어 우세 | 단독 표제 금지, `evaluation-design`, `metric`, `evaluation-data`로 분해 |
| `#glossary-dataset-candidate` | 9 | 하위 설명 | `dataset` 또는 `data-modeling` 하위 설명으로 흡수 |
| `#glossary-problem-representation-structure` | 9 | 문맥 한정 개념 후보 | `task-definition`, `data-modeling`, `output-structure`로 흡수 우선 |
| `#k-means` | 7 | 표준 모델 계열 | `clustering`, `centroid`, `distance` 하위 설명으로 충분한지 확인 후 등재 보류 |

## 남은 작업

1. E그룹의 남은 다국어 앵커 후보 736건을 위 표의 우선순위대로 처리한다.
2. 기존 표제가 있는 항목은 먼저 언어별 색인 경로 오류인지 확인한다.
3. 파일이 없는 후보는 `표준 개념`, `문맥 한정 개념`, `하위 설명`, `작업·형식 이름`, `구현·도구·사례`, `임시 표현` 중 하나로 1차 판정한다.
4. 작업·형식 이름과 하위 설명은 새 표제를 만들지 않고 기존 상위 표제로 흡수한다.
5. 표준 개념은 기존 단어별 원고가 있는지 먼저 확인하고, 없을 때만 한·영·중 항목과 공개 색인 include 추가를 검토한다.
6. D그룹은 검색 기준 정리 뒤에도 제목과 본문이 각 언어 독자에게 자연스러운지 별도 읽기 검토로 확인한다.
7. 변경 뒤에는 `management/concept-glossary-integrated-index.md`를 다시 맞추고, 빌드 경고에서 새 앵커 문제가 생겼는지 확인한다.

## 운영 원칙

- `topology`는 표준 수학 용어로 표제를 유지한다. 위치나 거리의 동의어처럼 쓰지 않고, 표현 공간의 연결성·연속성 같은 구조를 가리키는 제한된 맥락에서만 사용한다.
- 영어·중국어 항목을 수정할 때 한국어 원문의 `Section ID`와 `Version`을 임의로 바꾸지 않는다.
- 본문 Section을 같이 고치지 않는 한 Section 릴리즈노트는 만들지 않는다.
- `site/` 빌드 산출물은 이 리포트 정리와 함께 커밋하지 않는다.
