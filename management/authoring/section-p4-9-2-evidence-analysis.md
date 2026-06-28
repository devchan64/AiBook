# P4-9.2 배치와 텐서 계산 근거 메모

## Section 역할

- Part 4 Module 3 Chapter 9의 두 번째 절입니다.
- GPU/병렬 처리 관점을 실제 딥러닝 데이터 모양인 batch와 tensor로 연결합니다.
- Part 2의 배열/행렬 감각과 Part 4의 대규모 계산을 잇는 절입니다.

## 핵심 주장

1. batch는 여러 샘플을 한꺼번에 처리하는 계산 단위로 설명할 수 있다.
2. tensor는 벡터와 행렬을 포함하는 다차원 숫자 배열의 일반 이름으로 설명할 수 있다.
3. shape를 읽는 감각은 딥러닝 실습에서 핵심적이다.
4. batch와 tensor는 GPU 병렬 계산과 직접 연결되는 표현 방식이다.

## 근거 출처

### 1) Deep Learning

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - tensor-based computation background
  - minibatch processing perspective

### 2) Hands-On Machine Learning

- 문서: `Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow`
- 저자: Aurélien Géron
- 출판: O'Reilly, 2022
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - beginner-friendly explanations of batch and tensor shapes

### 3) NumPy ndarray docs

- 문서: `ndarray`
- 기관: NumPy Developers
- URL: https://numpy.org/doc/stable/reference/arrays.ndarray.html
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - multi-dimensional array terminology

## 집필 판단

- 텐서 엄밀 정의보다, 벡터/행렬 확장이라는 교육적 설명을 우선했습니다.
- shape 오류 감각을 강조해 실습 연결성을 높였습니다.
- Python 예제는 NumPy shape 확인 수준으로 제한해 개념을 명확히 했습니다.

## 제외한 내용

- memory layout details
- distributed batch pipeline
- framework-specific tensor internals
