# 5.1 근거 분석: 학습은 무엇을 바꾸는가

이 문서는 `docs/chapters/chapter-05/section-01.md`의 근거 연결을 검토한 관리 메모입니다.

원문 확인 규칙에 따라 자료를 `.tmp/section-5-1-evidence/` 아래에 내려받아 확인했습니다. `.tmp/`의 원문 파일은 근거 검토용이며 저장소에 커밋하지 않습니다.

## 확인한 자료

| 자료 | 로컬 확인 | 본문 반영 역할 |
| --- | --- | --- |
| Google for Developers, `Machine Learning Glossary` | `.tmp/section-5-1-evidence/google-ml-glossary.html` | training, parameter, loss, gradient descent, weight, inference 정의 확인 |
| Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning, Chapter 5: Machine Learning Basics` | `.tmp/section-5-1-evidence/deeplearningbook-ml.html` | 학습 알고리즘의 넓은 정의, 훈련 데이터 적합과 일반화 구분 확인 |
| scikit-learn, `Glossary of Common Terms and API Elements` | `.tmp/section-5-1-evidence/scikit-learn-glossary.html` | fit/fitted, fitted attributes, estimator parameter의 API 문맥 확인 |

## 핵심 근거 연결

| 본문 주장 | 근거 | 반영 판단 |
| --- | --- | --- |
| `learning`은 경험 이후 과제 성능이 개선되는 넓은 개념이고, `training`은 내부 값을 조정하는 구체 절차로 구분해서 읽을 수 있다 | Deep Learning Book Chapter 5는 Mitchell(1997)의 learning 정의를 experience, task, performance measure 관점으로 소개하고, Google ML Glossary는 training을 ideal parameters를 결정하는 과정으로 설명함 | 유지. 단, 학술 문헌이 항상 엄격한 대립쌍으로 분리하는 것은 아니므로 “구분해서 읽는 것이 안전하다”로 완화 |
| 훈련은 모델 내부의 파라미터를 조정하는 과정이다 | Google ML Glossary는 training을 모델을 구성하는 이상적인 parameters(weights and biases)를 결정하는 과정으로 설명함 | 유지 |
| `학습(learning)`이라는 표현은 경험 이후 과제 성능이 개선된다는 제한적 의미로 쓰인다 | Deep Learning Book Chapter 5는 Mitchell(1997)의 정의를 소개하며 experience, task, performance measure 관점에서 learning algorithm을 설명함 | 유지. 사람의 학습과 동일시하지 않도록 제한적 의미로 반영 |
| 지도학습, 비지도학습, 강화학습은 경험과 조정 신호가 다르다 | Google ML Glossary는 supervised learning을 features와 labels, unsupervised learning을 unlabeled examples의 구조 찾기, reinforcement learning을 policy와 reward 중심으로 설명함 | 유지. 5.1에서는 구분만 제시하고 세부 내용은 Chapter 8로 보냄 |
| 딥러닝은 학습 유형이라기보다 여러 학습 유형에 적용될 수 있는 신경망 기반 접근이다 | Google ML Glossary와 Deep Learning Book은 deep learning을 machine learning의 특정 종류로 다루며, supervised/unsupervised/reinforcement와 같은 학습 설정과 별도 축으로 설명함 | 유지. 딥러닝 구조 설명은 Part 4로 보냄 |
| 파라미터는 학습 중 모델이 배우는 가중치와 편향을 뜻한다 | Google ML Glossary의 parameter 항목은 weights와 biases를 모델이 training 중 배우는 값으로 설명함 | 유지 |
| 손실은 모델 예측과 라벨 사이의 차이를 나타내는 신호다 | Google ML Glossary의 loss 항목은 지도학습 중 prediction이 label에서 얼마나 떨어져 있는지의 측도로 설명함 | 유지 |
| 경사하강법은 손실을 줄이기 위해 가중치와 편향을 반복 조정한다 | Google ML Glossary의 gradient descent 항목은 loss를 최소화하기 위해 weights와 biases를 반복 조정한다고 설명함 | 수식 없이 역할만 반영 |
| 학습과 inference는 구분해야 한다 | Google ML Glossary의 weight 항목은 training을 ideal weights 결정 과정, inference를 learned weights로 prediction을 만드는 과정으로 구분함 | 유지. 5.2에서 자세히 다루도록 제한 |
| 학습은 단순 암기가 아니라 새 데이터에 일반화되는 관계를 찾는 문제와 연결된다 | Deep Learning Book Chapter 5는 training data에 fit하는 과제와 new data에 generalize되는 pattern을 찾는 과제를 구분함 | 유지. 일반화 세부 내용은 Part 3으로 보냄 |
| fitting은 도구/API 문맥에서 학습 실행을 가리키는 말로 자주 쓰인다 | scikit-learn glossary는 fitting을 fit 호출로, fitted를 fitting 이후 상태로 설명하고, fitted estimator가 prediction에 필요한 attributes를 가질 수 있음을 설명함 | 유지 |
| parameter라는 말은 문맥에 따라 다르게 쓰인다 | scikit-learn glossary는 estimator constructor에 전달하는 값도 parameter라고 부르며, 통계적 의미의 parameter와 다르게 쓴다고 설명함 | 4.3의 혼동 방지 논의를 5.1에서도 짧게 재확인 |

## 섹션 구성 검토

| 검토 항목 | 판단 |
| --- | --- |
| 4.3과의 경계 | 특징, 표현, 파라미터 정의를 반복하지 않고 “학습 때 무엇이 바뀌는가”로 확장 |
| 4.4와의 경계 | 문제 정의와 평가 지표 선택 논의를 반복하지 않고, 학습 목표가 내부 값 조정의 기준이 된다는 수준만 유지 |
| 5.2와의 경계 | inference는 학습과 대비되는 범위에서만 언급하고, 실행 과정 설명은 5.2로 넘김 |
| 5.3과의 경계 | 한국어 `추론` 표현의 혼동은 다루지 않고 영어 용어 training/inference만 구분 |
| Chapter 8과의 경계 | 지도학습, 비지도학습, 강화학습의 세부 원리는 다루지 않고 경험과 조정 신호가 다르다는 경계만 제시 |
| Part 3와의 경계 | 일반화, 과적합, 데이터 분리, 평가 계산은 언급만 하고 머신러닝 장으로 넘김 |
| Part 4와의 경계 | 역전파, 옵티마이저, 딥러닝 구조는 이름만 언급하고 계산 설명은 뒤로 보냄 |

## 주의한 표현

- “모델이 이해한다”는 표현을 피하고, “입력 표현과 출력 사이의 관계를 계산하도록 조정된다”로 일반화했습니다.
- `learning`은 사람의 학습과 완전히 같은 의미가 아니라, 경험 데이터 이후 과제 성능이 개선되는 계산적 의미로 제한했습니다.
- 한국어 `학습`이 `learning`과 `training`을 모두 덮을 수 있으므로, 본문에서는 `학습(learning)`과 `훈련(training)`을 구분했습니다. 다만 두 용어를 완전히 별개의 개념처럼 단정하지 않고, 넓은 개념과 대표적 실행 절차의 관계로 설명했습니다.
- 지도학습 예시를 일반 학습 전체처럼 오해하지 않도록, 강화학습은 라벨 대신 행동과 보상 신호가 중심임을 명시했습니다.
- 딥러닝을 지도학습/비지도학습/강화학습과 같은 분류로 놓지 않고, 여러 학습 설정에서 쓰일 수 있는 신경망 기반 접근으로 분리했습니다.
- “학습은 데이터를 외우지 않는다”를 절대 명제로 쓰지 않았습니다. 모델이 학습 데이터 일부를 기억하거나 재현할 위험은 별도 쟁점으로 남겼습니다.
- `parameter`는 모델 파라미터, 하이퍼파라미터, API 파라미터를 구분했습니다.
- `temperature` 같은 생성 설정값을 모델 내부 파라미터로 오해하지 않도록 4.3의 주의점을 이어 받았습니다.
- 경사하강법은 손실을 줄이는 방향의 대표적 방법으로만 소개하고 수식과 구현은 제외했습니다.

## 본문에 넣지 않은 내용

- 손실 함수별 수식, cross entropy, MSE의 계산은 Part 3에서 다룹니다.
- 역전파와 옵티마이저의 세부 원리는 Part 4에서 다룹니다.
- 검증 데이터, 테스트 데이터, 과적합, 일반화의 상세 판단은 Part 3에서 다룹니다.
- inference의 실행 흐름과 한국어 `추론` 용어 혼동은 5.2와 5.3에서 다룹니다.
- 개인정보·저작권·데이터 암기 위험은 사회적 쟁점 장에서 다룹니다.

## 검증 필요

- `학습(learning)`, `훈련(training)`, `적합(fitting)`의 한국어 사용은 뒤의 머신러닝 실습 문서에서 일관성을 재검토합니다.
- 딥러닝에서 “표현도 함께 달라질 수 있다”는 설명은 Part 4의 표현 학습 절에서 더 엄밀하게 보강해야 합니다.

## 출처

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary), 확인 날짜: 2026-06-22.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning, Chapter 5: Machine Learning Basics](https://www.deeplearningbook.org/contents/ml.html), MIT Press, 2016, 확인 날짜: 2026-06-22.
- scikit-learn developers, [Glossary of Common Terms and API Elements](https://scikit-learn.org/stable/glossary.html), 확인 날짜: 2026-06-22.
