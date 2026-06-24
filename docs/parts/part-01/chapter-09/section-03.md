# 9.3 LLM(large language model)의 직접 계보(direct lineage)와 주변 근거(surrounding evidence) 구분

9.1에서는 이미지 인식(image recognition)과 표현 학습(representation learning)을 봤습니다. 9.2에서는 객체 검출(object detection)과 음성 생성(speech generation)을 봤습니다.

이제 이 사례들을 LLM(large language model)의 역사와 어떻게 연결해야 하는지 정리합니다.

이 절의 질문은 다음입니다.

```text
AlexNet, YOLO, WaveNet 같은 사례는
LLM의 직접 조상인가,
아니면 딥러닝 패러다임이 넓어진 주변 근거인가?
```

> LLM의 직접 계보는 언어 모델링(language modeling), 순차 모델링(sequence modeling), Seq2Seq, Attention, Transformer 쪽에서 설명해야 한다. 이미지, 객체 검출, 음성 생성 사례는 직접 조상이 아니라 딥러닝 접근이 여러 분야에서 힘을 얻었다는 주변 근거로 두는 편이 안전하다.

이 절에는 한 가지 더 중요한 의도가 있습니다. 최근에는 AI라는 말을 곧바로 LLM이나 챗봇으로 이해하는 분위기가 강합니다. 이 책에서는 그 시각을 조심합니다. LLM은 현대 AI를 이해하는 데 매우 중요한 기술이지만, AI 전체를 LLM으로 환원하면 규칙 기반 AI, 탐색, 확률 모델, 컴퓨터 비전, 음성, 강화학습, 추천, 로보틱스 같은 다른 흐름이 가려집니다.

## 이 절의 역할과 범위

이 절은 LLM의 전체 역사를 자세히 쓰지 않습니다. 통계적 언어 모델(statistical language model), 단어 임베딩(word embedding), RNN(recurrent neural network), LSTM(long short-term memory), Seq2Seq(sequence-to-sequence), Attention, Transformer, 사전학습(pretraining), 지시 튜닝(instruction tuning), RLHF(reinforcement learning from human feedback)는 뒤의 LLM 장에서 더 자세히 다룹니다.

여기서는 Chapter 9의 마무리로 두 가지 역할만 맡습니다.

첫째, LLM의 직접 계보(direct lineage)를 언어 모델링(language modeling)과 순차 모델링(sequence modeling) 쪽에 놓습니다. 둘째, AI 전체를 LLM과 같은 뜻으로 줄여 말하지 않도록 경계를 둡니다.

따라서 이 절의 범위는 다음 구분을 잡는 일입니다.

```text
직접 계보:
언어와 순차 데이터를 다루는 모델 구조와 학습 흐름

주변 근거:
딥러닝이 이미지, 위치, 음성, 생성 문제에서도
수작업 규칙과 특징 설계를 줄이며 성과를 보인 사례
```

이 구분이 필요한 이유는 단순합니다. 모든 딥러닝 성공 사례를 LLM으로 곧장 이어 붙이면 역사 설명이 쉬워 보이지만, 원인과 배경이 섞입니다.

## 이 절의 목표

- 직접 계보(direct lineage)와 주변 근거(surrounding evidence)를 구분합니다.
- LLM의 직접 흐름을 언어 모델링(language modeling)과 순차 모델링(sequence modeling) 쪽에서 잡습니다.
- AlexNet, YOLO, WaveNet 같은 사례를 LLM의 직접 조상으로 과장하지 않습니다.
- AI 전체를 LLM으로 환원하지 않고, LLM을 AI 지형 안의 중요한 한 흐름으로 배치합니다.
- Transformer를 중요한 전환점으로 보되, Transformer 하나만으로 LLM 전체 역사를 설명하지 않습니다.
- 뒤의 LLM 장으로 넘어가기 위한 지도를 만듭니다.

## 먼저 구분하기: 직접 계보와 주변 근거

직접 계보(direct lineage)는 어떤 기술이 LLM의 핵심 문제와 구조를 설명하는 데 직접 필요한 흐름입니다. 생성형 LLM은 보통 언어를 토큰(token)의 순서로 다루고, 앞의 문맥(context)을 바탕으로 다음 토큰 후보의 확률 분포(probability distribution)를 계산하며, 학습된 파라미터(parameter)를 사용해 출력을 생성합니다.

여기서 토큰(token)은 사람이 읽는 단어(word)와 항상 같지 않습니다. 원래 token은 표식이나 증거에 가까운 뜻을 가진 말이고, LLM에서는 텍스트를 모델이 처리할 수 있도록 나눈 기본 단위를 가리킵니다. 토큰화(tokenization)와 임베딩(embedding)은 뒤의 LLM 장에서 다룹니다.

```text
문자열(text)
-> 토큰(token)
-> 다음 토큰 확률 분포
```

이 흐름은 앞에서 본 개념들과 완전히 끊어져 있지 않습니다. 이 책의 학습 흐름에서는 기호(symbol)를 컴퓨터가 구분할 수 있는 표식으로 본 관점이 토큰을 이해하는 데 도움을 주고, 특징(feature)과 표현(representation)은 원래 입력을 계산 가능한 형태로 바꾼다는 점에서 토큰화와 임베딩을 이해하는 준비가 됩니다.

다만 9.3의 중심은 토큰화 설명이 아닙니다. 이 절의 중심은 LLM의 직접 계보와 주변 근거를 구분하는 일입니다.

```text
앞 장의 연결:
기호, 라벨, 특징, 표현

이 절의 역할:
언어 모델링, Seq2Seq, Attention, Transformer가
LLM의 직접 계보에 놓인다는 지도 만들기
```

따라서 직접 계보는 다음 질문과 연결됩니다.

```text
단어와 문장을 어떻게 숫자로 표현할 것인가?
앞의 단어들을 보고 다음 단어를 어떻게 예측할 것인가?
긴 문맥에서 어떤 정보를 참고할 것인가?
이 구조를 큰 데이터와 큰 계산 자원으로 어떻게 학습할 것인가?
```

반면 주변 근거(surrounding evidence)는 LLM의 핵심 구조로 직접 이어지지는 않지만, 딥러닝이 강력한 연구 방향으로 받아들여지는 데 영향을 준 사례입니다.

| 구분 | 중심 질문 | 예시 |
| --- | --- | --- |
| 직접 계보(direct lineage) | 언어와 순차 데이터를 어떻게 모델링하는가? | 신경망 언어 모델, Seq2Seq, Attention, Transformer |
| 주변 근거(surrounding evidence) | 딥러닝이 여러 분야에서 왜 설득력을 얻었는가? | AlexNet, YOLO, WaveNet |

이 표에서 중요한 것은 “주변 근거는 덜 중요하다”가 아닙니다. 주변 근거는 LLM의 직접 조상은 아니지만, 딥러닝 패러다임이 넓게 확산된 배경을 보여 줍니다.

이 경계는 반대로도 중요합니다.

```text
AI 전체 -> LLM
```

이렇게 줄여 말하면 현재의 도구 경험은 설명하기 쉬워지지만, AI의 전체 역사는 좁아집니다. 9.3의 목적은 LLM을 작게 보려는 것이 아니라, LLM이 어떤 직접 계보 위에 있고 어떤 주변 근거 속에서 등장했는지 구분해 보는 것입니다.

## LLM에 가까운 자료들은 어디에 놓이는가

LLM의 조상처럼 보이는 자료는 여럿 있습니다. 다만 모두 같은 의미의 조상은 아닙니다.

| 자료 또는 흐름 | LLM과 가까운 이유 | 이 절에서의 위치 |
| --- | --- | --- |
| 신경망 언어 모델(neural language model) | 단어열의 확률과 단어 표현을 신경망으로 학습하는 흐름을 보여 줍니다. | 직접 계보의 출발점 |
| word2vec | 단어를 벡터 표현(vector representation)으로 학습하는 흐름을 널리 각인시켰습니다. | 표현 학습과 단어 임베딩의 중요한 전 단계 |
| Seq2Seq | 입력 순서에서 출력 순서로 가는 언어 처리 구조를 보여 줬습니다. | 직접 계보 |
| Attention | 출력 시점마다 관련 입력 위치를 참고하는 구조를 보여 줬습니다. | 직접 계보 |
| Transformer | Attention 중심 구조를 대규모 순차 모델링에 강하게 연결했습니다. | 현대 LLM의 핵심 구조 계열 |
| ELMo | 문맥에 따라 달라지는 단어 표현(contextualized word representation)을 제시했습니다. | 문맥화된 언어 표현의 전 단계 |
| ULMFiT | 사전학습된 언어 모델(pretrained language model)을 downstream task에 fine-tuning하는 흐름을 보여 줬습니다. | NLP 전이학습(transfer learning)의 중요한 전 단계 |
| BERT | Transformer 기반 사전학습(pre-training)과 fine-tuning 절차를 강하게 보여 줬습니다. | 현대 언어 표현 모델의 직접 배경 |
| GPT 계열 | Transformer decoder와 언어 모델링, 사전학습, 생성, scaling, in-context learning 흐름을 직접 보여 줍니다. | 현대 생성형 LLM에 매우 가까운 직접 계보 |

이 표는 LLM 역사를 모두 설명하려는 표가 아닙니다. 여기서는 이미지 인식이나 객체 검출보다 언어 모델링, 표현 학습, 사전학습, Transformer 계열 연구가 LLM 설명에 더 직접적이라는 경계만 잡습니다.

## 직접 계보 1: 언어 모델링

언어 모델링(language modeling)은 단어 또는 토큰의 순서를 확률적으로 다루는 문제입니다. Bengio 등은 통계적 언어 모델링(statistical language modeling)의 목표를 언어 안에서 단어열(word sequence)의 결합확률(joint probability)을 학습하는 것으로 설명했습니다. 이 논문은 동시에 단어의 분산 표현(distributed representation)을 학습해 차원의 저주(curse of dimensionality)를 줄이려는 방향을 제시했습니다.

입문 단계에서는 다음처럼 이해하면 충분합니다.

```text
언어 모델은 문장을 이해했다는 선언에서 출발하지 않는다.
먼저 단어와 토큰의 순서가 얼마나 그럴듯한지,
또 다음에 무엇이 올 가능성이 높은지를 계산하는 문제에서 출발한다.
```

여기서 “확률”은 정답을 맞힌다는 뜻이 아닙니다. 불확실한 다음 후보들에 점수를 주는 방식입니다. 이 관점은 6장에서 본 확률(probability), 불확실성(uncertainty), 확률적 과정(stochastic process)의 설명과 연결됩니다.

## 직접 계보 2: Seq2Seq

Seq2Seq(sequence-to-sequence)는 입력 시퀀스(input sequence)를 받아 출력 시퀀스(output sequence)를 만드는 구조입니다. 대표적 사례는 기계번역(machine translation)입니다. 현대 LLM이 모두 Seq2Seq 구조라는 뜻은 아니지만, Seq2Seq는 언어를 순차 입력과 순차 출력의 학습 문제로 다루는 흐름을 이해하게 해 주는 중요한 전 단계입니다.

Sutskever, Vinyals, Le의 Seq2Seq 논문은 LSTM(long short-term memory)이 일반적인 sequence-to-sequence 문제를 풀 수 있음을 보였고, 큰 deep LSTM을 사용해 영어 문장을 프랑스어 문장으로 번역하는 실험을 제시했습니다.

입문 관점에서 핵심은 다음입니다.

```text
입력 문장 전체를 읽는다.
그 문장을 내부 표현으로 바꾼다.
그 표현을 바탕으로 출력 문장을 순서대로 만든다.
```

이 구조는 LLM 그 자체도 아니고, 모든 LLM의 직접 구조도 아닙니다. 하지만 언어를 고정된 규칙 목록으로 처리하기보다, 입력 문장과 출력 문장의 대응을 신경망이 학습하는 방향을 보여 줍니다.

## 직접 계보 3: Attention

초기 encoder-decoder 구조에는 문제가 있었습니다. 긴 문장을 하나의 고정 길이 벡터(fixed-length vector)에 모두 담으려 하면 정보가 병목(bottleneck)에 걸릴 수 있습니다.

Bahdanau, Cho, Bengio의 Attention 논문은 이 문제를 줄이기 위해 번역을 생성하는 각 시점마다 입력 문장의 관련 부분을 참고하는 구조를 제안했습니다. 논문은 decoder가 source sentence의 어떤 부분에 주의를 기울일지 결정한다고 설명합니다.

입문 단계에서는 Attention을 다음처럼 볼 수 있습니다.

```text
출력 단어를 만들 때마다
입력 전체를 뭉뚱그려 기억하는 것이 아니라,
지금 필요한 입력 위치를 더 강하게 참고한다.
```

여기서 Attention은 사람이 의식적으로 “주의를 기울인다”는 심리 설명과 같지 않습니다. 모델 내부에서 입력 위치별 가중치(weight)를 계산해 관련 정보를 더 많이 쓰는 기계적 구조로 보는 편이 안전합니다.

## 직접 계보 4: Transformer

Transformer는 Attention 흐름의 중요한 전환점입니다. Vaswani 등의 논문은 기존의 강한 sequence transduction 모델들이 recurrent neural network나 convolutional neural network에 기반하고 encoder와 decoder를 포함한다고 설명한 뒤, recurrence와 convolution을 배제하고 attention mechanism에 기반한 Transformer를 제안했습니다.

중요한 점은 두 가지입니다.

| 관점 | 의미 |
| --- | --- |
| self-attention | 한 시퀀스 안의 여러 위치가 서로를 참고해 표현을 만든다 |
| 병렬화(parallelization) | RNN처럼 순서대로만 처리하는 부담을 줄여 큰 데이터 학습에 유리해진다 |

Transformer 논문은 모델이 recurrence와 convolution 없이 attention만으로 sequence transduction을 수행할 수 있음을 보였고, 더 병렬화하기 쉽다고 설명했습니다.

하지만 여기서도 과장은 피해야 합니다.

```text
Transformer -> 곧바로 현대 LLM
```

이렇게 쓰면 너무 짧습니다. 현대 생성형 LLM은 Transformer 계열 구조만이 아니라 대규모 데이터, 사전학습(pretraining), 토큰화(tokenization), 스케일링(scaling), 학습 안정화, 그리고 제품이나 연구 흐름에 따라 지시 튜닝(instruction tuning), RLHF 같은 정렬(alignment) 기법이 결합된 결과로 봐야 합니다.

## 주변 근거는 딥러닝의 설득력을 만들었다

9.1과 9.2의 사례는 LLM의 직접 계보라기보다 딥러닝 패러다임이 여러 분야로 확산되었다는 주변 근거로 두는 편이 안전합니다.

| 사례 | 직접 계보인가? | 이 장에서의 역할 |
| --- | --- | --- |
| AlexNet | 아니오 | 이미지 인식에서 대규모 데이터, 깊은 CNN, GPU, 학습 기법의 결합을 보여 준 전환점 |
| YOLO | 아니오 | 객체 검출을 단일 신경망 예측 문제로 재구성한 사례 |
| WaveNet | 아니오 | raw audio를 확률적 순차 생성 문제로 다룬 사례 |

이 구분을 통해 다음 문장을 더 안전하게 쓸 수 있습니다.

```text
LLM은 이미지 인식이나 객체 검출에서 직접 태어난 것이 아니다.
그러나 2010년대 여러 분야의 딥러닝 성공은
대규모 데이터, 계산 자원, 표현 학습, end-to-end 학습이
강력한 방향이라는 믿음을 강화했다.
그 배경 위에서 언어 모델링과 Transformer 계열 연구가 커졌다.
```

## 피해야 할 축약

이 절에서 특히 피해야 할 축약은 다음입니다.

| 피할 표현 | 문제 | 더 안전한 표현 |
| --- | --- | --- |
| AI는 곧 LLM이다 | AI의 여러 연구 흐름과 응용 분야가 사라짐 | LLM은 현대 AI의 중요한 흐름이지만 AI 전체와 같은 말은 아니다 |
| AlexNet이 LLM을 만들었다 | 이미지 분류와 언어 모델링의 직접 계보가 섞임 | AlexNet은 딥러닝 확산의 대표 전환점이다 |
| YOLO가 LLM 발전을 이끌었다 | 객체 검출 모델을 직접 조상처럼 보이게 함 | YOLO는 end-to-end 예측 문제 재구성의 사례다 |
| WaveNet이 LLM의 조상이다 | 음성 파형 생성과 언어 모델링을 혼동함 | WaveNet은 확률적 순차 생성의 주변 사례다 |
| Transformer만 알면 LLM 역사를 설명할 수 있다 | 사전학습, 데이터, 스케일링, 정렬이 빠짐 | Transformer는 핵심 구조지만 전체 역사는 더 넓다 |

이 장에서 원하는 설명은 “모든 것이 LLM으로 직선 연결된다”가 아닙니다. 더 적절한 설명은 다음입니다.

```text
딥러닝은 여러 분야에서 표현을 학습하고 출력을 예측하거나 생성하는 방식으로 확산되었다.
LLM은 그중 언어 모델링과 순차 모델링의 직접 계보 위에서 성장했다.
```

## 이 절에서 기억할 관점

LLM의 역사를 설명할 때는 직접 계보와 주변 근거를 나눠야 합니다. 직접 계보는 언어 모델링, Seq2Seq, Attention, Transformer처럼 언어와 순차 데이터를 다루는 구조입니다. 주변 근거는 AlexNet, YOLO, WaveNet처럼 딥러닝이 여러 분야에서 성공하면서 연구자와 산업계가 대규모 신경망 접근을 더 강하게 받아들이게 된 배경입니다.

이 구분은 사용자의 직관을 버리기 위한 것이 아닙니다. 오히려 직관을 더 안전한 문장으로 바꾸기 위한 장치입니다.

```text
생성형 AI와 LLM은 갑자기 등장한 기술이 아니다.
다만 그 직접 계보는 이미지나 객체 검출이 아니라,
언어 모델링과 순차 모델링의 발전사에서 찾아야 한다.
이미지, 음성, 객체 검출 사례는 딥러닝 패러다임이 확산된 배경으로 함께 읽는다.
```

## 체크리스트

- 직접 계보(direct lineage)와 주변 근거(surrounding evidence)를 구분할 수 있다.
- LLM의 직접 흐름을 언어 모델링(language modeling), Seq2Seq, Attention, Transformer 쪽에서 설명할 수 있다.
- AlexNet, YOLO, WaveNet을 LLM의 직접 조상으로 쓰지 않을 수 있다.
- Transformer를 중요한 전환점으로 보되, LLM 전체 역사를 Transformer 하나로 축약하지 않을 수 있다.
- 딥러닝 패러다임의 확산과 LLM의 직접 발전사를 함께 설명하되 혼동하지 않을 수 있다.
- AI 전체를 LLM과 같은 뜻으로 쓰지 않을 수 있다.

## 출처와 참고 자료

- Yoshua Bengio, Rejean Ducharme, Pascal Vincent, Christian Jauvin, [A Neural Probabilistic Language Model](https://jmlr.org/papers/v3/bengio03a.html), Journal of Machine Learning Research, 2003, 확인 날짜: 2026-06-23.
- Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean, [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781), arXiv, 2013, 확인 날짜: 2026-06-23.
- Ilya Sutskever, Oriol Vinyals, Quoc V. Le, [Sequence to Sequence Learning with Neural Networks](https://arxiv.org/abs/1409.3215), arXiv, 2014, 확인 날짜: 2026-06-23.
- Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio, [Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473), arXiv, 2014, 확인 날짜: 2026-06-23.
- Ashish Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), arXiv, 2017, 확인 날짜: 2026-06-23.
- Matthew E. Peters et al., [Deep contextualized word representations](https://arxiv.org/abs/1802.05365), arXiv, 2018, 확인 날짜: 2026-06-23.
- Jeremy Howard, Sebastian Ruder, [Universal Language Model Fine-tuning for Text Classification](https://arxiv.org/abs/1801.06146), arXiv, 2018, 확인 날짜: 2026-06-23.
- Alec Radford et al., [Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), OpenAI, 2018, 확인 날짜: 2026-06-23.
- Jacob Devlin et al., [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805), arXiv, 2018, 확인 날짜: 2026-06-23.
- Alec Radford et al., [Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf), OpenAI, 2019, 확인 날짜: 2026-06-23.
- Tom B. Brown et al., [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165), arXiv, 2020, 확인 날짜: 2026-06-23.
- Yann LeCun, Yoshua Bengio, Geoffrey Hinton, [Deep learning](https://www.nature.com/articles/nature14539), Nature 521, 436-444, 2015-05-27, 확인 날짜: 2026-06-23.
