# Section P2-2.1 근거 검토: 변수, 함수, 식 다시 읽기

## 검토 목적

- P2-2.1의 중심 질문은 “AI 문서에서 변수, 함수, 식을 어떻게 다시 읽을 것인가?”입니다.
- 이 절은 Chapter 2의 시작으로, 시그마와 극한을 다루기 전에 수학 표기의 가장 기본 단위를 복구합니다.

## 확인한 자료

P2-1.1에서 내려받아 확인한 자료를 재사용했습니다. 원문 HTML/PDF는 `.tmp/section-p2-1-1-evidence/` 아래에 있습니다.

| 자료 | 저장 위치 | 반영 판단 |
| --- | --- | --- |
| Deisenroth, Faisal, Ong, *Mathematics for Machine Learning* | `.tmp/section-p2-1-1-evidence/mml-book-home.html` | 머신러닝을 읽기 위한 수학 기초라는 큰 방향의 근거로 사용했습니다. |
| Goodfellow, Bengio, Courville, *Deep Learning* | `.tmp/section-p2-1-1-evidence/deeplearningbook-home.html` | 딥러닝 교재가 수학 기초와 머신러닝 기초를 선행 구성으로 둔다는 점을 근거로 사용했습니다. |
| Harris et al., *Array Programming with NumPy* | `.tmp/section-p2-1-1-evidence/harris-2020-array-programming-numpy.pdf` | 코드에서 값의 타입, 배열, shape를 확인하는 관점의 배경 근거로 사용했습니다. |

## 본문 반영 기준

- 변수(variable), 함수(function), 식(expression)을 엄밀한 수학 정의보다 AI 문서 독해용 관점으로 설명했습니다.
- `y = f(x)`를 입력, 함수 또는 모델, 출력의 관계로 설명했습니다.
- 코드의 변수와 수학의 변수를 같은 것으로 단정하지 않고, 타입(type), shape, 재할당 가능성 차이를 설명했습니다.
- 손실(loss), 파라미터(parameter), 예측(prediction)은 위치를 잡는 정도로만 사용했습니다.

## Section 경계 검토

- P2-2.1은 변수, 함수, 식의 기본 표기만 다룹니다.
- 시그마(sigma)와 반복 계산은 P2-2.2로 넘겼습니다.
- 극한(limit)과 변화의 직관은 P2-2.3으로 넘겼습니다.
- 벡터(vector), 행렬(matrix), 텐서(tensor)의 구조적 설명은 P2-3.x와 P2-11.x로 넘겼습니다.
- 손실 함수(loss function), 경사하강법(gradient descent), 최적화(optimization)는 P2-6.x로 넘겼습니다.

## 용어 검토

- `변수(variable)`, `함수(function)`, `식(expression)`, `입력(input)`, `출력(output)`, `모델(model)`, `파라미터(parameter)`, `손실(loss)`, `예측(prediction)`, `목표값(target)`, `타입(type)`, `모양(shape)`, `데이터셋(dataset)`을 한영 병기했습니다.
- `함수`는 Python 함수와 수학 함수가 완전히 같지 않다는 점을 명시했습니다.
- `모델을 함수처럼 다룰 수 있다`는 표현은 입문적 비유로 사용하고, 모델 내부의 학습된 파라미터가 있다는 차이를 함께 적었습니다.

## 주의한 오해

- 변수 이름만 보면 의미를 알 수 있다고 설명하지 않았습니다.
- `y = f(x)` 하나로 모든 AI 모델을 설명할 수 있다고 단정하지 않았습니다.
- 손실 계산과 파라미터 업데이트를 실제 알고리즘처럼 자세히 설명하지 않았습니다.
- NumPy 예시는 shape와 dtype 확인의 필요성을 보여 주는 수준으로 제한했습니다.

## 참고 자료

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/), Cambridge University Press, 2020, 확인 날짜: 2026-06-24.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/), MIT Press, 2016, 확인 날짜: 2026-06-24.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256), Nature, 2020, 확인 날짜: 2026-06-24.
