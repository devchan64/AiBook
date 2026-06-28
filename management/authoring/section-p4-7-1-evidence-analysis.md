# P4-7.1 옵티마이저의 역할 근거 메모

## Section 역할

- Part 4 Module 2 Chapter 7의 첫 번째 절입니다.
- 손실, 역전파 다음에 optimizer가 학습 절차에서 어떤 자리를 차지하는지 정리합니다.
- 다음 절의 SGD, Adam 비교를 위한 기준 절입니다.

## 핵심 주장

1. optimizer는 backpropagation이 계산한 gradient를 실제 parameter update로 바꾸는 규칙이다.
2. gradient와 update는 같은 것이 아니며, learning rate 같은 설정이 중간에 개입한다.
3. optimizer 선택은 단순 구현 선택이 아니라 학습 전략과 dynamics에 영향을 준다.
4. 딥러닝 커리큘럼에서 optimizer는 loss/backprop과 분리해 설명하는 편이 초심자에게 안전하다.

## 근거 출처

### 1) Deep Learning

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - optimization overview
  - gradient-based learning과 update rule 연결

### 2) Bottou 2010

- 문서: `Large-Scale Machine Learning with Stochastic Gradient Descent`
- 저자: Léon Bottou
- 매체: COMPSTAT, 2010
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - SGD의 역할과 large-scale learning 관점

### 3) Ruder 2016

- 문서: `An overview of gradient descent optimization algorithms`
- 저자: Sebastian Ruder
- 매체: arXiv, 2016
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - optimizer family 비교의 입문적 구조

## 집필 판단

- 이 절은 세부 optimizer 공식 대신 `누가 파라미터를 실제로 바꾸는가`를 명확히 하는 데 집중했습니다.
- learning rate를 핵심 하이퍼파라미터로 다시 불러와 Part 3과 연결했습니다.
- gradient와 update의 차이를 아주 작은 수치 예제로 직접 보여 주도록 구성했습니다.

## 제외한 내용

- momentum formula
- Adam internals
- convergence proof
