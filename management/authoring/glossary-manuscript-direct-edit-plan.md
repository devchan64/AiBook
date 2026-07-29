# 개념사전 표제 정리 실행 기록

작성일: 2026-07-29

## 목적

Part 1~7 원고의 개념사전 링크와 표제 후보를 정리한 완료 기록이다. 표제 판정과 본문 링크 정리 원칙은 `management/guidelines/concept-glossary-guidelines.md`에 흡수했으며, 이 문서는 해당 정리 작업의 범위, 대표 처리 결과, 검증 증거만 남긴다.

이 문서는 기존 `glossary-heading-guideline-deviation-report.md`와 `part-01-07-glossary-heading-review.md`를 흡수한 뒤 압축한 관리 기록이다.

## 기준 문서

- 표준 가이드라인: `management/guidelines/concept-glossary-guidelines.md`
- 통합 인덱스: `management/concept-glossary-integrated-index.md`
- 단어별 원고: `docs/reference/concept-glossary-terms/`
- 공개 색인:
  - 한국어: `docs/reference/concept-glossary-parts/`
  - 영어: `docs/reference/concept-glossary-alpha/`
  - 중국어: `docs/reference/concept-glossary-pinyin/`

## 처리 범위

- 본문 링크 수정 대상: `docs/parts/**/*.md`, `docs/parts/**/*.en.md`, `docs/parts/**/*.zh.md`
- 개념사전 항목과 색인 대상: `docs/reference/concept-glossary-terms/`, `docs/reference/concept-glossary-parts/`, `docs/reference/concept-glossary-alpha/`, `docs/reference/concept-glossary-pinyin/`
- 관리 인덱스 대상: `management/concept-glossary-integrated-index.md`
- 제외 대상: `site/` 빌드 산출물, 배포 nav 연결

## 대표 처리 결과

| 범위 | 처리 결과 |
| --- | --- |
| 삭제·제외 표제 | 작업·형식·도구 설명 성격이 강한 표제를 단어별 원고와 언어별 공개 색인 include에서 제거 |
| 문맥 한정 표제 | `kernel`, `search`, `state`, `action`, `event`, `visualization`, `metadata`, `permission`, `output-structure`, `model-input`, `model-output`, `model-score`, `evaluation-design`, `tool-use`, `topology` 등은 단독 일반어로 넓어지지 않게 제목과 첫 문장 범위를 좁혀 유지 |
| Part 2 작업·형식 링크 | `formula`, `notebook`, `dataframe`, `plot`, `line-plot`, `legend`, `value`, `list`, `dictionary`, `loop`, `class`, `branch`, `indexing` 링크를 제거하거나 대표 Section 참조로 전환 |
| Part 3 산출물·작업 판단 링크 | `review-queue`, `comparison-report`, `comparison-table`, `summary-table`, `glossary-*` 산출물 앵커를 `output-structure`, `data-modeling`, `baseline`, `model-input`, `supervised-learning-label`, `label-consistency`, `feature`, `target` 등으로 흡수 |
| Part 4 모델 옵션·하위 방법 링크 | 모델 내부 옵션, 세부 알고리즘명, 수식 하위 요소를 `hyperparameter`, `decision-tree`, `random-forest`, `value-based-reinforcement-learning`, `policy-based-reinforcement-learning`, `exploration`, `reinforcement-learning-policy` 등으로 흡수 |
| Part 5 딥러닝 하위 구성요소 링크 | 세부 부품 링크를 `multilayer-neural-network`, `weighted-sum`, `loss-function`, `self-attention`, `recurrent-neural-network`, `transformer`, `model-output`, `cnn-convolutional-neural-network`, `hyperparameter` 등으로 흡수 |
| Part 7 프로젝트 일반어 링크 | `review`, `retrospective`, `deployment`, `evaluation`, `token-coverage`, `static-deployment` 등을 본문 설명으로 돌리거나 `tokenization`, `evaluation-design`으로 좁힘 |
| 표준 모델·방법 계열 | `support-vector-machine`, `k-means`, `dbscan`, `random-forest`, `bootstrap`, `oob-score`, `optimizer`는 독립 표제로 판정해 한·영·중 단어별 원고와 공개 색인 include를 맞춤 |

## 완료 감사

- 우선순위 후보는 `흡수`, `기존 표제 연결`, `신규 표제 보류`, `신규 표제 생성` 중 하나로 처리했다.
- 기존 표제가 있는 항목은 언어별 색인 경로 오류를 먼저 확인하고 실제 include 위치로 보정했다.
- 파일이 없는 후보는 `표준 개념`, `문맥 한정 개념`, `하위 설명`, `작업·형식 이름`, `구현·도구·사례`, `임시 표현` 중 하나로 1차 판정했다.
- 작업·형식 이름과 하위 설명은 새 표제로 만들지 않고 기존 상위 표제로 흡수했다.
- `topology`는 표준 수학 용어 표제를 유지하되, 위치나 거리의 동의어가 아니라 공간의 연결성·연속성 같은 구조를 가리키는 제한된 맥락으로 정리했다.
- 본문 Section을 같이 고치지 않은 링크 정리는 개념사전 전용 규칙에 따라 Section 릴리즈노트를 만들지 않았다.

## 검증 기록

2026-07-29 기준 검증 결과:

- 대표 후보 앵커 검색: 잔여 0건
- 전체 `docs/parts/` 개념사전 링크 앵커 정적 검사: `broken_count 0 unique 0`
- `git diff --check`: 통과
- `.venv/bin/python -m mkdocs build --strict`: 성공, `274.81 seconds`

배포가 아닌 평상시 후속 정리에서는 빌드를 반복 실행하지 않고, `management/guidelines/concept-glossary-guidelines.md`의 검증 절차에 따라 `rg`, `git diff --check`, 필요한 정적 링크 검사로 확인한다.
