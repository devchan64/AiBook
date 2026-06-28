# P4-10.1 표현 학습 근거 메모

## Section 역할

- Part 4 Module 3 Chapter 10의 첫 번째 절입니다.
- 딥러닝의 핵심 가치를 `표현 학습` 관점으로 설명합니다.
- 특징 공학에서 learned representation으로의 전환을 Part 1 흐름과 다시 연결합니다.

## 핵심 주장

1. representation learning은 모델이 유용한 내부 표현을 데이터에서 학습하는 과정으로 설명할 수 있다.
2. 이는 사람이 직접 특징을 설계하는 전통적 feature engineering과 대비된다.
3. 딥러닝 확산의 핵심은 규모만이 아니라 강한 표현 학습 능력에도 있다.
4. 이미지, 추천, 텍스트 임베딩 등 여러 도메인에서 같은 관점이 적용될 수 있다.

## 근거 출처

### 1) Bengio et al. 2013

- 문서: `Representation Learning: A Review and New Perspectives`
- 저자: Yoshua Bengio, Aaron Courville, Pascal Vincent
- 매체: IEEE TPAMI, 2013
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - representation learning 정의와 역사적 중요성

### 2) Deep Learning

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - learned representation vs hand-crafted features framing

### 3) AlexNet paper

- 문서: `ImageNet Classification with Deep Convolutional Neural Networks`
- 저자: Alex Krizhevsky, Ilya Sutskever, Geoffrey E. Hinton
- 매체: NeurIPS 2012
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - image recognition success as practical expression of learned hierarchical features

## 집필 판단

- feature engineering과 대비해 설명해 초심자에게 의미를 명확히 했습니다.
- 추천/임베딩 사례를 넣어 이미지에만 국한되지 않도록 했습니다.
- 표현 학습을 곧바로 LLM과 임베딩으로 이어지는 관점으로 남겨 두었습니다.

## 제외한 내용

- disentanglement theories
- self-supervised modern methods
- representation quality metrics
