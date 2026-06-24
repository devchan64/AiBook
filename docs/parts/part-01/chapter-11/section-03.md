# 11.3 Transformer와 사전학습 LLM(pretrained LLM)

11.1에서는 언어 모델(language model)과 임베딩(embedding)을 봤고, 11.2에서는 RNN, Seq2Seq, Attention이 순서와 문맥을 다루는 흐름을 봤습니다.

이번 절에서는 현대 LLM(large language model)의 직접 계보를 만들었던 두 가지 전환을 봅니다.

> Attention을 중심 구조로 올려놓은 Transformer
> 대규모 텍스트로 먼저 학습하는 사전학습(pretraining)

이 절의 질문은 다음입니다.

> Attention이 중요해졌다면,
> 현대 LLM은 어떻게 Transformer와 사전학습 위에서 커졌는가?

입문 단계에서는 다음 흐름이 중요합니다.

> Transformer는 self-attention을 중심에 놓아 시퀀스 안의 토큰들이 서로를 직접 참고하게 했고, 사전학습 LLM은 대규모 텍스트에서 언어 패턴을 먼저 학습한 뒤 fine-tuning이나 prompt, in-context learning 방식으로 여러 과업에 연결되었다.

## 이 절의 범위

이 절은 Transformer의 수식, multi-head attention의 내부 계산, 대규모 학습 인프라를 자세히 설명하지 않습니다. 그런 내용은 딥러닝 구조와 LLM 심화에서 다시 다루는 편이 안전합니다.

여기서는 다음 질문에만 집중합니다.

| 주제 | 이 절에서 볼 질문 |
| --- | --- |
| Transformer | 왜 Attention이 모델의 중심 구조가 되었는가? |
| Encoder와 Decoder | BERT와 GPT 계열은 왜 다르게 쓰이는가? |
| 사전학습(pretraining) | 모델은 왜 먼저 큰 텍스트에서 학습되는가? |
| 문맥 내 학습(in-context learning) | 왜 prompt 안의 예시가 모델 행동을 바꿀 수 있는가? |

이 절은 prompt engineering, RAG(retrieval-augmented generation), vector search, AI 서비스 아키텍처를 자세히 다루지 않습니다. 여기서는 현대 LLM이 갑자기 등장한 것이 아니라, 언어 모델링, 임베딩, sequence modeling, Attention, 사전학습이 결합된 결과라는 큰 흐름만 잡습니다.

## 이 절의 목표

- Transformer를 self-attention 중심 구조로 이해합니다.
- self-attention을 사람의 주의가 아니라 토큰 사이의 관련도를 계산하는 구조로 이해합니다.
- positional encoding이 왜 필요한지 직관적으로 이해합니다.
- Encoder, Decoder, Encoder-Decoder의 역할 차이를 구분합니다.
- BERT와 GPT가 모두 Transformer 계열이지만 학습 목표와 사용 방향이 다르다는 점을 이해합니다.
- pretraining과 fine-tuning을 구분합니다.
- GPT-2와 GPT-3가 zero-shot, few-shot, in-context learning 경험으로 이어졌다는 흐름을 이해합니다.
- LLM을 AI 전체와 동일시하지 않습니다.

## Transformer는 Attention을 중심 구조로 올려놓았다

11.2에서 본 RNN은 순서를 따라 hidden state를 넘기며 계산했습니다. 이 구조는 시퀀스 데이터를 다루기에 자연스럽지만, 긴 입력을 처리할 때 순차 계산 부담이 큽니다.

Attention은 다른 가능성을 보여 주었습니다. 출력 단어를 만들 때 입력의 관련 위치를 다시 참고할 수 있다면, 모든 정보를 하나의 fixed-length vector에만 넣을 필요가 줄어듭니다.

Transformer는 이 Attention을 보조 장치가 아니라 중심 구조로 올려놓았습니다. Vaswani 등의 2017년 논문은 recurrence와 convolution을 사용하지 않고 attention만으로 sequence transduction을 수행하는 구조를 제안했습니다. 논문 제목인 *Attention Is All You Need*는 이 전환을 상징적으로 보여 줍니다.

Transformer의 핵심 직관은 다음과 같습니다.

> 문장 안의 각 토큰이
> 문장 안의 다른 토큰들을 참고해
> 자기 표현을 갱신한다.

예를 들어 다음 문장을 봅니다.

> 그 모델은 이전 문맥을 보고 다음 토큰을 예측한다.

`예측한다`를 처리할 때는 `모델`, `이전 문맥`, `다음 토큰`이 모두 관련될 수 있습니다. self-attention은 같은 시퀀스 안의 토큰들이 서로를 참고하도록 가중치를 계산합니다.

여기서 `self`는 자기 자신만 본다는 뜻이 아닙니다. 같은 입력 시퀀스 안에서 토큰들끼리 서로 참고한다는 뜻입니다.

## Positional encoding은 순서 정보를 보완한다

RNN은 입력을 순서대로 처리하기 때문에 순서 정보가 구조 안에 자연스럽게 들어갑니다. 하지만 Transformer는 recurrence 없이 self-attention을 사용합니다. 이 경우 토큰들의 순서를 알려 주는 별도 장치가 필요합니다.

그래서 Transformer는 positional encoding을 사용합니다.

> 토큰 임베딩(token embedding):
> 토큰이 무엇인지 나타내는 벡터
>
> positional encoding:
> 토큰이 어느 위치에 있는지 알려 주는 정보

입문 단계에서는 다음처럼 이해하면 충분합니다.

> "나는 책을 읽었다"
>
> 나는: 토큰 의미 + 1번째 위치
> 책을: 토큰 의미 + 2번째 위치
> 읽었다: 토큰 의미 + 3번째 위치

Transformer가 순서를 모르는 모델이라는 뜻은 아닙니다. 순차적으로 hidden state를 넘기는 방식이 아니라, 위치 정보를 더해 self-attention 계산 안에서 순서를 반영한다는 뜻입니다.

## Encoder와 Decoder는 역할이 다르다

Transformer 논문은 Encoder-Decoder 구조를 사용했습니다. Encoder는 입력 시퀀스의 표현을 만들고, Decoder는 출력 시퀀스를 생성합니다.

| 구조 | 대표 흐름 | 직관 |
| --- | --- | --- |
| Encoder | BERT 계열 | 입력 전체를 보고 문맥적 표현(contextual representation)을 만든다. |
| Decoder | GPT 계열 | 왼쪽 문맥을 바탕으로 다음 토큰을 생성한다. |
| Encoder-Decoder | 원래 Transformer 번역 구조 | 입력 시퀀스를 읽고 출력 시퀀스로 변환한다. |

이 구분은 BERT와 GPT를 이해할 때 중요합니다.

BERT(Bidirectional Encoder Representations from Transformers)는 Transformer encoder를 사용합니다. Devlin 등의 BERT 논문은 masked language model과 next sentence prediction을 사용해 deep bidirectional representation을 사전학습하고, 여러 과업에 fine-tuning할 수 있다고 설명합니다.

GPT(Generative Pre-Training)는 Transformer decoder를 사용한 흐름입니다. Radford 등의 2018년 GPT 논문은 language model의 generative pre-training 뒤에 task-specific fine-tuning을 붙이는 방식을 제시했습니다. GPT 계열은 기본적으로 앞의 문맥을 보고 다음 토큰을 예측하는 autoregressive language model 흐름과 가깝습니다.

다만 이 구분을 너무 단순화하면 안 됩니다.

> BERT = 이해 모델
> GPT = 생각하는 모델

이렇게 말하면 오해가 생깁니다. 더 안전한 표현은 다음입니다.

> BERT 계열:
> 입력 전체의 문맥적 표현을 만드는 데 강한 encoder 중심 흐름
>
> GPT 계열:
> 이전 토큰 문맥을 바탕으로 다음 토큰을 생성하는 decoder 중심 흐름

## 사전학습은 모델에 언어 패턴을 먼저 익히게 한다

사전학습(pretraining)은 특정 과업 하나만 바로 학습하는 대신, 큰 텍스트에서 일반적인 언어 패턴을 먼저 학습하는 절차입니다.

> pretraining:
> 큰 텍스트 말뭉치에서 언어 패턴을 먼저 학습
>
> fine-tuning:
> 특정 과업 데이터로 모델을 조정

이 흐름은 Transformer만의 발명은 아닙니다. ELMo는 단어의 의미가 문맥에 따라 달라진다는 점을 반영한 deep contextualized word representation을 제시했습니다. ULMFiT는 language model pretraining 뒤에 목표 과업으로 fine-tuning하는 절차를 체계적으로 보여 주었습니다.

Transformer 계열에서는 이 흐름이 더 큰 규모로 이어졌습니다. GPT는 generative pre-training과 supervised fine-tuning을 결합했고, BERT는 masked language model 방식으로 bidirectional representation을 사전학습했습니다.

여기서 중요한 점은 다음입니다.

> 사전학습은 모델이 사실을 검증해 저장한다는 뜻이 아니다.
> 대규모 텍스트에서 다음 단어, 빈칸, 문맥 관계 같은 학습 목표를 통해
> 언어적 패턴과 표현을 학습한다는 뜻이다.

따라서 사전학습된 LLM(pretrained LLM)이 그럴듯한 문장을 만든다고 해서, 그 문장이 항상 근거 있는 사실이라는 뜻은 아닙니다. 이 책에서 계속 근거 검토를 강조하는 이유도 여기에 있습니다.

## 문맥적 표현은 정적 임베딩을 넘어섰다

11.1에서 본 초기 임베딩은 단어마다 비교적 고정된 벡터를 주는 방식으로 이해할 수 있습니다. 하지만 실제 언어에서 단어의 의미는 문맥에 따라 달라집니다.

> 은행에 돈을 맡겼다.
> 강가의 은행나무를 보았다.

`은행`이라는 표면형이 같아도 문맥은 다릅니다. ELMo는 이런 문제를 다루기 위해 문맥에 따라 달라지는 단어 표현을 만들었습니다. BERT도 Transformer encoder를 사용해 입력 전체 문맥을 반영한 표현을 만듭니다.

이 흐름은 LLM을 이해할 때 중요합니다. LLM은 단어를 단순한 사전 항목처럼 처리하는 것이 아니라, 주변 문맥 안에서 토큰의 역할을 계산합니다.

## GPT-2와 GPT-3는 프롬프트 경험으로 이어졌다

GPT-2는 language model이 자연어 지시와 예시를 통해 여러 과업 행동을 보일 수 있음을 강조했습니다. 논문은 WebText로 학습한 모델이 별도의 task-specific fine-tuning 없이 zero-shot setting에서 여러 downstream task를 수행하는 사례를 보였습니다.

GPT-3는 이 흐름을 더 크게 확장했습니다. Brown 등의 2020년 논문은 175B parameter 모델을 사용해 zero-shot, one-shot, few-shot setting을 비교했습니다. 여기서 중요한 점은 few-shot이 모델 가중치를 다시 학습한다는 뜻이 아니라는 점입니다.

> fine-tuning:
> 학습 데이터를 사용해 모델 가중치(weight)를 업데이트한다.
>
> in-context learning:
> prompt 안의 설명과 예시를 보고 출력 행동을 바꾼다.
> 이때 기본적으로 모델 가중치는 업데이트되지 않는다.

이것이 오늘날 사용자가 LLM에게 자연어로 작업을 설명하고 예시를 넣는 경험으로 이어졌습니다. 하지만 이 절에서는 prompt 작성 기법을 다루지 않습니다. 여기서는 GPT-2와 GPT-3가 “자연어 입력 자체가 과업 지정 방식이 될 수 있다”는 경험을 넓혔다는 정도만 기억합니다.

GPT-3 논문도 한계를 함께 언급합니다. few-shot 성능이 좋아졌다고 해서 모델이 사람처럼 새 과업을 이해해 학습한다고 단정할 수는 없습니다. 논문은 모델이 새로운 과업을 실제로 학습하는지, 학습 데이터에서 본 패턴을 인식하는지 구분하기 어렵다는 문제도 지적합니다.

## 이 절에서 피해야 할 축약

LLM을 이해할 때 다음 축약은 조심해야 합니다.

| 위험한 축약 | 더 안전한 표현 |
| --- | --- |
| Transformer가 곧 LLM이다. | Transformer는 현대 LLM에 널리 쓰인 핵심 구조지만, LLM 전체를 뜻하지 않는다. |
| 사전학습은 사실을 외우는 과정이다. | 사전학습은 대규모 텍스트에서 언어 패턴과 표현을 학습하는 과정이다. |
| BERT는 이해하고 GPT는 생각한다. | BERT와 GPT는 Transformer 계열 안에서 구조와 학습 목표가 다른 흐름이다. |
| prompt 예시는 모델을 다시 학습시킨다. | in-context learning에서는 보통 가중치 업데이트 없이 입력 문맥이 출력 행동을 바꾼다. |
| AI는 결국 LLM이다. | LLM은 현대 AI의 중요한 흐름이지만 AI 전체는 아니다. |

특히 마지막 축약이 중요합니다. 최근에는 AI를 곧 LLM으로 보는 분위기가 강하지만, AI에는 규칙 기반 AI, 탐색, 머신러닝, 강화학습, 컴퓨터 비전, 음성 인식, 로봇, 추천 시스템 등 다양한 흐름이 있습니다. LLM은 그중 언어와 생성 인터페이스에서 큰 전환을 만든 계열로 이해하는 편이 안전합니다.

## 이 절에서 기억할 관점

현대 LLM을 안전하게 요약하면 다음과 같습니다.

> 언어 모델링은 다음 토큰의 확률을 다루는 문제를 만들었다.
> 임베딩은 토큰을 벡터로 바꾸었다.
> RNN, Seq2Seq, Attention은 순서와 입력-출력 대응을 다루었다.
> Transformer는 Attention 중심 구조와 병렬 학습 가능성을 강화했다.
> 사전학습은 대규모 텍스트에서 일반 언어 패턴을 먼저 학습하게 했다.
> GPT-2와 GPT-3는 자연어 prompt와 in-context learning 경험을 넓혔다.

이 흐름을 알면 LLM을 갑자기 등장한 마술 같은 기술로 보지 않게 됩니다. LLM은 언어를 확률적으로 다루는 연구, 벡터 표현, sequence modeling, Attention, Transformer, 대규모 사전학습이 결합된 결과입니다.

## 체크리스트

- Transformer를 self-attention 중심 구조로 설명할 수 있다.
- self-attention을 사람의 의식적 주의가 아니라 토큰 간 관련도 계산으로 설명할 수 있다.
- positional encoding이 왜 필요한지 설명할 수 있다.
- Encoder, Decoder, Encoder-Decoder의 역할을 구분할 수 있다.
- BERT와 GPT가 모두 Transformer 계열이지만 구조와 학습 목표가 다르다는 점을 설명할 수 있다.
- pretraining과 fine-tuning을 구분할 수 있다.
- ELMo와 ULMFiT를 문맥적 표현과 사전학습 흐름의 중요한 전조로 설명할 수 있다.
- in-context learning을 가중치 업데이트 없는 입력 문맥 기반 행동 변화로 설명할 수 있다.
- LLM을 AI 전체와 동일시하지 않을 수 있다.

## 출처와 참고 자료

- Ashish Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), arXiv, 2017, 확인 날짜: 2026-06-23.
- Matthew E. Peters et al., [Deep contextualized word representations](https://arxiv.org/abs/1802.05365), arXiv, 2018, 확인 날짜: 2026-06-23.
- Jeremy Howard, Sebastian Ruder, [Universal Language Model Fine-tuning for Text Classification](https://arxiv.org/abs/1801.06146), arXiv, 2018, 확인 날짜: 2026-06-23.
- Alec Radford et al., [Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), OpenAI, 2018, 확인 날짜: 2026-06-23.
- Jacob Devlin et al., [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805), arXiv, 2018, 확인 날짜: 2026-06-23.
- Alec Radford et al., [Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf), OpenAI, 2019, 확인 날짜: 2026-06-23.
- Tom B. Brown et al., [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165), arXiv, 2020, 확인 날짜: 2026-06-23.
