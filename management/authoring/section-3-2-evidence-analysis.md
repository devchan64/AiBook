# 3.2 근거 분석: 데이터에서 패턴을 배운다는 것

이 문서는 `docs/chapters/chapter-03/section-02.md`의 근거 연결을 검토한 관리 메모입니다.

원문 확인 규칙에 따라 이미 내려받은 자료를 우선 사용했습니다. `.tmp/`의 원문 파일은 근거 검토용이며 저장소에 커밋하지 않습니다.

## 확인한 자료

| 자료 | 로컬 확인 | 본문 반영 역할 |
| --- | --- | --- |
| Stanford Encyclopedia of Philosophy, `Artificial Intelligence` | `.tmp/section-01-evidence/sep-ai.html` | 머신러닝을 예시 또는 경험을 통해 과제 성능을 개선하는 시스템으로 설명하는 근거, 지도학습·비지도학습·강화학습의 기본 구분 |
| Tom Mitchell, `Machine Learning textbook` | `.tmp/section-3-2-evidence/mitchell-mlbook.html` | 머신러닝을 경험을 통해 자동으로 개선되는 알고리즘 연구로 설명하는 고전적 교재 근거 |
| Google for Developers, `Supervised Learning` | `.tmp/section-2-1-labeling-evidence/google-ml-terminology.html` | 예시, 특징, 라벨, 학습, 평가, 추론, 데이터셋의 크기와 다양성 설명의 근거 |
| scikit-learn, `Underfitting vs. Overfitting` | `.tmp/section-3-2-evidence/sklearn-underfitting-overfitting.html` | 과소적합, 과적합, 새 데이터 일반화 문제를 입문 예제로 설명하는 근거 |
| Fayyad et al., `From Data Mining to Knowledge Discovery in Databases` | `.tmp/section-01-evidence/fayyad-kdd-kdnuggets.pdf`, `.txt` | KDD의 패턴 정의, 새 데이터에서의 유효성, 데이터마이닝과 모델 fitting, 패턴 발견 과정의 근거 |
| George A. Miller, `The Magical Number Seven, Plus or Minus Two` | `.tmp/section-3-2-evidence/miller-magical-number-seven.html` | 청킹(chunking), 재부호화(recoding), 익숙한 단위로 입력을 묶어 처리한다는 학습용 비유의 근거. 머신러닝 모델이 사람처럼 이해한다는 근거로 사용하지 않음 |

## 핵심 근거 연결

| 본문 주장 | 근거 | 반영 판단 |
| --- | --- | --- |
| 머신러닝은 사람이 규칙을 모두 쓰는 대신 데이터나 경험에서 판단 기준을 조정하는 접근으로 설명할 수 있다 | SEP AI 항목은 머신러닝을 예시나 반복 경험을 통해 과제 성능을 개선하는 시스템으로 설명함 | 유지 |
| 머신러닝에서 `경험`은 학습의 핵심 단서로 설명할 수 있다 | Mitchell 교재 소개 페이지는 머신러닝을 경험을 통해 자동으로 개선되는 알고리즘 연구로 설명함 | 고객 문의 예시에서 경험을 과거 문의와 분류로 연결 |
| 지도학습은 입력과 정답의 관계를 배우는 방식으로 설명할 수 있다 | SEP AI 항목은 supervised learning을 입력과 함수값의 예시로부터 함수에 가까운 것을 배우는 방식으로 설명함 | 3.2에서는 지도학습 중심으로 단순화 |
| 예시는 특징과 라벨을 포함할 수 있고, 특징은 모델이 라벨을 예측하는 데 사용하는 값이다 | Google Supervised Learning 자료가 examples, features, label을 설명함 | 유지 |
| 학습된 모델은 새 라벨 없는 데이터에 대해 inference를 수행할 수 있다 | Google 자료가 학습·평가 후 inference에서 새 unlabeled data를 예측한다고 설명함 | 유지하되 5.2의 inference 상세를 침범하지 않음 |
| 데이터셋의 크기와 다양성은 일반화에 영향을 준다 | Google 자료가 dataset size와 diversity가 성능과 generalization에 영향을 준다고 설명함 | 유지 |
| 패턴은 단순 반복이 아니라 새 데이터에서도 어느 정도 유효해야 한다 | Fayyad et al.은 KDD의 패턴이 valid, novel, potentially useful, understandable이어야 하고 새 데이터에서 certainty가 필요하다고 설명함 | 유지 |
| 데이터마이닝은 관찰 데이터에 모델을 맞추거나 패턴을 결정하는 일로 설명될 수 있다 | Fayyad et al.은 data mining involves fitting models to, or determining patterns from, observed data라고 설명함 | 유지하되 3.2에서는 KDD 상세를 길게 다루지 않음 |
| 학습은 단순 암기가 아니라 새 데이터에 적용 가능한 관계를 찾는 과정이다 | Google의 generalization 설명과 Fayyad의 new data validity 관점에서 일반화 | 유지 |
| 과소적합은 모델이 데이터 관계를 충분히 설명하지 못하는 상태이고, 과적합은 학습 데이터의 잡음까지 배워 새 데이터에 약해지는 상태로 설명할 수 있다 | scikit-learn의 Underfitting vs. Overfitting 예제가 단순 모델과 복잡한 모델의 차이를 통해 설명함 | 입문 수준 설명으로 유지하고 대응 기법은 후속 절로 보냄 |
| 모델 출력이 점수나 확률일 수 있고 규칙·사람 검토가 함께 붙을 수 있다 | 본문 자체의 서비스 설계 일반화. 3.1의 규칙과 모델 결합 설명과 연결 | 유지하되 특정 제품 구조처럼 단정하지 않음 |
| 사람의 빠른 판단은 입력을 의미 단위로 묶어 처리한다는 비유로 설명할 수 있다 | Miller는 입력을 익숙한 units or chunks로 조직하고, 더 큰 chunk로 재부호화하면 기억 가능한 정보량이 늘 수 있다고 설명함 | `컨텍스트 압축`을 표준 신경과학 용어로 쓰지 않고 학습용 비유로만 사용 |
| 반복되는 입력을 의미 단위로 묶는 것은 패턴의 한 모양으로 보여줄 수 있다 | Miller의 chunking/recoding 근거와 3.2의 pattern/generalization 설명을 연결한 저자적 일반화 | 사람의 사고를 설명하는 보조 비유로만 유지. 머신러닝의 작동 원리 근거로 확장하지 않음 |

## 주의한 표현

- 3.2에서는 선형회귀, 결정트리, 신경망 같은 알고리즘 상세를 다루지 않습니다. 이는 Part 3과 Part 4로 넘깁니다.
- 과적합(overfitting), 과소적합(underfitting), 일반화(generalization)는 본문에서 영문 병기로 처리합니다. 3.2에서는 용어의 기본 직관까지만 다루고, 평가 지표와 검증 절차는 머신러닝 파트에서 다룹니다.
- `추론`은 3.2에서 inference의 의미로만 짧게 언급합니다. reasoning과의 본격 구분은 5.3에서 다룹니다.
- 고객 문의와 날씨 예시는 학습용 자체 예시입니다. 특정 회사나 실제 서비스의 운영 기준이 아닙니다.
- 3.2는 추상 개념이 많아지기 쉬우므로 고객 문의 분류 예시를 반복 사용합니다. `예시`, `특징`, `라벨`, `학습`, `일반화`, `패턴`을 서로 다른 예시로 흩뜨리지 않고 하나의 흐름으로 연결합니다.
- 모델 출력의 점수표는 개념 예시입니다. 실제 확률 보정(calibration)이나 분류 임계값 설정은 후속 절에서 다룹니다.
- `데이터에서 패턴을 배운다`는 표현을 데이터 안의 우연한 반복을 그대로 믿는 뜻으로 쓰지 않았습니다. 새 데이터에서의 유효성과 일반화 관점을 함께 설명했습니다.
- `컨텍스트 압축`은 본문에서 표준 용어로 정의하지 않습니다. 사용자의 직관을 일반화한 학습용 비유이며, 청킹과 재부호화 근거를 연결해 “패턴이 나타나는 한 가지 모양”으로만 설명합니다.
- 사람의 이해와 머신러닝 모델을 동일시하지 않습니다. 사람의 판단은 언어, 목적, 기억, 사회적 맥락을 포함하고, 머신러닝 모델은 데이터에서 통계적 관계나 표현을 학습한다는 차이를 남겼습니다.
- 3.2의 결론은 지도학습 예시를 중심으로 정리합니다. `데이터 안의 구조`처럼 비지도학습까지 넓어질 수 있는 표현은 피하고, `입력과 출력의 관계`로 좁혀 설명합니다.

## 본문에 넣지 않은 내용

- 지도학습, 비지도학습, 강화학습의 상세 비교는 Chapter 8에서 다룹니다.
- 특징 공학(feature engineering)과 표현 학습(representation learning)의 깊은 비교는 3.3과 Part 4에서 다룹니다.
- 손실 함수, 최적화, 역전파는 Chapter 5와 Part 4에서 다룹니다.
- 데이터 분리, 검증, 평가 지표, 과적합 대응은 Part 3의 머신러닝 파트에서 다룹니다.
- 확률 출력의 해석, calibration, threshold 설정은 후속 머신러닝 평가 절에서 다룹니다.

## 검증 필요

- 데이터 품질과 일반화의 실무 예시는 공식 ML 교육 자료나 교과서 기반으로 추가 검토할 수 있습니다.
- 한국어 용어 `패턴`, `특징`, `라벨`, `추론`의 번역 일관성은 이후 용어표를 만들 때 다시 확인합니다.

## 출처

- Stanford Encyclopedia of Philosophy, Selmer Bringsjord and Naveen Sundar Govindarajulu, [Artificial Intelligence](https://plato.stanford.edu/entries/artificial-intelligence/), 2018-07-12, 확인 날짜: 2026-06-22.
- Tom Mitchell, [Machine Learning textbook](https://www.cs.cmu.edu/~tom/mlbook.html), Carnegie Mellon University, McGraw Hill, 1997, 확인 날짜: 2026-06-22.
- Google for Developers, [Supervised Learning](https://developers.google.com/machine-learning/intro-to-ml/supervised), 확인 날짜: 2026-06-22.
- scikit-learn, [Underfitting vs. Overfitting](https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html), 확인 날짜: 2026-06-22.
- Usama Fayyad, Gregory Piatetsky-Shapiro, Padhraic Smyth, [From Data Mining to Knowledge Discovery in Databases](https://www.kdnuggets.com/gpspubs/aimag-kdd-overview-1996-Fayyad.pdf), AI Magazine, 1996, 확인 날짜: 2026-06-22.
- George A. Miller, [The Magical Number Seven, Plus or Minus Two: Some Limits on our Capacity for Processing Information](http://psychclassics.yorku.ca/Miller/), Psychological Review, 1956, 확인 날짜: 2026-06-22.
