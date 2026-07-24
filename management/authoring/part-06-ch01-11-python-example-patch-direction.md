# Part 6 Chapter 1-11 Python 예제 개선 방안

작성일: 2026-07-24

## 목적

이 문서는 `management/authoring/python-example-improvement-report.md`를 기준으로 Part 6 Chapter 1부터 Chapter 11까지의 Python 예제를 어떻게 개선할지 정리한 패치 방향 문서다.

목표는 Python 예제 수를 늘리는 것이 아니라, LLM과 생성형 AI의 핵심 질문을 실제 입력 변화, 후보 순위, 생성 선택, 검색 결과, 실패 위치로 확인하게 만드는 것이다. 특히 Part 6은 외부 API, 로컬 LLM, tokenizer, retrieval, vector database 같은 실제 시스템과 연결될 여지가 크므로, 본문 기본 예제와 선택 실행 예제를 분리해 관리한다.

## 기준 문서

- `management/authoring/python-example-improvement-report.md`
- `management/guidelines/python-example-guidelines.md`
- `management/guidelines/manuscript-writing-workflow.md`
- `management/guidelines/section-metadata-guidelines.md`

## 현재 의존성 판단

현재 `requirements.txt` 기준으로 기본 실행 예제에 바로 사용할 수 있는 라이브러리는 다음이다.

- 사용 가능: `numpy`, `pandas`, `matplotlib`, `scikit-learn`, `chromadb`
- 고정 의존성 없음: `transformers`, `tiktoken`, `openai`, `ollama`

따라서 Chapter 1-11의 기본 패치는 다음 원칙을 따른다.

1. 본문 기본 예제는 가능하면 현재 고정 의존성 안에서 실행되게 한다.
2. 실제 LLM 호출, tokenizer SDK, OpenAI SDK, Ollama 호출은 선택 실행 또는 저장 로그 기반 예제로 분리한다.
3. 외부 모델 다운로드가 필요한 예제는 본문 핵심 예제로 바로 넣지 않고, 실행 결과 CSV/JSON과 차트 자산을 함께 둔다.
4. RAG와 검색 예제는 `TfidfVectorizer`, `NearestNeighbors`, `chromadb` 중 Section 중심 질문을 가장 덜 흐리는 것을 고른다.
5. 실시간 API 응답의 특정 문장 자체를 학습 목표로 두지 않고, 반복 응답의 형식 준수율, 후보 다양성, 검색 실패, 근거 연결 여부 같은 관찰값을 본다.

## 현재 범위 요약

대상 Section은 35개다.

| 범위 | Section 수 | 현재 Python 예제 Section 수 | 판단 |
| --- | ---: | ---: | --- |
| Chapter 1 | 3 | 0 | 개념 도입 중심, 새 Python 예제는 신중 |
| Chapter 2 | 5 | 1 | tokenizer 실제성 보강 여지 큼 |
| Chapter 3 | 4 | 1 | embedding/search 후보 실험 보강 여지 큼 |
| Chapter 4 | 5 | 2 | context window와 KV cache 예제 보강 후보 |
| Chapter 5 | 2 | 1 | 생성 누적 로그 보강 후보 |
| Chapter 6 | 2 | 2 | next-token과 decoding 선택 보강 후보 |
| Chapter 7 | 2 | 2 | 현행 CSV/차트 예제 유지 우선 |
| Chapter 8 | 2 | 1 | LoRA 저장 부담은 현행 유지, fine-tuning 판단 예제는 선택 후보 |
| Chapter 9 | 5 | 4 | instruction/alignment 예제는 실제 응답 로그화 후보 |
| Chapter 10 | 4 | 1 | 프롬프트 실험 로그와 반복 개선 예제 보강 후보 |
| Chapter 11 | 2 | 2 | RAG 검색/생성 실패 분리와 vector DB payload 연결 보강 후보 |

## 우선 패치 후보

| 우선순위 | Section | 현재 상태 | 권장 방식 | 패치 방향 |
| --- | --- | --- | --- | --- |
| 높음 | P6-2.3 길이·비용·청크를 바꾸는 토큰화 | Python 예제 없음 | `tiktoken` 선택 실행 또는 저장 tokenization 로그 | 한국어, 영어, 숫자, 공백, 코드 조각의 token 수 차이를 저장 CSV와 차트로 보여 준다. 기본 본문에는 저장 결과를 두고, SDK 실행은 선택 스크립트로 둔다. |
| 높음 | P6-2.5 토크나이저 계열 차이 | 선택 실행형 tokenizer 예제 있음 | `transformers`/`tiktoken` 저장 결과 | 의존성 없는 설명에 머물지 않게, 같은 입력을 tokenizer family별 token 수·토큰 조각·ID로 비교한 CSV/차트 자산을 만든다. |
| 높음 | P6-3.1 토큰 ID를 비교 가능한 좌표로 바꾸는 임베딩 | Python 예제 없음 | `numpy` 작은 embedding table 또는 `TfidfVectorizer` | token ID의 숫자 크기와 vector similarity가 다른 질문임을 작은 embedding matrix와 cosine similarity 출력으로 닫는다. |
| 높음 | P6-3.2 정답이 아니라 후보를 만드는 가까운 벡터 | Python 예제 없음 | `TfidfVectorizer` 또는 저장 embedding | query별 top-k 후보, 유사도, 오답 후보, 근거 확인 필요성을 출력한다. `가까움=정답` 오해를 깨는 실패 후보를 반드시 포함한다. |
| 높음 | P6-3.4 ANN 검색의 속도와 후보 누락 절충 | 무작위 벡터와 coarse window 예제 | `NearestNeighbors`, 선택적으로 `chromadb` | brute force와 후보 축소 검색을 비교하고 `recall@k`, 누락 문서 ID, 검색 후보 수를 출력한다. |
| 높음 | P6-4.2 attention의 참조 범위 | 수작업 token budget 예제 | tokenizer 저장 로그 또는 현재 예제 유지+차트 강화 | 실제 token count 로그를 붙여 공백·코드·로그 조각이 context budget을 다르게 쓰는 장면을 보인다. 최신 모델 context window 숫자는 고정하지 않는다. |
| 높음 | P6-6.2 답변 안정성과 다양성을 바꾸는 출력 선택 규칙 | 고정 확률 기반 예제 | 고정 logits 유지 + Ollama 저장 로그 선택 | temperature/top-k/top-p별 반복 생성 로그를 CSV로 저장하고, unique output 수, 형식 흔들림, 반복률을 차트로 비교한다. |
| 높음 | P6-9.1 지시 튜닝 | CSV 기반 형식 신호 집계 예제 | Ollama/OpenAI 저장 응답 로그 | 일반 prompt와 구조화 prompt의 응답 로그를 저장하고 format compliance, 필수 항목 보존율, 누락 슬롯을 비교한다. 실제 instruction tuning 구현으로 오해되지 않게 한다. |
| 높음 | P6-9.2 정렬 | 사람이 만든 후보 응답 문자열 규칙 예제 | 저장 응답 로그 + 다축 evaluator | helpfulness, safety, factuality가 서로 충돌하는 응답 후보를 늘리고, 자동 판정과 사람 검토 필요 사례를 분리한다. |
| 높음 | P6-10.1 프롬프트 엔지니어링 | Ollama 로컬 API 예제 있음 | 저장 로그 우선 + 선택 실행 | 실시간 호출 기본 의존을 낮추기 위해 저장 응답 CSV와 차트를 두고, Ollama 호출 스크립트는 선택 실행으로 분리한다. |
| 높음 | P6-10.3 답변 경로 관찰과 비교 | 비코드 중심 | 저장 응답 로그 | 같은 질문을 여러 번 생성한 결론 분포, 근거 누락, 형식 흔들림을 self-consistency 관점으로 집계한다. |
| 중간 | P6-10.4 프롬프트 후보 반복 개선 | Python 예제 없음 | 작은 prompt 후보 CSV + 평가 함수 | prompt 후보별 점수와 실패 항목을 계산하고, 다음 후보가 어떤 실패를 줄였는지 반복 로그로 보여 준다. |
| 높음 | P6-11.1 RAG 필요성 | `TfidfVectorizer` RAG 예제 있음 | 현행 유지 + 실패 후보 보강 | `current_signal`을 정답표처럼 보이지 않게 낮추고, top-k 문서 제목·유사도·현재 문서 여부·근거 연결 여부를 중심 출력으로 재정렬한다. |
| 높음 | P6-11.2 RAG 검색 실패와 생성 실패 | `TfidfVectorizer` + mock generation 예제 있음 | 현행 유지 + payload/평가 로그 강화 | 검색 실패와 생성 실패가 분리되는 점은 좋다. 다음 패치에서는 retrieved payload, answer source trace, failure matrix 차트를 더 직접 연결한다. |

## 중간·보류 후보

| Section | 판단 | 보류 이유 또는 다음 조건 |
| --- | --- | --- |
| P6-1.1 생성형 AI 출력 | 새 Python 예제보다는 비코드 검토표가 적합 | 산출물 검토 관점이 중심이라 코드가 형식적 정답 확인이 될 위험이 큼 |
| P6-1.2 LLM 중심 사례 | 새 Python 예제 보류 | Part 6 전체 지도를 잡는 절이라 도구 실행보다 구조 표가 낫다 |
| P6-1.3 후보 분포와 선택 반복 | P6-6.1/P6-6.2와 묶어 회수 | 이 절에 중복 예제를 넣기보다 생성 선택 장에서 실제 출력으로 닫는 편이 좋다 |
| P6-4.4 KV cache와 반복 생성 | 현행 NumPy 예제 유지 우선 | 실제 Transformer cache 구현은 설치와 세부 구현이 Section 중심 질문보다 커질 수 있음 |
| P6-5.1 디코더 기반 누적 생성 | 저장 logits/생성 로그 후보 | 내부 후보 분포 전체를 안정적으로 노출하기 어려우므로 저장 로그 방식이 먼저 필요 |
| P6-6.1 다음 토큰 예측 | 현행 n-gram/고정 분포 유지 + 선택 보강 | 작은 causal LM은 의존성 부담이 크고, n-gram 축약 예제가 더 투명함 |
| P6-7.1 사전학습 | 현행 유지 | 실제 pretraining SDK는 범위가 너무 큼 |
| P6-7.2 스케일 | tokenizer 기반 비용 계산 보조 후보 | 가격·context window 최신성 의존이 커서 본문 고정값으로 두면 위험 |
| P6-8.1 파인튜닝 | 새 Python 예제 신중 | 실제 fine-tuning API/학습은 Part 7 프로젝트가 더 적합 |
| P6-8.2 LoRA | 현행 저장 부담 예제 유지 | PEFT/LoRA 실제 학습보다 rank와 저장 부담 수치 감각이 중심 |
| P6-9.3 실패 신호 진단 | 저장 실패 로그 후보 | 자동 진단기가 정답처럼 보이지 않게 실패 유형과 경계 사례를 충분히 늘려야 함 |
| P6-9.4 LoRA low-rank | 현행 유지 | 실제 LoRA 구현보다 rank별 파라미터 수 비교가 중심 |
| P6-9.5 효율적 조정 방식 제약 | 새 예제 보류 | 조정 방식 선택의 조건표와 사례가 우선 |
| P6-10.2 프롬프트 한계 | 새 Python 예제 보류 또는 P6-10.1 로그 재사용 | 별도 코드보다 P6-10.1/P6-11.1의 실험 로그를 연결해 한계 판단으로 읽는 편이 좋다 |

## 권장 패치 순서

### 1차. 현재 의존성으로 바로 닫는 묶음

1. P6-3.1, P6-3.2
   - `numpy` 또는 `TfidfVectorizer`로 embedding/vector similarity 감각을 바로 보강할 수 있다.
   - Part 6 뒤쪽 RAG와 vector DB의 공통 기반이므로 학습 효과가 크다.
2. P6-3.4
   - `NearestNeighbors` 또는 현재 벡터 예제를 개선해 ANN의 속도·누락 trade-off를 더 실제 검색 API에 가깝게 만든다.
3. P6-11.1, P6-11.2
   - 이미 `TfidfVectorizer` 기반 예제가 있으므로 정답 확인형 냄새를 줄이고 payload/실패 위치 관찰을 강화한다.

### 2차. 저장 로그 기반으로 실제성 올리는 묶음

1. P6-6.2
   - 고정 logits 예제는 유지하되, Ollama/OpenAI 저장 응답 로그를 별도 CSV로 두면 실제 생성 다양성을 더 잘 볼 수 있다.
2. P6-9.1, P6-9.2
   - instruction/alignment 설명은 사람이 만든 후보 답변보다 실제 응답 로그가 학습밀도를 높인다.
3. P6-10.1, P6-10.3, P6-10.4
   - prompt engineering은 한 번의 응답보다 여러 입력·여러 후보의 반복 통계를 보게 만든다.

### 3차. 의존성 정책 결정 뒤 패치하는 묶음

1. P6-2.3, P6-2.5
   - `tiktoken` 또는 `transformers`를 기본 의존성에 넣을지 결정해야 한다.
   - 기본 본문은 저장 tokenization 로그와 차트로 닫고, 실제 SDK 실행은 선택 스크립트로 두는 편이 안정적이다.
2. P6-4.2
   - 실제 token count가 있으면 context budget 설명이 더 선명해진다.
   - 다만 최신 모델 window 수치를 본문 고정값으로 쓰지 않는다.

## 예제 설계 원칙

- 코드가 이미 설계된 정답을 확인하는 구조가 되지 않게 한다.
- 입력을 바꾸면 후보 순위, token count, context 선택, 생성 결과, 실패 위치 중 하나 이상이 달라져야 한다.
- LLM 실시간 호출 결과는 재현성이 흔들리므로 기본 본문은 저장 로그와 요약 차트를 우선한다.
- API key, 계정, 과금, 모델 다운로드가 필요한 코드는 선택 실행 스크립트로 분리한다.
- 저장 로그를 쓸 때도 `모델이 이렇게 말했다`가 아니라, 여러 응답의 형식 준수율, 근거 연결, 누락, 실패 유형을 본다.
- RAG 예제는 `retrieval result`, `source payload`, `generated answer`, `failure reason`을 분리해 출력한다.
- tokenizer 예제는 token 수만 출력하지 말고, 비용·chunk·context budget 판단이 어떻게 달라지는지 연결한다.

## 완료 판단 기준

- Chapter 1-11 각 Section이 `새 예제 필요`, `기존 예제 개선`, `현행 유지` 중 하나로 분류되어 있다.
- 우선 후보는 사용할 라이브러리, 입력 자산, 관찰 출력, 주의점을 함께 가진다.
- 기본 본문 예제와 선택 실행 예제가 분리되어 있다.
- 외부 모델/API 의존 후보는 저장 로그 또는 보충 스크립트 정책이 정해져 있다.
- Part 6 기존 변경과 새 패치가 섞이지 않도록 커밋 시 범위를 `docs/parts/part-06`, `docs/assets/part-06`, 대응 릴리즈노트, 관리문서로 다시 확인한다.
