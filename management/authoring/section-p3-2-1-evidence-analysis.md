# P3-2.1 근거 검토 메모

## 대상 섹션

- `docs/parts/part-03/chapter-02/section-01.md`
- 주제: 지도학습(supervised learning)

## 확인한 근거

### scikit-learn Supervised Learning User Guide

- URL: https://scikit-learn.org/stable/supervised_learning.html
- 확인 날짜: 2026-06-25
- 활용 지점:
  - scikit-learn이 supervised learning 아래에서 선형 모델, SVM, 최근접 이웃, 나이브 베이즈, 결정트리, 앙상블 등 여러 알고리즘을 다룬다는 점을 확인했다.
  - 지도학습을 단일 알고리즘이 아니라 라벨이 있는 학습 문제의 큰 범주로 설명하는 근거로 사용했다.
  - 분류와 회귀가 지도학습에서 반복적으로 등장하는 문제 유형임을 설명하는 배경으로 사용했다.

### Google for Developers, Supervised Learning

- URL: https://developers.google.com/machine-learning/intro-to-ml/supervised
- 확인 날짜: 2026-06-25
- 활용 지점:
  - 지도학습이 라벨이 있는 데이터로 모델을 학습하고, 새 데이터의 결과를 예측하는 흐름으로 설명됨을 확인했다.
  - 데이터, 모델, 학습, 평가, 추론(inference)을 지도학습의 기초 개념으로 정리하는 설명을 확인했다.
  - 예시(example), 특징(feature), 라벨(label), labeled example, unlabeled example의 구분을 본문 설명에 일반화했다.
  - 데이터셋의 크기와 다양성이 모델 성능과 일반화에 영향을 준다는 설명을 확인했다.

## 반영 판단

- 이 절은 지도학습의 첫 도입이므로 개별 알고리즘의 수식보다 `X`, `y`, 분류, 회귀, 학습, 평가, 예측의 흐름을 중심으로 작성했다.
- Google 자료는 초심자용 개념 설명에 적합하고, scikit-learn 자료는 이후 실습과 알고리즘 분류로 이어지는 공식 문서로 적합하다.
- 출처 문장을 직접 인용하지 않고, 책의 흐름에 맞게 한국어 설명으로 재구성했다.
- 지도학습 흐름 도식은 자체 제작 Mermaid 도식이다. 특정 외부 그림을 재작성한 것이 아니라, 본문에서 설명한 labeled examples, train/test split, training, evaluation, prediction, service decision의 관계를 시각화했다.
- Part 3 초심자 기준에 맞춰 고객 문의 분류 예시를 앞쪽에 추가했다. 라벨이 있는 사례가 무엇인지 먼저 보여 준 뒤 `X`, `y` 표기로 이동하도록 구성했다.
- `X`, `y`, 행(row), 열(column)을 수학 표기보다 먼저 “모델에게 보여 주는 입력 묶음”과 “모델이 맞추려는 출력 묶음”으로 설명하도록 보강했다.
- 학습(training), 평가(evaluation), 예측(prediction)을 별도 표로 다시 구분해, 모델을 학습하는 것과 모델이 쓸 만한지 확인하는 것과 모델을 실행하는 것이 다르다는 점을 명확히 했다.

## 주의할 표현

- 라벨(label)을 현실의 완전한 정답으로 단정하지 않는다.
- 지도학습을 단순 암기나 정답 외우기로 설명하지 않는다.
- 모델 예측과 서비스 최종 결정을 같은 것으로 쓰지 않는다.
- 분류와 회귀를 특정 알고리즘 이름으로 구분하지 않고 출력의 성격으로 먼저 설명한다.
- 지도학습, 비지도학습, 강화학습의 비교 전체는 Chapter 2 전체에서 다루고, 이 절은 지도학습에 집중한다.
