# 개념사전 표제 정리와 원고 직접수정 계획

작성일: 2026-07-29

## 목적

Part 1~7 한국어 원고와 개념사전 통합 인덱스를 기준으로, 개념사전 표제로 계속 관리할 표현과 본문 설명 또는 상위 표제 안으로 흡수할 표현을 분리한다. 이어서 그 판정 결과를 `docs/parts/` 원고의 개념사전 링크와 문맥 문장에 직접 반영한다.

이 문서는 기존 표제 검토 리포트와 앵커 경고 실행 리포트를 흡수한 단일 관리 문서다. 새 개념사전 표제를 늘리는 것이 목적이 아니라, 깨진 앵커와 과잉 표제 링크를 줄이고 표준 개념·문맥 한정 개념·하위 설명·작업 형식 이름을 일관되게 연결하는 것이 목적이다.

## 기준 문서

- 통합 인덱스: `management/concept-glossary-integrated-index.md`
- 단어별 원고: `docs/reference/concept-glossary-terms/`
- 개념사전 작성 규칙: `management/guidelines/concept-glossary-guidelines.md`
- 원고 작성 절차: `management/guidelines/manuscript-writing-workflow.md`

## 검토 범위

- 기준 원고: `docs/parts/part-01/`부터 `docs/parts/part-07/`까지의 한국어 원고
- Section 파일 수: 364개
  - Part 1: 57개
  - Part 2: 63개
  - Part 3: 52개
  - Part 4: 59개
  - Part 5: 53개
  - Part 6: 54개
  - Part 7: 26개
- Part 시작/마무리 페이지까지 포함하면 378개
- 본문 링크 수정 대상: `docs/parts/**/*.md`, `docs/parts/**/*.en.md`, `docs/parts/**/*.zh.md`
- 제외 대상: `site/` 빌드 산출물, 배포 nav 연결

## 판정 기준

표제어는 다음 조건을 모두 만족할 때만 유지하거나 새로 세운다.

| 조건 | 질문 |
| --- | --- |
| 표준성 | 학술·기술 문맥에서 안정적으로 정의되는 용어인가 |
| 독립성 | 상위 표제의 하위 설명으로 흡수하면 의미 혼선이 생기는가 |
| 지속성 | 특정 예제, 도구 사용법, 원고 작업 절차가 아니라 후속 Part에서도 반복되는 개념 기준점인가 |
| 범위 안정성 | 한국어 표제, 영어 기준 용어, slug가 같은 의미 범위를 가리키는가 |

다음 표현은 표제로 세우지 않는다.

| 유형 | 예시 | 처리 |
| --- | --- | --- |
| 일반어가 우세한 단어 | 평가, 검토, 질의, 환경, 상태, 행동, 계획, 경로 | 단독 표제 금지. 필요한 경우 문맥 한정 표제로 재검토 |
| 문서·작업 형식 이름 | 테이블, 로그, 테스트, 패키지, 브랜치, 서버, 작업흐름 | 표제 제외. 본문 설명이나 상위 표제로 흡수 |
| 코드 예제 설명에 묶인 구현 단위 | 배열, 트리, 커널, 실행 환경, 의존성 | 표준 개념 여부와 본문 역할을 분리해 판정 |
| 상위 개념의 구성요소 이름 | 외부 리소스, 외부 도구, 외부 시스템 | `MCP`, `도구 사용`, `RAG` 같은 상위 표제로 흡수 |

단, 일반어가 표준 개념의 일부로 좁혀진 경우에는 단독 표제가 아니라 문맥 한정 표제로만 검토한다. 예를 들어 `환경`은 제외하지만 `강화학습 환경(reinforcement learning environment)`은 강화학습 문제 정의의 표준 구성요소이므로 유지할 수 있다.

## 표제 1차 판정 요약

| 분류 | 처리 상태 | 원칙 |
| --- | --- | --- |
| 삭제 후보 | 2026-07-29에 단어별 원고와 언어별 공개 색인 include 제거 완료 | 다시 필요해 보여도 즉시 재생성하지 않고 신규 표제 검토 큐에서 재판정 |
| 상위 표제 흡수 후보 | 일부 삭제, 일부 문맥 한정 표제로 좁힘 완료 | 본문 링크가 있는 항목은 slug와 앵커를 유지하고 표제·정의 범위를 먼저 좁힘 |
| 유지 후보 | 문맥 한정 유지 | 단독 일반어로 다시 넓어지지 않게 제목과 첫 문장에 범위를 명시 |
| 새 표제 제외 표현 | 금지 예시로 유지 | 예시 목록은 고정 금지어가 아니라 역할 판정 빠른 참조로 사용 |

## 삭제 완료 표제

아래 항목은 Part 1~7 원고에서 표준 개념 기준점보다 작업·형식·도구 설명 또는 하위 설명 성격이 강해 단어별 원고와 공개 색인 include를 제거했다.

| slug | 기존 표제 | 대표 위치 | 판정 근거 |
| --- | --- | --- | --- |
| `code` | 프로그램 코드(program code) | `P2-1.2` | Python 예제를 설명하는 매체로 쓰이며 별도 AI 개념 기준점으로 반복되지 않음 |
| `runtime` | 실행 환경(runtime) | `P2-7.1` | Python 학습 환경 관리어에 가까움 |
| `dependency` | 의존성(dependency) | `P2-7.5` | 패키지·환경 재현 설명에 묶인 구현 관리어 |
| `version-control` | 버전 관리(version control) | `P2-14.1` | Git 학습을 위한 도구 운용 개념 |
| `document-reproducibility` | 문서 재현성(document reproducibility) | `P2-14.2` | 문서 제작 절차에 가까우며 `reproducibility` 아래에서 설명 가능 |
| `calculation-language` | 계산 언어(calculation language) | `P2-1.1` | 수학을 읽는 비유적 설명 축 |
| `notation` | 압축 표기(notation) | `P2-1.1` | 수식 읽기 보조 설명 |
| `expression` | 식(expression) | `P2-2.1` | 수학 기초 설명의 하위 요소 |
| `service-operation` | 서비스 운영(service operation) | `P1-14.6` | 운영 일반어 성격이 강함 |
| `business-outcome` | 업무 성과(business outcome) | `P1-4.4` | 문제 정의 바깥 결과 설명에 가까움 |
| `orchestration` | 오케스트레이션(orchestration) | `P1-14.1` | `AI 에이전트`, `도구 사용`, `MCP` 하위 설명이 적합 |
| `external-resource` | 외부 리소스(external resource) | `P1-14.4` | MCP 구성요소 이름에 가까움 |
| `external-tool` | 외부 도구(external tool) | `P1-14.1` | `에이전트 도구 사용(tool use)`의 하위 구성요소 |
| `external-system` | 외부 시스템(external system) | `P1-14.2` | 일반 시스템 용어가 우세함 |
| `ai-application` | AI 앱(application) | `P1-14.1` | 제품·구성요소 명칭에 가까움 |
| `array` | 배열(array) | `P2` | NumPy와 자료구조 기초 설명의 하위 요소 |
| `tree` | 트리(tree) | `P2`, `P4` | 자료구조 트리와 결정트리가 섞임 |
| `graph` | 그래프(graph) | `P1`, `P2` | 그래프 이론·자료구조·시각화 그래프가 섞임 |
| `route` | 경로(route, path) | `P1`, `P2` | 파일 경로, 학습 경로, 탐색 경로가 섞임 |
| `planning` | 계획(planning) | `P1-7.4` | 일반 계획과 AI planning이 분리되지 않음 |

## 문맥 한정 표제로 유지

아래 항목은 단독 일반어로 두면 범위가 넓어지지만, 원고 전체에서 반복되는 기준점 역할이 있어 문맥 한정 표제로 유지한다.

| slug | 유지 표제 | 유지 조건 |
| --- | --- | --- |
| `kernel` | SVM 커널(kernel) | P2 노트북 커널과 P4 SVM 커널을 구분한다 |
| `search` | 상태공간 탐색(search) | 정보 검색과 상태공간 탐색을 분리한다 |
| `state` | 에이전트 상태(state) | 일반 상태가 아니라 강화학습·에이전트 실행 문맥으로 좁힌다 |
| `action` | 에이전트 행동(action) | 단독 `행동` 표제는 만들지 않는다 |
| `event` | 확률 사건(event) | 일반 사건과 확률 사건을 분리한다 |
| `visualization` | 데이터 시각화(visualization) | 일반 도식 제작과 데이터 분석 시각화를 분리한다 |
| `metadata` | 문서 검색 메타데이터(metadata) | 검색·출처 관리 문맥으로 좁힌다 |
| `permission` | 도구 실행 권한(permission) | 일반 권한이 아니라 에이전트·도구 실행 권한으로 좁힌다 |
| `output-structure` | 모델링 출력 구조(output structure) | 일반 출력 형식이 아니라 모델링 결과의 그릇을 정하는 개념으로 둔다 |
| `model-input` | 모델 입력 정의(model input) | 일반 입력 단독 표제는 만들지 않는다 |
| `model-output` | 모델 출력 정의(model output) | 일반 출력 단독 표제는 만들지 않는다 |
| `model-score` | 모델 후보 점수(model score) | 평가 점수 일반이 아니라 후보 비교 수치로 좁힌다 |
| `evaluation-design` | 모델 평가 설계(evaluation design) | 단독 평가가 아니라 모델 평가 설계로 둔다 |
| `accountability` | AI 책임성(accountability) | 단독 `책임` 표제와 묶음 표제는 만들지 않는다 |
| `safety` | AI 시스템 안전성(safety) | 단독 `안전`은 제외하고 AI 시스템 피해 경로와 제한 조건으로 설명한다 |
| `guardrail` | AI 가드레일(guardrail) | 정책·실행 제약 문맥을 제목과 첫 문장에서 드러낸다 |
| `tool-use` | 에이전트 도구 사용(tool use) | 외부 도구·외부 리소스·외부 시스템은 이 항목 안으로 흡수한다 |
| `data-structure` | 자료구조 선택(data structure) | Part 2 기초 복구의 기준점으로만 관리한다 |
| `reinforcement-learning-environment` | 강화학습 환경(reinforcement learning environment) | 일반 실행 환경과 구분한다 |
| `human-oversight` | 인간 감독(human oversight) | 단순 사람 검토가 아니라 중단·수정·반려 권한이 있는 감독 구조로 설명한다 |
| `model-context-protocol-mcp` | 모델 컨텍스트 프로토콜(Model Context Protocol, MCP) | 하위 구성요소인 서버·리소스·도구를 각각 독립 표제로 늘리지 않는다 |
| `decision` | 업무 의사결정(decision) | 모델 점수와 실제 업무 행동을 분리하는 기준점으로 유지 |
| `learning` | AI 학습(learning) | `learning`과 `training`을 구분하는 상위 기준점으로 유지 |
| `license` | 자료 라이선스(license) | 저작권·출처 표시·자료 사용 조건을 구분하는 법·운영 기준점으로 유지 |
| `retrieval` | RAG 검색(retrieval) | RAG 입력 근거 후보를 가져오는 단계로 유지 |
| `topology` | 위상(topology) | 표준 수학 용어로 유지하되 표현 공간의 연결성·연속성 같은 구조 문맥에서 사용 |
| `response-generation` | LLM 응답 생성(response generation) | LLM inference의 자연어 출력 생성 문맥으로 유지 |
| `software-regression` | AI 서비스 소프트웨어 회귀(software regression) | 모델·프롬프트·설정 변경 뒤 기존 품질 저하를 설명하는 검증 기준점으로 유지 |
| `text-and-data-mining` | 학습 데이터 맥락의 텍스트·데이터 마이닝(text and data mining, TDM) | 학습 데이터와 저작권 논의의 법·정책 전문 용어로 유지 |

## 새 표제로 만들지 않을 표현

Part 1~7 원고에서 반복되더라도 현재 기준으로는 새 표제를 만들지 않는다.

| 표현 | 원고상 역할 | 처리 |
| --- | --- | --- |
| 브랜치(branch) | Git 사용과 문서 재현성 설명 | 표제 제외 |
| 테이블(table) | 표 데이터, Markdown 표, 자료구조 예시가 섞임 | `자료구조` 또는 `데이터셋` 안에서 설명 |
| 패키지(package) | Python 환경 관리 | 표제 제외 |
| 테스트(test) | 평가 데이터, 코드 테스트, 배포 확인이 섞임 | 단독 표제 금지. 필요하면 `테스트 데이터`만 유지 |
| 로그(log) | 수학 로그와 실행 로그가 섞임 | 단독 표제 금지. 수학은 `logarithm`, 실행 기록은 본문 설명 |
| 서버(server) | MCP 서버, 웹 서버, 원격 서버가 섞임 | MCP 구성요소 설명으로만 처리 |
| 수식(formula) | 수학 설명 형식 | `함수`, `손실 함수`, `목적 함수` 같은 실제 개념으로 연결 |
| 평가(evaluation) | 일반 검토/시험/모델 평가가 섞임 | 단독 표제 금지. `평가 지표`, `모델 평가 설계`, `모델 검증`처럼 좁힌 표제만 허용 |
| 검토(review) | 사람 검토, 원고 검토, 모델 결과 검토가 섞임 | 표제 제외. `인간 감독`이나 본문 절차로 처리 |
| 질의(query) | 검색 입력, 사용자 질문, DB 질의가 섞임 | 필요 시 `검색 질의`처럼 문맥 한정 후 재검토 |
| 환경(environment) | 실행 환경, 강화학습 환경, 배포 환경이 섞임 | 단독 표제 금지. `강화학습 환경`만 유지 가능 |
| 작업흐름(workflow) | 에이전트 설명과 원고·운영 절차가 섞임 | `AI 에이전트`, `도구 사용` 안에서 설명 |
| 사람 검토 | 검토 절차 | 표제 제외. `인간 감독`과 구분해 본문 절차로만 설명 |
| 권리와 책임 | 여러 법·윤리 항목 묶음 | `저작권`, `개인정보`, `책임성` 등으로 분해 |

## 처리 기록

| 그룹 | 범위 | 2026-07-29 상태 | 다음 처리 |
| --- | --- | --- | --- |
| A | 삭제·제외 표제명이 관련 개념에 남은 경우 | 완료 | 새 잔존 표현이 생기면 유지 표제 기준으로 교체 |
| B | 영어·중국어 표제가 한국어 문맥 한정 표제보다 넓어진 경우 | 완료 | slug 변경은 보류하고 제목·첫 문장 동기화 원칙 유지 |
| C | 표제 자체 재검토 대상 | 완료 | 8개 항목은 삭제하지 않고 문맥 한정 표제로 유지 |
| D | 다국어 항목 품질 점검 | 1차 검색 정리 완료 | 제목·본문 전체의 자연스러운 번역 품질은 별도 읽기 검토 |
| 단어별 원고 slug 앵커 | 기존 표제 파일의 파일명 기준 명시 앵커 누락 | 52개 파일에 `<a id="slug"></a>` 보강 완료 | 새 단어별 원고를 만들 때 파일명 slug 앵커를 함께 확인 |
| Part 4 모델 옵션·하위 방법 링크 | `#feature-space`, `#cluster-label`, `#hierarchical-clustering`, `#spectral-clustering`, `#connectivity`, `#extra-trees`, `#max-features`, `#n-estimators`, `#permutation-importance`, `#correlated-features`, `#log-odds`, `#multinomial-logistic-regression`, `#latency`, `#dqn`, `#policy-gradient`, `#policy-gradient-theorem`, `#reinforce`, `#actor-critic`, `#one-vs-rest`, `#argmax`, `#dropout`, `#support-vector` | `vector-space`, `cluster`, `clustering`, `hyperparameter`, `logistic-regression`, `softmax`, `value-based-reinforcement-learning`, `policy-based-reinforcement-learning`, `regularization`, `support-vector-machine` 기준으로 흡수하거나 본문 설명으로 전환 완료 | `connectivity`는 `topology`와 동일 의미로 간주하지 않고 그래프 연결 구조 문맥의 본문 설명으로 유지 |
| Part 5 세부 함수·상태 링크 | `#relu`, `#tanh`, `#dropout`, `#training-mode`, `#evaluation-mode`, `#batch`, `#batch-normalization`, `#initialization` | `activation-function`, `regularization`, `model-training`, `model-validation`, `numerical-stability`, `tensor` 기준으로 흡수 완료 | 개별 세부 표제가 계속 필요해 보이면 신규 표제 검토 큐에서 독립성 재판정 |
| E | 본문 개념사전 링크 앵커 경고 후보 | 진행 중 | 남은 앵커 경고는 빈도순으로 1차 판정 후 흡수·추가·보류 결정 |

대표 처리 내역:

| 항목 | 처리 |
| --- | --- |
| 삭제·제외 표제의 관련 개념 잔존 | `external resource`, `external tool`, `external system`, `orchestration`, `service operation`, `dependency`, `planning`, `expression`, `tree`, `array` 등을 유지 표제 중심으로 교체 |
| 영어 파일의 한국어 본문 잔존 | 검색 기준 잔존 0건으로 정리 |
| 중국어 관련 개념의 영어-only 표현 | 중국어 표제어 우선 표기로 정리 |
| 영어·중국어 Related concepts 직접 이탈 표현 | 유지 표제 중심으로 교체 |
| `#glossary-sample` | `sample-unit` 단어별 원고 3개 언어에 호환 앵커 추가 |
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
| `data-modeling` 중국어 링크 | 실제 include 위치인 `d.zh.md`로 수정 |
| `generalization` 중국어 링크 | 실제 include 위치인 `f.zh.md`로 수정 |
| `activation-function` 중국어 링크 | 실제 include 위치인 `j.zh.md`로 수정 |
| `#glossary-row` | 하위 설명으로 판정해 문맥별 `sample-unit` 링크로 흡수 |
| `#glossary-dataset-candidate` | 하위 설명으로 판정해 `dataset` 링크로 흡수 |
| `#feature-scale` | 하위 설명으로 판정해 `standardization` 링크로 흡수 |
| `#feature-importance` | 하위 설명으로 판정해 `random-forest` 링크로 흡수 |
| `#error-case` | 작업·분석 산출물로 판정해 `model-validation` 링크로 흡수 |
| `#glossary-evaluation` | 일반어 우세로 판정해 `evaluation-design` 링크로 흡수 |
| `#validation` | 일반어 우세로 판정해 문맥별 `model-validation`, `validation-data`, `test-data` 링크로 분해 |
| `#glossary-evidence-strength` | 문맥 한정 후보로 판정해 `interpretation-boundary` 링크로 흡수 |
| `#glossary-policy-rule` | 문맥 한정 후보로 판정해 `decision` 링크로 흡수 |
| `#glossary-problem-representation-structure` | 문맥 한정 후보로 판정해 `data-modeling`, `task-definition` 링크로 분해 |
| `support-vector-machine` | 표준 모델 계열로 판정해 한·영·중 단어별 원고와 공개 색인 include 추가 |
| `k-means` | 표준 군집화 방법으로 판정해 한·영·중 단어별 원고와 공개 색인 include 추가 |
| `dbscan` | `k-means`와 같은 Section의 표준 군집화 방법 링크로 확인되어 한·영·중 단어별 원고와 공개 색인 include 추가 |
| Part 2 작업·형식 표제 링크 | `formula`, `notebook`, `dataframe`, `plot`, `line-plot`, `legend`, `value`, `list`, `dictionary`, `loop`, `class`, `branch`, `indexing` 링크를 제거하고 대표 Section 참조로 전환 |

## 원고 직접수정 원칙

1. 한 Section 안에서 같은 개념사전 링크는 기본적으로 1회만 둔다.
2. 작업·형식 이름은 새 표제를 만들지 않고 기존 상위 표제로 흡수한다.
3. 하위 설명은 독립 링크보다 현재 문단의 상위 개념 링크로 연결한다.
4. 표준 모델·방법 계열은 기존 상위 표제와 본문 대표 설명으로 충분한지 먼저 확인한다.
5. 언어별 본문 링크는 같은 언어의 개념사전 색인을 우선 가리킨다.
6. 링크만 바꿔도 문장이 어색해지는 경우에는 주변 문장을 함께 고친다.
7. 본문 Section의 개념 설명 자체가 바뀌는 경우에만 Section 메타데이터와 릴리즈노트 필요 여부를 확인한다.

## 작업 우선순위

### 1차: 경로 오류와 이미 유지 표제가 있는 링크

실제 단어별 원고와 언어별 색인 include가 있는데 본문 링크가 잘못된 경우를 먼저 고친다. 이 작업은 개념 판정보다 기계적 오류에 가깝고, 새 표제를 만들 필요가 없다.

| 후보 | 처리 |
| --- | --- |
| 언어별 색인 경로 오류 | 실제 include 위치로 링크 변경 |
| 기존 표제의 호환 앵커 누락 | 단어별 원고에 호환 앵커를 추가할지, 본문 링크를 대표 앵커로 바꿀지 선택 |
| 같은 Section의 중복 링크 | 첫 등장 링크만 남기고 반복 링크 제거 |

### 2차: 하위 설명 또는 작업·형식 이름 흡수

아래 후보는 새 표제를 만들기보다 본문 링크를 상위 표제로 바꾸는 것을 기본값으로 둔다.

| 후보 앵커 | 건수 | 1차 판정 | 우선 연결 대상 |
| --- | ---: | --- | --- |
| `#glossary-row` | 12 | 하위 설명 | `sample-unit`, `data-modeling`, `data-structure` |
| `#glossary-dataset-candidate` | 9 | 하위 설명 | `dataset`, `data-modeling` |
| `#feature-scale` | 9 | 하위 설명 | `standardization`, `feature`, `distance` |
| `#feature-importance` | 9 | 하위 설명 | `random-forest` |
| `#error-case` | 9 | 작업·분석 산출물 | `model-validation`, `error-cost`, `evaluation-design` |
| `#glossary-evaluation` | 9 | 일반어 우세 | `evaluation-design`, `metric`, `evaluation-data` |

### 3차: 문맥 한정 개념 후보

아래 후보는 원고 문맥을 읽고 상위 표제로 흡수할지, 문맥 한정 표제로 유지할지 결정한다. 새 항목 생성은 보류가 기본값이다.

| 후보 앵커 | 건수 | 1차 판정 | 우선 검토 |
| --- | ---: | --- | --- |
| `#glossary-evidence-strength` | 12 | 문맥 한정 개념 후보 | `interpretation-boundary`, `evaluation-design` 흡수 가능성 |
| `#glossary-policy-rule` | 9 | 문맥 한정 개념 후보 | `decision`, `model-output`, `AI agent` 문맥 분리 |
| `#glossary-problem-representation-structure` | 9 | 문맥 한정 개념 후보 | `task-definition`, `data-modeling`, `output-structure` 흡수 가능성 |
| `#validation` | 9 | 일반어 우세 | `model-validation`, `validation-data`, `evaluation-design`로 분해 |

### 4차: 표준 모델 계열 보류 검토

아래 후보는 표준 용어이지만, 현재 원고에서 독립 표제 기준점이 필요한지 확인한 뒤 처리한다.

| 후보 앵커 | 건수 | 1차 판정 | 우선 검토 |
| --- | ---: | --- | --- |
| `#support-vector-machine` | 9 | 표준 모델 계열 | 독립 표제 유지. 한·영·중 단어별 원고와 공개 색인 include 추가 완료 |
| `#k-means` | 7 | 표준 모델 계열 | 독립 표제 유지. 한·영·중 단어별 원고와 공개 색인 include 추가 완료 |

## 작업 절차

1. 남은 앵커 후보를 빈도순으로 묶고, 각 후보의 실제 등장 파일을 추출한다.
2. 후보별로 대표 Section 1개와 반복 Section을 분리한다.
3. 대표 Section에서는 링크 대상 변경이 문장 의미를 바꾸는지 읽어 본다.
4. 반복 Section에서는 링크만 상위 표제로 교체할 수 있는지 먼저 확인한다.
5. 링크 대상이 언어별로 다르면 한국어, 영어, 중국어를 같은 의미 범위로 맞춘다.
6. 본문 링크를 수정한 뒤 같은 후보 앵커가 남았는지 검색한다.
7. 새 단어별 원고를 만들었거나 표제명을 바꿨다면 `management/concept-glossary-integrated-index.md`를 갱신한다.
8. 빌드는 배포 준비 또는 배포 지시가 있을 때만 `.venv/bin/python -m mkdocs build`로 실행한다. 평상시 검증은 `rg`와 정적 링크 후보 추출로 제한한다.

## 신규 표제 검토 큐

새로운 개념사전 표제가 필요해 보일 때는 단어별 파일을 바로 만들지 않고 이 큐에 먼저 추가한다.

후보는 `보류`를 기본값으로 둔다. 등재 조건을 모두 통과하고 기존 상위 표제로 흡수하기 어렵다는 근거가 확인된 뒤에만 개념사전 항목 생성으로 넘긴다.

| 후보 표제 | 영어 기준 용어 | 제안 Section | 역할 분류 | 기존 상위 표제/관련 표제 | 1차 판정 | 필요한 확인 |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  | 보류 | 표준성, 독립성, 지속성, slug 안정성 확인 |

## 신규 표제 검토 절차

1. 후보가 나온 Section ID와 문맥을 먼저 적는다.
2. 후보 표현을 `표준 개념`, `문맥 한정 개념`, `하위 설명`, `작업·형식 이름`, `구현·도구·사례`, `임시 표현` 중 하나로 분류한다.
3. 기존 개념사전 단어별 원고와 공개 색인에서 같은 의미를 이미 다루는 표제가 있는지 확인한다.
4. 기존 상위 표제의 하위 설명으로 충분하면 새 항목을 만들지 않는다.
5. 일반어가 전문 문맥에서 좁혀진 경우에는 단독 표제 대신 문맥 한정 표제명을 적는다.
6. 영어 기준 용어와 slug가 같은 범위를 안정적으로 가리키는지 확인한다.
7. 등재 조건을 모두 통과한 후보만 개념사전 단어별 원고 생성 대상으로 넘긴다.

## 남은 작업

1. 다음 저빈도 다국어 앵커 후보를 이 문서의 우선순위대로 계속 처리한다.
2. 기존 표제가 있는 항목은 먼저 언어별 색인 경로 오류인지 확인한다.
3. 파일이 없는 후보는 `표준 개념`, `문맥 한정 개념`, `하위 설명`, `작업·형식 이름`, `구현·도구·사례`, `임시 표현` 중 하나로 1차 판정한다.
4. 작업·형식 이름과 하위 설명은 새 표제를 만들지 않고 기존 상위 표제로 흡수한다.
5. 표준 개념은 기존 단어별 원고가 있는지 먼저 확인하고, 없을 때만 한·영·중 항목과 공개 색인 include 추가를 검토한다.
6. D그룹은 검색 기준 정리 뒤에도 제목과 본문이 각 언어 독자에게 자연스러운지 별도 읽기 검토로 확인한다.
7. 변경 뒤에는 `management/concept-glossary-integrated-index.md`를 다시 맞추고, 배포 전 빌드에서 새 앵커 문제가 생겼는지 확인한다.

## 운영 원칙

- `topology`는 표준 수학 용어로 표제를 유지한다. 위치나 거리의 동의어처럼 쓰지 않고, 표현 공간의 연결성·연속성 같은 구조를 가리키는 제한된 맥락에서만 사용한다.
- 영어·중국어 항목을 수정할 때 한국어 원문의 `Section ID`와 `Version`을 임의로 바꾸지 않는다.
- 본문 Section을 같이 고치지 않는 한 Section 릴리즈노트는 만들지 않는다.
- `site/` 빌드 산출물은 이 계획과 함께 커밋하지 않는다.

## 검증 명령

```bash
rg -n '#glossary-row|#glossary-evidence-strength|#validation\\)|#error-case|#feature-scale|#feature-importance|#glossary-policy-rule|#glossary-evaluation|#glossary-dataset-candidate|#glossary-problem-representation-structure' docs/parts
```

표준 표제로 유지한 모델·방법 계열은 본문 링크와 단어별 원고가 함께 존재하는지 확인한다.

```bash
rg -n '#support-vector-machine|#k-means|#dbscan' docs/parts docs/reference/concept-glossary-terms docs/reference/concept-glossary-parts docs/reference/concept-glossary-alpha docs/reference/concept-glossary-pinyin
```

배포 준비 또는 배포 지시가 있을 때만 다음 명령으로 최종 빌드를 확인한다.

```bash
.venv/bin/python -m mkdocs build
```

`--strict` 빌드는 git revision date 플러그인의 미커밋 파일 경고 때문에 실패할 수 있다. strict 결과를 볼 때는 앵커 경고와 git 히스토리 경고를 분리해서 보고한다.

## 완료 기준

- 우선순위 표의 후보마다 `흡수`, `기존 표제 연결`, `신규 표제 보류`, `신규 표제 생성` 중 하나의 처리 결과가 남아 있다.
- 처리한 후보 앵커가 `docs/parts/` 본문 링크에서 다시 검색되지 않는다.
- 새 표제를 만든 경우 한·영·중 단어별 원고, 공개 색인 include, 통합 인덱스가 모두 맞는다.
- 배포 준비 또는 배포 지시 시점의 일반 빌드가 성공한다.
- 남은 경고는 다음 작업 큐에 이유와 함께 남긴다.
