# Section P2-3.3 근거 검토: 행렬 곱은 무엇을 재사용하는가

## 검토 목적

- P2-3.3의 중심 질문은 “행렬 곱(matrix multiplication)을 AI 입문자가 어떤 관점으로 읽어야 하는가?”입니다.
- 이 절은 행렬 곱을 공식 암기가 아니라, 가중합(weighted sum)을 여러 번 재사용해 입력 표현을 출력 표현으로 바꾸는 계산으로 설명합니다.

## 확인한 자료

P2-1.1에서 내려받아 확인한 자료를 재사용했습니다. 원문 HTML/PDF는 `.tmp/section-p2-1-1-evidence/` 아래에 있습니다.

| 자료 | 저장 위치 | 반영 판단 |
| --- | --- | --- |
| Deisenroth, Faisal, Ong, *Mathematics for Machine Learning* | `.tmp/section-p2-1-1-evidence/mml-book-home.html` | 머신러닝 수학 기초에서 선형대수와 행렬 계산이 핵심 기반으로 배치된다는 근거로 사용했습니다. |
| Goodfellow, Bengio, Courville, *Deep Learning* | `.tmp/section-p2-1-1-evidence/deeplearningbook-home.html` | 딥러닝에서 선형대수와 벡터/행렬 표현이 기초 배경이라는 근거로 사용했습니다. |
| Harris et al., *Array Programming with NumPy* | `.tmp/section-p2-1-1-evidence/harris-2020-array-programming-numpy.pdf` | 배열, shape, 벡터화된 계산의 코드적 감각을 연결하는 배경 근거로 사용했습니다. |

## 본문 반영 기준

- 행렬 곱(matrix multiplication)을 위치별 곱(element-wise multiplication)과 구분했습니다.
- 벡터와 가중치의 곱을 가중합(weighted sum)으로 설명했습니다.
- 행렬 곱을 여러 가중합을 한꺼번에 계산하는 방식으로 설명했습니다.
- 입력 차원(input dimension), 출력 차원(output dimension), shape의 일치가 계산 가능 여부를 정한다는 점을 강조했습니다.
- 여러 샘플을 행렬로 묶어 같은 가중치 행렬을 적용하는 배치(batch) 계산의 직관을 추가했습니다.
- 선형 변환(linear transformation)을 입력 표현을 다른 출력 표현으로 바꾸는 계산으로 설명했습니다.
- 2차원 벡터가 행렬 곱을 통해 다른 위치로 이동하는 SVG 도표를 추가했습니다.

## Section 경계 검토

- P2-3.3은 행렬 곱과 선형 변환의 직관까지만 다룹니다.
- NumPy 코드 실습과 실제 실행은 P2-3.4로 넘겼습니다.
- 행렬식(determinant), 역행렬(inverse matrix), 고유값(eigenvalue), 고유벡터(eigenvector)는 다루지 않았습니다.
- 활성화 함수(activation function), 역전파(backpropagation), 최적화(optimization)는 후속 장으로 넘겼습니다.
- 신경망 층(layer)은 행렬 곱이 다시 등장하는 위치를 안내하는 수준으로만 언급했습니다.
- 도표는 위치 변화의 직관을 돕기 위한 2차원 예시로 제한하고, 고차원 AI 표현을 그대로 시각화한 것처럼 설명하지 않았습니다.

## 용어 검토

- `행렬 곱(matrix multiplication)`, `위치별 곱(element-wise multiplication)`, `가중합(weighted sum)`, `가중치(weight)`, `가중치 행렬(weight matrix)`, `shape`, `입력 차원(input dimension)`, `출력 차원(output dimension)`, `샘플(sample)`, `배치(batch)`, `선형 변환(linear transformation)`, `층(layer)`, `활성화 함수(activation function)`를 한영 병기했습니다.

## 주의한 오해

- 행렬 곱을 같은 위치끼리 곱하는 계산으로 설명하지 않았습니다.
- 가중치를 “중요도”로만 단정하지 않고, 입력값을 출력에 반영하는 숫자 정도로 제한했습니다.
- 선형 변환만으로 신경망 전체를 설명할 수 있다고 단정하지 않았습니다.
- 행렬 곱을 배우는 목적을 계산 숙련이 아니라 AI 문서와 코드의 shape, weight, layer 설명을 읽기 위한 기반으로 제한했습니다.
- 2차원 도표를 고차원 모델 내부 표현의 실제 모습으로 오해하지 않도록 “직관용 예시”로 표현했습니다.

## 참고 자료

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/), Cambridge University Press, 2020, 확인 날짜: 2026-06-24.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/), MIT Press, 2016, 확인 날짜: 2026-06-24.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256), Nature, 2020, 확인 날짜: 2026-06-24.
