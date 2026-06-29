# P5-3.1 LLM 발전사의 큰 흐름

P5-2장에서는 토큰(token)이 임베딩(embedding) 벡터로 바뀌고, 그 벡터 사이의 거리와 유사도(similarity)가 검색과 비교의 기준이 된다는 점을 보았습니다. 이제 질문은 조금 더 역사적인 방향으로 옮겨갑니다.

그렇다면 오늘의 LLM(large language model)은 어떤 연구 흐름이 겹쳐져서 만들어졌는가?

이 절은 그 질문에 답합니다.

LLM은 갑자기 등장한 하나의 기술이 아니라, 언어 모델(language model), 임베딩, 순차 모델(sequence model), Attention, Transformer, 대규모 사전학습(pretraining)이 겹치며 만들어진 흐름이다.

## 이 절의 범위

이 절은 다음 질문에 답합니다.

- LLM 이전에는 언어를 어떻게 모델링했는가?
- 임베딩과 순차 모델은 어떤 문제를 해결하려 했는가?
- Attention과 Transformer는 왜 전환점이 되었는가?
- 사전학습 LLM은 무엇을 바꾸었는가?

이 절은 다음 내용은 깊게 다루지 않습니다.

- 각 논문의 수식 전개
- 모델별 벤치마크 세부 비교
- 최신 상용 모델 계보 전수조사

대신 이 절에서 잡은 큰 흐름은 바로 다음의 P5-3.2에서 `직접 계보와 주변 근거`로 정리되고, 구조 차이는 P5-4.1 Transformer 구조 복습, P5-5.1 BERT 계열의 위치, P5-6.1 GPT 계열의 위치에서 다시 구체화됩니다. 최신 상용 모델 계보 전수조사는 현재 판의 본편 범위 밖으로 둡니다.

이 절의 목적은 세부 구조를 모두 외우게 하는 데 있지 않습니다. Part 5 본류로 들어가기 전에 필요한 최소한의 `역사 지도`를 만드는 데 있습니다.

## 이 절의 목표

- LLM 발전사를 몇 개의 큰 전환점으로 설명할 수 있습니다.
- 통계적 언어 모델(statistical language model), 임베딩, RNN, Attention, Transformer, 사전학습의 위치를 구분할 수 있습니다.
- LLM을 AI 전체와 동일시하지 않고, 언어 모델 계열의 한 흐름으로 설명할 수 있습니다.
- 다음 절의 `직접 계보와 주변 근거` 구분으로 자연스럽게 넘어갈 수 있습니다.

## 1단계. 언어를 확률 문제로 다루기 시작했다

이 절은 이후 GPT 구조와 다음 토큰 예측을 읽기 위한 배경만 남기는 장입니다. 따라서 각 단계의 핵심 질문만 붙잡고, 세부 알고리즘 경쟁은 여기서 길게 확장하지 않습니다.

초기 언어 모델(language model)의 핵심 질문은 단순했습니다.

- 앞의 단어를 보고 다음 단어가 무엇일 가능성이 높은가?
- 어떤 문장열이 더 그럴듯한가?

이 단계에서는 n-gram 같은 방식이 널리 쓰였습니다. 짧은 문맥 안에서 단어 빈도를 세어 다음 단어 확률을 근사하는 접근입니다.

이 시기의 핵심 공헌은 다음과 같습니다.

- 언어를 규칙 목록만이 아니라 확률(probability) 문제로 다루기 시작했다
- `다음 단어 예측`이라는 관점이 분명해졌다

하지만 한계도 분명했습니다.

- 긴 문맥을 잘 다루기 어렵고
- 드문 표현과 새로운 조합에 약하며
- 비슷한 단어끼리 일반화하기 어렵습니다

## 2단계. 단어를 벡터로 표현하기 시작했다

다음 전환은 임베딩(embedding)입니다.

단어를 one-hot처럼 완전히 분리된 기호로만 두지 않고, 여러 숫자로 된 벡터로 표현하면 비슷한 문맥에서 쓰이는 단어가 어느 정도 가까운 위치를 가질 수 있습니다.

이 단계에서 중요해진 질문은 다음입니다.

- `고양이`와 `개`처럼 비슷한 쓰임의 단어를 모델이 어떻게 더 가깝게 볼 수 있는가?
- 텍스트를 어떻게 계산 가능한 연속 표현(continuous representation)으로 바꿀 수 있는가?

word2vec 같은 연구는 이 감각을 널리 퍼뜨렸습니다. 이 시기 이후 언어 모델은 `다음 단어 확률`뿐 아니라 `좋은 표현 공간(representation space)`을 함께 배우는 방향으로 강하게 움직입니다.

## 3단계. 순서를 신경망 구조로 다루기 시작했다

언어는 순서(sequence)가 중요한 데이터이므로, 단어 벡터를 얻었다고 끝나지 않습니다. 앞 문맥이 뒤 해석에 영향을 주는 구조를 더 잘 다뤄야 했습니다.

이 단계에서 RNN(recurrent neural network), LSTM(long short-term memory), GRU(gated recurrent unit)가 중요해졌습니다.

이 구조들은 다음 문제를 해결하려 했습니다.

- 앞에서 본 정보를 뒤까지 전달할 수 있는가?
- 순서가 있는 문장을 상태(state)로 누적할 수 있는가?
- 긴 문맥에서도 정보를 덜 잃을 수 있는가?

기계번역(machine translation) 같은 문제에서는 Seq2Seq(sequence-to-sequence)도 큰 전환이었습니다.

- 입력 문장을 읽고
- 내부 표현을 만들고
- 출력 문장을 생성한다

이 흐름이 만들어졌기 때문입니다.

## 4단계. Attention이 병목을 줄였다

RNN 기반 Seq2Seq는 강력했지만, 입력 전체를 하나의 고정 길이 표현으로 압축하는 병목(bottleneck) 문제가 있었습니다.

Attention은 이 문제를 줄이려 했습니다.

- 출력 단어를 만들 때
- 입력 전체를 다시 훑어보고
- 관련 있는 위치에 더 큰 가중치를 주는 방식입니다

이렇게 기억하면 충분합니다.

`Attention은 모델이 필요한 순간에 입력의 관련 부분을 다시 참고하게 만든 구조다.`

이 단계가 중요한 이유는, LLM으로 가는 직접적인 구조 전환이 여기서 시작되기 때문입니다.

## 5단계. Transformer가 중심 구조를 바꿨다

Transformer는 Attention을 보조 장치가 아니라 중심 구조로 올려놓았습니다.

이 전환의 의미는 매우 큽니다.

- 긴 순차 계산에 덜 묶이고
- 병렬 처리(parallel processing)에 더 잘 맞고
- 토큰들 사이 관계를 더 직접적으로 계산할 수 있게 되었기 때문입니다

Part 4에서 이미 본 것처럼, Transformer는 self-attention을 중심에 두고 token-to-token 관계를 큰 행렬 연산으로 다룹니다.

이 구조는 GPU 기반 대규모 학습과 잘 맞았습니다. 그래서 Transformer는 단순히 `번역 모델 하나`가 아니라, 이후 LLM 확산의 기반 구조가 됩니다.

## 6단계. 사전학습이 모델 사용 방식을 바꿨다

다음 전환은 사전학습(pretraining)입니다.

모델을 특정 작은 과업에 바로 맞추는 대신, 먼저 대규모 텍스트에서 일반적인 언어 패턴을 배우게 하고, 그 뒤에 여러 작업으로 연결하는 방식이 중심이 되었습니다.

이 단계에서 중요한 변화는 다음과 같습니다.

- 언어 패턴을 먼저 크게 학습한다
- 이후 fine-tuning 또는 prompt 기반 사용으로 연결한다
- 하나의 큰 모델이 여러 과업을 처리할 가능성이 커진다

이 전환은 BERT와 GPT 계열에서 서로 다른 방향으로 강하게 나타납니다.

## 7단계. LLM은 생성 인터페이스를 넓혔다

GPT 계열이 커지면서 사용자 경험도 달라졌습니다.

- 모델에게 자연어로 지시를 줄 수 있고
- 예시를 몇 개 넣어 행동을 바꿀 수 있으며
- 같은 모델이 요약, 분류, 번역, 초안 작성, 코드 생성 등 여러 작업을 수행하는 것처럼 보이기 시작했습니다

이때 사용자는 종종 `AI 전체가 LLM이 되었다`고 느끼기 쉽습니다. 하지만 더 안전한 설명은 다음입니다.

`LLM은 AI 전체가 아니라, 언어와 생성 인터페이스에서 매우 큰 전환을 만든 한 계열이다.`

## 이 흐름을 아주 단순하게 그리면

```mermaid
flowchart TD
  A["statistical language models"]
  B["embeddings and distributed representations"]
  C["RNN / LSTM / Seq2Seq"]
  D["attention"]
  E["Transformer"]
  F["large-scale pretraining"]
  G["modern LLM experience"]

  A --> B --> C --> D --> E --> F --> G
```

이 도식은 복잡한 세부보다 `큰 전환의 순서`를 보여 주는 데 목적이 있습니다.

## 사례로 보기

### 사례 1. 번역

초기에는 짧은 문맥 기반 확률 모델이 중심이었고, 이후 Seq2Seq와 Attention이 번역 품질을 크게 끌어올렸습니다. Transformer는 이 흐름을 더 넓은 범용 구조로 확장했습니다.

### 사례 2. 검색과 임베딩

단어 임베딩과 문장 임베딩 흐름은 나중에 벡터 검색(vector search), RAG, 추천(recommendation) 시스템과 직접 연결됩니다.

### 사례 3. 챗봇 경험

사용자가 자연어로 요구를 적고, 모델이 여러 과업에 대응하는 현재의 경험은 GPT 계열과 대규모 사전학습 흐름 위에서 가능해졌습니다.

## 작은 Python 예제로 보기

이번 예제의 목표는 실제 언어 모델을 구현하는 것이 아니라, `짧은 문맥 빈도 기반 판단`과 `표현 기반 일반화`가 왜 다른 문제인지 감각만 잡는 것입니다.

입력:

- 짧은 말뭉치
- 다음 단어 빈도

출력:

- 간단한 bigram 빈도 표

```python
sentences = [
    ["나는", "커피를", "마신다"],
    ["나는", "차를", "마신다"],
    ["나는", "커피를", "좋아한다"],
]

counts = {}
for sent in sentences:
    for left, right in zip(sent, sent[1:]):
        counts[(left, right)] = counts.get((left, right), 0) + 1

for pair, count in sorted(counts.items()):
    print(pair, "->", count)
```

실행 결과 예시는 다음처럼 읽을 수 있습니다.

```text
('나는', '차를') -> 1
('나는', '커피를') -> 2
('차를', '마신다') -> 1
('커피를', '마신다') -> 1
('커피를', '좋아한다') -> 1
```

이 예제에서 읽어야 할 핵심은 다음입니다.

- 초기 언어 모델은 이런 빈도 구조에서 출발했다는 점
- 하지만 이 구조만으로는 긴 문맥과 일반화가 부족하다는 점
- 그래서 임베딩, 순차 모델, Attention, Transformer로 흐름이 이어졌다는 점입니다

## 역사와 커리큘럼 관점

이 절은 LLM을 최신 제품 이름의 나열로 설명하지 않습니다. 오히려 `왜 이런 구조가 순서대로 필요해졌는가`를 보여 줍니다.

커리큘럼 관점에서 이 절이 중요한 이유는 다음과 같습니다.

- Part 4의 Transformer를 Part 5의 LLM 계보 안에 다시 위치시키고
- 이후 BERT, GPT, pretraining, instruction tuning, RAG를 읽을 때 구조적 혼동을 줄이며
- LLM을 AI 전체와 동일시하는 오해를 줄이기 때문입니다

## 다음 절과의 연결

여기까지 오면 다음 질문이 남습니다.

- 이 큰 흐름 중에서 무엇이 LLM의 `직접 계보`인가?
- 반대로 무엇은 LLM의 분위기와 확산을 설명하는 `주변 근거`인가?

이 질문은 P5-3.2 직접 계보와 주변 근거로 이어집니다.

## 이 절에서 기억할 관점

- LLM은 통계적 언어 모델, 임베딩, 순차 모델, Attention, Transformer, 사전학습이 겹쳐진 결과입니다.
- Transformer는 중요한 중심 구조이지만, 그 앞단의 문제의식 없이 이해하면 흐름이 끊깁니다.
- 사전학습은 모델 사용 방식 자체를 바꾸었습니다.
- LLM은 AI 전체가 아니라 언어와 생성 인터페이스에서 큰 전환을 만든 계열입니다.

## 체크리스트

- LLM 발전사를 큰 전환점 중심으로 설명할 수 있는가?
- 통계적 언어 모델, 임베딩, RNN, Attention, Transformer, 사전학습의 위치를 구분할 수 있는가?
- 왜 Transformer가 구조적 전환점이었는지 말할 수 있는가?
- 왜 LLM을 AI 전체와 동일시하면 안 되는지 설명할 수 있는가?

## 출처와 참고 자료

- Yoshua Bengio et al., `A Neural Probabilistic Language Model`, Journal of Machine Learning Research, 2003, 확인 날짜: 2026-06-29.
- Tomas Mikolov et al., `Efficient Estimation of Word Representations in Vector Space`, arXiv, 2013, 확인 날짜: 2026-06-29.
- Ilya Sutskever, Oriol Vinyals, Quoc V. Le, `Sequence to Sequence Learning with Neural Networks`, arXiv, 2014, 확인 날짜: 2026-06-29.
- Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio, `Neural Machine Translation by Jointly Learning to Align and Translate`, arXiv, 2014, 확인 날짜: 2026-06-29.
- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, 확인 날짜: 2026-06-29.
- Tom B. Brown et al., `Language Models are Few-Shot Learners`, arXiv, 2020, 확인 날짜: 2026-06-29.
