# 8.1 근거 검토 메모

이 문서는 `docs/chapters/chapter-08/section-01.md`의 근거 연결과 표현 판단을 기록한 관리 메모입니다.

## 작성 목적

- Chapter 8의 첫 절로 지도학습(supervised learning)의 기본 구조를 설명하되, 중심 목표는 라벨(label)의 의미와 기준을 잡는 것입니다.
- 4.2의 입력/출력/데이터, 5.1의 학습/훈련 설명을 반복하지 않고, “학습 유형”의 관점으로 재배치합니다.
- 지도학습을 “라벨 목록 암기”로 오해하지 않도록 입력과 라벨 사이의 관계를 맞추는 방식으로 일반화합니다.
- `label`을 `정답`으로 단순 번역하면 절대적 진실처럼 읽히므로, 본문에서는 라벨(label), 타깃(target), 목표 출력(expected output)을 우선 사용합니다.
- 한국어 독자의 오해를 줄이기 위해 라벨(label)을 `대상을 구분할 수 있게 붙인 표식`, 라벨링(labeling)을 `데이터에 구분 표식을 붙이는 일`로 설명합니다.
- 라벨(label)이 절대적 진실이 아니라 문제 정의 안에서 정한 목표 값일 수 있음을 강조합니다.
- 분류(classification)와 회귀(regression)는 알고리즘 소개가 아니라 라벨 형태의 차이를 보여 주는 예시로 제한합니다.

## 사용 근거

| 자료 | 로컬 확인 | 반영 내용 |
| --- | --- | --- |
| Google for Developers, `Machine Learning Glossary` | `.tmp/section-2-1-labeling-evidence/google-ml-glossary.html` | supervised machine learning, labeled example, label, target, classification model, regression model, proxy label 설명 |
| scikit-learn, `1. Supervised learning` | `.tmp/chapter-04-reference-review/scikit-learn-supervised-learning.html` | supervised learning 아래에 linear models, SVM, decision trees, neural networks, classification/regression 계열 알고리즘이 배치된 구조 |
| AWS, `What is Data Labeling?` | `.tmp/section-8-1-evidence/aws-data-labeling.html`, `.tmp/section-8-1-evidence/aws-data-labeling.txt` | data labeling을 raw data 식별과 label 추가 과정으로 설명, human-provided labels와 ground truth/label accuracy 설명 |
| IBM, `What Is Data Labeling?` | `.tmp/section-8-1-evidence/ibm-data-labeling.html`, `.tmp/section-8-1-evidence/ibm-data-labeling.txt` | data labeling/annotation을 ML preprocessing으로 설명, raw data에 label을 assign하는 과정과 human error/label auditing 설명 |
| Timnit Gebru et al., `Datasheets for Datasets` | `.tmp/section-8-1-evidence/datasheets-for-datasets-abstract.html`, `.tmp/section-8-1-evidence/datasheets-for-datasets-abstract.txt` | 데이터셋의 motivation, composition, collection process, recommended uses 문서화 필요성 |
| `docs/chapters/chapter-04/section-02.md` | 저장소 본문 | 입력(input), 출력(output), 데이터(data)의 기존 설명 |
| `docs/chapters/chapter-05/section-01.md` | 저장소 본문 | learning, training, supervised/unsupervised/reinforcement learning의 기존 경계 |

## 확인한 원문 위치

- `.tmp/section-2-1-labeling-evidence/google-ml-glossary.html`
  - labeled example이 features와 label로 구성되고 training에 사용된다는 설명: 9225-9247행 부근
  - label 설명과 spam/rainfall 예시: 9206-9218행 부근
  - supervised machine learning이 features와 corresponding labels에서 모델을 훈련한다는 설명: 15778-15784행 부근
  - target이 label의 동의어라는 설명: 15864-15867행 부근
  - classification model은 class를 예측하고 regression model은 숫자를 예측한다는 설명: 4024-4025행 부근
  - regression model은 숫자 예측 모델이라는 설명: 13687-13709행 부근
  - 사람 평가자가 라벨링에서 실수할 수 있다는 설명: 11320행 부근
  - proxy labels는 실제 라벨이 없을 때 조심해서 선택해야 한다는 설명: 13080-13105행 부근
- `.tmp/chapter-04-reference-review/scikit-learn-supervised-learning.html`
  - `1. Supervised learning` 제목: 734행 부근
  - supervised learning 아래의 classification/regression 계열 알고리즘 목록: 739-874행 부근
- `.tmp/section-8-1-evidence/aws-data-labeling.txt`
  - data labeling이 raw data를 식별하고 labels를 추가해 ML model이 학습할 수 있게 한다는 설명: 27-30행
  - supervised learning에는 labeled set of data가 필요하고, 사람이 unlabeled data에 판단을 내려 tag를 붙이는 예시: 31-32행
  - human-provided labels가 model training에 쓰이고, ground truth의 정확도가 모델 정확도와 관련된다는 설명: 32-33행
  - labeler consensus, label auditing 설명: 45-48행
- `.tmp/section-8-1-evidence/ibm-data-labeling.txt`
  - data labeling/annotation이 ML model 개발의 preprocessing 단계라는 설명: 257-261행
  - raw data에 label을 assign해 ML model이 interpret하고 prediction할 수 있게 한다는 설명: 261행
  - labeled data는 supervised learning에, unlabeled data는 unsupervised learning에 쓰인다는 설명: 273-284행
  - labeling은 단순해 보이지만 구현이 쉽지 않고, task complexity 등을 고려해야 한다는 설명: 289-290행
  - human error와 label auditing 설명: 319-328행
- `.tmp/section-8-1-evidence/datasheets-for-datasets-abstract.txt`
  - dataset documentation 부재가 고위험 영역에서 문제를 만들 수 있다는 설명: 64행
  - datasheets가 motivation, composition, collection process, recommended uses 등을 문서화한다는 설명: 64행

## 핵심 주장별 검토

| 본문 주장 | 근거 연결 | 판단 |
| --- | --- | --- |
| 8.1의 중심은 지도학습 알고리즘보다 라벨의 의미와 기준이다 | Google Glossary의 labeled example, label, target 설명 | 유지 |
| 라벨은 한국어 설명에서 구분 표식으로 풀어 설명할 수 있다 | label이 데이터에 붙은 목표 값이라는 근거를 한국어 입문용 비유로 일반화 | 유지. 정답이나 정의문으로 번역하지 않기 위한 설명 장치 |
| 라벨은 기호(symbol)와 닮은 면이 있지만 라벨링은 기호 기반 AI와 같지 않다 | 2.1의 기존 도메인 경계와 label 설명 | 유지. 라벨은 구분 가능한 표식이라는 점에서 기호와 닮았지만, 라벨링은 학습 데이터 준비 과정으로 제한 |
| 라벨링은 데이터에 구분 표식을 붙이는 일로 설명할 수 있다 | AWS/IBM의 raw data 식별, label 추가/assign 설명 | 유지. `구분 표식`은 번역어가 아니라 한국어 설명 표현 |
| 지도학습은 입력과 라벨이 함께 있는 예시를 사용한다 | Google Glossary의 supervised machine learning, labeled example 설명 | 유지 |
| labeled example은 입력과 라벨의 묶음으로 설명할 수 있다 | Google Glossary는 features와 label로 설명하지만, 8.1에서는 입문용으로 input + label로 단순화 | 유지. feature 상세는 4.3/Part 3로 넘김 |
| label과 target은 가까운 의미로 쓰일 수 있다 | Google Glossary는 target을 label의 synonym으로 설명 | 유지 |
| classification은 범주를 고르고 regression은 숫자를 예측한다 | Google Glossary의 classification model/regression model 구분, scikit-learn supervised learning 구조 | 유지 |
| 라벨은 절대적 진실이 아니라 문제 정의 안에서 정한 목표 값일 수 있다 | label/proxy label/human labeling error 설명을 입문용으로 일반화 | 유지 |
| 라벨 기준은 데이터셋 문맥과 함께 남기는 것이 바람직하다 | Datasheets for Datasets의 dataset documentation 제안 | 유지. 라벨 기준 문서화까지 확장하되 8.1에서는 원칙 수준으로 제한 |
| 지도학습, 비지도학습, 강화학습, 딥러닝은 같은 분류축이 아니다 | 5.1의 기존 도메인 경계와 목차 기준 | 유지 |

## 도메인 경계

| 섹션 | 맡는 역할 |
| --- | --- |
| 4.2 | 입력, 출력, 데이터의 일반 구조 |
| 5.1 | learning/training/fitting의 의미와 내부 값 조정 |
| 6.3 | 확률 출력, threshold, calibration의 위치 |
| 8.1 | 지도학습의 입력과 라벨 구조, 특히 라벨의 의미와 기준 |
| 8.2 | 라벨 없는 데이터에서 구조를 찾는 비지도학습 |
| 8.3 | 행동과 보상을 다루는 강화학습 |
| Part 3 | 실제 알고리즘, 평가, 과적합, 검증 데이터, 손실 함수 |

## 보수화한 표현

- “지도학습은 라벨 목록을 외운다”라고 쓰지 않았습니다. 입력과 라벨 사이의 관계를 맞추는 방식으로 표현했습니다.
- `정답`은 label의 직접 번역처럼 사용하지 않고, “흔한 입문용 비유지만 조심해야 할 표현”으로 제한했습니다.
- `인식표`와 `구분 표식`은 학술 용어가 아니라 한국어 독자의 오해를 줄이기 위한 설명 표현으로 사용했습니다. 여기서 표식은 대상을 정의하는 설명문이 아니라 구분 가능하게 만드는 이름 또는 표시를 뜻합니다.
- 손실 함수, 경사하강법, 과적합, 검증 데이터는 언급만 하고 Part 3으로 넘겼습니다.
- 분류와 회귀는 알고리즘 이름이 아니라 출력 라벨의 형태 차이로 설명했습니다.
- 딥러닝은 학습 유형이 아니라 여러 학습 유형에 함께 쓰일 수 있는 모델링 접근으로 분리했습니다.

## 남은 검토 사항

- 8.2에서는 비지도학습을 “라벨 없는 데이터에서 구조를 찾는 방식”으로 설명하고, 라벨 없음이 목표 없음과 같지 않음을 강조합니다.
- 8.3에서는 강화학습을 “라벨 대신 행동 후 보상 신호를 사용한다”는 흐름으로 연결합니다.
- Part 3에서 supervised learning의 평가, train/validation/test split, overfitting, loss function을 실제 절차로 다룹니다.

## 검토 결과

- 본문 방향은 유지합니다. 8.1의 중심을 라벨(label)의 의미와 기준으로 둔 것은 근거와 목차 흐름에 맞습니다.
- `인식표`, `구분 표식`은 표준 학술 용어가 아니므로 본문에서 학술 용어처럼 단정하지 않고 한국어 이해를 돕는 설명 표현으로만 사용해야 합니다.
- `라벨 = ground truth`로 쓰지 않습니다. AWS/IBM 자료는 ground truth라는 표현을 쓰지만, 본문에서는 라벨 품질과 기준이 중요하다는 방향으로만 반영합니다.
- `라벨은 기호와 닮았다`는 설명은 2.1과 연결되지만, 라벨링을 기호 기반 AI와 동일시하지 않도록 현재의 경계를 유지합니다.
- Datasheets 논문은 라벨 자체의 정의 근거가 아니라 데이터셋 문서화와 투명성 근거로만 사용합니다.
