# 11.2 근거 검토: RNN, Seq2Seq, Attention

## 검토 목적

11.2는 11.1의 언어 모델링과 임베딩 다음 단계로, 순서 데이터(sequence data)를 신경망이 어떻게 다루려 했는지 설명하는 절이다.

이 절에서는 다음 경계를 둔다.

- RNN, LSTM, GRU는 순서 처리와 긴 의존성 문제를 설명하는 수준으로만 다룬다.
- Seq2Seq는 Encoder-Decoder 구조와 입력 시퀀스에서 출력 시퀀스로 바꾸는 직관을 중심으로 다룬다.
- Attention은 fixed-length vector 병목을 줄이는 구조로 설명한다.
- Transformer와 self-attention의 세부 구조는 11.3으로 넘긴다.
- Attention을 인간의 의식적 주의나 완전한 설명 가능성으로 과장하지 않는다.

## 확인한 원문

원문은 `.tmp/section-11-2-evidence/` 아래에 저장했다.

| 자료 | 파일 | 확인 내용 |
| --- | --- | --- |
| Sutskever et al., 2014 | `sutskever-2014-sequence-to-sequence.pdf`, `.txt` | LSTM 기반 sequence-to-sequence, input sequence를 fixed-dimensional vector로 매핑한 뒤 output sequence 생성 |
| Bahdanau et al., 2014 | `bahdanau-2014-align-translate.pdf`, `.txt` | fixed-length vector 병목, soft-search, soft alignment, attention mechanism |
| Cho et al., 2014 | `cho-2014-rnn-encoder-decoder.pdf`, `.txt` | RNN Encoder-Decoder, symbol sequence를 fixed-length vector로 encode/decode, conditional probability |
| Neubig, 2017 | `neubig-2017-nmt-seq2seq-tutorial.pdf`, `.txt` | RNN, hidden state, LSTM, encoder-decoder, attention의 튜토리얼 설명 |

시도했지만 확인하지 못한 자료:

| 자료 | 상태 | 처리 |
| --- | --- | --- |
| Hochreiter & Schmidhuber, 1997, LSTM PDF | `https://www.bioinf.jku.at/publications/older/2604.pdf` 연결 실패 | 본문에서는 LSTM 원 논문 세부 설명을 피하고, Sutskever와 Neubig 자료의 LSTM 설명을 보조 근거로 사용 |

## 자료별 근거 판단

### Sutskever et al., 2014

근거 위치:

- 추출 텍스트 17-20행 부근: sequence learning을 위한 end-to-end 접근을 제시하고, multilayered LSTM으로 input sequence를 fixed-dimensional vector representation으로 매핑한 뒤 다른 LSTM이 output sequence를 추출한다고 설명한다.
- 56-60행 부근: 하나의 LSTM이 입력 시퀀스를 읽고 fixed-dimensional vector representation을 얻은 뒤, 다른 LSTM이 그 벡터에서 출력 시퀀스를 추출한다는 구조.
- 122-126행 부근: conditional probability를 추정하기 위해 먼저 fixed-dimensional representation을 얻는다는 설명.
- 191-210행 부근: source sentence reversal이 학습을 개선했다는 관찰과 memory utilization 논의.

본문 반영:

- Seq2Seq를 입력 시퀀스에서 출력 시퀀스로 바꾸는 구조로 설명했다.
- Encoder가 입력을 벡터 표현으로 만들고 Decoder가 출력을 생성한다는 직관으로 정리했다.
- LSTM은 긴 의존성을 다루는 RNN 변형으로만 언급했다.

주의:

- BLEU 점수와 WMT 세부 결과는 11.2 입문 범위를 넘으므로 본문에 넣지 않았다.
- source sentence reversal은 흥미로운 사례지만 본문 중심 질문을 벗어나므로 근거 메모에만 남겼다.

### Cho et al., 2014

근거 위치:

- 추출 텍스트 60-67행 부근: RNN Encoder-Decoder는 두 RNN으로 구성되며, encoder는 variable-length source sequence를 fixed-length vector로 encode하고 decoder는 그 vector를 variable-length target sequence로 decode한다고 설명한다.
- 162-175행 부근: encoder가 각 symbol을 읽고, decoder가 hidden state를 사용해 target sequence를 생성한다는 설명.
- 1063-1169행 부근: source phrase와 target phrase를 sequence로 두고, decoder가 target phrase를 생성하는 구체 구조.

본문 반영:

- Encoder와 Decoder의 역할을 표로 구분했다.
- 입력 문장 전체도 모델 내부에서 벡터 표현으로 압축될 수 있다는 관점을 11.1 임베딩과 연결했다.

주의:

- Cho 논문은 phrase pair scoring과 SMT 시스템 결합이 중요한 맥락이다. 본문에서는 그 세부 실험 대신 RNN Encoder-Decoder 구조만 사용했다.

### Bahdanau et al., 2014

근거 위치:

- 추출 텍스트 11-18행 부근: neural MT의 encoder-decoder가 source sentence를 fixed-length vector로 encode하고, 이것이 bottleneck이 될 수 있으며, relevant source parts를 soft-search하는 방법을 제안한다.
- 37-45행 부근: source sentence 전체 정보를 fixed-length vector에 압축해야 하는 문제가 있고, output word 생성 시 관련 source positions를 찾는 방식 설명.
- 172-183행 부근: soft alignment를 계산하고, decoder가 source sentence의 어느 부분에 attention을 줄지 결정하며, encoder가 모든 정보를 fixed-length vector에 넣어야 하는 부담을 줄인다고 설명한다.
- 559-562행 부근: input words나 annotations를 soft-search하여 fixed-length vector에 전체 문장을 encode해야 하는 부담에서 벗어난다는 결론.

본문 반영:

- fixed-length vector 병목을 설명했다.
- Attention을 출력 시점마다 입력 위치별 가중치를 계산해 context vector를 만드는 구조로 설명했다.
- Attention을 인간의 주의가 아니라 기계적 가중치 기반 참조 구조로 제한했다.

주의:

- attention weight를 모델의 진짜 이유나 완전한 해석으로 쓰지 않았다.
- 수식은 생략하고, 입문용 절차로 재구성했다.

### Neubig, 2017

근거 위치:

- 추출 텍스트 83-94행 부근: RNN language model, encoder-decoder, attention으로 이어지는 튜토리얼 구조.
- 1430-1458행 부근: RNN은 previous hidden state를 참조해 current hidden state를 계산하고, unroll해서 볼 수 있다는 설명.
- 1484-1534행 부근: RNN의 vanishing gradient 문제와 LSTM이 cell을 추가해 장기 의존성을 다루는 설명.
- 1878-1886행 부근: encoder-decoder model의 기본 아이디어와 source sentence를 읽어 hidden state를 만든 뒤 decoder가 사용한다는 설명.
- 2390-2424행 부근: encoder-decoder의 문제와 attention의 기본 아이디어.
- 2464-2515행 부근: attention vector, attention score, softmax, context vector 설명.

본문 반영:

- RNN과 hidden state를 내부 벡터 상태로 설명했다.
- RNN의 긴 의존성 문제, LSTM/GRU의 필요성, attention vector와 context vector 직관을 보강했다.

주의:

- Neubig 튜토리얼은 교육 자료이므로 개념 설명 보조 근거로 사용했다.
- 최신 Transformer 이후 NMT 구조까지 일반화하지 않았다.

## 일반화 문구

11.2에서는 다음 문구가 안전하다.

> RNN은 이전 상태를 다음 계산에 넘기며 순서를 다루었고, Seq2Seq는 입력 시퀀스를 출력 시퀀스로 바꾸는 구조를 만들었으며, Attention은 출력 시점마다 입력의 관련 위치를 다시 참고할 수 있게 했다.

Attention에 대해서는 다음 표현이 안전하다.

> Attention은 출력 계산에 사용할 입력 위치별 가중치를 계산하는 구조다.

## 도메인 경계

11.2에서 다룬다:

- RNN의 hidden state 직관
- vanishing/exploding gradient와 긴 의존성 문제의 입문 설명
- LSTM/GRU의 필요성
- Seq2Seq와 Encoder-Decoder 구조
- fixed-length vector 병목
- Attention의 soft alignment와 context vector 직관

11.2에서 깊게 다루지 않는다:

- LSTM/GRU 게이트 수식
- BLEU 점수와 NMT 실험 세부
- beam search 상세
- Transformer self-attention
- multi-head attention
- positional encoding
- BERT/GPT 계열
