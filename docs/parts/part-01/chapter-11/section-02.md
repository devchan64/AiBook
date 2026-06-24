# 11.2 RNN, Seq2Seq, Attention

11.1에서는 언어 모델(language model)과 임베딩(embedding)을 봤습니다. 언어 모델은 단어와 토큰의 순서를 확률적으로 다루고, 임베딩은 단어와 토큰을 계산 가능한 벡터 표현(vector representation)으로 바꿉니다.

이번 절에서는 순서가 있는 데이터를 신경망이 어떻게 다루려고 했는지 봅니다.

이 절의 질문은 다음입니다.

> 단어와 토큰을 벡터로 바꾼 뒤,
> 그 순서와 문맥은 어떻게 모델 안에서 다룰 수 있었는가?

입문 단계에서는 다음 흐름이 중요합니다.

> RNN은 이전 상태를 다음 계산에 넘기며 순서를 다루었고, Seq2Seq는 입력 시퀀스를 출력 시퀀스로 바꾸는 구조를 만들었으며, Attention은 출력 시점마다 입력의 관련 위치를 다시 참고할 수 있게 했다.

## 이 절의 범위

이 절은 Transformer를 설명하지 않습니다. Transformer는 11.3에서 다룹니다.

여기서는 Transformer 이전에 중요한 전환이 된 세 가지 흐름만 봅니다.

| 주제 | 이 절에서 볼 질문 |
| --- | --- |
| RNN(recurrent neural network) | 순서가 있는 입력을 어떻게 누적해서 처리하는가? |
| Seq2Seq(sequence-to-sequence) | 입력 문장을 출력 문장으로 어떻게 바꾸는가? |
| Attention | 출력 단어를 만들 때 입력의 어떤 부분을 참고할지 어떻게 정하는가? |

LSTM(long short-term memory)과 GRU(gated recurrent unit)는 RNN 계열에서 긴 의존성(long-range dependency)을 다루기 위해 등장한 중요한 구조입니다. 하지만 이 절에서는 게이트(gate) 수식이나 내부 구조를 깊게 설명하지 않고, 왜 필요했는지 정도만 봅니다.

## 이 절의 목표

- RNN(recurrent neural network)을 순서 데이터를 처리하기 위한 신경망 구조로 이해합니다.
- hidden state를 사람의 기억이 아니라 모델 내부의 누적 상태로 이해합니다.
- LSTM과 GRU가 긴 문맥을 다루기 위한 RNN 변형이라는 점을 봅니다.
- Seq2Seq를 입력 시퀀스(input sequence)에서 출력 시퀀스(output sequence)로 바꾸는 구조로 이해합니다.
- Encoder-Decoder 구조의 fixed-length vector 병목을 이해합니다.
- Attention을 출력 시점마다 입력의 관련 위치를 가중치로 참고하는 구조로 이해합니다.
- Attention을 인간의 의식적 주의나 논리적 이해로 과장하지 않습니다.

## RNN은 이전 상태를 다음 계산에 넘긴다

n-gram 언어 모델은 짧은 이전 문맥을 사용했습니다. 하지만 문장은 단어가 한 줄로 이어지는 순서 데이터(sequence data)입니다. 앞에서 나온 정보가 뒤의 해석에 영향을 줍니다.

예를 들어 다음 문장을 봅니다.

> 나는 어제 도서관에서 빌린 책을 오늘 아침에 다 읽었다.

`다 읽었다`를 이해하려면 바로 앞 단어만 보는 것보다, 앞에서 `책`이 나왔다는 정보를 유지하는 편이 도움이 됩니다.

RNN(recurrent neural network)은 이런 순서 데이터를 다루기 위해 이전 단계의 hidden state를 다음 단계 계산에 넘깁니다.

> 입력 1 -> 상태 1
> 입력 2 + 상태 1 -> 상태 2
> 입력 3 + 상태 2 -> 상태 3

여기서 hidden state는 사람의 의식적 기억(memory)과 같은 말이 아닙니다. 모델이 지금까지의 입력을 처리하며 만든 내부 벡터 상태입니다.

> hidden state:
> 앞의 입력들이 현재 계산에 영향을 주도록 넘겨지는 내부 상태

이 구조 덕분에 RNN은 문장, 음성, 시계열(time series)처럼 순서가 중요한 데이터를 다룰 수 있었습니다.

## RNN은 긴 문맥에서 어려움을 겪었다

RNN의 아이디어는 단순하고 강력하지만, 긴 문맥을 안정적으로 학습하는 것은 쉽지 않았습니다. 멀리 떨어진 단어 사이의 관계를 학습하려면 오류 신호가 많은 시간 단계를 거슬러 전달되어야 합니다. 이 과정에서 gradient가 너무 작아지거나(vanishing gradient), 너무 커지는(exploding gradient) 문제가 생길 수 있습니다.

입문 단계에서는 다음 정도로 이해하면 충분합니다.

> 짧은 문맥:
> 앞의 정보가 비교적 쉽게 뒤까지 전달됨
>
> 긴 문맥:
> 중요한 정보가 여러 단계를 지나며 약해지거나 불안정해질 수 있음

LSTM(long short-term memory)은 이런 긴 의존성 문제를 다루기 위해 널리 쓰인 RNN 변형입니다. LSTM은 cell state와 gate 구조를 사용해 어떤 정보를 유지하고, 어떤 정보를 새로 받아들이고, 어떤 정보를 출력에 사용할지 조절합니다.

GRU(gated recurrent unit)는 LSTM보다 단순한 게이트 구조로 비슷한 목적을 수행하는 RNN 변형입니다. 이 절에서는 LSTM과 GRU를 자세히 비교하지 않습니다. 중요한 것은 RNN 계열 연구가 “순서가 있는 데이터를 어떻게 오래 기억하고 처리할 것인가”라는 문제를 중심으로 발전했다는 점입니다.

## Seq2Seq는 입력 순서를 출력 순서로 바꾼다

Seq2Seq(sequence-to-sequence)는 입력 시퀀스를 받아 출력 시퀀스를 만드는 구조입니다. 대표 사례는 기계번역(machine translation)입니다.

> 입력 시퀀스:
> I read a book.
>
> 출력 시퀀스:
> 나는 책을 읽었다.

Seq2Seq의 기본 구조는 Encoder-Decoder입니다.

| 구성 | 역할 |
| --- | --- |
| Encoder | 입력 시퀀스를 읽고 내부 표현을 만든다. |
| Decoder | 내부 표현을 바탕으로 출력 시퀀스를 생성한다. |

Sutskever, Vinyals, Le의 2014년 논문은 LSTM을 사용해 입력 시퀀스를 고정 차원 벡터로 바꾸고, 다른 LSTM이 그 벡터에서 출력 시퀀스를 생성하는 일반적인 sequence learning 접근을 제시했습니다. Cho 등의 RNN Encoder-Decoder 논문도 하나의 RNN이 심볼 시퀀스를 fixed-length vector로 인코딩하고, 다른 RNN이 그 표현을 다른 심볼 시퀀스로 디코딩하는 구조를 제안했습니다.

입문 관점에서는 다음 그림으로 충분합니다.

> 입력 문장
> -> Encoder
> -> 문장 표현 벡터
> -> Decoder
> -> 출력 문장

이 흐름은 11.1의 임베딩과 연결됩니다. 단어를 벡터로 표현하는 데서 끝나는 것이 아니라, 문장 전체도 모델 내부에서 어떤 벡터 표현으로 압축될 수 있다고 본 것입니다.

## fixed-length vector는 병목이 될 수 있다

기본 Encoder-Decoder 구조에는 중요한 문제가 있었습니다. 입력 문장 전체를 하나의 fixed-length vector에 담아야 했습니다.

짧은 문장에서는 그럴듯해 보입니다.

```text
I read.
-> [문장 벡터]
-> 나는 읽었다.
```

하지만 긴 문장에서는 문제가 생깁니다.

```text
회의에서 논의된 예산, 일정, 위험 요소, 담당자, 다음 작업을 모두 반영해 번역한다.
-> [하나의 문장 벡터]
-> 출력 문장
```

입력의 모든 정보를 하나의 벡터에 압축해야 하면, 중요한 정보가 빠지거나 약해질 수 있습니다. Bahdanau, Cho, Bengio의 Attention 논문은 이 fixed-length vector가 기본 encoder-decoder 구조의 병목(bottleneck)이 될 수 있다고 보고, 출력 단어를 만들 때마다 입력 문장의 관련 부분을 참고하는 방식을 제안했습니다.

## Attention은 필요한 입력 위치를 다시 참고한다

Attention은 출력의 각 단계에서 입력의 여러 위치를 가중치(weight)로 참고하는 구조입니다.

예를 들어 영어 문장을 한국어로 번역한다고 합시다.

> Source:
> The cat sat on the mat.
>
> Target을 생성하는 중:
> 고양이가 ...

`고양이가`를 만들 때는 source 문장의 `cat`이 중요할 수 있습니다. `매트 위에`를 만들 때는 `on the mat` 쪽이 중요할 수 있습니다.

Attention은 이 관계를 다음처럼 생각하게 해 줍니다.

> 출력 단어를 만들 때마다
> 입력의 각 위치에 점수를 준다.
> 점수를 확률처럼 정규화한다.
> 그 가중치로 입력 표현들을 섞어 context vector를 만든다.
> 그 context vector를 사용해 다음 출력 단어를 만든다.

Bahdanau 등의 논문은 이를 decoder가 source sentence의 관련 부분을 자동으로 soft-search하는 방식으로 설명합니다. 여기서 `soft`는 하나의 위치만 딱 고르는 것이 아니라, 여러 입력 위치에 가중치를 나누어 주는 방식으로 이해하면 됩니다.

## Attention은 인간의 주의와 같은 말이 아니다

Attention이라는 이름 때문에 모델이 사람처럼 의식적으로 주의를 기울인다고 이해하기 쉽습니다. 하지만 이 책에서는 그렇게 설명하지 않습니다.

더 안전한 설명은 다음입니다.

> Attention:
> 출력 계산에 사용할 입력 위치별 가중치를 계산하는 구조

Attention은 모델이 입력의 관련 위치를 더 많이 참고하도록 도와줍니다. 또한 일부 경우에는 어떤 입력 위치가 특정 출력에 강하게 연결되었는지 시각화할 수 있습니다.

하지만 attention weight를 곧바로 “모델의 진짜 이유”나 “인간식 이해”로 해석하면 위험합니다. 이 절에서는 Attention을 해석 가능성의 완전한 답이 아니라, sequence-to-sequence 모델의 병목을 줄이는 중요한 구조로만 둡니다.

## Transformer로 이어지는 이유

RNN, Seq2Seq, Attention은 LLM의 직접 계보에서 매우 중요합니다. 하지만 현대 LLM의 핵심 구조를 설명하려면 한 단계가 더 필요합니다.

RNN 기반 모델은 순서를 따라 계산합니다. 이전 상태를 다음 상태로 넘기는 구조이기 때문에 긴 시퀀스를 처리할 때 계산이 순차적으로 진행되는 부담이 있습니다.

Attention은 입력의 관련 위치를 직접 참고하는 강력한 방법을 보여 주었습니다. Transformer는 이 Attention을 더 중심에 놓고, recurrence 없이 self-attention을 사용해 시퀀스 안의 토큰들이 서로를 참고하게 만든 구조입니다.

이 절에서는 여기까지만 기억합니다.

> RNN:
> 이전 상태를 넘기며 순서를 처리
>
> Seq2Seq:
> 입력 시퀀스를 출력 시퀀스로 변환
>
> Attention:
> 출력 시점마다 입력의 관련 위치를 가중치로 참고
>
> Transformer:
> Attention을 중심 구조로 확장

Transformer의 구체적 구조와 사전학습 LLM(pretrained LLM)은 11.3에서 다룹니다.

## 이 절에서 기억할 관점

RNN, Seq2Seq, Attention은 모두 언어를 단순한 단어 목록이 아니라 순서와 문맥이 있는 데이터로 다루려는 흐름입니다.

> RNN은 순서를 내부 상태로 누적한다.
> Seq2Seq는 입력 순서를 출력 순서로 바꾼다.
> Attention은 출력할 때 입력의 관련 위치를 다시 참고한다.

이 흐름을 알면 Transformer와 LLM을 갑자기 등장한 구조로 보지 않게 됩니다. Transformer는 Attention 이전의 문제의식, 즉 긴 문맥, 입력-출력 대응, 병렬 계산의 필요성 위에서 이해해야 합니다.

## 체크리스트

- RNN(recurrent neural network)이 이전 hidden state를 다음 계산에 넘기는 구조임을 설명할 수 있다.
- hidden state를 사람의 기억이 아니라 내부 벡터 상태로 설명할 수 있다.
- LSTM과 GRU를 긴 의존성을 다루기 위한 RNN 변형으로 설명할 수 있다.
- Seq2Seq(sequence-to-sequence)를 입력 시퀀스에서 출력 시퀀스로 바꾸는 구조로 설명할 수 있다.
- Encoder와 Decoder의 역할을 구분할 수 있다.
- fixed-length vector 병목이 왜 문제가 될 수 있는지 설명할 수 있다.
- Attention을 입력 위치별 가중치로 관련 정보를 참고하는 구조로 설명할 수 있다.
- Attention을 인간의 의식적 주의나 완전한 설명 가능성으로 과장하지 않을 수 있다.
- 11.3에서 Transformer가 왜 Attention을 중심에 놓는지 이어서 읽을 준비가 되었다.

## 출처와 참고 자료

- Kyunghyun Cho et al., [Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation](https://arxiv.org/abs/1406.1078), arXiv, 2014, 확인 날짜: 2026-06-23.
- Ilya Sutskever, Oriol Vinyals, Quoc V. Le, [Sequence to Sequence Learning with Neural Networks](https://arxiv.org/abs/1409.3215), arXiv, 2014, 확인 날짜: 2026-06-23.
- Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio, [Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473), arXiv, 2014, 확인 날짜: 2026-06-23.
- Graham Neubig, [Neural Machine Translation and Sequence-to-sequence Models: A Tutorial](https://arxiv.org/abs/1703.01619), arXiv, 2017, 확인 날짜: 2026-06-23.
