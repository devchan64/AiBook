# P4-4.2 문제 유형별 손실 근거 메모

## Section 역할

- Part 4 Module 2 Chapter 4의 두 번째 절입니다.
- P4-4.1의 손실 함수 일반 개념 다음에, 회귀 / 분류 / 생성 문제에서 손실 관점이 어떻게 달라지는지 설명합니다.
- Part 5의 LLM 학습 손실 이해까지 이어지는 연결 고리 역할을 합니다.

## 핵심 주장

1. 손실 함수는 문제 유형에 따라 달라지며, 회귀는 오차 크기, 분류는 정답 클래스 확률, 생성은 다음 토큰 확률을 중심으로 읽는 것이 적절하다.
2. 분류와 생성은 모두 확률 분포 관점의 손실과 밀접하지만, 생성은 이것이 시퀀스 전체에 반복된다는 점이 다르다.
3. 출력 의미가 달라지면 손실 설계도 함께 달라져야 한다.
4. LLM 학습 손실을 이해하려면 Part 4에서 분류형 확률 손실 감각을 먼저 갖는 것이 유리하다.

## 근거 출처

### 1) Deep Learning book

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-29

### 2) Bishop - Pattern Recognition and Machine Learning

- 문서: `Pattern Recognition and Machine Learning`
- 저자: Christopher M. Bishop
- 출판: Springer, 2006
- 확인 날짜: 2026-06-29

## 제외한 내용

- KL divergence와 cross-entropy의 수학 관계
- sequence-to-sequence 특수 손실
- label smoothing, focal loss 등 특수 손실

이 내용은 Part 5나 후속 심화 절에서 확장할 수 있습니다.
