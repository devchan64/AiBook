# Section 2.3 근거 분석

## 대상 절

- `docs/chapters/chapter-02/section-03.md`
- 제목: `2.3 머신러닝, 딥러닝, 생성형 AI로의 흐름`

## 작성 목적

2.1의 기호 기반 AI와 규칙 기반 접근, 2.2의 탐색·지식 표현·확률 추론 다음에 이어지는 역사적 흐름을 정리한다. 핵심은 다음과 같다.

- 규칙을 사람이 모두 작성하기 어려운 문제가 데이터 기반 학습으로 이어졌다는 점
- 데이터마이닝, KDD, BI/DSS 같은 데이터 기반 의사결정 흐름이 머신러닝 확산의 배경이 된 점
- 딥러닝을 표현 학습과 가중치 최적화 관점에서 설명하되, 생물학적 뇌나 모든 확률 모델과 동일시하지 않는 점
- 생성형 AI와 LLM을 갑작스러운 단절이 아니라 머신러닝·딥러닝·언어 모델링 흐름의 최근 사례로 설명하는 점

## 근거 요약

| 주장 | 근거 | 반영 방식 |
| --- | --- | --- |
| 머신러닝은 예시가 주어졌을 때 과제 성능을 개선하는 시스템으로 설명할 수 있다. | Stanford Encyclopedia of Philosophy AI 항목 `.tmp/section-01-evidence/sep-ai.html` 1808행 근처 | 본문에서 머신러닝을 “데이터나 경험으로 모델 성능을 개선하는 접근”으로 설명 |
| 지도학습은 예시와 정답을 사용해 함수를 학습하는 방식으로 설명된다. | SEP AI 항목 1819-1831행 근처 | 지도학습을 “입력과 정답의 관계를 학습”하는 방식으로 요약 |
| 비지도학습은 정답 없이 데이터 안의 구조를 찾으며, 데이터마이닝과 연결될 수 있다. | SEP AI 항목 1841-1849행 근처 | 비지도학습과 데이터마이닝을 간단히 언급하되 세부 설명은 Chapter 8로 넘김 |
| 특징 벡터와 표현은 머신러닝에서 중요한 중간 표현이다. | SEP AI 항목 1992-2016행 근처 | 특징(feature), 표현(representation)을 딥러닝 전환의 핵심으로 설명 |
| 딥러닝은 표현 학습과 연결된다. | SEP AI 항목 1032-1042행, 2051행 근처 | 딥러닝을 “여러 층의 신경망으로 표현을 학습”하는 접근으로 설명 |
| KDD는 데이터에서 유용한 지식을 발견하는 전체 과정이고, 데이터마이닝은 그 안의 패턴 추출 단계다. | Fayyad et al. KDD 개요 `.tmp/section-01-evidence/fayyad-kdd-kdnuggets.txt` 160-165행, 286-331행 근처 | 데이터마이닝과 머신러닝을 같은 말로 쓰지 않고, 데이터 기반 판단의 배경으로 배치 |
| KDD는 데이터베이스, 통계, AI, 머신러닝과 만나는 다학제 영역이다. | Fayyad et al. 183-191행, 201-231행 근처 | BI/DSS/데이터마이닝을 AI 모델 자체가 아니라 데이터 기반 판단 인프라와 문화로 설명 |
| 현대 AI 교재는 머신러닝, 딥러닝, NLP, 컴퓨터 비전, 로보틱스를 독립 장으로 다룬다. | AIMA 목차 `.tmp/section-2-2-evidence/aima-contents.html` 534-766행 근처 | 2.3은 개론적 연결만 다루고 세부 기술은 이후 장으로 분리 |
| Poole & Mackworth 교재는 불확실성, 학습, 지식 그래프, 확률 추론을 함께 배치한다. | `.tmp/section-2-2-evidence/poole-mackworth-contents.html` 150-225행 근처 | 2.2와 2.3의 연결을 “확률 추론에서 학습으로 확장”으로 설명 |
| 생성형 AI는 입력 데이터의 구조와 특성을 모방해 이미지, 영상, 오디오, 텍스트 등 합성 콘텐츠를 생성하는 모델 범주다. | NIST AI 600-1 `.tmp/section-03-evidence/nist-ai-600-1-generative-ai-profile.txt` 125-129행 근처 | 생성형 AI를 출력의 성격으로 설명하고, 생성 결과가 사실이라는 뜻은 아니라고 보정 |
| LLM은 통계적 언어 모델, 신경망 언어 모델, 사전학습 언어 모델의 흐름 위에서 설명된다. | Zhao et al. LLM survey `.tmp/section-03-evidence/zhao-etal-2023-survey-llm.txt` 9-16행, 202-250행 근처 | LLM을 갑작스러운 예외가 아니라 언어 모델링과 대규모 사전학습의 흐름으로 설명 |

## 사용자 관점의 일반화

사용자의 관점:

> AI란 SW의 함수를 무언가로 바꾼 것이고, 요청 처리 응답의 함수 방법론을 포함한다. 사람이 행동하는 워크플로우의 연결과 유사하며, 그중 robust하게 만들 수 있는 요건을 찾아 구성하는 것이다.

본문 반영 문구:

> 현대 AI 서비스는 사람이 직접 작성한 로직, 데이터에서 학습한 모델, 검색과 도구, 검증 절차를 조합해 요청을 처리하는 워크플로우로 이해할 수 있습니다.

이 문구는 다음 경계를 유지한다.

- 모델을 전통적 함수와 완전히 동일시하지 않는다.
- LLM 하나가 서비스 전체라는 식으로 설명하지 않는다.
- 규칙, 검색, 데이터, 모델, 검증이 함께 들어가는 시스템 관점으로 일반화한다.

## 피한 표현

| 피한 표현 | 이유 | 대체 표현 |
| --- | --- | --- |
| AI라는 말 자체가 데이터 기반 판단을 뜻한다 | 초기 AI에는 규칙, 논리, 탐색, 지식 표현도 포함된다. | 현대 AI 이해에는 데이터에서 판단 기준을 학습하는 층위가 강하게 추가되었다. |
| 딥러닝은 생물학적 뇌와 같다 | 인공신경망은 생물학적 뇌의 복사본이 아니다. | 신경망과 시냅스 비유는 직관을 돕지만, 딥러닝은 계산 모델이다. |
| 딥러닝은 모두 확률 모델이다 | 모델과 목적 함수에 따라 확률 해석 가능성이 다르다. | 확률 모델, 표현 학습, 최적화를 구분한다. |
| 생성형 AI는 논리 추론으로 답을 만든다 | inference와 reasoning이 혼동될 수 있다. | 생성형 AI는 학습된 모델의 inference에서 출력을 생성한다. |
| LLM은 생성형 AI 전체다 | 이미지, 음성, 영상 생성 모델도 생성형 AI에 포함된다. | LLM은 생성형 AI의 대표 사례 중 하나다. |

## 검증 필요

- 딥러닝 부흥의 세부 연표는 이 절에서 깊게 다루지 않았다. Chapter 9에서 AlexNet, YOLO, WaveNet, Seq2Seq, Attention, Transformer 근거를 별도 분석해야 한다. Deep Voice는 필요한 경우 TTS 보조 사례로만 둔다.
- LLM의 직접 발전사는 이 절에서 요약만 했다. Chapter 11에서 통계적 언어 모델, 신경망 언어 모델, 사전학습, Transformer, instruction tuning, RLHF를 별도 근거로 다뤄야 한다.
- BI/DSS/DW/OLAP의 역사적 설명은 현재 관리 메모 수준으로만 반영했다. 별도 절에서 다룰 경우 한국어권 산업 자료와 학술 자료를 추가로 확보해야 한다.

## 출처

- Stanford Encyclopedia of Philosophy, Selmer Bringsjord and Naveen Sundar Govindarajulu, `Artificial Intelligence`, 2018-07-12, 확인 날짜: 2026-06-22.
- Stuart Russell, Peter Norvig, `Artificial Intelligence: A Modern Approach, 4th US ed., Full Table of Contents`, 확인 날짜: 2026-06-22.
- David L. Poole, Alan K. Mackworth, `Artificial Intelligence: Foundations of Computational Agents, 3rd ed.`, 확인 날짜: 2026-06-22.
- Usama Fayyad, Gregory Piatetsky-Shapiro, Padhraic Smyth, `From Data Mining to Knowledge Discovery in Databases`, AI Magazine, 1996, 확인 날짜: 2026-06-22.
- NIST, `Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile`, NIST AI 600-1, 2024-07, 확인 날짜: 2026-06-22.
- Wayne Xin Zhao et al., `A Survey of Large Language Models`, arXiv:2303.18223, 확인 날짜: 2026-06-22.
