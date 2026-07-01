# P4-3.1 활성화 함수 근거 메모

## Section 역할

- Part 4 Module 1 Chapter 3의 첫 번째 절입니다.
- P4-2장의 다층 구조 설명 다음에, 활성화 함수가 왜 필요한지 설명합니다.
- 비선형성(nonlinearity)이 딥러닝 표현력과 어떻게 연결되는지 초심자 기준으로 정리하는 절입니다.

## 핵심 주장

1. 활성화 함수는 가중합 결과에 비선형 변환을 주어 신경망의 표현력을 높이는 역할로 설명할 수 있다.
2. 선형 층만 반복하면 전체 계산도 큰 선형 변환으로 접히기 쉬우므로, 깊이의 장점이 제한될 수 있다.
3. 활성화 함수는 은닉층의 내부 표현이 단순 복사에 머물지 않게 만드는 핵심 장치로 설명할 수 있다.
4. 활성화 함수의 구체적 종류 비교 이전에, `왜 필요한가`를 먼저 설명하는 것이 초심자에게 적절하다.

## 근거 출처

### 1) Deep Learning book

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-29

### 2) LeCun, Bengio, Hinton 2015

- 문서: `Deep learning`
- 저자: Yann LeCun, Yoshua Bengio, Geoffrey Hinton
- 매체: Nature, 2015
- URL: https://www.nature.com/articles/nature14539
- 확인 날짜: 2026-06-29

## 제외한 내용

- sigmoid, tanh, ReLU의 상세 비교
- dead ReLU, saturation 같은 최적화 문제
- output activation 설계

이 내용은 P4-3.2 이후 절에서 확장할 수 있습니다.
