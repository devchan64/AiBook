# 11.1 근거 검토: 통계적 언어 모델과 임베딩

## 검토 목적

11.1은 LLM의 직접 계보를 바로 Transformer로 시작하지 않고, 언어 모델링(language modeling), n-gram, 분산 표현(distributed representation), 임베딩(embedding)의 흐름으로 시작하는 절이다.

이 절에서는 다음 경계를 둔다.

- RNN, LSTM, Seq2Seq, Attention은 11.2로 넘긴다.
- Transformer와 사전학습 LLM은 11.3으로 넘긴다.
- 임베딩은 word2vec 중심의 정적 임베딩(static embedding) 직관까지만 설명한다.
- 문맥적 표현(contextual representation)은 예고만 하고 깊게 설명하지 않는다.
- 기호 기반 AI와 임베딩의 관계는 “대체”가 아니라 “표현 층위(representation level)의 차이”로 설명한다.

## 확인한 원문

원문은 `.tmp/section-11-1-evidence/` 아래에 저장했다.

| 자료 | 파일 | 확인 내용 |
| --- | --- | --- |
| Jurafsky & Martin, SLP3 Chapter 3 | `jurafsky-martin-slp3-ch03-ngram.pdf`, `.txt` | language model, n-gram, Markov assumption, MLE, smoothing, LLM과 n-gram의 연결 |
| Jurafsky & Martin, SLP3 Chapter 6 | `jurafsky-martin-slp3-ch06-vector-semantics.pdf`, `.txt` | embedding matrix, one-hot vector, static embedding, neural language model의 embedding 사용 |
| Bengio et al., 2003 | `bengio-2003-neural-probabilistic-language-model.pdf`, `.txt` | n-gram의 일반화 한계, curse of dimensionality, distributed representation, word feature vectors |
| Mikolov et al., 2013, Efficient Estimation | `mikolov-2013-efficient-estimation-word-representations.pdf`, `.txt` | continuous vector representations, CBOW, Skip-gram, syntactic and semantic similarity |
| Mikolov et al., 2013, Distributed Representations | `mikolov-2013-distributed-representations-phrases.pdf`, `.txt` | Skip-gram, negative sampling, phrase representation, analogy task |

## 자료별 근거 판단

### Jurafsky & Martin, Chapter 3

근거 위치:

- 추출 텍스트 15-18행 부근: language model을 upcoming words를 예측하고 다음 단어의 probability distribution을 주는 모델로 설명한다.
- 41-44행 부근: n-gram language model을 가장 단순한 언어 모델로 소개하고, LLM 개념 학습의 출발점으로 삼는다.
- 108-124행 부근: n-gram이 전체 history 대신 짧은 이전 문맥으로 조건부 확률을 근사하며, 이를 Markov assumption과 연결한다.
- 141-184행 부근: n-gram 확률을 corpus counts와 normalization으로 추정하는 MLE 설명.
- 637-684행 부근: unseen n-gram과 smoothing 문제.
- 1110-1116행 부근: neural language model은 continuous space로 단어를 투영해 n-gram의 두 가지 문제를 줄인다고 설명한다.

본문 반영:

- 언어 모델을 다음 단어 또는 다음 토큰 후보의 확률을 계산하는 모델로 설명했다.
- n-gram을 짧은 문맥과 빈도 기반 추정으로 설명했다.
- n-gram의 한계를 문맥 길이, 데이터 희소성, 단어 유사성 일반화 문제로 정리했다.

주의:

- SLP3는 2026년 draft이므로 교재성 자료로 사용하되, 조문처럼 고정된 표준으로 표현하지 않는다.
- 본문에는 수식 전개를 최소화하고 입문용 예시로 재구성했다.

### Jurafsky & Martin, Chapter 6

근거 위치:

- 추출 텍스트 630-653행 부근: static word2vec/GloVe embedding, embedding matrix, vocabulary와 embedding row 설명.
- 660-679행 부근: one-hot vector와 embedding matrix 곱셈으로 token embedding을 선택하는 설명.
- 810-825행 부근: neural language model이 prior context의 단어를 embedding으로 표현하고, 유사 단어 context로 일반화할 수 있다는 설명.
- 1371행 부근: neural language model은 pretrained embedding을 사용하거나 embedding을 학습할 수 있다는 요약.

본문 반영:

- one-hot 표현과 dense vector 표현의 차이를 설명했다.
- embedding matrix와 token/vector 표현의 관계를 초심자용으로 풀었다.
- 정적 임베딩과 문맥적 표현의 차이는 예고만 했다.

주의:

- Chapter 6의 자세한 신경망 구조 설명은 11.1 범위를 넘으므로 사용하지 않았다.

### Bengio et al., 2003

근거 위치:

- 추출 텍스트 13-20행 부근: word sequence modeling의 어려움, curse of dimensionality, distributed representation을 통한 일반화, 단어 표현과 probability function의 동시 학습.
- 84-121행 부근: 전통 n-gram 모델의 일반화와 distributed feature vector를 사용하는 목표.
- 745-760행 부근: learned distributed representation이 curse of dimensionality를 줄이는 데 쓰인다는 논의.

본문 반영:

- n-gram의 한계가 신경망 언어 모델과 분산 표현으로 이어지는 흐름을 설명했다.
- 단어 표현과 다음 단어 확률 함수를 함께 학습한다는 방향을 LLM 이전의 중요한 전환으로 정리했다.

주의:

- Bengio 논문의 모델 구조 자체를 자세히 설명하지 않았다.
- “LLM의 직접 조상”이라는 표현은 과도할 수 있으므로 “직접 계보의 중요한 전 단계” 정도로 해석했다.

### Mikolov et al., 2013

근거 위치:

- `mikolov-2013-efficient-estimation-word-representations.txt` 18-23행 부근: continuous vector representations와 syntactic/semantic word similarity 평가.
- 155-182행 부근: CBOW와 continuous Skip-gram 모델 구조.
- 209-210행 부근: CBOW는 context로 current word를 예측하고, Skip-gram은 current word로 surrounding words를 예측한다는 도식 설명.
- `mikolov-2013-distributed-representations-phrases.txt` 25-27행 부근: Skip-gram이 syntactic and semantic relationships를 포착하는 distributed vector representations를 학습한다는 설명.
- 421-422행 부근: word and phrase distributed representations와 linear structure.

본문 반영:

- word2vec을 단어 임베딩을 널리 각인시킨 사례로 소개했다.
- CBOW와 Skip-gram을 각각 주변 단어로 가운데 단어 예측, 현재 단어로 주변 단어 예측이라는 직관으로 설명했다.
- 임베딩을 사전적 정의가 아니라 문맥 사용에서 학습된 벡터 위치로 설명했다.

주의:

- analogy 결과를 과장해 “모델이 의미를 이해한다”로 쓰지 않았다.
- word2vec은 현재 LLM의 전체 구조가 아니라 임베딩과 분산 표현의 중요한 전 단계로만 사용했다.

## 일반화 문구

11.1에서는 다음 문구가 안전하다.

> 언어 모델은 단어와 토큰의 순서를 확률적으로 다루고, 임베딩은 단어와 토큰을 계산 가능한 벡터 표현으로 바꾼다.

LLM으로 연결할 때는 다음 문구가 적절하다.

> LLM은 갑자기 등장한 챗봇이 아니라, 언어 모델링과 벡터 표현을 대규모 신경망과 긴 문맥 처리로 확장한 결과로 이해할 수 있다.

## 도메인 경계

11.1에서 다룬다:

- language model의 기본 직관
- n-gram과 Markov assumption의 입문 설명
- n-gram의 한계
- distributed representation과 embedding
- word2vec의 CBOW/Skip-gram 직관
- symbolic unit과 embedding의 층위(level) 구분

11.1에서 깊게 다루지 않는다:

- RNN, LSTM, Seq2Seq
- Attention
- Transformer
- BERT, GPT, ELMo, ULMFiT
- tokenizer 알고리즘 상세
- embedding 평가 지표와 벡터 연산의 수학
- RAG나 벡터 데이터베이스
