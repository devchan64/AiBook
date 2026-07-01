# P4-11.1 CNN의 직관 근거 메모

## Section 역할

- Part 4 Module 4 Chapter 11의 첫 번째 절입니다.
- 표현 학습을 이미지 도메인 구조로 연결하며 CNN의 큰 직관을 소개합니다.
- 다음 절의 convolution/pooling 설명을 위한 입문 절입니다.

## 핵심 주장

1. CNN은 이미지의 지역 패턴을 반복적으로 읽는 신경망으로 설명할 수 있다.
2. 이미지에서는 값 자체뿐 아니라 위치와 이웃 관계가 중요하므로 지역 처리 구조가 자연스럽다.
3. 완전연결층만 사용하는 방식보다 CNN은 공간 구조를 더 잘 보존하는 관점으로 설명할 수 있다.
4. CNN은 이미지 도메인에서 표현 학습의 힘을 크게 보여 준 대표 구조로 설명할 수 있다.

## 근거 출처

### 1) LeCun 1998

- 문서: `Gradient-Based Learning Applied to Document Recognition`
- 저자: Yann LeCun et al.
- 매체: Proceedings of the IEEE, 1998
- 확인 날짜: 2026-06-29

### 2) AlexNet paper

- 문서: `ImageNet Classification with Deep Convolutional Neural Networks`
- 저자: Alex Krizhevsky, Ilya Sutskever, Geoffrey E. Hinton
- 매체: NeurIPS 2012
- 확인 날짜: 2026-06-29

### 3) Deep Learning

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-29

## 제외한 내용

- padding/stride math
- modern convnet variants
- vision transformer comparison
