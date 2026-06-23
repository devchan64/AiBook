# Section P2-1.1 근거 검토: AI 계산에서 수학이 하는 일

## 검토 목적

- P2-1.1의 중심 질문은 “AI를 다시 공부하려면 수학을 어떤 관점으로 봐야 하는가?”입니다.
- 이 절은 수학 계산 자체를 가르치는 절이 아니라, Part 2 전체의 도입부입니다.
- 사용자의 관점인 “수학을 증명 중심으로 깊게 이해하기보다, 어떤 목적으로 연구되었고 현재 어떤 목표로 쓰이는지가 중요하다”를 일반화했습니다.

## 확인한 자료

공개 원문은 `.tmp/section-p2-1-1-evidence/` 아래에 내려받아 확인했습니다.

| 자료 | 저장 위치 | 반영 판단 |
| --- | --- | --- |
| Deisenroth, Faisal, Ong, *Mathematics for Machine Learning* | `.tmp/section-p2-1-1-evidence/mml-book-home.html` | 수학을 머신러닝 책을 읽기 위한 기초 역량으로 보는 관점, 선형대수·벡터 미적분·확률·최적화의 배치 근거로 사용했습니다. |
| Goodfellow, Bengio, Courville, *Deep Learning* | `.tmp/section-p2-1-1-evidence/deeplearningbook-home.html` | 딥러닝 교재의 Part I이 선형대수, 확률, 수치 계산, 머신러닝 기초로 구성된다는 점을 Part 2 구성 근거로 사용했습니다. |
| Higham & Higham, *Deep Learning: An Introduction for Applied Mathematicians* | `.tmp/section-p2-1-1-evidence/higham-2018-deep-learning-applied-mathematicians.pdf` | 딥러닝의 핵심에 미적분, 최적화, 선형대수 같은 응용수학 개념이 있다는 설명을 일반화해 사용했습니다. |
| Harris et al., *Array Programming with NumPy* | `.tmp/section-p2-1-1-evidence/harris-2020-array-programming-numpy.pdf` | NumPy와 배열 프로그래밍이 벡터, 행렬, 고차원 배열 계산을 다루는 도구라는 점을 “수학은 코드와 함께 확인해야 한다”는 설명의 근거로 사용했습니다. |

## 본문 반영 기준

- 수학을 시험 과목이나 증명 대상으로 설명하지 않고, AI 계산을 읽는 언어와 압축 표기로 설명했습니다.
- Part 2 전체의 방향을 먼저 제시하고, 세부 계산은 뒤 Section으로 넘겼습니다.
- `수학을 이해할 필요는 없다`는 표현은 너무 강하므로, “모든 증명을 이해할 필요는 없지만 수식이 무엇을 계산하려는지는 읽어야 한다”로 정제했습니다.
- 수학과 코드의 연결을 보여 주기 위해 NumPy 평균 계산 예시만 짧게 사용했습니다.

## Section 경계 검토

- P2-1.1은 Part 2 도입부입니다.
- 시그마(sigma), 극한(limit)의 실제 계산은 P2-2.2, P2-2.3으로 넘겼습니다.
- 벡터(vector), 행렬(matrix), 행렬 곱(matrix multiplication)의 실제 설명은 P2-3.x로 넘겼습니다.
- 미분(derivative), 그래디언트(gradient)는 P2-4.x로 넘겼습니다.
- 확률(probability), 분포(distribution), 평균(mean), 분산(variance)은 P2-5.x로 넘겼습니다.
- 최적화(optimization), 손실 함수(loss function), 경사하강법(gradient descent)은 P2-6.x로 넘겼습니다.

## 용어 검토

- `수식(formula)`, `데이터(data)`, `코드(code)`, `모델(model)`, `학습(learning)`, `손실(loss)`, `파라미터(parameter)`, `함수(function)`, `벡터(vector)`, `행렬(matrix)`, `텐서(tensor)`, `확률(probability)`, `통계(statistics)`, `최적화(optimization)`를 한영 병기했습니다.
- `수학은 언어다`라는 표현은 비유로 사용했으며, 수학의 정의로 단정하지 않았습니다.
- `텐서`는 깊게 설명하지 않고, 축이 더 많은 배열이라는 입문적 직관까지만 사용했습니다.

## 주의한 오해

- 수학을 몰라도 AI를 완전히 이해할 수 있다고 말하지 않았습니다.
- 반대로 수학 증명을 모두 이해해야만 AI를 학습할 수 있다고도 말하지 않았습니다.
- NumPy 예시를 수학 학습의 전부처럼 설명하지 않았습니다.
- Part 2의 모든 세부 개념을 P2-1.1에서 설명하지 않고, 목적과 위치만 소개했습니다.

## 참고 자료

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/), Cambridge University Press, 2020, 확인 날짜: 2026-06-24.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/), MIT Press, 2016, 확인 날짜: 2026-06-24.
- Catherine F. Higham, Desmond J. Higham, [Deep Learning: An Introduction for Applied Mathematicians](https://arxiv.org/abs/1801.05894), arXiv, 2018, 확인 날짜: 2026-06-24.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256), Nature, 2020, 확인 날짜: 2026-06-24.
