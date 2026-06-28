# P4-5.2 계산 그래프 근거 메모

## Section 역할

- Part 4 Module 2 Chapter 5의 두 번째 절입니다.
- 역전파의 직관을 `연산 그래프` 관점으로 정리해, 이후 자동미분과 프레임워크 이해로 연결합니다.
- 옵티마이저 장으로 가기 전, gradient가 어떤 구조에서 계산되는지 보이게 하는 절입니다.

## 핵심 주장

1. 계산 그래프는 연산과 의존 관계를 노드와 연결로 펼쳐 놓은 표현으로 설명할 수 있다.
2. 순전파는 값 계산, 역전파는 gradient 전달이라는 방향 차이를 그래프 위에서 읽을 수 있다.
3. 계산 그래프는 연쇄 법칙을 국소 규칙들의 조합으로 바꾸어 복잡한 미분을 읽기 쉽게 한다.
4. 자동미분은 계산 그래프를 따라 gradient를 체계적으로 계산하는 절차로 설명할 수 있다.

## 근거 출처

### 1) Deep Learning

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - computational graph와 backpropagation 관계
  - composed function과 chain rule 설명

### 2) Pattern Recognition and Machine Learning

- 문서: `Pattern Recognition and Machine Learning`
- 저자: Christopher M. Bishop
- 출판: Springer, 2006
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - layered computation, chain rule, network gradient intuition

### 3) micrograd

- 문서: `micrograd`
- 저자: Andrej Karpathy
- 형식: GitHub repository
- URL: https://github.com/karpathy/micrograd
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - 작은 연산 그래프와 역전파를 교육용 코드로 설명하는 대표 사례

## 집필 판단

- 이 절은 프레임워크 API보다 `왜 그래프로 보는가`에 집중했습니다.
- Python 예제는 자동미분 라이브러리 없이 단일 ReLU 경로를 수동으로 계산해, 중간값 저장과 gradient 분해를 보여 주도록 했습니다.
- micrograd는 학술 논문이 아니라 교육적 구현 사례로만 제한적으로 인용했습니다.

## 제외한 내용

- static vs dynamic graph implementation detail
- reverse-mode autodiff formalism
- framework internals
