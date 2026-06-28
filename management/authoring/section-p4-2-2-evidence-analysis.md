# P4-2.2 은닉층과 표현 근거 메모

## Section 역할

- Part 4 Module 1 Chapter 2의 두 번째 절입니다.
- P4-2.1에서 소개한 다층 구조를 이어 받아, 은닉층(hidden layer)이 왜 중요한지를 표현(representation) 관점에서 설명합니다.
- 딥러닝을 representation learning으로 읽는 기본 관점을 초심자에게 처음 제시하는 절입니다.

## 핵심 주장

1. 은닉층은 입력과 출력 사이의 단순 중계층이 아니라, 더 유용한 내부 표현을 형성하는 층으로 설명할 수 있다.
2. representation은 같은 입력을 모델 내부에서 다시 적는 방식, 또는 더 유리한 내부 좌표계처럼 설명할 수 있다.
3. 층이 깊어질수록 더 추상적이거나 문제 중심적인 표현이 형성될 수 있다는 설명은 딥러닝 문헌의 대표적 관점과 맞닿아 있다.
4. 은닉층 표현은 분산 표현(distributed representation)일 수 있으므로, 각 노드를 지나치게 단순한 인간 언어로 1:1 해석하는 것은 조심해야 한다.

## 근거 출처

### 1) Bengio, Courville, Vincent 2013

- 문서: `Representation Learning: A Review and New Perspectives`
- 저자: Yoshua Bengio, Aaron Courville, Pascal Vincent
- 매체: IEEE Transactions on Pattern Analysis and Machine Intelligence, 2013
- 확인 날짜: 2026-06-28
- 반영 포인트:
  - representation learning을 딥러닝의 핵심 관점으로 다루는 기준
  - distributed representation, abstraction, feature learning의 대표 설명

### 2) Deep Learning book

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-28
- 반영 포인트:
  - hidden units, representation, multilayer network의 교재적 설명

### 3) LeCun, Bengio, Hinton 2015

- 문서: `Deep learning`
- 저자: Yann LeCun, Yoshua Bengio, Geoffrey Hinton
- 매체: Nature, 2015
- URL: https://www.nature.com/articles/nature14539
- 확인 날짜: 2026-06-28
- 반영 포인트:
  - deep learning을 multiple levels of representation 학습으로 설명하는 상위 맥락

## 집필 판단

- 이 절은 hidden layer를 해석 가능한 의미 단위로 너무 단순화하지 않도록 주의했습니다.
- `내부 좌표계` 비유를 사용해 representation의 직관을 잡되, 실제 노드가 곧바로 인간이 붙인 이름과 1:1 대응하지 않을 수 있다는 점을 분명히 했습니다.
- Python 예제는 학습 없이도 입력이 은닉층을 지나며 다른 수치 표현으로 바뀐다는 점을 보여 주는 수준으로 제한했습니다.

## 제외한 내용

- feature visualization
- interpretability methods
- embedding geometry
- disentanglement의 이론적 논의

이 내용은 P4-10장 또는 후속 심화 파트에서 확장할 수 있습니다.
