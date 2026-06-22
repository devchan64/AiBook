# 2007년 AI 학습 기억의 일반화

## 목적

이 문서는 사용자가 2007년 무렵 인공지능을 학습하며 기억한 흐름을 표준적인 AI 역사 설명과 연결하기 위한 관리 메모입니다.

이 내용은 현재 1.1절 `AI라는 말의 범위`에 길게 넣지 않습니다. 주로 다음 Section과 Chapter로 분리해 다룹니다.

- Chapter 2. AI의 역사와 패러다임 변화
- Chapter 7. 탐색과 휴리스틱
- Chapter 8. 지도학습, 비지도학습, 강화학습
- Chapter 9. 딥러닝 패러다임의 확산
- Chapter 11. LLM은 어디에서 왔는가

## 사용자의 기억

사용자는 2007년 무렵 AI를 학습할 때 다음과 같이 기억하고 있습니다.

- 휴리스틱(heuristic) 기반 접근이 중요한 기반에 있었다.
- 강화학습(reinforcement learning)이 유행하던 시기로 기억한다.
- 시냅스 기반의 인공지능, 즉 신경망(neural network) 계열 AI가 시작되던 시기로 기억한다.
- 빅데이터(big data)와 데이터마이닝(data mining)이 함께 중요한 키워드로 등장하던 시기로 기억한다.
- 의사결정지원시스템(DSS, decision support system), 비즈니스 인텔리전스(BI, business intelligence), 데이터 웨어하우스(DW, data warehouse), OLAP 같은 대규모 데이터 지원 서비스 분야의 확장도 요구되던 시기로 기억한다.
- AI라는 의미에는 규칙 기반 판단에서 데이터 기반 판단으로 넘어가는 변화가 의미론적으로 담겨 있다고 이해한다.
- 이 구분은 비슷하지만 다른 AI 접근들을 설명하는 기준으로 남아 있다.

## 표준 설명으로 보정한 요약

이 기억은 다음처럼 보정할 수 있습니다.

> 2007년 전후의 AI 학습 환경에서는 여전히 탐색(search), 휴리스틱(heuristics), 지식 표현(knowledge representation), 확률적 추론(probabilistic reasoning), 머신러닝(machine learning), 강화학습(reinforcement learning)이 함께 다뤄졌다. 동시에 데이터마이닝(data mining), KDD(knowledge discovery in databases), 대규모 데이터 처리(big data processing), 의사결정지원시스템(DSS), 비즈니스 인텔리전스(BI), 데이터 웨어하우스(DW), OLAP이 산업과 연구 현장에서 중요한 키워드로 커지고 있었다. 신경망(neural networks)은 새로 시작된 분야가 아니라 오래된 연구 전통이었지만, 2006년 전후 딥 빌리프 네트워크(deep belief networks)와 표현 학습(representation learning) 연구를 계기로 딥러닝(deep learning) 부흥의 초기 신호가 나타났다. 대중적·산업적 전환점은 2012년 이후 이미지 인식과 음성 인식 성과를 통해 더 뚜렷해졌다.

## 세 접근의 차이

| 접근 | 중심 질문 | 대표 표현 | 2007년 전후 위치 |
| --- | --- | --- | --- |
| 탐색과 휴리스틱 | 가능한 해가 너무 많을 때 어디부터 볼 것인가 | search, heuristic search, planning | 전통 AI 개론의 핵심 축 |
| 데이터마이닝과 빅데이터 | 많은 데이터에서 어떤 패턴과 지식을 뽑을 것인가 | data mining, KDD, big data, MapReduce, Hadoop | 2000년대 웹 데이터와 분산 처리 인프라 확산과 함께 부상 |
| 의사결정 지원과 BI | 데이터를 어떻게 경영·운영 판단으로 연결할 것인가 | DSS, BI, DW, OLAP, dashboard, reporting | 기업 시스템에서 데이터 기반 의사결정 요구가 커지던 축 |
| 강화학습 | 행동의 결과가 나중에 보상으로 돌아올 때 어떻게 배울 것인가 | agent, state, action, reward, policy | 이미 확립된 연구 분야였고, 교재와 연구에서 중요하게 다뤄짐 |
| 신경망과 딥러닝 | 데이터에서 표현과 가중치를 어떻게 학습할 것인가 | neural network, weights, representation, deep learning | 신경망은 오래된 분야, 딥러닝은 2006년 전후 부흥 초기 |

## 휴리스틱은 무엇이었나

휴리스틱은 “불확실성을 확률로 직접 모델링한다”기보다, 탐색 공간(search space)이 너무 커서 모든 가능성을 계산할 수 없을 때 더 그럴듯한 후보를 먼저 보게 해주는 경험적 기준입니다.

예를 들어 게임, 퍼즐, 경로 찾기, 계획 문제에서 가능한 다음 상태를 모두 탐색하면 계산량이 폭발합니다. 휴리스틱은 이때 “정답을 보장하지는 않지만, 좋은 방향으로 탐색을 줄이는 규칙”으로 쓰입니다.

따라서 사용자의 “불확실성을 소프트웨어에 반영하려는 시도”라는 직관은 일부 맞습니다. 다만 표준적으로는 다음처럼 나누는 것이 안전합니다.

- 휴리스틱: 계산 한계 때문에 탐색을 줄이는 경험적 판단 기준
- 확률 모델: 불확실성을 수학적으로 표현하고 추론하는 모델
- 강화학습: 시행착오와 보상으로 행동 정책을 학습하는 틀
- 딥러닝: 많은 데이터에서 표현과 가중치를 학습하는 신경망 기반 방법

## 빅데이터와 데이터마이닝은 왜 함께 기억되는가

2007년 전후는 웹 서비스, 검색, 광고, 로그 분석, 추천 시스템이 커지면서 데이터 자체가 중요한 자산으로 인식되던 시기였습니다. 이때 `데이터마이닝(data mining)`은 많은 데이터에서 패턴(pattern), 규칙(rule), 군집(cluster), 예측 모델(predictive model)을 찾는 실무적·학문적 키워드로 널리 쓰였습니다.

데이터마이닝은 2007년에 새로 생긴 말은 아닙니다. KDD(knowledge discovery in databases)와 데이터마이닝 연구는 1990년대부터 이미 중요한 분야였고, 1996년 Fayyad, Piatetsky-Shapiro, Smyth의 글처럼 데이터에서 지식을 발견하는 과정으로 정리되어 왔습니다.

다만 2000년대 중반에는 데이터 규모와 처리 방식이 달라졌습니다. Google의 MapReduce 논문은 2004년에 발표되었고, Hadoop은 2006년 Apache 프로젝트로 분리되어 대규모 데이터를 분산 처리하는 오픈소스 흐름을 만들었습니다. 그래서 2007년 전후의 학습 기억에서 빅데이터와 데이터마이닝이 함께 등장하는 것은 자연스럽습니다.

이 흐름은 AI와 다음처럼 연결됩니다.

- 데이터마이닝은 “데이터에서 패턴을 발견한다”는 실무적 문제의식을 제공했습니다.
- 빅데이터는 더 많은 데이터와 더 큰 처리 인프라가 필요하다는 조건을 만들었습니다.
- 머신러닝은 발견한 패턴을 예측과 분류 모델로 연결했습니다.
- 딥러닝은 대규모 데이터와 병렬 계산이 충분해지면서 표현 학습을 크게 확장했습니다.

따라서 “빅데이터와 데이터마이닝이 함께 등장하던 시기”라는 기억은 AI가 규칙과 탐색 중심 설명에서 데이터 중심 설명으로 이동하던 배경을 이해하는 데 중요합니다.

## DSS, BI, DW/OLAP은 어떤 위치였나

의사결정지원시스템(DSS, decision support system), 비즈니스 인텔리전스(BI, business intelligence), 데이터 웨어하우스(DW, data warehouse), OLAP(online analytical processing)은 AI 모델 자체라기보다 데이터를 의사결정에 사용할 수 있게 만드는 기업 정보 시스템의 계층입니다.

2000년대 중반의 실무 환경에서는 다음 요구가 커지고 있었습니다.

- 여러 업무 시스템에 흩어진 데이터를 모아야 한다.
- 과거 데이터를 분석해 경영과 운영 판단에 써야 한다.
- 보고서(reporting), 대시보드(dashboard), 다차원 분석(OLAP)을 통해 의사결정자가 데이터를 직접 볼 수 있어야 한다.
- 데이터마이닝과 예측 분석을 통해 단순 집계보다 더 나은 판단 근거를 만들고 싶어 했다.
- 웹 기반 분석, 실시간 또는 준실시간 분석, 대규모 데이터 저장과 처리가 요구되기 시작했다.

이 흐름은 AI와 직접 동일하지는 않지만, 현대 AI 서비스의 배경이 됩니다. AI가 좋은 모델을 만들려면 데이터 수집, 저장, 정제, 통합, 품질 관리, 분석 환경이 필요합니다. DSS/BI/DW/OLAP은 이런 데이터 기반 의사결정 문화와 인프라를 확산시킨 축이었습니다.

따라서 책에서는 다음처럼 구분합니다.

| 층위 | 중심 역할 | AI와의 관계 |
| --- | --- | --- |
| DSS/BI | 의사결정자가 데이터를 보고 판단하도록 지원 | 모델 결과를 사람이 해석하고 운영 판단에 쓰는 접점 |
| DW/OLAP | 데이터를 통합·저장하고 다차원으로 분석 | 학습 데이터와 분석 데이터의 기반 인프라 |
| 데이터마이닝 | 데이터에서 패턴과 지식을 발견 | 머신러닝, 통계, 데이터베이스가 만나는 분석 방법 |
| 머신러닝/AI | 데이터로부터 예측, 분류, 추천, 생성 모델을 학습 | 의사결정 지원을 자동화하거나 보강하는 모델 계층 |

이 관점에서 2007년 기억은 “AI 알고리즘의 역사”만이 아니라 “데이터를 의사결정으로 연결하려던 정보 시스템의 역사”와 함께 읽어야 합니다.

## AI라는 말에 담긴 의미 변화

사용자의 “AI라는 의미는 규칙에서 데이터 기반으로 넘어가는 판단들이 의미론적으로 담겨 있다”는 표현은 중요한 작업 가설입니다.

다만 엄밀하게는 `AI`라는 단어 자체가 처음부터 데이터 기반 판단을 뜻했던 것은 아닙니다. 초기 AI에는 논리(logic), 규칙(rule), 탐색(search), 지식 표현(knowledge representation), 전문가 시스템(expert system)처럼 사람이 명시적으로 구조를 설계하는 접근이 강하게 포함되어 있었습니다.

이후 데이터가 많아지고 계산 자원이 커지면서 AI의 중심 설명은 점점 다음 방향으로 이동했습니다.

| 시기적 층위 | 판단을 만드는 방식 | 대표 표현 |
| --- | --- | --- |
| 규칙 중심 | 사람이 규칙과 지식을 명시적으로 작성 | rule-based AI, symbolic AI, expert system |
| 탐색과 휴리스틱 | 가능한 후보를 탐색하되 경험적 기준으로 줄임 | search, heuristic, planning |
| 확률과 통계 | 불확실성을 확률 모델로 표현 | probabilistic reasoning, Bayesian network |
| 데이터마이닝과 머신러닝 | 데이터에서 패턴과 예측 규칙을 찾음 | data mining, machine learning |
| 딥러닝 | 데이터에서 표현과 가중치를 계층적으로 학습 | representation learning, deep learning |
| 생성형 AI와 LLM | 대규모 데이터와 모델로 다음 출력과 콘텐츠를 생성 | generative AI, language model, LLM |

따라서 책에서는 이 작업 가설을 다음처럼 일반화합니다.

> 현대 독자가 AI라는 말을 들을 때는 단순히 “사람처럼 행동하는 기계”만 떠올리는 것이 아니라, 규칙을 사람이 직접 쓰던 방식에서 데이터로부터 판단 기준을 학습하는 방식으로 이동한 역사적 층위까지 함께 읽게 된다.

이 문장은 `표준적 설명`이라기보다 `작업 가설을 보정한 설명`으로 둡니다. 실제 본문에서는 사전적 의미, 역사적 변화, 현재 산업적 사용을 구분해야 합니다.

1. 사전적 의미: 인간 지능과 관련된 기능을 수행하는 컴퓨터 시스템 또는 분야
2. 역사적 변화: 규칙, 탐색, 확률, 데이터 학습, 딥러닝으로 중심 접근이 확장된 흐름
3. 현재 사용: 생성형 AI, LLM, 추천 시스템, 자동화 서비스까지 포괄하는 넓은 산업 용어

이 구분을 유지하면 “AI라는 말 자체”를 과도하게 해석하지 않으면서도, 사용자가 기억하는 규칙 기반 AI에서 데이터 기반 AI로의 전환을 책의 핵심 설명 흐름으로 살릴 수 있습니다.

## 강화학습은 왜 기억에 남았나

강화학습은 1990년대에 이미 중요한 연구 분야로 정리되어 있었습니다. Sutton과 Barto의 `Reinforcement Learning: An Introduction` 초판은 1998년에 출간되었고, 2000년대 AI·머신러닝 학습에서 강화학습은 에이전트(agent), 상태(state), 행동(action), 보상(reward), 정책(policy)을 설명하는 대표 틀이었습니다.

다만 2007년의 강화학습은 지금 대중에게 알려진 “딥 강화학습(deep reinforcement learning)”의 전성기와는 다릅니다. 딥러닝과 결합해 Atari, AlphaGo 같은 사례로 널리 알려진 흐름은 2010년대에 더 뚜렷해졌습니다.

## 시냅스 기반 AI라는 기억의 보정

“시냅스 기반 AI”라는 표현은 신경망의 가중치(weights)를 생물학적 시냅스(synapse)에 비유한 기억으로 볼 수 있습니다.

하지만 신경망 연구는 2007년에 시작된 것이 아닙니다. 퍼셉트론(perceptron), 역전파(backpropagation), 연결주의(connectionism)는 그보다 훨씬 이전부터 존재했습니다. 2007년 전후에 새로웠던 것은 “깊은 층을 가진 신경망을 더 잘 학습할 수 있을 것 같다”는 딥러닝 부흥의 초기 흐름입니다.

2006년 Hinton, Osindero, Teh의 딥 빌리프 네트워크 연구는 여러 은닉층을 가진 모델을 층별로 학습하는 빠른 방법을 제시했고, 이후 표현 학습과 딥러닝 흐름의 중요한 전환점으로 자주 언급됩니다.

## 책에서 사용할 설명 방향

책에서는 이 기억을 다음 구조로 일반화합니다.

1. 전통 AI는 탐색, 규칙, 지식 표현, 휴리스틱을 통해 문제를 풀려고 했다.
2. 확률적 추론은 불확실한 정보를 수학적으로 다루는 별도 축으로 발전했다.
3. DSS, BI, DW/OLAP은 데이터를 의사결정으로 연결하는 기업 정보 시스템의 기반을 만들었다.
4. 데이터마이닝과 빅데이터는 데이터에서 패턴을 찾고 대규모로 처리하는 실무적 흐름을 만들었다.
5. 머신러닝은 사람이 규칙을 모두 쓰기보다 데이터에서 관계를 학습하는 방향을 강화했다.
6. 강화학습은 환경과 상호작용하면서 보상을 최대화하는 행동 방식을 학습하는 틀을 제공했다.
7. 신경망과 딥러닝은 데이터에서 표현(representation)과 가중치(weights)를 학습하는 흐름을 크게 확장했다.
8. LLM은 이 중 딥러닝, 표현 학습, 대규모 데이터, 병렬 계산, 언어 모델링의 흐름 위에서 등장했다.

## 주의할 표현

| 피할 표현 | 이유 | 권장 표현 |
| --- | --- | --- |
| 2007년에 시냅스 기반 AI가 시작되었다 | 신경망 연구는 훨씬 이전부터 존재 | 2006년 전후 딥러닝 부흥의 초기 신호가 나타났다 |
| 휴리스틱은 확률이다 | 휴리스틱과 확률 모델은 다름 | 휴리스틱은 탐색을 줄이는 경험적 기준이고, 확률 모델은 불확실성을 수학적으로 표현한다 |
| 빅데이터가 곧 AI다 | 데이터 규모와 AI 모델링은 다른 층위 | 빅데이터는 대규모 데이터 처리 조건이고, AI는 그 데이터를 사용해 문제를 푸는 모델과 시스템을 포함한다 |
| 데이터마이닝과 머신러닝은 같다 | 겹치지만 목적과 역사적 맥락이 다름 | 데이터마이닝은 데이터에서 지식과 패턴을 발견하는 과정이고, 머신러닝은 경험 데이터로 성능을 개선하는 모델 학습에 초점을 둔다 |
| DSS/BI가 곧 AI다 | 의사결정 지원 시스템과 AI 모델은 층위가 다름 | DSS/BI는 데이터를 의사결정에 연결하는 시스템이고, AI는 그 안에서 예측·추천·자동화를 맡을 수 있는 모델 계층이다 |
| AI라는 단어 자체가 데이터 기반 판단을 뜻한다 | 초기 AI에는 규칙, 논리, 탐색 중심 접근도 포함됨 | 현대 AI 이해에는 규칙 기반에서 데이터 기반으로 확장된 역사적 층위가 함께 읽힌다 |
| 강화학습이 2007년에 처음 유행했다 | RL은 1990년대 이전부터 연구됨 | 2000년대 AI 학습에서 강화학습은 중요한 축으로 다뤄졌다 |
| 딥러닝은 LLM으로 바로 이어졌다 | 중간에 CNN, 음성 인식, seq2seq, attention, Transformer 등 여러 계보가 있음 | LLM은 딥러닝 확산과 NLP 계보가 만난 결과로 설명한다 |

## 출처와 참고 자료

- Stuart Russell, Peter Norvig, [Artificial Intelligence: A Modern Approach, 4th US ed.](https://aima.cs.berkeley.edu/), 확인 날짜: 2026-06-22.
- Geoffrey E. Hinton, Simon Osindero, Yee-Whye Teh, [A fast learning algorithm for deep belief nets](https://www.cs.toronto.edu/~hinton/absps/fastnc.pdf), Neural Computation, 2006, 확인 날짜: 2026-06-22.
- Yann LeCun, Yoshua Bengio, Geoffrey Hinton, [Deep learning](https://www.nature.com/articles/nature14539), Nature, 2015-05-27, 확인 날짜: 2026-06-22.
- L. P. Kaelbling, M. L. Littman, A. W. Moore, [Reinforcement Learning: A Survey](https://arxiv.org/abs/cs/9605103), 1996, 확인 날짜: 2026-06-22.
- Richard S. Sutton, Andrew G. Barto, `Reinforcement Learning: An Introduction`, MIT Press, 1998.
- Usama M. Fayyad, Gregory Piatetsky-Shapiro, Padhraic Smyth, `From Data Mining to Knowledge Discovery in Databases`, AI Magazine, 1996.
- Jeffrey Dean, Sanjay Ghemawat, `MapReduce: Simplified Data Processing on Large Clusters`, OSDI, 2004.
- Apache Hadoop, [History](https://hadoop.apache.org/), 확인 날짜: 2026-06-22.
- D. J. Power, `A Brief History of Decision Support Systems`, DSSResources.COM, 2007.
- William H. Inmon, `Building the Data Warehouse`, QED Technical Publishing Group, 1992.
- Surajit Chaudhuri, Umeshwar Dayal, Vivek Narasayya, `An Overview of Business Intelligence Technology`, Communications of the ACM, 2011.
