# P4-6.1 학습과 모델 실행 근거 메모

## Section 역할

- Part 4 Module 2 Chapter 6의 첫 번째 절입니다.
- 역전파 다음에, learning과 inference를 분리해 읽도록 만드는 절입니다.
- 이후 학습 모드/평가 모드, optimizer, 배포 구조를 이해하기 위한 운영적 관점을 준비합니다.

## 핵심 주장

1. learning은 파라미터를 바꾸는 단계이고, inference는 현재 파라미터를 사용해 출력을 계산하는 단계다.
2. 딥러닝의 learning은 forward pass, loss computation, backpropagation, optimizer update를 포함한다.
3. inference도 forward pass를 포함하지만, 목적과 후속 단계가 learning과 다르다.
4. 이 구분이 학습 모드/평가 모드와 배포 관점을 이해하는 전제가 된다.

## 근거 출처

### 1) Deep Learning

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-29

### 2) Pattern Recognition and Machine Learning

- 문서: `Pattern Recognition and Machine Learning`
- 저자: Christopher M. Bishop
- 출판: Springer, 2006
- 확인 날짜: 2026-06-29

### 3) Hands-On Machine Learning

- 문서: `Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow`
- 저자: Aurélien Géron
- 출판: O'Reilly, 2022
- 확인 날짜: 2026-06-29

## 제외한 내용

- serving stack detail
- batch norm and dropout formulas
- online learning and continual learning detail
