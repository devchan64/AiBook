# P4-3.3 출력층과 활성화의 선택 근거 메모

## Section 역할

- Part 4 Module 1 Chapter 3의 세 번째 절입니다.
- 은닉층 활성화 설명을 마무리하고, 출력층 활성화가 문제 유형과 어떻게 연결되는지 정리합니다.
- 손실 함수 장으로 넘어가기 전에 `출력의 의미`와 `손실의 해석`을 연결하는 준비 절입니다.

## 핵심 주장

1. 은닉층 활성화와 출력층 활성화는 역할이 다르며, 출력층 활성화는 최종 출력의 해석과 직접 연결된다.
2. 회귀에서는 선형 출력, 이진 분류에서는 sigmoid, 다중 분류에서는 softmax 기반 해석이 전형적으로 등장한다.
3. score, logit, probability-like output을 구분해야 손실 함수와의 연결을 정확히 설명할 수 있다.
4. 출력층 활성화와 손실 함수는 함께 설계되는 한 쌍으로 설명하는 편이 초심자에게 안전하다.

## 근거 출처

### 1) Deep Learning

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - output unit, probabilistic output, loss function 연결
  - sigmoid / softmax / regression output의 교육적 정리

### 2) Pattern Recognition and Machine Learning

- 문서: `Pattern Recognition and Machine Learning`
- 저자: Christopher M. Bishop
- 출판: Springer, 2006
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - regression, binary classification, multiclass classification의 출력 해석 차이
  - probabilistic classification 관점

### 3) Probabilistic Machine Learning: An Introduction

- 문서: `Probabilistic Machine Learning: An Introduction`
- 저자: Kevin P. Murphy
- 출판: MIT Press, 2022
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - logits와 probability interpretation 구분
  - multiclass output 해석의 일반적 틀

## 집필 판단

- 초심자 기준에서 softmax 수식 유도는 넣지 않고, `후보 간 비교 구조`라는 해석을 먼저 두었습니다.
- 서비스 정책과 모델 출력의 차이를 간단한 스팸 필터 사례로 설명해, `확률처럼 보이는 값`과 실제 action을 섞지 않도록 했습니다.
- 이 절의 중심은 손실 함수 설명의 사전 정리이므로, cross-entropy 자체는 다음 장 범위로 넘겼습니다.

## 제외한 내용

- softmax derivative
- calibration theory
- multi-label classification detail
- logit-loss implementation detail
