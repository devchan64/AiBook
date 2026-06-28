# P4-9.1 GPU와 병렬 처리 근거 메모

## Section 역할

- Part 4 Module 3 Chapter 9의 첫 번째 절입니다.
- 딥러닝 확산을 계산 자원과 함께 읽게 만드는 역사·구조 절입니다.
- 다음 절의 batch/tensor 계산으로 넘어가기 전, 왜 대규모 병렬 수치 연산이 핵심인지 설명합니다.

## 핵심 주장

1. 딥러닝은 큰 행렬/텐서 연산과 반복 계산 때문에 계산 자원에 민감하다.
2. GPU는 유사한 수치 연산을 대량 병렬 처리하는 데 강하며, 딥러닝과 궁합이 좋다.
3. 딥러닝 확산은 알고리즘뿐 아니라 GPU 같은 가속기의 실용화와 강하게 연결된다.
4. AlexNet은 데이터, 깊은 CNN, GPU, 학습 기법이 결합된 전환점으로 설명할 수 있다.

## 근거 출처

### 1) AlexNet paper

- 문서: `ImageNet Classification with Deep Convolutional Neural Networks`
- 저자: Alex Krizhevsky, Ilya Sutskever, Geoffrey E. Hinton
- 매체: NeurIPS 2012
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - GPU-backed large CNN training as landmark turning point

### 2) Deep Learning

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - large-scale neural network computation and tensor operations background

### 3) NVIDIA GPU explanation

- 문서: `What Is a GPU?`
- 기관: NVIDIA
- URL: https://www.nvidia.com/en-us/glossary/gpu/
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - beginner-level explanation of GPU as massively parallel processor

## 집필 판단

- CPU/GPU 차이는 하드웨어 내부 구조보다 `작업 배치 방식` 비유로 설명했습니다.
- Python 예제는 GPU 코드를 직접 돌리기보다, 왜 행렬/벡터 반복 계산이 병렬화와 잘 맞는지 보여 주는 수준으로 제한했습니다.
- AlexNet은 과장 없이 `대표적 전환점`으로만 기술했습니다.

## 제외한 내용

- CUDA internal details
- TPU/NPU comparison
- hardware throughput benchmarks
