# Section P2-2.2 근거 검토: 시그마와 반복 계산

## 검토 목적

- P2-2.2의 중심 질문은 “시그마(sigma)를 AI 계산 문맥에서 어떻게 읽을 것인가?”입니다.
- 이 절은 시그마를 엄밀한 수학 기호 전체로 가르치기보다, 반복 덧셈과 평균, 손실 집계의 직관으로 설명합니다.

## 확인한 자료

P2-1.1에서 내려받아 확인한 자료를 재사용했습니다. 원문 HTML/PDF는 `.tmp/section-p2-1-1-evidence/` 아래에 있습니다.

| 자료 | 저장 위치 | 반영 판단 |
| --- | --- | --- |
| Deisenroth, Faisal, Ong, *Mathematics for Machine Learning* | `.tmp/section-p2-1-1-evidence/mml-book-home.html` | 머신러닝 수학 기초 구성의 배경 근거로 사용했습니다. |
| Goodfellow, Bengio, Courville, *Deep Learning* | `.tmp/section-p2-1-1-evidence/deeplearningbook-home.html` | 손실, 학습, 수치 계산을 읽기 위한 수학 표기 복구의 배경 근거로 사용했습니다. |
| Harris et al., *Array Programming with NumPy* | `.tmp/section-p2-1-1-evidence/harris-2020-array-programming-numpy.pdf` | 반복문과 배열 계산을 연결하는 설명의 근거로 사용했습니다. |

## 본문 반영 기준

- 시그마(sigma)를 반복 덧셈의 압축 표기로 설명했습니다.
- 시그마 표기를 큰 기호, 아래 첨자, 위 첨자, 오른쪽 항으로 나누어 읽는 수학교육적 설명을 추가했습니다.
- 시그마가 이후 통계, 손실 계산, 배치 계산, 최적화 설명을 읽는 데 왜 도움이 되는지 사전 안내를 추가했습니다.
- 평균(mean)과 평균 손실(mean loss)을 예시로 사용했습니다.
- 실제 손실 함수(loss function)의 종류나 최적화(optimization)는 후속 Chapter로 넘겼습니다.
- 코드 예시는 Python 반복문과 NumPy 배열 계산의 차이를 직관적으로 보여 주는 수준으로 제한했습니다.

## Section 경계 검토

- P2-2.2는 시그마와 반복 계산만 다룹니다.
- 극한(limit)은 P2-2.3으로 넘겼습니다.
- 벡터(vector), 행렬(matrix), 텐서(tensor)의 상세 구조는 P2-3.x로 넘겼습니다.
- 평균 제곱 오차(MSE)는 이름만 언급하고, 평가 지표와 손실 함수 설명은 Part 3과 P2-6.x로 넘겼습니다.
- 배치(batch)는 반복 계산의 문맥으로만 설명하고, 딥러닝 학습의 세부 구현은 Part 4로 넘겼습니다.
- 통계, 그래디언트, 최적화는 “시그마가 이후 도움이 되는 위치”로만 예고하고, 상세 설명은 후속 Section으로 넘겼습니다.

## 용어 검토

- `시그마(sigma)`, `반복 계산(iterative calculation)`, `인덱스(index)`, `항(term)`, `평균(mean)`, `손실(loss)`, `평균 손실(mean loss)`, `반복문(loop)`, `배열 계산(array computation)`, `배치(batch)`, `샘플(sample)`, `예측(prediction)`, `목표값(target)`을 한영 병기했습니다.
- `Σ` 기호와 평균, 평균 손실 표기는 MathJax 렌더링을 전제로 수식 블록으로 설명했습니다.

## 주의한 오해

- 시그마를 모든 반복 계산과 완전히 같은 것으로 단정하지 않았습니다.
- 시그마를 코드 반복문과 완전히 동일한 것으로 단정하지 않고, 같은 반복 구조를 다른 방식으로 보여 주는 표현으로 제한했습니다.
- NumPy의 `.mean()` 내부 구현을 시그마와 동일하다고 단정하지 않고, 같은 집계 구조를 가진다고 설명했습니다.
- 손실 함수와 최적화의 세부 수학을 이 절에서 확장하지 않았습니다.
- 배치 계산을 딥러닝 전체 구조로 확장하지 않았습니다.

## 참고 자료

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/), Cambridge University Press, 2020, 확인 날짜: 2026-06-24.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/), MIT Press, 2016, 확인 날짜: 2026-06-24.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256), Nature, 2020, 확인 날짜: 2026-06-24.
