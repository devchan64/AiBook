# 7.2 근거 검토 메모

이 문서는 `docs/chapters/chapter-07/section-02.md`의 근거 연결과 표현 판단을 기록한 관리 메모입니다.

## 작성 목적

- 7.1의 탐색 공간(search space)과 계산 한계(computational limit) 설명에서 휴리스틱(heuristic)으로 자연스럽게 넘어갑니다.
- 사용자의 “휴리스틱은 불확실성과 계산 한계를 소프트웨어에 반영한 시도”라는 직관 중, 7.2에서는 계산 한계 속에서 후보를 줄이는 기준에 집중합니다.
- 휴리스틱을 정답, 확률 모델, 학습 모델과 혼동하지 않도록 경계를 세웁니다.

## 사용 근거

| 자료 | 로컬 확인 | 반영 내용 |
| --- | --- | --- |
| Douglas Harper, Online Etymology Dictionary, `heuristic` | `.tmp/section-7-2-evidence-etymology/etymonline-heuristic.html` | `heuristic`이 그리스어 `heuriskein`의 “찾다, 알아내다, 발견하다” 의미와 연결된다는 어원 설명 |
| Merriam-Webster, `heuristic` | 웹 확인 및 `.tmp/section-7-2-evidence-etymology/merriam-webster-heuristic.html` 다운로드 시도 | 웹에서는 Greek `heuriskein`과 discovery/problem-solving 의미를 확인. 로컬 파일은 Cloudflare challenge 응답이라 본문 직접 근거로는 사용하지 않음 |
| ACM A.M. Turing Award, `Allen Newell` | 웹 확인 및 `.tmp/section-7-2-evidence-etymology/acm-newell.html` 다운로드 시도 | Newell이 Pólya의 heuristic problem-solving 영향을 받았고, 인간은 완전한 알고리즘으로 모든 문제를 풀 시간이나 처리 능력이 없어 단순화된 규칙으로 selective search를 수행한다는 설명 |
| ACM A.M. Turing Award, `Herbert A. Simon` | 웹 확인 및 `.tmp/section-7-2-evidence-etymology/acm-simon.html` 다운로드 시도 | Simon이 heuristic programming을 옹호했고, 사람은 모든 정보와 시간을 갖지 못하므로 최적 결과보다 만족할 만한 결과를 받아들이는 휴리스틱을 쓴다는 설명 |
| Nobel Prize, `Herbert Simon - Facts` | `.tmp/section-7-2-evidence-etymology/nobel-simon-facts.html` | Simon이 완전한 합리성을 가정한 경제 이론과 달리 실제 선택이 엄격한 합리성에서 벗어난다고 보았다는 배경 설명 |
| Poole & Mackworth, Section 3.1 `Problem Solving as Search` | `.tmp/section-2-2-evidence/poole-mackworth-ch3-s1-search-problem.html` | 사람은 항상 최적해가 아니라 satisficing 또는 good enough solution을 찾을 수 있음, search space 바깥의 추가 지식을 heuristic knowledge라고 부름 |
| AIMA 4th US ed. table of contents | `.tmp/section-2-2-evidence/aima-contents.html` | `Informed (Heuristic) Search Strategies`, `Heuristic Functions`, `Satisficing search`, `Learning heuristics from experience`가 AI 문제 해결의 정식 항목으로 배치됨 |
| Google for Developers, `Machine Learning Glossary` | `.tmp/section-2-1-labeling-evidence/google-ml-glossary.html` | classification threshold가 사람이 선택하는 값이며 false positive/false negative 수에 영향을 준다는 설명, hyperparameter 용어 확인 |
| Google DeepMind, `FunSearch` | `.tmp/section-7-1-evidence-modern/deepmind-funsearch.html`, `.tmp/section-7-1-evidence-modern/deepmind-funsearch.html.txt` | LLM이 만든 프로그램 후보를 자동 평가하고 높은 점수의 후보를 다음 탐색에 사용한다는 설명, bin packing에서 기존 heuristic과 비교한 현대 사례 |
| `management/authoring/heuristics-and-ai-thinking.md` | 저장소 관리 문서 | 휴리스틱을 탐색, 판단, 모델링의 경험적 기준으로 설명하고, 확률 모델과 구분하는 내부 기준 |
| `management/authoring/section-7-1-evidence-analysis.md` | 저장소 관리 문서 | 7.1과 7.2의 도메인 경계, 탐색 공간에서 휴리스틱으로 넘어가는 연결 |

## 확인한 원문 위치

- `.tmp/section-7-2-evidence-etymology/etymonline-heuristic.html`
  - 메타 설명과 본문 데이터에 `heuristic`이 “serving to discover or find out” 의미와 연결된다는 설명 확인
  - `Greek heuriskein`과 “to find; find out, discover” 의미 확인
  - `eureka`가 `heuriskein`의 “to find”와 연결된다는 설명 확인
- `.tmp/section-7-2-evidence-etymology/merriam-webster-heuristic.html`
  - 다운로드는 성공했으나 Cloudflare challenge HTML만 저장됨
  - 웹 확인에서는 Greek `heuriskein`과 discovery/problem-solving 의미를 확인했지만, 로컬 원문 확인이 제한되어 본문 출처에는 Etymonline을 우선 사용
- `.tmp/section-7-2-evidence-etymology/acm-newell.html`
  - 다운로드는 성공했으나 Cloudflare block HTML만 저장됨
  - 웹 확인에서는 Newell 소개의 Pólya 영향, heuristic problem-solving, simplified rules, selective searches 설명을 확인
- `.tmp/section-7-2-evidence-etymology/acm-simon.html`
  - 다운로드는 성공했으나 Cloudflare block HTML만 저장됨
  - 웹 확인에서는 Simon 소개의 heuristic programming, 제한된 정보와 시간, satisfactory rather than optimal results, Logic Theorist와 GPS 설명을 확인
- `.tmp/section-7-2-evidence-etymology/nobel-simon-facts.html`
  - Simon의 수상 동기와 작업 배경 확인
  - 기존 경제학의 완전 합리성 가정과 달리 실제 선택이 엄격한 합리성에서 벗어난다는 설명 확인
- `.tmp/section-2-2-evidence/poole-mackworth-ch3-s1-search-problem.html`
  - `satisficing, or good enough, solutions`: 184행 부근
  - special cases에 대한 지식을 활용해 solution으로 안내한다는 설명: 195행 부근
  - search space 바깥의 추가 지식을 `heuristic knowledge`라고 부르는 설명: 196행 부근
  - 한 종류의 휴리스틱 지식이 node에서 goal까지의 cost estimate 형태라는 설명: 197-198행 부근
- `.tmp/section-2-2-evidence/aima-contents.html`
  - `Informed (Heuristic) Search Strategies`: 108행 부근
  - `Greedy best-first search`, `A* search`: 109-110행 부근
  - `Satisficing search`: 112행 부근
  - `Heuristic Functions`: 115행 부근
  - `Learning heuristics from experience`: 121행 부근
- `.tmp/section-2-1-labeling-evidence/google-ml-glossary.html`
  - classification threshold: 4083행 부근
  - classification threshold는 사람이 선택하는 값이라는 설명: 4093행 부근
  - threshold 선택이 false positive와 false negative 수에 영향을 준다는 설명: 4109행 부근
  - hyperparameter: 8300행 부근
- `.tmp/section-7-1-evidence-modern/deepmind-funsearch.html.txt`
  - FunSearch가 LLM과 automated evaluator를 결합한다는 설명: 16행 부근
  - 현재 pool의 프로그램을 선택해 LLM에 입력하고, 새 프로그램을 자동 평가해 좋은 후보를 다시 pool에 추가한다는 설명: 20-24행 부근
  - online bin-packing이 기존에는 human experience 기반 heuristics로 다뤄졌고, FunSearch가 자동 맞춤 프로그램으로 기존 heuristic보다 적은 bin을 사용했다는 설명: 48-54행 부근

## 핵심 주장별 검토

| 본문 주장 | 근거 연결 | 판단 |
| --- | --- | --- |
| 휴리스틱의 어원은 “찾다, 알아내다, 발견하다”와 연결된다 | Etymonline의 Greek `heuriskein` 설명 | 유지 |
| 휴리스틱은 “정답을 맞히는 요령”보다 “찾아내기 위한 방법”으로 이해하는 편이 안전하다 | 어원과 7.1의 search 개념을 연결한 본문 일반화 | 유지. 어원 자체가 현대 AI 용법을 모두 결정한다고 쓰지 않음 |
| AI에서 휴리스틱 발상은 사람의 문제 해결을 시뮬레이션하려는 초기 연구와 연결된다 | ACM Newell, ACM Simon 소개 | 유지 |
| 사람은 모든 정보, 시간, 처리 능력을 갖지 못하므로 완전 탐색 대신 선택적 탐색과 단순화된 규칙을 사용한다 | ACM Newell, ACM Simon, Nobel Simon 자료 | 유지 |
| Logic Theorist와 GPS는 휴리스틱 문제 해결 원리를 적용한 초기 AI 프로그램으로 소개할 수 있다 | ACM Simon, ACM Newell 소개 | 유지. 상세 역사는 2장/AI 역사 영역으로 넘김 |
| 휴리스틱은 모든 후보를 보지 않기 위한 기준이다 | Poole & Mackworth의 heuristic knowledge 설명과 search difficulty 설명 | 유지 |
| 휴리스틱은 정답을 보장하는 공식이 아니라 후보의 우선순위를 정하는 경험적 기준이다 | AIMA의 heuristic search, heuristic functions 배치와 내부 휴리스틱 기준 문서 | 유지 |
| 휴리스틱은 후보 수, 시간, 메모리, 비교 부담을 줄일 수 있다 | 탐색 공간이 커질 때 search를 안내하는 지식이라는 근거를 입문용으로 일반화 | 유지 |
| 휴리스틱 함수는 후보에 추정값을 붙여 우선순위를 정하는 방식으로 설명할 수 있다 | Poole & Mackworth의 node에서 goal까지 cost estimate 예시 | 유지. 수식과 A* 조건은 제외 |
| 충분히 좋은 해는 현실적인 계산 한계에서 필요할 수 있다 | Poole & Mackworth의 satisficing 또는 good enough solution 설명, AIMA의 satisficing search 항목 | 유지 |
| 현대 AI 서비스에서도 휴리스틱은 후보를 줄이거나 우선순위를 정하는 기준으로 나타난다 | Google ML Glossary의 threshold, FunSearch의 프로그램 후보 평가, 내부 실무 휴리스틱 기준 | 유지 |
| classification threshold는 운영 휴리스틱 예시가 될 수 있다 | Google ML Glossary는 threshold가 사람이 선택하는 값이고 false positive/false negative에 영향을 준다고 설명 | 유지. 확률 모델 자체와 혼동하지 않음 |
| FunSearch는 현대적 프로그램 탐색에서 평가 기준으로 후보를 줄이는 사례다 | DeepMind는 자동 평가기와 높은 점수 후보 재사용, bin packing heuristic 비교를 설명함 | 유지. 모든 LLM 사용을 휴리스틱 탐색으로 일반화하지 않음 |
| 휴리스틱은 검증을 대신하지 않는다 | 휴리스틱의 최적 보장 부재와 편향 가능성을 반영한 보수적 일반화 | 유지 |
| 휴리스틱은 규칙, 확률 모델, 최적화, 학습, 모델과 같은 말이 아니다 | 내부 기준 문서와 6장, 7.3 예정 도메인 경계 | 유지 |

## 도메인 경계

| 섹션 | 맡는 역할 |
| --- | --- |
| 7.1 | 탐색 공간과 계산 한계가 왜 생기는지 설명 |
| 7.2 | 휴리스틱이 탐색에서 무엇을 줄이는지 설명 |
| 7.3 | 휴리스틱과 확률 모델의 차이를 설명 |
| Part 2 | 조합, 지수적 증가, 확률, 함수의 기초 복구 |
| Part 3 | 특징 선택, 전처리, 모델 선택, 튜닝에서 쓰이는 실무 휴리스틱 |

## 보수화한 표현

- “휴리스틱은 AI적 사고의 첫 시도”라는 표현은 본문에 넣지 않았습니다. 역사적으로 과장될 수 있으므로 “초기 AI의 핵심 문제 해결 방식 중 하나”라는 관리 문서 기준을 유지합니다.
- “휴리스틱은 불확실성을 계산한다”라고 쓰지 않았습니다. 7.2에서는 계산 한계 속에서 후보를 줄이는 기준으로 제한했습니다.
- 어원 설명은 개념 도입을 돕는 용도로만 사용했습니다. 어원이 현대 AI에서의 휴리스틱 정의를 모두 결정한다고 쓰지 않았습니다.
- 발상 설명은 Newell과 Simon의 초기 AI/인지 시뮬레이션 맥락으로 제한했습니다. 휴리스틱의 전체 철학사나 수학 교육사는 이 절에서 다루지 않았습니다.
- Pólya는 Newell에게 영향을 준 배경으로만 언급했습니다. `How to Solve It`의 상세 내용은 원문 확인 후 별도 절에서 다루는 것이 안전합니다.
- 현대 예시는 동일한 층위(level)의 기술로 묶지 않았습니다. 운영 기준, 실험 전략, 생성형 AI 검토, 자동 프로그램 탐색을 모두 “후보를 줄이는 기준”이라는 공통점으로만 연결했습니다.
- classification threshold 예시는 6.3의 확률 출력 해석을 반복하지 않도록, 자동 처리와 사람 검토를 나누는 운영 기준으로만 설명했습니다.
- 하이퍼파라미터 튜닝은 Part 3에서 자세히 다룰 예정이므로, 여기서는 조합 폭발을 줄이는 현대 실무 예시로만 배치했습니다.
- FunSearch는 `LLM이 정답을 검색한다`가 아니라 `프로그램 후보를 만들고 자동 평가로 선별한다`는 사례로 제한했습니다.
- 직선거리 예시는 휴리스틱 함수의 감각을 잡기 위한 예시이며, 실제 최단 경로 보장을 뜻하지 않는다고 명시했습니다.
- satisficing은 `충분히 좋은 해(good-enough solution, satisficing solution)`로 병기하되, 한국어 독자가 먼저 이해할 수 있도록 “충분히 좋은 해”를 앞에 두었습니다.
- A*, greedy best-first search, admissible heuristic, consistent heuristic은 범위 밖으로 두었습니다. 알고리즘 조건을 여기서 다루면 7.2의 입문 목적을 벗어납니다.
- 휴리스틱과 확률 모델의 차이는 7.3에서 다루도록 남겼고, 7.2에서는 혼동 방지 표만 배치했습니다.

## 남은 검토 사항

- 7.3에서는 휴리스틱과 확률 모델(probabilistic model)을 분리하면서, “휴리스틱은 불확실성을 반영하는가”라는 사용자 직관을 더 직접적으로 검토합니다.
- 이후 Part 3의 실무 휴리스틱 장에서는 데이터 전처리, 특징 선택, 모델 선택, 하이퍼파라미터 튜닝에서 휴리스틱을 검증 가능한 출발점으로 다룹니다.
