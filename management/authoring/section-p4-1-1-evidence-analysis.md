# P4-1.1 퍼셉트론 근거 메모

## Section 역할

- Part 4 Module 1 Chapter 1의 첫 번째 절입니다.
- 딥러닝 파트의 출발점으로서, 퍼셉트론을 가장 작은 신경망 계산 단위로 소개합니다.
- 초심자가 입력, 가중치, 편향, 출력의 흐름을 먼저 이해하도록 만드는 절입니다.

## 핵심 주장

1. 퍼셉트론은 여러 입력을 받아 가중합(weighted sum)을 만들고 그 결과로 출력을 정하는 가장 단순한 신경망 판단 단위로 설명할 수 있다.
2. 퍼셉트론은 역사적으로 Rosenblatt의 1958년 작업을 통해 널리 알려졌으며, 오늘날 딥러닝의 완성형이라기보다 기본 계산 문법의 출발점으로 읽는 것이 적절하다.
3. 가중치(weight)는 입력 중요도를 조절하고, 편향(bias)은 기준선을 옮기는 역할로 설명할 수 있다.
4. 초심자에게는 학습 규칙보다 순전파(forward pass) 계산을 먼저 보여 주는 편이 이해에 유리하다.

## 근거 출처

### 1) Rosenblatt 1958

- 문서: `The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain`
- 저자: Frank Rosenblatt
- 매체: Psychological Review, 1958
- 확인 날짜: 2026-06-28

### 2) Deep Learning book

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-28

### 3) LeCun, Bengio, Hinton 2015

- 문서: `Deep learning`
- 저자: Yann LeCun, Yoshua Bengio, Geoffrey Hinton
- 매체: Nature, 2015
- URL: https://www.nature.com/articles/nature14539
- 확인 날짜: 2026-06-28

## 제외한 내용

- perceptron learning rule의 상세 유도
- activation function 비교
- XOR와 선형 분리 한계의 상세 설명
- 다층 퍼셉트론의 수학

이 내용은 P4-1.2와 P4-2장에서 이어서 다룰 수 있습니다.
