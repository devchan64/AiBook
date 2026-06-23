# 1.3 Section 근거 분석

## 목적

이 문서는 `docs/chapters/chapter-01/section-03.md`의 핵심 주장과 참고 자료가 실제로 연결되는지 검토한 관리 메모입니다.

원문 확인 규칙에 따라 가능한 자료는 `.tmp/section-01-evidence/`와 `.tmp/section-03-evidence/` 아래에 임시로 내려받아 확인했습니다. `.tmp/`의 원문 파일은 근거 검토용이며 저장소에 커밋하지 않습니다.

## 원문 확인 상태

| 자료 | 로컬 확인 상태 | 1.3에서의 역할 |
| --- | --- | --- |
| OECD.AI, `Updates to the OECD’s definition of an AI system explained` | HTML 다운로드 확인 | AI를 입력, 목표, 출력, 환경 영향 관점으로 보는 기본 범위 근거 |
| Stanford Encyclopedia of Philosophy, `Artificial Intelligence` | HTML 다운로드 확인 | 머신러닝, 지도학습·비지도학습·강화학습, 신경망, 딥러닝, 표현 학습 설명의 근거 |
| AIMA 공식 사이트 | HTML 다운로드 확인 | AI 교재 목차에서 머신러닝, 딥러닝, NLP, 컴퓨터 비전, 로보틱스가 AI의 하위 주제로 배치되는 보조 근거 |
| NIST, `Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile` | PDF 다운로드 및 텍스트 추출 확인 | 생성형 AI 정의, LLM을 생성형 AI 관련 공통 활동으로 언급하는 근거 |
| Zhao et al., `A Survey of Large Language Models` | PDF 다운로드 및 텍스트 추출 확인 | LLM이 대규모 사전학습 언어 모델 계열이며, Transformer, 대규모 코퍼스, 파라미터 규모와 연결된다는 설명의 근거 |

## 본문 주장별 검토

| 본문 위치 | 핵심 주장 | 근거 연결 | 판정 |
| --- | --- | --- | --- |
| `section-03.md:5` | 이 절은 용어의 완전한 포함 관계보다 층위(level) 구분을 목적으로 한다 | 1.1, 1.2의 연장선인 저자적 구조화. AIMA 목차와 SEP가 AI 안에 다양한 접근을 배치함 | 유지 가능 |
| `section-03.md:15-23` | AI는 가장 넓은 말이고, 머신러닝·딥러닝·생성형 AI·LLM은 서로 다른 층위(level)의 용어다 | OECD의 AI 시스템 정의, SEP의 machine learning/deep learning 설명, NIST의 생성형 AI 정의, Zhao et al.의 LLM 설명이 연결됨 | 유지 가능 |
| `section-03.md:19` | 딥러닝은 머신러닝 안에서 깊은 신경망과 표현 학습을 사용하는 접근이다 | SEP는 deep neural networks, feature representation, deep learning을 설명함 | 유지 가능 |
| `section-03.md:21` | 생성형 AI는 출력의 성격에 가까운 말이고, 딥러닝과 같은 말이 아니다 | NIST는 생성형 AI를 입력 데이터의 구조와 특성을 모방해 합성 콘텐츠를 생성하는 모델 범주로 설명함. 딥러닝과 생성형 AI의 층위(level) 구분은 저자적 정리 | 유지 가능 |
| `section-03.md:23` | LLM은 생성형 AI의 대표 기술 중 하나이지만 생성형 AI 전체는 아니다 | Zhao et al.은 LLM을 큰 규모의 사전학습 언어 모델로 설명함. NIST는 생성형 AI 프로파일에서 LLM을 공통 활동 예로 언급하고, 생성형 AI 출력 예로 이미지, 영상, 오디오, 텍스트 등을 제시함 | 유지 가능 |
| `section-03.md:25-48` | 도식은 학습용 지도이며 실제 경계는 복잡하다 | AIMA와 SEP는 AI 안에 여러 접근이 병렬로 존재함을 보여주고, NIST는 생성형 AI가 LLM뿐 아니라 다양한 콘텐츠를 포함함을 보여줌 | 도식의 과도한 포함 관계를 완화 |
| `section-03.md:50-62` | 용어를 같은 층위(level)로 보지 않아야 한다 | 근거 자료들을 바탕으로 한 학습용 정리 | 유지 가능 |
| `section-03.md:64-82` | 단순 포함 관계에는 예외가 있다 | 규칙 기반 AI, 딥러닝의 비생성 과업, 생성형 AI의 다양한 출력은 자료와 일반적 기술 구분으로 뒷받침됨 | 유지 가능 |
| `section-03.md:84-96` | 실제 구현 확인 전에는 “가능”, “대개”, “보통”으로 표현해야 한다 | 서비스 내부 구조는 자료만으로 확정할 수 없으므로 신중한 표현으로 적절함 | 유지 가능 |

## 일반화 문구

사용자의 재학습 관점에서는 다음처럼 정리할 수 있습니다.

> AI는 가장 넓은 문제 해결 분야이고, 머신러닝은 그 안에서 데이터나 경험으로 판단 기준을 학습하는 접근이다. 딥러닝은 머신러닝 안에서 깊은 신경망과 표현 학습을 사용하는 방법이며, 생성형 AI는 새 콘텐츠를 생성하는 모델과 서비스 범주에 가깝다. LLM은 생성형 AI 시대를 대표하는 언어 모델 계열이지만, AI 전체나 생성형 AI 전체와 같은 말은 아니다.

## 추가 보강 필요

- 생성형 AI와 LLM의 관계는 Part 5에서 OpenAI, Google, Anthropic 등 제품 문서가 아니라 우선 교과서성 NLP 자료와 논문 계보로 다시 정리합니다.
- `AI > 머신러닝 > 딥러닝 > 생성형 AI > LLM` 도식은 학습용 단순화입니다. 특히 생성형 AI는 출력 성격과 서비스 범주에 가까우므로 딥러닝의 단순 하위 단계로 단정하지 않습니다.
- LLM을 “추론한다”고 표현할 때는 `inference`와 `reasoning`을 구분해야 합니다.

## 출처와 참고 자료

- OECD.AI, Stuart Russell, Karine Perset, Marko Grobelnik, [Updates to the OECD’s definition of an AI system explained](https://oecd.ai/en/wonk/ai-system-definition-update), 2023-11-29, 확인 날짜: 2026-06-22.
- Stanford Encyclopedia of Philosophy, Selmer Bringsjord and Naveen Sundar Govindarajulu, [Artificial Intelligence](https://plato.stanford.edu/entries/artificial-intelligence/), 2018-07-12, 확인 날짜: 2026-06-22.
- Stuart Russell, Peter Norvig, [Artificial Intelligence: A Modern Approach, 4th US ed.](https://aima.cs.berkeley.edu/), 확인 날짜: 2026-06-22.
- NIST, [Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile](https://doi.org/10.6028/NIST.AI.600-1), NIST AI 600-1, 2024-07, 확인 날짜: 2026-06-22.
- Wayne Xin Zhao et al., [A Survey of Large Language Models](https://arxiv.org/abs/2303.18223), arXiv:2303.18223, 확인 날짜: 2026-06-22.
