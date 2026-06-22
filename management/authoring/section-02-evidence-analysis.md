# 1.2 Section 근거 분석

## 목적

이 문서는 `docs/chapters/chapter-01/section-02.md`의 핵심 주장과 참고 자료가 실제로 연결되는지 검토한 관리 메모입니다.

원문 확인 규칙에 따라 가능한 자료는 `.tmp/section-01-evidence/` 아래에 임시로 내려받아 확인했습니다. 이 디렉터리 이름은 1.1 검토에서 시작했지만, 1.2에서 재사용한 공통 참고 자료도 함께 들어 있습니다. `.tmp/`의 원문 파일은 근거 검토용이며 저장소에 커밋하지 않습니다.

## 원문 확인 상태

| 자료 | 로컬 확인 상태 | 1.2에서의 역할 |
| --- | --- | --- |
| OECD.AI, `Updates to the OECD’s definition of an AI system explained` | HTML 다운로드 확인 | AI 시스템을 입력, 목표, 출력, 영향 관점으로 설명하는 근거 |
| Cambridge Dictionary, `artificial intelligence` | HTML 다운로드 확인 | 언어, 이미지, 문제 해결, 학습 같은 AI 과업 예시의 근거 |
| Stanford Encyclopedia of Philosophy, `Artificial Intelligence` | HTML 다운로드 확인 | 지능형 에이전트, 지각 입력, 행동, 탐색, 계획, 머신러닝, 신경망 흐름의 보조 근거 |
| AIMA 공식 사이트 | HTML 다운로드 확인 | Russell/Norvig 교재의 공식 사이트 확인. 에이전트 관점의 직접 내용은 SEP에 인용된 설명으로 보조 확인 |
| Poole & Mackworth, `Artificial Intelligence: Foundations of Computational Agents` | HTML 다운로드 확인 | 입력·출력 black-box, software agent, human-in-the-loop, transduction, controller, agent function 설명의 직접 근거 |
| Fayyad, Piatetsky-Shapiro, Smyth, `From Data Mining to Knowledge Discovery in Databases` | PDF 다운로드 및 텍스트 추출 확인 | 데이터마이닝, KDD, 분류, 회귀, 군집화, 예측, 패턴 발견 설명의 근거 |

## 본문 주장별 검토

| 본문 위치 | 핵심 주장 | 근거 연결 | 판정 |
| --- | --- | --- | --- |
| `section-02.md:5` | 대부분의 AI 시스템은 입력을 받아 목표에 맞는 출력을 만들고, 그 결과가 사람이나 환경에 영향을 준다 | OECD의 AI 시스템 정의가 입력, 목표, 출력, 환경 영향 관점을 제공함 | 유지 가능 |
| `section-02.md:15` | 같은 이미지 데이터도 분류, 위치 탐지, 생성처럼 다른 문제로 정의될 수 있다 | Cambridge는 이미지 인식/생성, 문제 해결, 학습을 AI 예시로 제시함. 문제 정의에 따른 분화는 저자적 설명 | 유지 가능 |
| `section-02.md:23-32` | 인식, 분류, 군집화, 예측, 탐색과 계획, 추천, 생성, 제어 같은 문제 유형으로 나눌 수 있다 | Cambridge는 언어·이미지·문제 해결·학습, OECD는 예측·콘텐츠·추천·결정, SEP는 탐색·계획·에이전트·학습, Fayyad는 분류·회귀·군집화·예측을 뒷받침함 | 대체로 유지 가능 |
| `section-02.md:34` | 문제 유형과 구현 방식은 같지 않다 | 여러 자료가 같은 AI 범주 안에서 다양한 과업과 접근을 제시함. 직접 정식 명제라기보다 학습용 정리 | 유지 가능 |
| `section-02.md:38-50` | 같은 데이터도 질문에 따라 다른 AI 문제가 된다 | Fayyad의 KDD 설명은 같은 데이터에서 목표와 절차에 따라 패턴, 모델, 예측, 분류, 군집화가 달라질 수 있음을 뒷받침함 | 유지 가능 |
| `section-02.md:52-60` | AI 시스템을 함수와 워크플로우 관점으로 읽을 수 있다 | Poole & Mackworth는 에이전트의 입력·출력 black-box 관점, software agent, human-in-the-loop, 지각 또는 입력 이력을 명령으로 바꾸는 transduction, controller를 설명함. SEP/AIMA 계열도 지각 입력을 행동으로 매핑하는 agent function 관점을 제공함. 업무 워크플로우 연결은 이 자료들을 바탕으로 한 학습용 일반화임 | 본문에 학습용 일반화임을 표시 |
| `section-02.md:64-74` | 모델보다 문제 정의가 먼저이며, 입력·출력·목표·제약·영향을 확인해야 한다 | OECD 정의와 Fayyad의 KDD 절차 설명이 목표, 데이터 선택, 평가, 해석의 필요성을 뒷받침함 | 유지 가능 |
| `section-02.md:78-84` | 실제 서비스는 여러 문제 유형이 겹친다 | SEP의 다중 패러다임 사례, OECD의 복수 출력 유형, Fayyad의 KDD 절차가 복합성을 뒷받침함. 검색/자율주행 예시는 본문 설명용 예시 | 유지 가능 |

## 수정 반영

- `함수와 워크플로우로 읽기` 절의 “학습용 비유” 표현을 “학습용 일반화”로 정제하고, Poole & Mackworth의 `black-box`, 지각 또는 입력 이력을 다루는 `transduction`, `controller`, `software agent`, `human-in-the-loop` 근거를 연결했습니다.
- 1.2 참고 자료에 AIMA 공식 사이트를 추가했습니다. 본문이 직접 AIMA 내용을 길게 설명하지는 않지만, SEP가 설명하는 지능형 에이전트 관점과 연결되는 대표 교재로 보조 근거가 됩니다.

## 일반화 문구

사용자의 해석은 다음처럼 정제할 수 있습니다.

> AI 시스템은 소프트웨어의 입력-처리-출력 구조를 확장해, 요청이나 관측값을 받아 목표에 맞는 응답·추천·결정·행동을 만드는 시스템으로 읽을 수 있다. 다만 AI는 사람이 모든 규칙을 명시한 함수만으로 동작하지 않고, 데이터에서 얻은 패턴, 통계적 관계, 파라미터 또는 학습된 표현을 사용해 출력 과정을 구성한다. 따라서 AI 설계는 사람의 업무 흐름 전체를 복제하는 일이 아니라, 그 흐름 중 계산으로 처리할 수 있고 반복 가능하며 검증 가능한 부분을 찾아 자동화하거나 보조하는 일에 가깝다.

## 추가 보강 필요

- `추천과 순위화`, `제어와 행동`은 1.2에서는 개론적 분류로 충분하지만, 후속 장에서는 추천 시스템, 강화학습, 제어 이론 자료를 별도로 확인해야 합니다.
- 검색 서비스와 자율주행 예시는 이해를 돕는 자체 예시입니다. 해당 주제를 자세히 다루는 Section을 작성할 때는 별도 근거가 필요합니다.
- `robust`는 이 문서에서 공학적 요구를 가리키는 일반 표현으로 사용했습니다. 안전성, 신뢰성, 견고성 개념은 윤리·보안·서비스 운영 장에서 공식 자료와 함께 다시 정리해야 합니다.

## 출처와 참고 자료

- OECD.AI, Stuart Russell, Karine Perset, Marko Grobelnik, [Updates to the OECD’s definition of an AI system explained](https://oecd.ai/en/wonk/ai-system-definition-update), 2023-11-29, 확인 날짜: 2026-06-22.
- Cambridge Dictionary, [Meaning of artificial intelligence in English](https://dictionary.cambridge.org/dictionary/english/artificial-intelligence), 확인 날짜: 2026-06-22.
- Stanford Encyclopedia of Philosophy, Selmer Bringsjord and Naveen Sundar Govindarajulu, [Artificial Intelligence](https://plato.stanford.edu/entries/artificial-intelligence/), 2018-07-12, 확인 날짜: 2026-06-22.
- Stuart Russell, Peter Norvig, [Artificial Intelligence: A Modern Approach, 4th US ed.](https://aima.cs.berkeley.edu/), 확인 날짜: 2026-06-22.
- David L. Poole, Alan K. Mackworth, [Artificial Intelligence: Foundations of Computational Agents, 3rd ed.](https://artint.info/3e/html/ArtInt3e.html), 2023, 확인 날짜: 2026-06-22.
- Usama M. Fayyad, Gregory Piatetsky-Shapiro, Padhraic Smyth, [From Data Mining to Knowledge Discovery in Databases](https://www.kdnuggets.com/gpspubs/aimag-kdd-overview-1996-Fayyad.pdf), AI Magazine, 1996, 확인 날짜: 2026-06-22.
