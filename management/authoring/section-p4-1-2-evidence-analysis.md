# P4-1.2 선형 결합과 활성화 근거 메모

## Section 역할

- Part 4 Module 1 Chapter 1의 두 번째 절입니다.
- P4-1.1의 퍼셉트론 소개 다음에, 선형 결합과 활성화의 역할을 분리해 설명합니다.
- 퍼셉트론 하나의 표현 한계를 직관적으로 소개하고, P4-2 다층 신경망으로 연결하는 다리 역할을 합니다.

## 핵심 주장

1. 퍼셉트론은 입력의 선형 결합(linear combination)을 먼저 계산하고, 활성화 규칙을 통해 출력을 만든다고 설명할 수 있다.
2. 퍼셉트론 하나는 입력 공간을 하나의 선형 경계(linear boundary)로 나누는 판단기처럼 볼 수 있다.
3. 활성화는 단순 점수를 판단 또는 다음 층 입력으로 바꾸는 단계로 설명할 수 있다.
4. XOR 같은 패턴은 퍼셉트론 하나의 한계를 설명하는 대표적 입문 사례로 사용할 수 있다.
5. 이런 한계가 다층 신경망의 필요성으로 이어진다고 초심자 수준에서 설명할 수 있다.

## 근거 출처

### 1) Rosenblatt 1958

- 문서: `The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain`
- 저자: Frank Rosenblatt
- 매체: Psychological Review, 1958
- 확인 날짜: 2026-06-28
- 반영 포인트:
  - perceptron의 기본 구조와 임계적 판단 장치라는 역사적 기준

### 2) Minsky and Papert - Perceptrons

- 문서: `Perceptrons: An Introduction to Computational Geometry`
- 저자: Marvin Minsky, Seymour Papert
- 출판: MIT Press, 1969/1988
- 확인 날짜: 2026-06-28
- 반영 포인트:
  - 단일 perceptron의 표현 한계와 선형 분리 한계의 대표 기준
  - XOR류 직관을 설명할 때의 역사적 맥락

### 3) Deep Learning book

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-28
- 반영 포인트:
  - perceptron, linear unit, activation, multilayer network의 연결을 설명하는 현대 교재 기준

## 집필 판단

- 이 절은 수식 유도보다 `점수 계산`과 `판단 단계`를 분리해서 보여 주는 데 집중했습니다.
- XOR는 역사적으로 복잡한 논쟁이 있는 주제이지만, 초심자에게는 `단일 선형 경계의 한계`를 보여 주는 가장 간단한 사례라 판단해 짧게 넣었습니다.
- 활성화 함수의 종류 비교는 P4-3장으로 넘기고, 1.2에서는 활성화의 역할만 먼저 소개했습니다.
- Python 예제는 여전히 학습이 아니라 순전파를 보여 주는 수준으로 제한했습니다.

## 제외한 내용

- step, sigmoid, tanh, ReLU의 상세 수학
- perceptron learning rule
- XOR의 엄밀한 기하학적 증명
- multilayer perceptron 학습 수식

이 내용은 P4-2장과 P4-3장에서 이어서 다룰 수 있습니다.
