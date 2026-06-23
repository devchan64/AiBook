# 9.3 근거 검토: LLM의 직접 계보와 주변 근거 구분

## 검토 목적

9.3은 9.1과 9.2에서 다룬 딥러닝 확산 사례를 LLM의 직접 발전사와 구분하는 절이다. 목적은 다음이다.

- AlexNet, YOLO, WaveNet을 LLM의 직접 조상으로 쓰지 않는다. Deep Voice는 주요 소재가 아니라 TTS 보조 사례로만 둔다.
- LLM의 직접 계보는 언어 모델링, 순차 모델링, Seq2Seq, Attention, Transformer 쪽으로 잡는다.
- 딥러닝 패러다임의 확산 사례는 주변 근거로만 둔다.
- 최근의 `AI = LLM` 식의 축약을 경계하고, LLM을 AI 전체가 아니라 AI 지형 안의 중요한 한 흐름으로 배치한다.

## 확인한 원문

원문 PDF와 추출 텍스트는 `.tmp/section-9-3-evidence/` 아래에 저장해 확인했다.

| 자료 | 파일 | 확인 내용 |
| --- | --- | --- |
| Bengio et al., 2003 | `neural-probabilistic-lm-bengio2003.pdf` | 통계적 언어 모델링, 단어열의 결합확률, 분산 표현 |
| Sutskever et al., 2014 | `seq2seq-1409.3215.pdf` | LSTM 기반 sequence-to-sequence 학습과 기계번역 |
| Bahdanau et al., 2014 | `attention-1409.0473.pdf` | encoder-decoder의 fixed-length vector 병목과 attention |
| Vaswani et al., 2017 | `transformer-1706.03762.pdf` | recurrence/convolution을 배제한 attention 중심 sequence transduction |

추가 비교 자료는 `.tmp/section-9-3-additional-lineage/` 아래에 저장해 확인했다.

| 자료 | 파일 | 비교 판단 |
| --- | --- | --- |
| Mikolov et al., 2013 | `word2vec-1301.3781.pdf` | 단어 벡터 표현과 의미·구문 관계 평가 |
| Peters et al., 2018 | `elmo-1802.05365.pdf` | deep contextualized word representation |
| Howard and Ruder, 2018 | `ulmfit-1801.06146.pdf` | pretrained language model fine-tuning |
| Devlin et al., 2018 | `bert-1810.04805.pdf` | Transformer 기반 pre-training/fine-tuning |
| Radford et al., 2018 | `gpt-2018-language-understanding.pdf` | Transformer decoder, generative pre-training, fine-tuning |
| Radford et al., 2019 | `gpt2-2019-language-models.pdf` | WebText language model, zero-shot task transfer |
| Brown et al., 2020 | `gpt3-2005.14165.pdf` | 175B autoregressive language model, few-shot/in-context learning |

## 자료별 근거 판단

### Bengio et al., A Neural Probabilistic Language Model

근거 위치:

- 추출 텍스트 15-22행: statistical language modeling의 목표를 단어열의 결합확률 학습으로 설명하고, distributed representation을 학습한다고 설명한다.
- 124-136행: 각 단어에 distributed word feature vector를 연결하고, 단어 feature vector와 확률 함수의 파라미터를 동시에 학습하는 흐름을 설명한다.

본문 반영:

- 언어 모델링(language modeling)을 단어와 토큰 순서의 확률적 모델링으로 소개했다.
- 단어 임베딩(word embedding)의 상세 설명은 뒤 LLM 장으로 넘기고, 여기서는 분산 표현(distributed representation)만 짧게 언급했다.

주의:

- 이 논문만으로 현대 LLM을 설명하지 않는다.
- "언어 모델은 문장을 이해한다"보다 "단어열의 확률을 모델링한다"는 표현이 안전하다.

### Sutskever et al., Sequence to Sequence Learning with Neural Networks

근거 위치:

- 추출 텍스트 52-62행: speech recognition과 machine translation 같은 sequential problem을 언급하고 LSTM이 sequence-to-sequence 문제를 풀 수 있다고 설명한다.
- 179-190행: source sentence가 주어졌을 때 correct translation의 log probability를 최대화하고 beam search decoder를 사용한다고 설명한다.
- 233-234행: encoder LSTM과 decoder LSTM 구조를 언급한다.

본문 반영:

- Seq2Seq를 입력 시퀀스에서 출력 시퀀스로 가는 구조로 소개했다.
- 기계번역을 대표 예시로 두었다.

주의:

- Seq2Seq를 현대 LLM 자체로 설명하지 않는다.
- 이 절에서는 encoder-decoder 구조를 직관 수준으로만 설명한다.

### Bahdanau et al., Neural Machine Translation by Jointly Learning to Align and Translate

근거 위치:

- 추출 텍스트 16-19행: encoder-decoder가 source sentence를 fixed-length vector로 encode하고 decoder가 생성하며, 이 방식이 bottleneck일 수 있음을 설명한다.
- 45-48행: align and translate를 jointly learning하고, 생성 시점마다 source sentence의 관련 부분을 찾는다고 설명한다.
- 193-197행: decoder가 source sentence의 parts to pay attention to를 결정하고, encoder가 모든 정보를 fixed-length vector에 담아야 하는 부담을 줄인다고 설명한다.

본문 반영:

- Attention을 긴 입력을 하나의 고정 길이 벡터에 모두 담는 부담을 줄이는 구조로 소개했다.
- "주의"라는 심리적 표현이 아니라 입력 위치별 가중치를 계산하는 구조로 설명했다.

주의:

- Attention을 인간의 의식적 주의와 동일시하지 않는다.
- Transformer와 구분해서 Attention을 전 단계로 설명한다.

### Vaswani et al., Attention Is All You Need

근거 위치:

- 추출 텍스트 32-38행: 기존 sequence transduction 모델은 recurrent/convolutional neural network 기반이고, Transformer는 attention mechanism에 기반하며 더 parallelizable하다고 설명한다.
- 81-105행: recurrence를 피하고 self-attention에 의존하는 architecture를 제안한다고 설명한다.
- 107-118행: encoder-decoder 구조와 Transformer의 stacked self-attention 구조를 설명한다.
- 464-466행: Transformer를 attention 기반 sequence transduction model로 정리한다.

본문 반영:

- Transformer를 attention 중심 구조가 대규모 순차 모델링에 유리해진 전환점으로 설명했다.
- self-attention과 병렬화(parallelization)를 핵심 관점으로 제시했다.

주의:

- "Transformer만으로 현대 LLM이 완성됐다"는 식으로 쓰지 않는다.
- 사전학습, 데이터, 스케일링, 지시 튜닝, RLHF는 뒤 장에서 따로 다룬다.

## 추가 비교 자료 판단

### Mikolov et al., Efficient Estimation of Word Representations in Vector Space

근거 위치:

- 추가 추출 텍스트 20-26행: 큰 데이터셋에서 단어 표현의 품질을 다루고, semantic/syntactic word similarity를 평가한다고 설명한다.
- 167-193행: CBOW와 Skip-gram architecture를 제안한다.
- 472-477행: 여러 언어 작업에서 단어 벡터 표현의 품질을 연구했다고 정리한다.

판단:

- LLM의 직접 구조는 아니지만, 단어를 분산 벡터 표현으로 다루는 흐름을 설명할 때 중요한 전 단계다.
- 9.3 본문에는 "표현 학습과 단어 임베딩의 중요한 전 단계"로만 반영한다.

### Peters et al., Deep contextualized word representations

근거 위치:

- 추가 추출 텍스트 4-19행: deep contextualized word representations와 bidirectional language model을 설명한다.
- 31-53행: pretrained word representations와 ELMo representations를 언급한다.
- 543행 부근: downstream tasks에서 성능 개선을 언급한다.

판단:

- 고정 단어 벡터보다 문맥에 따라 달라지는 단어 표현을 보여 준다.
- 현대 LLM 구조 자체라기보다 contextual representation의 중요한 전 단계로 둔다.

### Howard and Ruder, ULMFiT

근거 위치:

- 추가 추출 텍스트 18-30행: Universal Language Model Fine-tuning을 제안하고 transfer learning을 설명한다.
- 84-103행: ULMFiT가 robust inductive transfer learning을 가능하게 한다고 설명한다.
- 278행 부근: pretrained general-domain LM을 사용한다고 설명한다.

판단:

- 사전학습된 언어 모델을 downstream task에 fine-tuning하는 흐름을 보여 준다.
- 현대 LLM 서비스 자체와는 다르지만 NLP 전이학습의 중요한 연결점이다.

### Devlin et al., BERT

근거 위치:

- 추가 추출 텍스트 12-21행: Bidirectional Encoder Representations from Transformers와 pre-training을 설명한다.
- 85-107행: masked language model과 pre-training 방식을 설명한다.
- 243-245행: pre-training과 fine-tuning framework를 설명한다.

판단:

- BERT는 생성형 decoder-only LLM과는 구조와 목적이 다르지만, Transformer 기반 사전학습 언어 표현 모델의 핵심 자료다.
- 9.3에서는 "현대 언어 표현 모델의 직접 배경"으로 표현한다.

### Radford et al., GPT, GPT-2, Brown et al., GPT-3

근거 위치:

- GPT 2018 추가 추출 텍스트 60-67행: unsupervised pre-training과 supervised fine-tuning, Transformer 사용을 설명한다.
- GPT 2018 추가 추출 텍스트 130-140행: tokens에 대한 language modeling objective와 multi-layer Transformer decoder를 설명한다.
- GPT-2 추가 추출 텍스트 114-121행: zero-shot setting과 language modeling core를 설명한다.
- GPT-3 추가 추출 텍스트 19-24행: 175B autoregressive language model, few-shot, no gradient updates/fine-tuning을 설명한다.
- GPT-3 추가 추출 텍스트 108-128행: in-context learning을 설명한다.

판단:

- GPT 계열은 현대 생성형 LLM과 가장 가까운 직접 계보로 볼 수 있다.
- 단, 9.3에서는 자세한 GPT 역사와 제품사는 다루지 않고, "현대 생성형 LLM에 매우 가까운 직접 계보"로만 반영한다.

## 일반화 문구

사용자의 직관은 다음처럼 일반화하는 것이 안전하다.

> 생성형 AI와 LLM은 갑자기 등장한 기술이 아니다. 다만 그 직접 계보는 이미지 인식이나 객체 검출이 아니라, 언어 모델링과 순차 모델링의 발전사에서 찾아야 한다. 이미지, 음성, 객체 검출 사례는 딥러닝 패러다임이 확산된 배경으로 함께 읽는다.

또한 9.3의 숨은 의도는 다음 문장으로 정리한다.

> LLM은 현대 AI를 이해하는 핵심 기술이지만 AI 전체와 같은 말은 아니다. LLM의 직접 계보를 따로 잡는 이유는 LLM을 과소평가하기 위해서가 아니라, AI의 넓은 지형을 LLM 하나로 좁히지 않기 위해서다.

## 도메인 경계

9.3에서 다룬다:

- 직접 계보와 주변 근거의 구분
- 언어 모델링, Seq2Seq, Attention, Transformer의 지도 수준 소개
- AlexNet, YOLO, WaveNet의 역할 재분류. Deep Voice는 TTS 보조 사례로만 관리

9.3에서 깊게 다루지 않는다:

- Transformer의 세부 수식
- pretraining, fine-tuning, instruction tuning, RLHF의 상세
- tokenizer, embedding, decoder-only architecture
- 최신 LLM 제품사

이 항목들은 Part 5의 LLM과 생성형 AI에서 다루는 것이 적절하다.

## 본문 반영 결론

9.3 본문은 다음 기준으로 작성했다.

- 직접 계보: 언어 모델링, Seq2Seq, Attention, Transformer. 다만 Seq2Seq와 Attention은 현대 LLM의 구조와 동일하다는 뜻이 아니라, 언어와 순차 모델링의 직접 설명 배경으로 둔다.
- 주변 근거: AlexNet, YOLO, WaveNet. Deep Voice는 주요 비교축이 아니라 TTS 보조 사례
- 안전한 설명: 딥러닝의 확산과 LLM의 직접 발전사를 연결하되, 원인 관계를 과장하지 않는다.

## 추가 검토: 과장 가능성이 있는 문장

| 검토 지점 | 위험 | 수정 방향 |
| --- | --- | --- |
| `LLM은 다음 토큰 확률 분포를 계산한다` | 모든 LLM 구조를 하나로 단정할 수 있음 | `생성형 LLM은 보통`이라는 표현으로 제한 |
| `Seq2Seq는 직접 계보인가` | 현대 decoder-only LLM이 Seq2Seq 구조라는 오해 가능 | `언어·순차 모델링 계보`로 표현 |
| `RLHF가 현대 LLM의 구성 요소` | 모든 현대 LLM이 RLHF를 쓰는 것처럼 보일 수 있음 | 제품이나 연구 흐름에 따라 쓰이는 정렬 기법으로 표현 |
| `token은 대리물` | 어원 설명이 과도하게 넓어질 수 있음 | 9.3 본문에서는 `표식이나 증거`로 축소 |
| `토큰화와 임베딩 상세` | Part 5 영역 침범 | 9.3에서는 짧은 연결만 남기고 상세는 뒤 장으로 이동 |
