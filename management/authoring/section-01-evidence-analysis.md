# 1.1 Section 근거 분석

## 목적

이 문서는 `docs/chapters/chapter-01/section-01.md`의 핵심 주장과 참고 자료가 실제로 연결되는지 검토한 관리 메모입니다.

원문 확인 규칙에 따라 가능한 자료는 `.tmp/section-01-evidence/` 아래에 임시로 내려받아 확인했습니다. `.tmp/`의 원문 파일은 근거 검토용이며 저장소에 커밋하지 않습니다.

## 원문 확인 상태

| 자료 | 로컬 확인 상태 | 판단 |
| --- | --- | --- |
| OECD.AI, `Updates to the OECD’s definition of an AI system explained` | HTML 다운로드 확인 | AI 시스템을 입력, 목표, 출력, 환경 영향 중심으로 설명하는 근거로 적절함 |
| NIST AI Resource Center, `Glossary` | HTML 다운로드 확인 | 단일 정의보다 공통 어휘와 다의성 관리를 설명하는 보조 근거로 적절함 |
| Cambridge Dictionary, `artificial intelligence` | HTML 다운로드 확인 | 컴퓨터 시스템, 기계, 인간 두뇌의 일부 능력, 언어, 이미지, 문제 해결, 학습을 설명하는 근거로 적절함 |
| Merriam-Webster, `artificial intelligence` | `curl` 다운로드는 403, 사용자 제공 원문 발췌로 확인 | 컴퓨터 시스템/알고리즘의 인간 지능 행동 모방 능력, 그 능력을 가진 시스템, 컴퓨터과학 분야라는 설명의 근거로 적절함 |
| Britannica Dictionary, `artificial intelligence` | `curl` 다운로드는 403, 브라우저 조회로 확인 | 컴퓨터과학 분야와 기계의 인간 지능 유사 능력 설명의 근거로 적절함 |
| 汉典(ZDIC), `人工智能` | HTML 다운로드 확인 | 동북아권 자료 중 중국어 사전 근거로 적절함 |
| Stanford Encyclopedia of Philosophy, `Artificial Intelligence` | HTML 다운로드 확인 | AI가 하나의 기술이 아니라 분야이며, 탐색, 계획, 머신러닝, 신경망 등 여러 접근을 포함한다는 설명의 보조 근거로 적절함 |
| AIMA 공식 사이트 | HTML 다운로드 확인 | 교재 존재와 공식 자료 확인에는 적절하지만, 현재 내려받은 홈페이지 자체만으로는 1.1의 세부 주장을 직접 뒷받침하기에는 약함 |
| NIST, `Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile` | PDF 다운로드 및 텍스트 추출 확인 | 생성형 AI의 출력 범위와 LLM 관계를 보강하는 근거로 적절함 |
| Zhao et al., `A Survey of Large Language Models` | PDF 다운로드 및 텍스트 추출 확인 | LLM을 대규모 사전학습 언어 모델 계열로 설명하는 근거로 적절함 |
| Fayyad, Piatetsky-Shapiro, Smyth, `From Data Mining to Knowledge Discovery in Databases` | 사용자가 제공한 KDnuggets PDF 다운로드 확인 | KDD와 data mining의 관계, 데이터에서 패턴을 찾는 과정, 데이터 웨어하우징과 OLAP의 관련성을 설명하는 근거로 적절함 |
| D. J. Power, `A Brief History of Decision Support Systems` | HTML 다운로드 확인 | DSS, data-driven DSS, OLAP, BI, data warehouse 흐름을 설명하는 근거로 적절함 |

## 본문 주장별 검토

| 본문 위치 | 핵심 주장 | 근거 연결 | 판정 |
| --- | --- | --- | --- |
| `section-01.md:15` | AI는 하나의 기술 이름이라기보다 넓은 연구 분야이자 시스템 범주다 | Merriam-Webster, Britannica, Cambridge, SEP가 분야, 시스템, 능력의 복수 의미를 제시함 | 유지 가능 |
| `section-01.md:17` | 체스, 바둑, 이미지 인식, 번역, 챗봇은 입력을 받아 출력·결정·추천·예측·생성 결과를 만든다 | OECD의 입력, 출력, 예측, 콘텐츠, 추천, 결정 설명과 Cambridge의 언어·이미지·문제 해결·학습 예시가 연결됨 | 유지 가능 |
| `section-01.md:19` | 영어권 사전, 동북아권 자료, 기관 정의에서 컴퓨터 시스템, 기계, 알고리즘, 인간 지능 관련 기능이 반복된다 | 영어권 사전과 OECD는 충분함. 동북아권은 현재 ZDIC만 직접 확인됨 | 표현 조정 필요 |
| `section-01.md:23` | AI는 분야와 시스템을 함께 가리키는 넓은 말이다 | Merriam-Webster는 능력, 그 능력을 가진 시스템, 컴퓨터과학 분야를 함께 제시하고, Cambridge는 사용/연구와 특정 시스템 의미를 모두 제시함 | 유지 가능 |
| `section-01.md:25-27` | 튜링 테스트는 기계가 생각하는가라는 질문을 관찰 가능한 대화 행동으로 바꾸려 한 역사적 시도다 | SEP는 Turing이 “Can a machine think?”라는 질문을 Turing Test로 대체하는 논의를 제시한다고 설명함 | 유지 가능 |
| `section-01.md:29` | OECD는 AI 시스템을 기계 기반 시스템, 목표, 입력, 예측·콘텐츠·추천·결정 출력으로 설명한다 | OECD 원문과 직접 연결됨 | 유지 가능 |
| `section-01.md:35` | 초기 AI에서 규칙, 지식, 탐색, 휴리스틱이 중요했다 | SEP의 AI 역사, 탐색, 계획, 머신러닝·신경망 구분과 연결됨. 다만 휴리스틱 자체는 이후 Section에서 더 직접 근거가 필요함 | 유지 가능, 후속 장에서 보강 |
| `section-01.md:37` | 데이터마이닝, DSS, BI, DW, OLAP는 데이터 기반 의사결정 환경의 배경이다 | DSSResources는 DSS, OLAP, BI, data warehouse 흐름을 직접 설명함. Fayyad 논문은 KDD/data mining이 대규모 데이터에서 유용한 패턴과 지식을 찾는 흐름이며, data warehousing과 OLAP가 KDD와 관련된 배경임을 설명함 | 유지 가능 |
| `section-01.md:39` | 머신러닝은 데이터에서 패턴을 학습하고, 딥러닝은 신경망·가중치·표현 학습으로 복잡한 입출력을 다룬다 | SEP의 machine learning, neural networks, deep neural networks 설명과 연결됨 | 유지 가능 |
| `section-01.md:51` | 사전적 정의와 역사적 변화를 구분해야 한다 | 사전 자료와 SEP/OECD의 성격 차이를 구분하는 저자적 정리임 | 유지 가능 |
| `section-01.md:88` | LLM은 생성형 AI의 대표 모델 계열 중 하나이나 모든 생성형 AI가 LLM은 아니다 | NIST는 생성형 AI 출력 예로 이미지, 영상, 오디오, 텍스트를 제시하고 LLM을 생성형 AI 관련 공통 활동 예로 언급함. Zhao et al.은 LLM을 대규모 사전학습 언어 모델 계열로 설명함 | 유지 가능 |

## 수정 반영

- `section-01.md:19`의 `주요 영어권·동북아권 사전과 기관 정의`는 동북아권 사전이 복수로 검증된 것처럼 읽힐 수 있어 `주요 영어권 사전, 동북아권 자료, 기관 정의`로 조정했습니다.
- ZDIC는 동북아권 자료 중 하나로 유지하되, 한국어권·일본어권 사전은 아직 검증 필요 상태로 남깁니다.
- 튜링 테스트는 AI의 전체 정의가 아니라, “지능을 어떻게 판정할 것인가”를 둘러싼 역사적 문제 제기로 1.1에 짧게 반영했습니다.

## 추가 보강 필요

- 한국어권 `인공지능` 정의를 표준국어대사전 또는 우리말샘에서 확인합니다.
- 일본어권 `人工知能` 정의를 신뢰 가능한 일본어 사전 또는 백과 자료에서 확인합니다.
- LLM과 생성형 AI의 관계는 1.3 작성 과정에서 NIST 생성형 AI 프로파일과 LLM 설문 논문으로 1차 보강했습니다. Part 5에서는 NLP 자료와 논문 계보로 더 자세히 정리합니다.

## 출처와 참고 자료

- OECD.AI, Stuart Russell, Karine Perset, Marko Grobelnik, [Updates to the OECD’s definition of an AI system explained](https://oecd.ai/en/wonk/ai-system-definition-update), 2023-11-29, 확인 날짜: 2026-06-22.
- NIST AI Resource Center, [Glossary](https://airc.nist.gov/glossary/), 확인 날짜: 2026-06-22.
- Merriam-Webster, [Artificial intelligence Definition & Meaning](https://www.merriam-webster.com/dictionary/artificial%20intelligence), 확인 날짜: 2026-06-22.
- Cambridge Dictionary, [Meaning of artificial intelligence in English](https://dictionary.cambridge.org/dictionary/english/artificial-intelligence), 확인 날짜: 2026-06-22.
- Britannica Dictionary, [Artificial intelligence Definition & Meaning](https://www.britannica.com/dictionary/artificial-intelligence), 확인 날짜: 2026-06-22.
- 汉典, [人工智能](https://www.zdic.net/hans/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD), 확인 날짜: 2026-06-22.
- Stanford Encyclopedia of Philosophy, Selmer Bringsjord and Naveen Sundar Govindarajulu, [Artificial Intelligence](https://plato.stanford.edu/entries/artificial-intelligence/), 2018-07-12, 확인 날짜: 2026-06-22.
- Stuart Russell, Peter Norvig, [Artificial Intelligence: A Modern Approach, 4th US ed.](https://aima.cs.berkeley.edu/), 확인 날짜: 2026-06-22.
- NIST, [Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile](https://doi.org/10.6028/NIST.AI.600-1), NIST AI 600-1, 2024-07, 확인 날짜: 2026-06-22.
- Wayne Xin Zhao et al., [A Survey of Large Language Models](https://arxiv.org/abs/2303.18223), arXiv:2303.18223, 확인 날짜: 2026-06-22.
- Usama M. Fayyad, Gregory Piatetsky-Shapiro, Padhraic Smyth, [From Data Mining to Knowledge Discovery in Databases](https://www.kdnuggets.com/gpspubs/aimag-kdd-overview-1996-Fayyad.pdf), AI Magazine, 1996, 확인 날짜: 2026-06-22.
- D. J. Power, [A Brief History of Decision Support Systems](https://dssresources.com/history/dsshistory.html), DSSResources.COM, version 4.0, 2007-03-10, 확인 날짜: 2026-06-22.
