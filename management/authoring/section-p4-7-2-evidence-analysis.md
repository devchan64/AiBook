# P4-7.2 SGD, Adam의 직관 근거 메모

## Section 역할

- Part 4 Module 2 Chapter 7의 두 번째 절입니다.
- P4-7.1에서 정의한 optimizer 개념 위에, SGD와 Adam을 초심자 기준으로 비교합니다.
- 현대 실무에서 Adam이 왜 많이 언급되는지와, SGD가 왜 여전히 기준점인지 함께 설명합니다.

## 핵심 주장

1. SGD는 gradient를 비교적 직접 반영하는 기본 업데이트 규칙으로 설명할 수 있다.
2. Adam은 gradient의 누적 정보와 좌표별 적응을 더 반영하는 optimizer로 설명할 수 있다.
3. Adam은 실무에서 편하게 쓰이지만, SGD는 여전히 중요한 기준선과 교육적 출발점이다.
4. optimizer 비교는 속도와 안정성뿐 아니라 일반화 관점도 함께 보아야 한다.

## 근거 출처

### 1) Bottou 2010

- 문서: `Large-Scale Machine Learning with Stochastic Gradient Descent`
- 저자: Léon Bottou
- 매체: COMPSTAT, 2010
- 확인 날짜: 2026-06-29

### 2) Adam paper

- 문서: `Adam: A Method for Stochastic Optimization`
- 저자: Diederik P. Kingma, Jimmy Ba
- 매체: arXiv, 2014
- 확인 날짜: 2026-06-29

### 3) Ruder 2016

- 문서: `An overview of gradient descent optimization algorithms`
- 저자: Sebastian Ruder
- 매체: arXiv, 2016
- 확인 날짜: 2026-06-29

## 제외한 내용

- Adam bias correction formula
- AdamW and decoupled weight decay
- convergence debates in detail
