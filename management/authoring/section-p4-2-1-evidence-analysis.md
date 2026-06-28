# P4-2.1 다층 신경망 근거 메모

## Section 역할

- Part 4 Module 1 Chapter 2의 첫 번째 절입니다.
- P4-1장의 퍼셉트론과 선형 한계 설명 다음에, 다층 신경망이 왜 등장하는지 설명합니다.
- 입력층, 은닉층, 출력층의 역할을 초심자 기준으로 정리하고, P4-2.2의 표현 설명으로 넘기는 다리 역할을 합니다.

## 핵심 주장

1. 다층 신경망은 퍼셉트론 같은 계산 단위를 여러 층으로 쌓아 중간 표현을 만들고 더 복잡한 판단을 구성하는 구조로 설명할 수 있다.
2. 은닉층(hidden layer)은 입력도 출력도 아닌 중간 계산층이며, 모델 내부 표현이 형성되는 핵심 위치로 소개할 수 있다.
3. 단일 퍼셉트론의 선형 한계가 다층 구조의 필요성으로 이어진다고 초심자 수준에서 설명할 수 있다.
4. 다층 구조는 딥러닝이 표현 학습(representation learning)으로 들어가는 출발점처럼 읽을 수 있다.

## 근거 출처

### 1) Deep Learning book

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-28
- 반영 포인트:
  - multilayer perceptron과 hidden unit의 기본 설명
  - deep feedforward networks가 중간 표현을 구성하는 교재 기준

### 2) LeCun, Bengio, Hinton 2015

- 문서: `Deep learning`
- 저자: Yann LeCun, Yoshua Bengio, Geoffrey Hinton
- 매체: Nature, 2015
- URL: https://www.nature.com/articles/nature14539
- 확인 날짜: 2026-06-28
- 반영 포인트:
  - deep learning을 multiple levels of representation을 학습하는 구조로 설명하는 상위 배경

### 3) Cybenko 1989

- 문서: `Approximation by Superpositions of a Sigmoidal Function`
- 저자: George Cybenko
- 매체: Mathematics of Control, Signals, and Systems, 1989
- 확인 날짜: 2026-06-28
- 반영 포인트:
  - hidden layer를 가진 feedforward network의 표현력 논의와 연결되는 고전적 기준

## 집필 판단

- 이 절은 universal approximation theorem을 엄밀히 설명하지 않고, `층을 쌓는 이유`와 `중간 표현`의 직관을 먼저 잡는 데 집중했습니다.
- 은닉층은 해석 가능한 명시적 특징이라기보다 내부 중간 표현이라는 점을 강조했습니다.
- Python 예제는 학습이 아니라 층을 거치는 순전파 흐름만 보여 주도록 제한했습니다.
- CNN, RNN, Transformer 같은 구조는 뒤 Chapter에서 다루므로 2.1에서는 일반 feedforward 감각만 유지했습니다.

## 제외한 내용

- backpropagation을 통한 다층 학습 공식
- 활성화 함수 비교
- hidden representation 해석 기법
- 깊이와 너비의 이론적 trade-off

이 내용은 P4-2.2 이후 절에서 확장할 수 있습니다.
