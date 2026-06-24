# Section P2-3.1 근거 검토: 스칼라, 벡터, 행렬

## 검토 목적

- P2-3.1의 중심 질문은 “스칼라(scalar), 벡터(vector), 행렬(matrix)을 AI 데이터 모양 관점에서 어떻게 복구할 것인가?”입니다.
- 이 절은 선형대수의 엄밀한 공리나 증명보다, 데이터가 숫자 하나, 숫자 목록, 행과 열의 배열로 표현되는 방식을 설명합니다.

## 확인한 자료

P2-1.1에서 내려받아 확인한 자료를 재사용했습니다. 원문 HTML/PDF는 `.tmp/section-p2-1-1-evidence/` 아래에 있습니다.

| 자료 | 저장 위치 | 반영 판단 |
| --- | --- | --- |
| Deisenroth, Faisal, Ong, *Mathematics for Machine Learning* | `.tmp/section-p2-1-1-evidence/mml-book-home.html` | 머신러닝 수학 기초에서 선형대수가 핵심 전제 지식으로 배치된다는 근거로 사용했습니다. |
| Goodfellow, Bengio, Courville, *Deep Learning* | `.tmp/section-p2-1-1-evidence/deeplearningbook-home.html` | 딥러닝에서 선형대수, 확률, 수치 계산이 기본 배경 지식이라는 근거로 사용했습니다. |
| Harris et al., *Array Programming with NumPy* | `.tmp/section-p2-1-1-evidence/harris-2020-array-programming-numpy.pdf` | 배열 계산과 shape 확인을 코드 관점으로 연결하는 근거로 사용했습니다. |

## 본문 반영 기준

- 스칼라(scalar)는 숫자 하나, 벡터(vector)는 순서가 있는 값의 목록, 행렬(matrix)은 행(row)과 열(column)을 가진 숫자 배열로 설명했습니다.
- 수학적 정의보다 AI 데이터 모양(shape)과 코드의 배열(array) 관점에 초점을 맞췄습니다.
- 하나의 샘플(sample)을 벡터로, 여러 샘플을 행렬로 읽는 예시를 사용했습니다.
- shape이 계산 가능 여부와 오류에 영향을 줄 수 있음을 설명했습니다.
- 임베딩, 특징, 배치, 손실, 파라미터에서 다시 등장한다는 사전 안내를 추가했습니다.

## Section 경계 검토

- P2-3.1은 스칼라, 벡터, 행렬의 기본 모양과 의미만 다룹니다.
- 벡터 공간(vector space), 거리(distance), 유사도(similarity), 위치의 직관은 P2-3.2로 넘겼습니다.
- 행렬 곱(matrix multiplication), 선형 변환(linear transformation), 가중치 행렬(weight matrix)은 P2-3.3으로 넘겼습니다.
- NumPy로 벡터와 행렬을 실제 계산하는 실습은 P2-3.4와 P2-11.x로 넘겼습니다.
- 텐서(tensor)는 행렬보다 많은 축을 가진 배열이라는 정도만 후속에서 다루고, 이 절에서는 중심 개념으로 확장하지 않았습니다.

## 용어 검토

- `선형대수(linear algebra)`, `스칼라(scalar)`, `벡터(vector)`, `행렬(matrix)`, `배열(array)`, `모양(shape)`, `행(row)`, `열(column)`, `샘플(sample)`, `특징(feature)`, `입력(input)`, `데이터셋(dataset)`, `목표값(target)`, `라벨(label)`, `임베딩(embedding)`, `배치(batch)`, `파라미터(parameter)`, `가중치(weight)`를 한영 병기했습니다.
- 이미 Part 1에서 반복 등장한 일부 용어도 Part 2의 수학 문맥에서 다시 확인하도록 병기했습니다.

## 주의한 오해

- 벡터를 “단순한 리스트”와 완전히 동일한 것으로 단정하지 않았습니다. 입문 단계에서는 값의 목록으로 읽되, 이후 벡터 공간과 방향/위치의 의미가 확장됨을 남겼습니다.
- 행렬을 모든 표 데이터와 동일한 것으로 단정하지 않았습니다. 표 데이터는 행렬 또는 데이터프레임으로 표현될 수 있다고 제한했습니다.
- shape을 단순 출력값으로만 설명하지 않고, 계산 가능 여부와 오류에 영향을 주는 조건으로 설명했습니다.
- 행렬 곱과 선형 변환은 이 절에서 계산하지 않았습니다.

## 참고 자료

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/), Cambridge University Press, 2020, 확인 날짜: 2026-06-24.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/), MIT Press, 2016, 확인 날짜: 2026-06-24.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256), Nature, 2020, 확인 날짜: 2026-06-24.
