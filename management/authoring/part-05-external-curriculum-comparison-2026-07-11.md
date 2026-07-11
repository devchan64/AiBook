# Part 5 외부 커리큘럼 비교 메모

작성일: 2026-07-11

이 문서는 Part 5 `딥러닝` 파트가 외부 딥러닝 입문 커리큘럼과 비교해 어떤 축에서 표준 범위와 맞고, 어떤 축에서 의도적으로 좁아졌는지 점검하기 위한 내부 메모다.

이번 비교의 목적은 `외부 목차를 그대로 따라가기`가 아니라, 현재 Part 5가 초심자 기준에서 필요한 핵심 설명을 빠뜨리지 않았는지 확인하는 데 있다.

## 비교에 사용한 외부 기준

이번 비교는 가능한 한 1차 자료나 공식 교육 자료만 사용했다.

### 1. Dive into Deep Learning

- 자료: Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola, `Dive into Deep Learning`
- URL: https://d2l.ai/
- 확인 날짜: 2026-07-11
- 비교에 쓴 기준:
  - `Multilayer Perceptrons`
  - `Forward Propagation, Backward Propagation, and Computational Graphs`
  - `Numerical Stability and Initialization`
  - `Generalization in Deep Learning`
  - `Dropout`
  - `GPUs`
  - `Convolutional Neural Networks`
  - `Recurrent Neural Networks`
  - `Attention Mechanisms and Transformers`
  - `Optimization Algorithms`
  - `Computational Performance`
  - `Generative Adversarial Networks`

### 2. Deep Learning

- 자료: Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-07-11
- 비교에 쓴 기준:
  - Part II `Modern Practical Deep Networks`
  - `Deep Feedforward Networks`
  - `Regularization for Deep Learning`
  - `Optimization for Training Deep Models`
  - `Convolutional Networks`
  - `Sequence Modeling: Recurrent and Recursive Nets`
  - `Practical Methodology`
  - Part III의 `Representation Learning`
  - Part III의 `Deep Generative Models`

### 3. Stanford CS231n

- 자료: Stanford `CS231n: Deep Learning for Computer Vision`
- URL: https://cs231n.stanford.edu/
- 확인 날짜: 2026-07-11
- 비교에 쓴 기준:
  - `Regularization and Optimization`
  - `Neural Networks and Backpropagation`
  - `Image Classification with CNNs`
  - `CNN Architectures`
  - `Batch Normalization`
  - `Recurrent Neural Networks`
  - `Attention and Transformers`
  - `Large Scale Distributed Training`
  - `Generative Models 1`
  - `Generative Models 2`

### 4. Stanford CS224N

- 자료: Stanford `CS224N: Natural Language Processing with Deep Learning`
- URL: https://web.stanford.edu/class/cs224n/index.html
- 확인 날짜: 2026-07-11
- 비교에 쓴 기준:
  - course content 설명의 `basics of Deep Learning for NLP`와 `LLMs`
  - Assignment 2 `Neural network foundations, calculating tensor derivatives`
  - Assignment 3 `Self-attention and Transformers`
  - `Transformers`
  - `Post-training (RLHF, SFT, DPO)`
  - `Agents, RAG, tool use` 계열 주차

### 5. DeepLearning.AI Deep Learning Specialization

- 자료: DeepLearning.AI `Deep Learning Specialization`
- URL: https://www.deeplearning.ai/specializations/deep-learning
- 확인 날짜: 2026-07-11
- 비교에 쓴 기준:
  - `Neural Networks and Deep Learning`
  - `Improving Deep Neural Networks: Hyperparameter Tuning, Regularization and Optimization`
  - `Convolutional Neural Networks`
  - `Sequence Models`
  - specialization 소개의 `Dropout, BatchNorm, Xavier/He initialization`
  - `Various Sequence To Sequence Architectures`
  - `Transformer Network`

### 6. fast.ai Practical Deep Learning for Coders

- 자료: fast.ai `Practical Deep Learning for Coders`
- URL: https://course.fast.ai/
- 확인 날짜: 2026-07-11
- 비교에 쓴 기준:
  - Part 1의 `Neural net foundations`, `Natural Language (NLP)`, `Convolutions (CNNs)`
  - Part 2의 `Backpropagation & MLP`, `Initialization/normalization`, `Accelerated SGD & ResNets`, `Attention & transformers`, `Mixed Precision`

## 외부 기준에서 반복해서 보이는 공통 뼈대

외부 기준을 묶어 보면, 딥러닝 입문 커리큘럼의 공통 뼈대는 대체로 다음 순서로 반복된다.

1. 다층 퍼셉트론(MLP)과 비선형성
2. 순전파와 역전파, 계산 그래프
3. 손실, 최적화, 학습 안정화
4. 정규화와 일반화
5. GPU, 미니배치, 계산 성능
6. CNN
7. RNN/LSTM/GRU 같은 순차 구조
8. Attention과 Transformer
9. 생성 모델 또는 생성 출력 해석

Part 5는 이 큰 줄기 자체는 거의 그대로 따른다.

## Part 5와 잘 맞는 축

### 1. 구조 축과 학습 절차 축을 분리한 점

Part 5는 퍼셉트론 -> 다층 구조 -> 활성화 -> 손실 -> 역전파 -> optimizer -> regularization -> GPU/배치 -> 표현 학습 -> CNN -> RNN -> Attention -> Transformer -> 생성/샘플링으로 이어진다.

이 순서는 D2L과 Deep Learning 교재의 `네트워크 구조 -> 역전파/정규화/최적화 -> CNN/RNN/Attention` 흐름과 크게 어긋나지 않는다.

특히 현재 원고가 `구조 문제`와 `학습 절차 문제`를 명시적으로 나눠 읽게 만드는 점은 초심자에게 오히려 장점이다. 외부 교재는 이 둘을 더 촘촘히 섞는 경우가 많지만, 지금 책의 독자 기준에서는 분리 설명이 더 안전하다.

### 2. CNN -> RNN -> Attention -> Transformer 흐름

CS231n과 D2L은 모두 CNN과 RNN 이후 Attention/Transformer를 이어서 소개한다. Part 5 후반부도 같은 축을 따른다.

또한 현재 Part 5는 각 구조를 `이미지의 지역 구조`, `순차 상태`, `관계 재참조`, `병렬 블록` 문제로 다시 묶고 있어, 단순 모델 이름 나열로 흐르지 않으려는 방향도 적절하다.

### 3. GPU, 배치, 텐서 계산을 별도 축으로 둔 점

D2L은 `GPUs`, `Optimization Algorithms`, `Computational Performance`를 따로 길게 다룬다. CS231n도 `Large Scale Distributed Training`을 별도 강의로 둔다.

Part 5의 P5-9.1, P5-9.2는 이 축을 입문 수준에서 회수하는 역할을 한다. 이 덕분에 딥러닝을 `모델 이름 모음`으로 읽지 않고 계산 환경과 함께 읽게 만드는 점은 커리큘럼상 타당하다.

### 4. 생성과 샘플링을 Transformer 뒤에 두는 점

D2L과 CS231n은 생성 모델을 더 넓게 다루고, CS224N은 Transformer 뒤에 next-token prediction, post-training, evaluation으로 이어진다.

Part 5의 생성/샘플링 배치는 `LLM 이전의 생성 감각`을 먼저 닫는다는 점에서 현재 책의 Part 6 연결 구조와도 잘 맞는다.

## 외부 기준보다 상대적으로 약한 축

### 1. 초기화(initialization)와 수치 안정성(numerical stability)

이 축은 외부 기준에서 생각보다 자주 독립적으로 등장한다.

- D2L은 `Numerical Stability and Initialization`을 MLP 장 안의 별도 절로 둔다.
- Deep Learning 교재는 최적화와 practical methodology에서 학습 가능성, 초기화, 실험 안정성을 반복해서 다룬다.
- CS231n도 regularization/optimization과 backprop 설명을 빠르게 붙여, 깊은 학습이 `왜 실제로 가능해지는가`를 초반에 회수한다.

현재 Part 5에서는 이 축이 완전히 빠진 것은 아니다.

- P5-3.2에서 ReLU 확산 맥락과 함께 `더 나은 초기화와 최적화 기법`을 짧게 언급한다.
- P5-index에서도 `학습 안정화와 초기화`를 한 번 언급한다.

하지만 초심자 기준에서는 아직 `왜 깊은 네트워크가 그냥 쌓는다고 바로 학습되지 않는가`, `초기화와 수치 안정성이 무엇을 막는가`를 따로 붙잡을 중심 절이 약하다.

이 점은 비교 당시 현재 Part 5에서 가장 먼저 보강 후보로 볼 만했다. 이후 보강 작업으로 `P5-6.3 보충학습: 초기화(initialization), 수치 안정성(numerical stability), 배치 정규화(batch normalization)를 처음 묶어 읽는 법`을 추가해, 이 축을 초심자용으로 한 자리에서 다시 읽을 수 있게 했다.

### 2. batch normalization의 위치

batch normalization은 현재 원고에 존재한다.

- P5-6.2에서 학습 모드/평가 모드 차이의 핵심 사례로 설명한다.
- P5-8.1에서 regularization과 normalization을 구분하는 예로 다시 언급한다.

즉, `완전히 빠진 개념`은 아니다.

다만 외부 기준에서는 batch normalization이 자주 다음 두 축 사이의 다리로 나온다.

1. 깊은 네트워크를 어떻게 실제로 안정적으로 학습시키는가
2. CNN/현대 네트워크 아키텍처가 왜 바뀌었는가

현재 Part 5에서는 이 개념이 `mode 차이에 민감한 층`으로는 잘 설명되지만, `학습 안정화 도구`로서의 위치는 상대적으로 약하다.

이 지점도 위 보강 Section `P5-6.3`에서 `초기화 -> 수치 안정성 -> batch normalization`을 하나의 안정화 축으로 묶으면서 상당 부분 회수했다. 따라서 현재 상태의 잔여 과제는 `batch normalization`의 존재 여부가 아니라, 훗날 normalization 계열을 더 넓게 비교할 필요가 생길 때 본편 범위를 어디까지 넓힐지 정도로 줄었다.

### 3. Sequence-to-sequence / encoder-decoder 전환

D2L과 CS224N은 RNN 다음에 machine translation, encoder-decoder, attention을 조금 더 직접적으로 연결한다.

현재 Part 5는 RNN/LSTM/GRU -> 장기 의존성 -> Attention -> self-attention -> Transformer로 넘어간다. 이 흐름은 구조적으로는 맞지만, `seq2seq가 왜 attention으로 이어졌는가`라는 전환 장면은 외부 NLP 커리큘럼보다 더 압축돼 있다.

다만 이 책의 전체 구조상 LLM 본류를 Part 6으로 넘기고 있으므로, 이것은 `즉시 결손`이라기보다 `의도적 압축`에 가깝다. 이후 보강 작업으로 `P5-12.2`의 attention 전환부에 seq2seq / encoder-decoder 압축 병목을 설명하는 짧은 문단과 비교 표를 추가해, 이 전환 장면도 현재 Part 5 안에서 더 직접 회수했다.

### 4. 생성 모델의 계열 비교

CS231n과 D2L은 GAN, VAE, diffusion 같은 생성 계열을 더 직접 다룬다. Deep Learning 교재도 `Deep Generative Models`를 별도 축으로 둔다.

현재 Part 5는 생성 모델과 샘플링의 최소 감각만 닫고, LLM/생성형 AI의 본류를 Part 6으로 넘긴다.

이것은 현재 책의 주 흐름과는 맞지만, `일반 딥러닝 입문서`와 비교하면 생성 계열의 폭은 의도적으로 좁다.

즉, 현재 Part 5는 `Transformer와 생성 감각` 중심의 딥러닝 파트이지, `비전/확률/잠재변수 생성 모델을 폭넓게 훑는 파트`는 아니다.

## 커리큘럼 적합성 판단

### 전체 판단

현재 Part 5는 외부 딥러닝 입문 커리큘럼과 비교했을 때 `큰 구조는 적합하고, 책 전체 설계에 맞는 의도적 축소도 분명한 편`이다.

즉, 지금 상태를 `목차가 크게 잘못되었다`고 보기는 어렵다.

### 가장 중요한 강점

- MLP -> backprop -> optimization/regularization -> CNN/RNN/Attention/Transformer -> generation의 큰 줄기가 외부 기준과 잘 맞는다.
- 구조와 학습 절차를 분리해 읽게 만드는 현재 편집 방식은 초심자 기준에서 오히려 명확하다.
- Part 6과의 경계도 이전보다 더 분명하다.

### 가장 중요한 리스크

외부 비교 기준으로 봤을 때, 가장 큰 리스크는 `학습 안정화 toolkit`이 초심자에게 하나의 묶음으로 잡히지 않을 수 있다는 점이다.

구체적으로는 다음 셋이 약하게 흩어져 있다.

1. 초기화(initialization)
2. 수치 안정성(numerical stability)
3. batch normalization 같은 안정화 장치

외부 입문 교재에서는 이 셋이 `깊은 모델이 왜 학습되기 시작했는가`라는 질문 아래 더 직접 묶인다.

현재 Part 5는 optimizer, regularization, mode, normalization, GPU를 잘 나눠 놓았지만, 그 반대급부로 `깊은 학습이 실제로 덜 흔들리게 된 이유`가 한 자리에서 덜 보일 수 있다.

## 비교 이후 반영 상태

외부 비교 뒤 실제로 반영한 조치는 다음과 같다.

1. `P5-6.3`을 새로 추가해 `초기화(initialization) + 수치 안정성(numerical stability) + batch normalization`을 초심자용 안정화 축으로 묶었다.
2. 독자용 목차 `BOOK-toc`, `mkdocs.yml`, 개념사전, 관련 릴리즈노트를 함께 갱신해 새 Section이 Part 5 구조 안에서 바로 보이게 했다.
3. `P5-12.2`의 attention 전환부에 seq2seq / encoder-decoder 압축 병목 설명과 작은 비교 표를 넣어, `상태 전달 한계 -> 직접 참조` 사이의 NLP 전환 장면을 더 선명하게 만들었다.
4. Chapter 14~15와 Part 시작/마무리 페이지의 회수 문장을 구체적인 Section ID 기준으로 고쳐, Part 5에서 Part 6으로 넘어가는 학습 경계도 더 분명히 했다.

## 남는 관찰 포인트

외부 비교 기준으로 큰 공백은 우선 회수했지만, 앞으로 다시 점검할 수 있는 포인트는 남아 있다.

1. 생성 모델 계열 비교는 여전히 의도적으로 얇다. 다만 현재 책의 설계상 이것은 `Part 5의 결손`보다는 `Part 6과 역할 분담을 위한 범위 제한`으로 보는 편이 맞다.
2. normalization 계열을 더 넓게 다뤄야 할 필요가 생기면, batch normalization 자체를 더 늘리기보다 `왜 batch normalization이 여기까지 중요했고, 왜 다른 normalization들이 뒤에 나왔는가`를 별도 보충학습으로 분리하는 편이 구조상 안전하다.
3. DeepLearning.AI의 `Sequence Models`는 `word embeddings -> seq2seq/attention -> transformer`를 한 코스 안에서 잇는다. 현재 책은 임베딩을 Part 6 초반으로 넘겼으므로, 이것은 결손이라기보다 `언어 표현 층위`를 LLM 파트로 미루는 구조 선택으로 보는 편이 맞다. 다만 훗날 Part 5와 Part 6의 경계를 다시 조정한다면, 이 축이 가장 먼저 재검토 대상이 될 수 있다.

## 보강 이후 추가 교차 점검

보강 반영 뒤에 DeepLearning.AI Deep Learning Specialization과 fast.ai Practical Deep Learning for Coders를 추가로 대조해 보니, 현재 판단은 크게 흔들리지 않았다.

- DeepLearning.AI 기준에서는 `Dropout`, `BatchNorm`, `Xavier/He initialization`을 같은 실전 학습 안정화 묶음으로 다루고, `Sequence Models` 안에서 `seq2seq`, `attention`, `transformer`를 직접 이어 준다. 이는 `P5-6.3`과 `P5-12.2` 보강이 적절한 방향이었다는 추가 근거가 된다.
- fast.ai 기준에서는 `Initialization/normalization`, `Accelerated SGD`, `Mixed Precision`, `Attention & transformers`가 실무형 foundation block처럼 묶여 있다. 이 관점에서도 현재 Part 5가 `학습 루프와 안정화`, `계산 환경`, `attention/transformer`를 분리해 둔 방식은 충분히 방어 가능하다.
- 반면 fast.ai는 배포, 협업 필터링, 랜덤 포레스트, Stable Diffusion까지 함께 다루므로 범위 자체가 더 실무 지향적이고 넓다. 따라서 fast.ai와의 차이는 `누락`이라기보다 책 전체 설계의 범위 차이로 읽는 편이 맞다.
- 추가 비교까지 포함해도, 현재 Part 5에서 새로 즉시 보강해야 할 결손은 더 발견되지 않았다.

## 지금 단계 결론

외부 비교 기준으로 볼 때 Part 5는 처음부터 `큰 구조는 적합`했고, 비교에서 드러난 핵심 약점은 `학습 안정화 축`과 `seq2seq -> attention 전환`의 설명 밀도였다.

현재 상태에서는 그 두 약점에 대한 직접 보강까지 반영됐으므로, Part 5는 `구조적으로 적합하고, 외부 비교에서 드러난 핵심 공백도 우선 회수된 상태`로 정리할 수 있다.
