# P4-8.1 정규화 근거 메모

## Section 역할

- Part 4 Module 2 Chapter 8의 첫 번째 절입니다.
- optimizer 다음에, 일반화(generalization)를 지키기 위한 제약 관점으로 regularization을 도입합니다.
- 다음 절의 dropout을 넓은 regularization 흐름 안에 배치하는 기준 절입니다.

## 핵심 주장

1. regularization은 과적합을 줄이기 위해 학습에 제약이나 비용을 추가하는 생각으로 설명할 수 있다.
2. regularization은 penalty term만이 아니라 더 넓은 설계 철학으로 볼 수 있다.
3. optimizer와 regularization은 모두 학습에 영향을 주지만 질문이 다르다.
4. data loss와 regularization term을 함께 읽어야 전체 목적 함수를 이해할 수 있다.

## 근거 출처

### 1) The Elements of Statistical Learning

- 문서: `The Elements of Statistical Learning`
- 저자: Trevor Hastie, Robert Tibshirani, Jerome Friedman
- 출판: Springer, 2009
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - overfitting, model complexity, regularization background

### 2) Deep Learning

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - modern deep learning regularization overview
  - parameter norm penalties and broader strategies

### 3) Pattern Recognition and Machine Learning

- 문서: `Pattern Recognition and Machine Learning`
- 저자: Christopher M. Bishop
- 출판: Springer, 2006
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - penalty-based regularization and generalization connection

## 집필 판단

- 이 절은 L1/L2 수식 심화보다 `왜 제약이 필요한가`를 먼저 설명했습니다.
- dropout을 별도 절로 넘기기 위해, regularization을 넓은 철학으로 정리했습니다.
- Python 예제는 weight penalty intuition만 보여 주는 수준으로 제한했습니다.

## 제외한 내용

- full L1/L2 derivation
- early stopping detail
- data augmentation detail
