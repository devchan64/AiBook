# P4-8.2 드롭아웃 근거 메모

## Section 역할

- Part 4 Module 2 Chapter 8의 두 번째 절입니다.
- regularization의 대표 사례로 dropout을 소개합니다.
- training/eval mode, generalization, model capacity를 한 절에서 다시 묶는 역할을 합니다.

## 핵심 주장

1. dropout은 학습 중 일부 노드 출력이나 연결을 무작위로 제거해 과적합을 줄이려는 정규화 기법으로 설명할 수 있다.
2. dropout은 특정 경로 의존을 줄이고 더 견고한 표현을 배우게 만드는 직관으로 설명할 수 있다.
3. dropout은 training mode와 evaluation mode에서 다르게 동작하는 대표 사례다.
4. fully connected network 확산기와 함께 dropout이 큰 실용적 주목을 받았다는 역사적 설명이 가능하다.

## 근거 출처

### 1) Dropout paper

- 문서: `Dropout: A Simple Way to Prevent Neural Networks from Overfitting`
- 저자: Nitish Srivastava et al.
- 매체: JMLR, 2014
- 확인 날짜: 2026-06-29

### 2) Deep Learning

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-29

### 3) Hands-On Machine Learning

- 문서: `Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow`
- 저자: Aurélien Géron
- 출판: O'Reilly, 2022
- 확인 날짜: 2026-06-29

## 제외한 내용

- Monte Carlo dropout
- variational dropout
- framework implementation detail
