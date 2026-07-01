# P4-11.2 합성곱과 풀링 근거 메모

## Section 역할

- Part 4 Module 4 Chapter 11의 두 번째 절입니다.
- CNN의 직관을 실제 핵심 연산인 convolution과 pooling으로 연결합니다.
- 다음 장의 순차 구조 설명 전, 이미지 구조 계산을 마무리합니다.

## 핵심 주장

1. convolution은 작은 필터로 지역 패턴 점수를 계산하는 연산으로 설명할 수 있다.
2. feature map은 필터 반응이 공간적으로 기록된 결과로 설명할 수 있다.
3. pooling은 중요한 반응을 더 작은 형태로 요약하는 연산으로 설명할 수 있다.
4. convolution + pooling 조합은 지역 패턴 탐지와 요약의 반복 흐름으로 읽을 수 있다.

## 근거 출처

### 1) LeCun 1998

- 문서: `Gradient-Based Learning Applied to Document Recognition`
- 저자: Yann LeCun et al.
- 매체: Proceedings of the IEEE, 1998
- 확인 날짜: 2026-06-29

### 2) Deep Learning

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-29

### 3) AlexNet paper

- 문서: `ImageNet Classification with Deep Convolutional Neural Networks`
- 저자: Alex Krizhevsky, Ilya Sutskever, Geoffrey E. Hinton
- 매체: NeurIPS 2012
- 확인 날짜: 2026-06-29

## 제외한 내용

- dilated convolution
- average pooling variants
- FFT optimization details
