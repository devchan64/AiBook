# P4-6.2 학습 모드와 평가 모드 근거 메모

## Section 역할

- Part 4 Module 2 Chapter 6의 두 번째 절입니다.
- learning/inference 구분 위에 training mode / evaluation mode를 올려 설명합니다.
- dropout, batch normalization, validation/test 측정을 자연스럽게 읽게 하는 준비 절입니다.

## 핵심 주장

1. 학습 모드와 평가 모드는 같은 모델의 서로 다른 계산 상태로 설명할 수 있다.
2. dropout은 학습 중에는 무작위 제거를 사용하지만 평가 중에는 안정적 실행을 위해 같은 동작을 유지하지 않는다.
3. batch normalization은 학습 중 배치 통계를, 평가 중 누적 통계를 사용하는 관점으로 설명할 수 있다.
4. validation, test, deployment는 평가 모드 설명과 자연스럽게 연결된다.

## 근거 출처

### 1) Deep Learning

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - dropout, batch normalization의 교육적 배경
  - train/test behavior distinction

### 2) Dropout paper

- 문서: `Dropout: A Simple Way to Prevent Neural Networks from Overfitting`
- 저자: Nitish Srivastava et al.
- 매체: JMLR, 2014
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - training-time stochastic masking이라는 핵심 아이디어

### 3) Batch Normalization paper

- 문서: `Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift`
- 저자: Sergey Ioffe, Christian Szegedy
- 매체: ICML, 2015
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - batch statistics와 inference-time behavior distinction

## 집필 판단

- PyTorch나 Keras의 `train()/eval()` 호출 문법보다 먼저 개념적 차이를 설명했습니다.
- dropout scaling 구현 세부는 이 절의 범위를 벗어나므로 의도적으로 생략했습니다.
- batch normalization은 수식 대신 `현재 배치`와 `누적 기준`의 차이로 먼저 설명했습니다.

## 제외한 내용

- framework-specific API detail
- distributed batch norm
- Monte Carlo dropout interpretation
