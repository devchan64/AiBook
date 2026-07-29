# 개념사전 표제 가이드라인 이탈 후보 리포트

작성일: 2026-07-29

## 검토 목적

`management/concept-glossary-integrated-index.md`와 `docs/reference/concept-glossary-terms/`의 단어별 원고를 기준으로, 개념사전 작성 규칙에서 벗어날 가능성이 있는 표제와 관련 개념 표현을 추적한다. 이 리포트는 즉시 삭제 목록이 아니라 후속 정리 큐다. 실제 수정 전에는 각 항목의 중심 Section, 등장 Section, 공개 색인 include, 본문 링크를 다시 확인한다.

## 진행 상태

- 2026-07-29: A그룹의 삭제·제외 표제 잔존 표현을 관련 개념 필드에서 우선 정리했다. `permission.en.md`의 `service operation` 잔존도 같은 묶음으로 처리했다.
- 2026-07-29: B그룹 중 slug 변경 없이 처리 가능한 영어·중국어 표제와 첫 의미 문장을 문맥 한정 표현으로 좁혔다.
- 2026-07-29: 위 변경 뒤 `management/concept-glossary-integrated-index.md`를 현재 단어별 원고 기준으로 다시 생성했다.
- 2026-07-29: D그룹 중 영어 파일의 한국어 본문 잔존을 정리하고, 영어 `Related concepts`의 표제 관리 제외 표현을 유지 표제 중심으로 교체했다.
- 2026-07-29: D그룹 중 중국어 `相关概念`에 영어-only 또는 일반어로 직접 남은 표현을 중국어 표제 우선 표기로 정리했다.
- 2026-07-29: 위 변경 뒤 `management/concept-glossary-integrated-index.md`를 현재 단어별 원고 기준으로 다시 생성했다.
- 2026-07-29: C그룹 8개 항목은 삭제보다 문맥 한정 표제로 유지하는 쪽으로 재판정하고, 한국어 표제와 첫 뜻 문장을 좁혔다.
- 2026-07-29: 위 변경 뒤 `management/concept-glossary-integrated-index.md`를 현재 단어별 원고 기준으로 다시 생성했다.
- 2026-07-29: C그룹 8개 항목의 영어·중국어 단어별 원고를 추가하고, 영어 알파벳 색인과 중국어 병음 색인 include를 갱신했다.
- 2026-07-29: 위 변경 뒤 `management/concept-glossary-integrated-index.md`를 현재 단어별 원고 기준으로 다시 생성했다.
- 2026-07-29: 한국어 Part 본문에서 개념사전 자음별 색인 링크와 실제 include 앵커를 대조했다. 즉시 수정 가능한 `sample`, `output-structure`, `score` 링크 호환성을 먼저 보강했다.
- 2026-07-29: 남은 고빈도 후보 9개를 1차 판정 기준으로 처리했다. 표준 모델·학습 용어인 `random-forest`, `bootstrap`, `oob-score`, `optimizer`는 단어별 원고와 한·영·중 색인 include를 추가했고, 운영 산출물·표 형식 이름인 `review-queue`, `comparison-report`, `comparison-table`, `summary-table` 및 단독 `training` 링크는 기존 상위 표제로 흡수했다.
- 남은 작업: D그룹은 제목·본문 전체 번역 품질을 별도 읽기 검토로 이어갈 수 있다. C그룹의 `topology`는 표준 수학 용어로 표제를 유지하되, 본문에서는 표현 공간 맥락의 짧은 안내로만 사용한다.

## 기준 문서

- 통합 인덱스: `management/concept-glossary-integrated-index.md`
- 단어별 원고: `docs/reference/concept-glossary-terms/`
- 적용 기준: `management/guidelines/concept-glossary-guidelines.md`
- 선행 검토: `management/authoring/part-01-07-glossary-heading-review.md`

## 판정 축

- 삭제된 표제 잔존: 이미 단어별 원고와 공개 색인에서 제거한 표제명이 `Related concepts`, `相关概念`, `함께 볼 개념`에 남아 있는가.
- 범위 재확장: 한국어 표제는 문맥 한정으로 좁혔는데 영어·중국어 표제가 다시 단독 일반어로 열려 있는가.
- 일반어 우세: 표준 개념보다 일반 사전적 의미, 작업 절차, 문서 형식, 도구 구성요소 이름이 표제의 주 역할이 되는가.
- 언어 대응 불일치: 같은 slug의 한국어, 영어, 중국어 표제가 서로 다른 범위를 가리키는가.

## A. 즉시 정리 후보: 삭제·제외 표제명이 관련 개념에 남은 경우

아래 항목은 `part-01-07-glossary-heading-review.md`에서 삭제 또는 표제 제외 흐름으로 정리한 표현이 관련 개념 필드에 남아 있던 사례다. 독자가 클릭 가능한 표제처럼 읽을 수 있으므로 2026-07-29에 우선 정리했다.

| 파일 | 남은 표현 | 문제 | 권장 처리 |
| --- | --- | --- | --- |
| `data.en.md` | `external resource` | 삭제된 `external-resource` 표제명이 관련 개념에 남음 | `retrieval-augmented generation, RAG`, `provenance`, `source data` 등 실제 유지 표제로 대체 |
| `tool-use.en.md` | `external tool`, `orchestration` | 외부 도구와 오케스트레이션을 독립 관련 표제로 다시 노출 | `permission`, `least privilege`, `AI agent`, `trust boundary` 중심으로 재작성 |
| `reproducibility.en.md` | `dependency` | 삭제된 `dependency`가 관련 개념에 남음 | `standardization`, `model validation`, `execution order` 중 유지 표제로 정리 |
| `security.en.md` | `service operation` | 삭제된 `service-operation`이 관련 개념에 남음 | `permission`, `least privilege`, `accountability`, `privacy` 중심으로 정리 |
| `search.en.md` | `planning` | 삭제된 `planning`이 관련 개념에 남음 | `search space`, `heuristic`, `motion planning`처럼 유지 표제로 좁힘 |
| `decision-tree.en.md` | `tree` | 삭제된 `tree`가 관련 개념에 남음 | `threshold`, `overfitting`, `classification`, `regression` 중심으로 정리 |
| `heuristic.en.md` | `planning` | 삭제된 `planning`이 관련 개념에 남음 | `search`, `search space`, `computational limit` 중심으로 정리 |
| `function.en.md` | `expression` | 삭제된 `expression`이 관련 개념에 남음 | `variable`, `model`, `loss function`, `objective function` 중 문맥에 맞게 대체 |
| `vectorization.en.md` | `array` | 삭제된 `array`가 관련 개념에 남음 | `tensor`, `matrix`, `broadcasting`, `shape` 중 유지 표제로 대체하거나 제거 |
| `data-structure.en.md` | `array`, `graph`, `tree` | 삭제된 하위 구조명이 관련 개념에 남음 | 하위 설명으로 본문에만 두고 관련 개념은 `dataset`, `feature`, `vectorization` 등으로 재검토 |
| `model.en.md` | `AI application`, `orchestration` | 삭제된 제품·운영 구성 표현이 관련 개념에 남음 | `model input`, `model output`, `parameter`, `task definition` 중심으로 정리 |
| `model-context-protocol-mcp.en.md` | `external tool`, `orchestration`, `external resource`, `external system` | MCP 하위 구성요소와 운영어가 독립 표제처럼 남음 | `tool use`, `AI agent`, `trust boundary`, `permission` 중심으로 정리 |
| `retrieval-augmented-generation-rag.en.md` | `external resource` | 삭제된 `external-resource`가 관련 개념에 남음 | `retrieval`, `provenance`, `search index`, `supporting evidence`로 대체 |
| `variable.en.md` | `expression` | 삭제된 `expression`이 관련 개념에 남음 | `function`, `model input`, `value` 중 표제 유지 여부 확인 후 정리 |
| `ai-agent.en.md` | `external tool`, `orchestration`, `service operation` | 삭제된 외부 도구·오케스트레이션·서비스 운영 표현이 관련 개념에 남음 | `tool use`, `permission`, `human oversight`, `reinforcement learning agent` 중심으로 정리 |
| `retrieval-augmented-generation-rag.zh.md` | `external resource` | 중국어 관련 개념에 영어 삭제 표제명이 남음 | 중국어 유지 표제 기준으로 `检索`, `出处追踪`, `搜索索引`, `支持证据` 계열로 정리 |
| `function.zh.md` | `expression` | 삭제된 `expression`이 관련 개념에 남음 | `变量`, `模型`, `损失函数` 등 유지 표제 기준으로 정리 |
| `decision-tree.zh.md` | `树(tree)` | 삭제된 `tree` 표제가 중국어 관련 개념에 남음 | `阈值`, `过拟合`, `分类`, `回归` 중심으로 정리 |
| `variable.zh.md` | `program code` | 삭제된 `code` 계열 표현이 관련 개념에 남음 | `function`, `model input`, `value` 계열로 재검토 |
| `model.zh.md` | `AI 应用(AI application)`, `编排(orchestration)` | 삭제된 `ai-application`, `orchestration`이 관련 개념에 남음 | `模型输入`, `模型输出`, `参数`, `任务定义` 중심으로 정리 |
| `model-context-protocol-mcp.zh.md` | `编排`, `资源`, `服务器`, `客户端` | MCP 구성요소가 독립 표제처럼 나열됨 | 유지 표제인 `工具使用`, `AI 智能体`, `信任边界`, `权限` 계열로 좁힘 |
| `ai-agent.zh.md` | `编排`, `测试框架` | 운영·검토 형식 이름이 관련 개념에 남음 | `工具使用`, `权限`, `人工监督`, `强化学习智能体` 중심으로 정리 |
| `human-oversight.zh.md` | `测试框架`, `审批` | 검토·승인 절차명이 독립 관련 개념처럼 남음 | `安全性`, `问责`, `权限`, `模型验证` 중심으로 정리 |

## B. 표제 범위 재동기화 후보

한국어 항목은 최근 문맥 한정 표제로 좁혔지만, 영어·중국어 항목은 단독 일반어 제목을 유지하던 사례다. slug를 당장 바꾸기보다 제목과 첫 문장을 먼저 좁히는 쪽이 안전하므로, 2026-07-29에 확인 가능한 항목을 우선 반영했다.

| slug | 현재 한국어 표제 | 영어·중국어 상태 | 문제 | 권장 처리 |
| --- | --- | --- | --- | --- |
| `state` | 에이전트 상태(state) | `state`, `状态(state)` | 일반 상태, 실행 상태, 강화학습 상태가 다시 섞임 | 영어·중국어 제목과 첫 문장을 agent/RL context로 좁힘 |
| `event` | 확률 사건(event) | `event`, `事件` | 일반 사건과 확률 사건이 구분되지 않음 | `probability event`, `概率事件`처럼 확률 문맥 명시 |
| `visualization` | 데이터 시각화(visualization) | `visualization`, `可视化` | 도식·차트 제작 일반과 데이터 분석 시각화가 섞임 | `data visualization`, `数据可视化`로 좁힘 |
| `metadata` | 문서 검색 메타데이터(metadata) | `metadata` | 일반 부가정보 의미가 먼저 읽힘 | `search metadata` 또는 `document retrieval metadata`로 좁힘 |
| `permission` | 도구 실행 권한(permission) | `permission` | 일반 권한과 에이전트/도구 실행 권한이 섞임 | `tool execution permission`으로 좁힘 |
| `search` | 상태공간 탐색(search) | `search`, `search` | 정보 검색과 상태공간 탐색이 섞임 | `state-space search` 계열로 제목과 Related concepts 동기화 |
| `model-input` | 모델 입력 정의(model input) | 영어·중국어가 일반 `model input`으로 읽힐 가능성 | 단순 입력과 문제 정의의 입력 축이 섞일 수 있음 | 첫 문장에서 modeling contract/definition 문맥 명시 |
| `model-output` | 모델 출력 정의(model output) | 영어·중국어가 일반 `model output`으로 읽힐 가능성 | 단순 출력값과 문제 정의의 출력 축이 섞일 수 있음 | 첫 문장에서 task/output contract 문맥 명시 |
| `model-score` | 모델 후보 점수(model score) | `model score` | 일반 모델 점수, 평가 점수, 후보 점수가 섞임 | candidate score/ranking context를 제목이나 첫 문장에 반영 |
| `evaluation-design` | 모델 평가 설계(evaluation design) | `evaluation design` | 일반 평가 설계로 열림 | model evaluation design으로 좁힘 |
| `output-structure` | 모델링 출력 구조(output structure) | `output structure` | 일반 출력 형식으로 열림 | modeling output structure로 제목 동기화 |

## C. 표제 자체 재검토 결과

아래 항목은 한국어 표제도 가이드라인의 제외 조건과 충돌할 가능성이 있어 재검토한 사례다. 2026-07-29 기준으로는 단어별 원고를 삭제하지 않고, 표제와 첫 뜻 문장을 문맥 한정 표현으로 좁혀 유지한다.

| slug | 조정 후 한국어 표제 | 재판정 | 후속 처리 |
| --- | --- | --- | --- |
| `decision` | 업무 의사결정(decision) | 모델 점수와 실제 업무 행동을 분리하는 기준점으로 유지 | 영어 `business decision`, 중국어 `业务决策`로 추가 |
| `learning` | AI 학습(learning) | `learning`과 `training`을 구분하는 상위 기준점으로 유지 | 영어 `AI learning`, 중국어 `AI 学习`으로 추가 |
| `license` | 자료 라이선스(license) | 저작권·출처 표시·자료 사용 조건을 구분하는 법·운영 기준점으로 유지 | 영어 `material license`, 중국어 `资料许可`로 추가 |
| `retrieval` | RAG 검색(retrieval) | 일반 검색이 아니라 RAG 입력 근거 후보를 가져오는 단계로 유지 | 영어 `RAG retrieval`, 중국어 `RAG 检索`로 추가 |
| `topology` | 위상(topology) | 표준 수학 의미와 동일하게 유지하되 이 책에서는 표현 공간 구조를 읽는 짧은 안내로 제한 | 영어 `topology`, 중국어 `拓扑`으로 정리. 표현 공간은 표제가 아니라 적용 맥락으로만 둠 |
| `response-generation` | LLM 응답 생성(response generation) | LLM inference의 자연어 출력 생성 문맥으로 제한해 유지 | 영어 `LLM response generation`, 중국어 `LLM 响应生成`으로 추가 |
| `software-regression` | AI 서비스 소프트웨어 회귀(software regression) | 모델·프롬프트·설정 변경 뒤 기존 품질 저하를 설명하는 검증 기준점으로 유지 | 영어 `AI service software regression`, 중국어 `AI 服务软件回归`으로 추가 |
| `text-and-data-mining` | 학습 데이터 맥락의 텍스트·데이터 마이닝(text and data mining, TDM) | 학습 데이터와 저작권 논의의 법·정책 전문 용어로 유지 | 영어 `text and data mining in the training-data context`, 중국어 `学习数据语境下的文本与数据挖掘`으로 추가 |

## D. 다국어 항목 품질 점검 후보

아래 유형은 표제 자체보다 언어별 원고 운영 원칙과 연결된다. 통합 인덱스의 제목만으로는 완전 판정할 수 없으므로, 번역 정리 때 함께 점검한다.

| 유형 | 예시 | 문제 | 권장 처리 |
| --- | --- | --- | --- |
| 영어 파일에 한국어 본문이 남음 | `vector-space.en.md`, `probability.en.md` 등 | 영어판 개념사전은 영어 독자 기준으로 작성해야 한다는 규칙과 충돌 | 2026-07-29에 검색 기준 잔존 0건으로 정리. 이후 자연스러운 영문 품질은 별도 읽기 검토 |
| 중국어 관련 개념에 영어 일반어가 직접 남음 | `retrieval-augmented-generation-rag.zh.md`의 `external resource`, `provenance`, `search index` | 중국어판 관련 개념은 중국어 표제어 우선이라는 규칙과 충돌 | 2026-07-29에 검색 기준 잔존 0건으로 정리. 약어와 모델명은 중국어 설명어를 앞에 두고 영어를 괄호 병기 |
| Related concepts가 현재 개념사전 표제와 맞지 않음 | `review`, `trace`, `example`, `shape`, `value`, `type`, `client`, `server` 등 | 관련 개념이 표제 관리 제외 대상인지, 아직 미등재 표준 개념인지 불분명 | 2026-07-29에 영어·중국어 관련 개념 필드의 직접 잔존 표현을 유지 표제 중심으로 교체. 남은 표제 적합성은 C그룹과 함께 재판정 |

## E. 본문 개념사전 링크 앵커 경고 후보

한국어 Part 본문에서 `docs/reference/concept-glossary-parts/*.md`로 향하는 링크를 모아, 대상 자음별 색인이 실제로 include하는 단어별 원고의 앵커와 대조했다. 2026-07-29 기준으로 실제 앵커가 없는 한국어 본문 링크 후보는 351개였고, 즉시 수정 가능한 항목을 반영한 뒤 328개가 남았다.

### 2026-07-29에 정리한 항목

| 항목 | 처리 |
| --- | --- |
| `#glossary-sample` | Part 3에서는 `sample`이 `샘플 단위(sample unit)` 문맥으로 반복되므로 `sample-unit` 단어별 원고 3개 언어에 호환 앵커를 추가 |
| `#glossary-output-structure` | 한국어 Part 3 링크가 `11-chieut.md`를 가리키던 경로를 실제 include 위치인 `05-mieum.md`로 수정 |
| `#glossary-score` | 한국어 Part 3 링크가 `09-jieut.md`를 가리키던 경로를 실제 include 위치인 `05-mieum.md`로 수정 |
| `review-queue` | 운영 출력 구조 이름으로 판정해 새 표제를 만들지 않고 `output-structure` 링크로 흡수 |
| `comparison-report` | 문서 산출물 이름으로 판정해 새 표제를 만들지 않고 `output-structure` 링크로 흡수 |
| `comparison-table` | 표 형식 이름으로 판정해 새 표제를 만들지 않고 `output-structure` 링크로 흡수 |
| `summary-table` | 표 형식 이름으로 판정해 새 표제를 만들지 않고 `data-modeling` 링크로 흡수 |
| `training` | 일반어로 넓게 열리는 단독 링크를 기존 `model-training` 표제로 흡수 |
| `random-forest` | 표준 모델 계열로 판정해 한·영·중 단어별 원고와 공개 색인 include 추가 |
| `bootstrap` | 통계·앙상블 문맥의 표준 용어로 판정해 한·영·중 단어별 원고와 공개 색인 include 추가 |
| `oob-score` | Random Forest 하위 평가 용어로 판정해 한·영·중 단어별 원고와 공개 색인 include 추가 |
| `optimizer` | 표준 딥러닝 학습 용어로 판정해 한·영·중 단어별 원고와 공개 색인 include 추가 |

### 남은 고빈도 후보

2026-07-29 처리 뒤 위 9개 고빈도 후보는 본문 링크 기준으로 남기지 않는다. 이후 빌드 경고에서 다시 나타나면 새 표제 생성보다 1차 판정의 흡수 대상과 실제 단어별 원고 include 위치를 먼저 확인한다.

## 우선순위

1. A그룹을 먼저 정리한다. 이미 삭제한 표제명이 관련 개념에 남아 있어 관리 기준과 가장 직접적으로 충돌한다.
2. B그룹은 한국어 표제와 영어·중국어 표제의 범위를 맞춘다. slug 변경은 본문 링크 비용이 크므로 제목과 첫 문장 좁힘을 먼저 검토한다.
3. C그룹은 한국어 표제를 문맥 한정으로 좁혀 유지했다. 후속 번역을 만들 때 같은 범위를 다시 넓히지 않는다.
4. D그룹은 검색 기준 직접 이탈 표현을 정리했으므로, 다음 단계에서는 제목과 본문 문장의 자연스러운 번역 품질을 읽기 검토로 확인한다.

## 후속 작업 체크리스트

1. `topology`는 표준 수학 용어로 표제를 유지한다. 다만 원고에서는 위치나 거리의 동의어처럼 쓰지 않고, 표현 공간의 연결성·연속성 같은 구조를 가리키는 제한된 맥락에서만 사용한다.
2. 바꾼 관련 개념이 실제 단어별 원고로 존재하는지 `management/concept-glossary-integrated-index.md`에서 확인한다.
3. 영어·중국어 항목을 수정할 때 한국어 원문의 `Section ID`와 `Version`을 임의로 바꾸지 않는다.
4. 본문 Section을 같이 고치지 않는 한 Section 릴리즈노트는 만들지 않는다.
