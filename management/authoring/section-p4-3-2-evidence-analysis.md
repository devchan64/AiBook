# P4-3.2 ReLU, sigmoid, tanh 근거 메모

## Section 역할

- Part 4 Module 1 Chapter 3의 두 번째 절입니다.
- P4-3.1에서 다룬 활성화 함수의 필요성 다음에, 대표 함수 세 가지를 비교합니다.
- 초심자가 함수 이름 암기가 아니라 출력 범위, 반응 방식, 역사적 위치를 기준으로 읽도록 돕는 절입니다.

## 핵심 주장

1. sigmoid, tanh, ReLU는 모두 비선형 활성화 함수이지만 출력 범위와 입력 반응 방식이 다르다.
2. sigmoid와 tanh는 초기 신경망과 확률형 출력, 0 중심 표현 설명에 중요한 함수로 남아 있다.
3. ReLU는 단순성과 양수 구간에서의 전달 특성 때문에 현대 딥러닝에서 널리 쓰이는 대표 활성화 함수로 설명할 수 있다.
4. 활성화 함수 비교는 수식보다 `출력 범위와 반응 모양`으로 먼저 설명하는 것이 초심자에게 적절하다.

## 근거 출처

### 1) Deep Learning book

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-29

### 2) LeCun, Bengio, Hinton 2015

- 문서: `Deep learning`
- 저자: Yann LeCun, Yoshua Bengio, Geoffrey Hinton
- 매체: Nature, 2015
- URL: https://www.nature.com/articles/nature14539
- 확인 날짜: 2026-06-29

### 3) Glorot, Bordes, Bengio 2011

- 문서: `Deep Sparse Rectifier Neural Networks`
- 저자: Xavier Glorot, Antoine Bordes, Yoshua Bengio
- 매체: AISTATS, 2011
- 확인 날짜: 2026-06-29

## 제외한 내용

- GELU, Swish, Leaky ReLU 비교
- saturation과 vanishing gradient의 수학적 상세
- softmax와 output activation 비교

이 내용은 뒤 학습 계산 파트나 후속 심화 절에서 다룰 수 있습니다.
