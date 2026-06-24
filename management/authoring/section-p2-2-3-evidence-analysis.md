# Section P2-2.3 근거 검토: 극한과 변화의 직관

## 검토 목적

- P2-2.3의 중심 질문은 “극한(limit)을 AI 계산 문맥에서 어느 수준까지 복구할 것인가?”입니다.
- 이 절은 극한의 엄밀한 증명보다, 변화율(rate of change), 미분(derivative), 그래디언트(gradient), 최적화(optimization)로 이어지는 표기 독해를 목표로 합니다.

## 확인한 자료

P2-1.1에서 내려받아 확인한 자료를 재사용했습니다. 원문 HTML/PDF는 `.tmp/section-p2-1-1-evidence/` 아래에 있습니다.

| 자료 | 저장 위치 | 반영 판단 |
| --- | --- | --- |
| Deisenroth, Faisal, Ong, *Mathematics for Machine Learning* | `.tmp/section-p2-1-1-evidence/mml-book-home.html` | 머신러닝 수학 기초의 전체 배치와 미적분 연결 배경으로 사용했습니다. |
| Goodfellow, Bengio, Courville, *Deep Learning* | `.tmp/section-p2-1-1-evidence/deeplearningbook-home.html` | 딥러닝 학습에서 손실, 그래디언트, 최적화가 연결된다는 배경 근거로 사용했습니다. |
| Higham & Higham, *Deep Learning: An Introduction for Applied Mathematicians* | `.tmp/section-p2-1-1-evidence/higham-2018-deep-learning-applied-mathematicians.pdf` | 응용수학 관점에서 딥러닝을 함수, 미분, 최적화 흐름으로 소개하는 배경 근거로 사용했습니다. |

## 본문 반영 기준

- 극한(limit)을 “값이 가까워질 때 함수값의 경향을 보는 표기”로 설명했습니다.
- 극한 표기를 \(\lim\), \(x \to a\), \(f(x)\), \(L\)로 나누어 읽는 수학교육적 설명을 추가했습니다.
- 극한이 이후 미분, 그래디언트, 최적화, 수치 계산에서 다시 등장하는 이유를 사전 안내했습니다.
- 극한을 직접 대입하거나 식을 정리해 주변 경향을 확인하는 가벼운 풀이 예시를 추가했습니다.
- \(x \to a\), \(h \to 0\), \(f(x) \to L\)의 의미를 구분했습니다.
- 단순 대입(substitution)과 극한이 항상 같지 않다는 점을 간단한 유리식 예시로 설명했습니다.
- 변화율(rate of change)과 미분(derivative)으로 이어지는 직관만 소개했습니다.
- 딥러닝 학습에서는 파라미터 변화와 손실 변화의 관계를 읽는 준비 개념으로 연결했습니다.

## Section 경계 검토

- P2-2.3은 극한 표기와 변화의 직관만 다룹니다.
- 미분 공식, 도함수 계산, 편미분, 그래디언트 계산은 Chapter 4로 넘겼습니다.
- 손실 함수(loss function)와 최적화(optimization)의 세부 알고리즘은 Chapter 6으로 넘겼습니다.
- 수치 미분, 자동미분, 역전파는 Part 4 또는 후속 심화 절에서 다루는 것이 적절합니다.
- 수치 계산과 근사는 극한이 이후 도움이 되는 위치로만 예고하고, 구체적인 수치해석 설명은 후속 Section으로 넘겼습니다.
- 극한의 엄밀한 \(\epsilon\)-\(\delta\) 정의와 연속성 증명은 이 책의 입문 복구 목적에서는 제외했습니다.
- 극한 풀이도 대입 가능한 경우와 간단한 인수분해로 정리되는 경우만 다루고, 복잡한 극한 계산 기법은 제외했습니다.

## 용어 검토

- `극한(limit)`, `함수(function)`, `입력(input)`, `함수값(function value)`, `대입(substitution)`, `변화량(change)`, `변화율(rate of change)`, `미분(derivative)`, `그래디언트(gradient)`, `최적화(optimization)`, `손실(loss)`, `파라미터(parameter)`를 한영 병기했습니다.
- \(\epsilon\)-\(\delta\) 정의는 이름만 언급하고 설명하지 않았습니다. 이 절의 목표가 표기 독해와 직관 복구이기 때문입니다.

## 주의한 오해

- 극한을 단순히 “그 값을 넣는 것”으로 설명하지 않았습니다.
- 극한을 미분과 동일한 개념으로 설명하지 않았습니다.
- 그래디언트와 최적화를 이 절에서 계산 가능한 주제로 확장하지 않았습니다.
- AI 학습에서 모든 변화가 극한 표기로 직접 계산된다고 단정하지 않았습니다. 학습 설명을 읽기 위한 수학적 준비로 제한했습니다.

## 참고 자료

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/), Cambridge University Press, 2020, 확인 날짜: 2026-06-24.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/), MIT Press, 2016, 확인 날짜: 2026-06-24.
- Catherine F. Higham, Desmond J. Higham, [Deep Learning: An Introduction for Applied Mathematicians](https://arxiv.org/abs/1801.05894), arXiv, 2018, 확인 날짜: 2026-06-24.
