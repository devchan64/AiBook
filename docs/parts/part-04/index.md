# Part 4. 머신러닝

> Section ID: `P4-index`
> Version: `v2026.07.26`

Part 2에서는 수식, Python, 배열, 표, 그래프, 실행 환경을 다시 읽는 기초를 복구했습니다. 이제 Part 4에서는 그 도구들이 실제로 무엇을 위해 쓰이는지, 즉 `데이터로부터 규칙을 학습한다`는 말이 무엇인지 정리합니다.

이미 AI 서비스를 써 본 독자도 많겠지만, 여기서는 경험을 표준 개념으로 다시 묶는 일이 더 중요합니다. 모델 이름을 외우기보다 어떤 문제가 머신러닝 문제인지, 어떤 데이터를 모아야 하는지, 모델은 무엇을 배우는지, 학습이 잘되었다는 것은 무엇을 뜻하는지, 왜 어떤 모델은 잘 맞는 것처럼 보여도 실제로는 위험할 수 있는지부터 분명히 잡습니다.

Part 4의 핵심 목적은 “[머신러닝](../../reference/concept-glossary-parts/05-mieum.md#machine-learning)을 모델 목록이 아니라 문제-데이터-학습-평가-적용의 흐름으로 읽게 되는 것”입니다. [선형회귀](../../reference/concept-glossary-parts/07-siot.md#linear-regression), [로지스틱 회귀](../../reference/concept-glossary-parts/04-rieul.md#logistic-regression), [결정트리](../../reference/concept-glossary-parts/01-giyeok.md#decision-tree), [랜덤포레스트](../../reference/concept-glossary-parts/04-rieul.md#random-forest), 부스팅, [클러스터링](../../reference/concept-glossary-parts/01-giyeok.md#clustering), [차원 축소](../../reference/concept-glossary-parts/11-chieut.md#dimensionality-reduction), [강화학습](../../reference/concept-glossary-parts/01-giyeok.md#reinforcement-learning)은 각각 따로 외우는 항목이 아닙니다. 어떤 문제를 풀고 있는지, [모델 입력](../../reference/concept-glossary-parts/05-mieum.md#model-input)과 [모델 출력](../../reference/concept-glossary-parts/05-mieum.md#model-output)이 무엇인지, 어떤 기준으로 좋고 나쁨을 판단하는지에 따라 등장하는 선택지들입니다.

Part 4도 같은 Part 안에서는 주요 개념의 상세 설명을 가능한 한 한 Section에 먼저 둡니다. 이후 절에서는 현재 맥락에 필요한 최소 설명만 남깁니다. 그래서 `지도학습(supervised learning)`은 `P4-2.1`, `비지도학습(unsupervised learning)`은 `P4-2.2`, `강화학습(reinforcement learning)`은 `P4-2.3`, `검증(validation)`과 `테스트(test)`의 역할 구분은 `P4-4.2`, `과적합(overfitting)`과 `과소적합(underfitting)`은 `P4-5.1`, `평가 지표(metric)`는 `P4-6.1`, `특징 선택(feature selection)`은 `P4-7.1`, `전처리(preprocessing)`는 `P4-7.2`, `기준 모델(baseline)`은 `P4-8.2`, `선형회귀(linear regression)`는 `P4-10.1`, `로지스틱 회귀(logistic regression)`는 `P4-11.1`, `k-NN`은 `P4-12.1`, `SVM`은 `P4-13.1`, `결정트리(decision tree)`는 `P4-14.1`, `랜덤포레스트(random forest)`는 `P4-15.1`, `그래디언트 부스팅(gradient boosting)`은 `P4-16.1`, `클러스터링(clustering)`은 `P4-17.1`, `차원 축소(dimensionality reduction)`는 `P4-18.1`을 대표 설명 위치로 먼저 붙잡고, 다시 등장할 때는 [머신러닝](../../reference/concept-glossary-parts/05-mieum.md#machine-learning), [차원 축소](../../reference/concept-glossary-parts/11-chieut.md#dimensionality-reduction) 같은 관련 개념사전 항목과 현재 맥락을 함께 확인합니다.

그래서 Part 4는 머신러닝의 지형도를 다음 순서로 다시 연결합니다.

1. AI, 머신러닝, 딥러닝의 구분
2. 지도학습, 비지도학습, 강화학습의 차이
3. 데이터 분리, 검증, 과적합, 일반화, 평가 지표
4. 특징 선택, 전처리, 모델 선택, 기준 모델, 튜닝
5. 대표 전통 모델의 직관
6. 군집화, 차원 축소, 강화학습까지의 확장
7. Part 5 딥러닝으로 넘어가기 위한 공통 관점 정리

## 이 파트에서 다루는 주요 질문

Part 4는 알고리즘 이름을 늘어놓기보다, 머신러닝 설명을 읽을 때 반복해서 붙잡아야 할 질문을 먼저 세웁니다.

- 어떤 문제가 [지도학습(supervised learning)](../../reference/concept-glossary-parts/09-jieut.md#supervised-learning), [비지도학습(unsupervised learning)](../../reference/concept-glossary-parts/06-bieup.md#unsupervised-learning), [강화학습(reinforcement learning)](../../reference/concept-glossary-parts/01-giyeok.md#reinforcement-learning)으로 나뉘는가?
- [모델 입력 정의(model input)](../../reference/concept-glossary-parts/05-mieum.md#model-input), [모델 출력 정의(model output)](../../reference/concept-glossary-parts/05-mieum.md#model-output), [지도학습 라벨(supervised learning label)](../../reference/concept-glossary-parts/09-jieut.md#supervised-learning-label), [보상(reward)](../../reference/concept-glossary-parts/06-bieup.md#reward)은 각각 무엇을 뜻하며 어디서 구분되는가?
- [학습(training)](../../reference/concept-glossary-parts/05-mieum.md#model-training), [검증(validation)](../../reference/concept-glossary-parts/01-giyeok.md#validation-data), [테스트(test)](../../reference/concept-glossary-parts/12-tieut.md#test-data)는 왜 나뉘고, [일반화(generalization)](../../reference/concept-glossary-parts/08-ieung.md#generalization)는 무엇으로 확인하는가?
- [평가 지표(metric)](../../reference/concept-glossary-parts/13-pieup.md#metric)는 어떤 오류를 보여 주고, 어떤 오류를 가릴 수 있는가?
- [특징 선택(feature selection)](../../reference/concept-glossary-parts/12-tieut.md#feature-selection), [전처리(preprocessing)](../../reference/concept-glossary-parts/09-jieut.md#preprocessing), [기준 모델(baseline)](../../reference/concept-glossary-parts/01-giyeok.md#baseline-model), 튜닝(tuning)은 왜 모델 이름보다 먼저 점검해야 하는가?
- 대표 전통 모델은 어떤 문제 감각을 주고, 어디까지를 강점으로 보고 어디서부터 한계를 의심해야 하는가?

## 머신러닝을 문제와 평가의 흐름으로 읽기

이 Part는 머신러닝의 큰 구조를 잡고, 오래전에 배운 개론 지식을 다시 표준 흐름으로 묶어 주는 구간입니다.

머신러닝을 어렵게 만드는 이유는 알고리즘 수가 많아서만이 아닙니다. 같은 데이터라도 문제를 어떻게 정의하느냐에 따라 분류(classification), 회귀(regression), 군집화(clustering), 차원 축소(dimensionality reduction), 강화학습(reinforcement learning)으로 읽는 방식이 달라집니다. 또한 모델을 선택하는 일보다 먼저, 학습 데이터(training data), 검증 데이터(validation data), 테스트 데이터(test data)를 왜 나누는지, 과적합(overfitting)과 일반화(generalization)를 왜 구분해야 하는지, 평가 지표(metric)를 어떻게 읽는지가 중요합니다.

Part 4는 이 기반을 잡습니다. 목적은 모든 알고리즘의 수학을 깊게 파는 것이 아니라, 머신러닝 설명을 읽을 때 문제를 정의하고, 데이터를 보고, 입력(input)과 출력(output)을 정하고, 모델이 무엇을 배울지 정하고, 학습과 평가를 분리하고, 지표를 읽고, 모델의 한계와 적용 조건을 점검하는 흐름을 스스로 복원할 수 있게 되는 것입니다.

이때 P1-8에서 잡은 세 구분을 그대로 가져와야 합니다. 지도학습은 `입력과 라벨`이 함께 있는 예시에서 목표 출력을 맞추는 문제이고, 비지도학습은 `사람이 붙인 라벨 없이` 구조와 표현을 찾는 문제이며, 강화학습은 `라벨 대신 행동 뒤의 보상`으로 정책을 조정하는 문제입니다. 특히 강화학습의 보상은 지도학습의 라벨과 같은 신호가 아니라는 점을 Part 4 전체에서도 계속 유지합니다.

## 머신러닝에서 닫을 핵심 질문

Part 4를 읽고 나면 다음 정도의 이해를 갖는 것이 목표입니다.

- AI, 머신러닝(machine learning), 딥러닝(deep learning)의 관계를 큰 흐름에서 설명할 수 있습니다.
- 지도학습, 비지도학습, 강화학습의 차이를 데이터와 문제 정의 관점에서 구분할 수 있습니다.
- 학습 데이터, 검증 데이터, 테스트 데이터가 왜 분리되는지 말할 수 있습니다.
- 과적합(overfitting), 과소적합(underfitting), 일반화(generalization)의 차이를 설명할 수 있습니다.
- 평가 지표(metric)가 모델 자체의 숫자이면서 동시에 업무 판단 기준과 연결된다는 점을 이해할 수 있습니다.
- 특징 선택(feature selection), 전처리(preprocessing), 모델 선택(model selection), 기준 모델(baseline), 튜닝(tuning)의 역할을 설명할 수 있습니다.
- 선형회귀(linear regression), 로지스틱 회귀(logistic regression), 결정트리(decision tree), 랜덤포레스트(random forest), 그래디언트 부스팅(gradient boosting)의 직관과 쓰임새를 구분할 수 있습니다.
- 클러스터링(clustering)과 차원 축소(dimensionality reduction)를 `정답 라벨 없이 구조를 읽는 방법`으로 설명할 수 있습니다.
- 강화학습을 행동과 보상으로 정책을 조정하는 학습으로 이해하고, 가치 기반과 정책 기반의 차이까지 입문 수준에서 구분할 수 있습니다.

## 머신러닝이 설명할 경계와 남겨 둘 질문

Part 4는 머신러닝의 공통 구조를 설명하는 파트입니다. 여기서는 다음 흐름을 본편의 중심 질문으로 붙잡습니다.

- 지도학습, 비지도학습, 강화학습의 큰 구분
- 데이터 분리, 검증, 과적합, 일반화, 평가 지표
- 특징 선택, 전처리, 기준 모델(baseline), 모델 선택, 튜닝
- 대표 전통 모델, 군집화, 차원 축소, 강화학습의 직관

Part 4는 먼저 `머신러닝을 어떤 공통 질문으로 읽을 것인가`를 닫는 역할을 맡습니다. 딥러닝과 대규모 생성 모델의 본격 구조는 뒤 Part에서 이어집니다.

## 무엇을 설명하는가

Part 4는 크게 네 흐름으로 구성됩니다.

먼저 머신러닝의 큰 구분을 다시 잡습니다. AI, 머신러닝, 딥러닝의 관계를 보고, 지도학습, 비지도학습, 강화학습의 차이를 정리합니다. 이 구간의 목적은 알고리즘 이름보다 `문제의 종류가 어떻게 다른가`를 이해하는 것입니다.

여기서 독자가 가장 먼저 붙잡아야 할 비교축은 학습 신호입니다. 지도학습은 사람이 붙인 라벨을, 비지도학습은 라벨 없는 구조를, 강화학습은 행동 뒤에 돌아오는 보상을 중심 신호로 읽습니다. 이 구분이 흔들리면 뒤의 분류, 군집화, 가치 기반 강화학습 설명도 서로 다른 문제 설정으로 읽히지 않게 됩니다.

그다음 학습을 읽는 공통 기반을 다룹니다. 데이터 분리, 검증, 과적합, 일반화, 평가 지표, 특징 선택, 전처리, 모델 선택, 기준 모델, 튜닝을 다룹니다. 이 구간은 Part 4의 중심부입니다. 왜냐하면 이후 어떤 알고리즘을 만나더라도, 결국 독자는 데이터는 어떻게 나뉘었는지, 모델은 무엇을 학습했는지, 점수는 어떻게 읽어야 하는지, 지금 좋아 보이는 결과가 실제로도 믿을 만한지를 다시 묻게 되기 때문입니다.

평가 지표 범위도 이 흐름 안에서 분명히 둡니다. Part 4 본편에서는 정확도(accuracy), 정밀도(precision), 재현율(recall), F1, MAE, RMSE, R²처럼 `문제 유형에 따라 먼저 어떤 질문을 던져야 하는가`를 붙잡는 지표를 우선 다룹니다. ROC, PR, log loss, calibration, reliability, silhouette처럼 점수 해석을 더 섬세하게 만드는 항목은 P4-6.4 보충학습에서 입문 해설로 모으고, threshold와 calibration의 재등장은 P4-15.3에서 다시 회수합니다.

이때 독자가 같이 붙잡아야 할 비교 장치는 두 가지입니다. [혼동 행렬(confusion matrix)](../../reference/concept-glossary-parts/14-hieut.md#confusion-matrix)과 [오류 사례(error case)](../../reference/concept-glossary-parts/05-mieum.md#model-validation)는 `어디서 어떻게 틀렸는가`를 읽게 하고, [기준선(baseline)](../../reference/concept-glossary-parts/01-giyeok.md#baseline)은 `그 점수가 정말 의미 있는 개선인가`를 묻게 합니다. Part 4는 점수를 단독 숫자로 외우게 하기보다, 오류 구조와 기준선을 함께 읽는 습관을 만드는 데 더 큰 비중을 둡니다.

이 흐름은 다음 순서로 읽습니다.

| 평가 읽기 순서 | 먼저 확인할 질문 | 왜 필요한가 |
| --- | --- | --- |
| 혼동 행렬(confusion matrix) | 어느 칸에서 가장 많이 틀렸는가? | 정확도 하나로 가려지는 오류 방향을 먼저 드러냅니다. |
| 대표 오류 사례(error case) | 실제로 어떤 입력에서 왜 틀렸는가? | 숫자만으로는 보이지 않는 데이터 문제와 경계 사례를 확인합니다. |
| 기준 모델(baseline) 비교 | 이 개선이 정말 의미 있는가? | 높아 보이는 점수가 쉬운 문제 덕분인지 실제 개선인지 구분합니다. |

Part 4 초반에서 특히 붙잡아야 할 평가는 아래 세 단계입니다.

| 먼저 보는 것 | 바로 다음에 붙는 질문 | 그다음 절에서 이어질 곳 |
| --- | --- | --- |
| 혼동 행렬과 오류 사례 | 어디서 틀렸고 어떤 입력을 놓쳤는가 | P4-6 평가 지표 |
| 기준선(baseline) 비교 | 이 점수가 쉬운 기준보다 정말 나은가 | P4-8 기준 모델 |
| 튜닝(tuning) 결과 | 작은 점수 상승이 비용과 복잡도를 정당화하는가 | P4-9 하이퍼파라미터 |

이 순서는 아래 세 줄로 다시 압축해 둘 수 있습니다.

| 평가를 읽는 최소 순서 | 왜 이 순서가 먼저인가 |
| --- | --- |
| 혼동 행렬(confusion matrix) | 어디서 틀렸는지 먼저 봐야 점수의 방향을 읽을 수 있기 때문입니다. |
| 대표 오류 사례(error case) | 실제 입력을 봐야 데이터 문제와 경계 사례를 확인할 수 있기 때문입니다. |
| 기준선(baseline) 비교 | 마지막에야 그 차이가 정말 의미 있는 개선인지 판단할 수 있기 때문입니다. |

Part 4 전체를 관통하는 기록 언어도 이 흐름 안에서 함께 고정합니다. 같은 점수나 구조가 그럴듯해 보여도, 먼저 사실로 남길 것과 검토가 더 필요한 해석을 분리해 적어야 합니다.

| 이 Part에서 반복해 남길 것 | 가장 짧은 기록 언어 |
| --- | --- |
| 보인 점수, 구조, 비교 결과 | 사실(fact) |
| 그 결과를 어디까지 믿고 어디서 멈출지 | 해석(interpretation) |
| 다음 실험이나 다음 확인 항목 | 다음 질문(next question) |

그다음 전통적인 대표 모델들을 봅니다. 선형회귀, 로지스틱 회귀, k-NN, SVM, 결정트리, 랜덤포레스트, 그래디언트 부스팅을 다루며, 각각이 무엇을 잘하고 어디서 조심해야 하는지 봅니다. 이때 목표는 공식 유도보다 문제 감각을 잡는 것입니다.

여기서는 모델 이름을 외우기보다, 아래처럼 `작은 데이터 장면에서 무엇을 먼저 떠올릴 것인가`를 확인합니다.

| 작은 데이터 장면 | 먼저 떠올릴 모델 계열 | 왜 그 계열이 출발점이 되는가 |
| --- | --- | --- |
| 숫자 입력으로 연속값을 예측해야 함 | 선형회귀(linear regression) | 가장 단순한 관계와 기준선(baseline)을 빠르게 확인하기 좋기 때문입니다. |
| 예/아니오나 범주를 나눠야 함 | 로지스틱 회귀(logistic regression), 결정트리(decision tree) | 분류 문제의 기본 기준선과 규칙 감각을 비교하기 좋기 때문입니다. |
| 표 형식(tabular) 데이터에서 강한 성능 후보가 필요함 | 랜덤포레스트(random forest), 그래디언트 부스팅(gradient boosting) | 비선형 관계와 특징 상호작용을 잘 다루는 대표 후보이기 때문입니다. |
| 라벨 없이 비슷한 묶음을 보고 싶음 | 클러스터링(clustering) | 정답 없이 구조를 읽는 가장 직접적인 출발점이기 때문입니다. |
| 변수가 너무 많아 먼저 축을 줄이고 싶음 | 차원 축소(dimensionality reduction) | 예측보다 표현 요약과 시각화가 먼저 필요하기 때문입니다. |
| 행동 결과가 나중에 돌아오는 문제를 다룸 | 강화학습(reinforcement learning) | 입력-정답 쌍보다 상태, 행동, 보상 구조가 핵심이기 때문입니다. |

마지막으로 비지도학습과 강화학습 쪽으로 확장합니다. 클러스터링, 차원 축소, 강화학습 알고리즘을 통해 `정답을 맞히는 학습` 밖의 영역도 머신러닝에 포함된다는 점을 정리합니다.

## 왜 필요한가

AI 서비스를 써 본 경험만으로는 머신러닝 전체를 이해했다고 보기 어렵습니다. 예를 들어 모델을 학습용 데이터로 `fit`했다는 말, 검증 점수는 올랐지만 테스트 점수는 떨어졌다는 말, 특징 전처리를 바꿨더니 과적합이 줄었다는 말, 기준선(baseline)보다 1% 좋아졌지만 운영상 의미는 불분명하다는 말은 자주 등장합니다.

이 문장들을 읽으려면 알고리즘 이름보다 먼저 구조를 알아야 합니다. `fit`이 무엇을 의미하는지, 왜 검증과 테스트를 나누는지, 성능 향상이 왜 곧바로 배포 의미로 이어지지 않는지 알아야 합니다.

또 다음과 같은 오해가 자주 나타납니다.

- 모델만 바꾸면 성능이 해결될 것이다.
- 점수 하나만 높으면 좋은 시스템이다.
- 데이터가 많으면 자동으로 일반화가 잘된다.
- 강화학습은 스스로 배우니 현실에서도 많이 시도하면 된다.

Part 4는 이런 오해를 줄이는 구간입니다. 이 Part는 모델 카탈로그를 제공하는 것이 아니라, 머신러닝을 읽고 비교하고 의심할 수 있는 기본 문해력을 만드는 구간입니다.

## 이 파트에서 끝내지 않는 질문

Part 4는 머신러닝의 공통 구조를 설명하므로 다음 질문은 의도적으로 Part 5와 Part 6으로 넘깁니다.

- 표현 학습(representation learning)은 왜 전통 모델보다 더 큰 전환점이 되었는가?
- gradient, loss, optimizer는 신경망에서 어떻게 더 큰 계산 구조로 이어지는가?
- 생성 모델과 대규모 언어 모델은 이 공통 구조를 어떻게 확장하는가?

이 질문들은 표현 학습과 신경망 계산 구조는 Part 5에서, 생성 모델과 LLM 확장은 Part 6에서 본문 설명으로 회수합니다.

## 이 파트를 마치면 생기는 이해

이 Part를 마치면 머신러닝을 단순한 모델 목록이 아니라 하나의 작업 흐름으로 볼 수 있습니다. 문제를 정하고, 데이터를 고르고, 입력과 출력을 정하고, 모델을 학습시키고, 일반화 여부를 확인하고, 지표를 읽고, 적용 조건과 한계를 검토하는 순서가 한 묶음으로 보이게 됩니다.

이 이해가 생기면 선형회귀, 로지스틱 회귀, 랜덤포레스트, 클러스터링, 강화학습이 서로 무관한 이름처럼 보이지 않게 됩니다. 각각은 다른 문제를 다루기 위한 선택지이며, 그 앞에는 항상 데이터 정의와 평가 기준이 있고, 그 뒤에는 항상 적용 한계와 운영 판단이 따라온다는 점이 드러납니다.

즉, Part 4는 모델 이름 모음보다 `문제 구조 -> 점검 기준 -> 다음 질문`을 반복해서 남기는 파트입니다. 여기서 점검 기준은 곧바로 원인 확정이나 정책 결론으로 넘어가기보다, 먼저 검토 필요 신호와 다음 확인 순서를 남기는 기준이어야 합니다.

## 완료 기준

- 머신러닝 문제를 지도학습, 비지도학습, 강화학습 관점에서 구분할 수 있다.
- 학습용, 검증용, 테스트용 데이터 분리의 이유를 설명할 수 있다.
- 과적합, 과소적합, 일반화의 차이를 예시와 함께 말할 수 있다.
- 평가 지표가 문제 유형과 업무 목표에 따라 달라진다는 점을 설명할 수 있다.
- 특징 선택, 전처리, 기준 모델, 튜닝의 역할을 구분할 수 있다.
- 선형회귀, 로지스틱 회귀, 결정트리, 랜덤포레스트, 그래디언트 부스팅의 직관과 차이를 입문 수준으로 설명할 수 있다.
- 클러스터링과 차원 축소가 라벨 없는 데이터 구조를 읽는 방법임을 설명할 수 있다.
- 강화학습을 행동과 보상 중심의 학습으로 이해하고, 적용 시 주의점까지 말할 수 있다.
- Part 4에서 왜 딥러닝을 따로 다루는지 연결해서 설명할 수 있다.

## 출처와 참고 자료

이 개요 페이지는 Part 4의 목적과 학습 경로를 정리한 자체 개요입니다. 외부 자료를 직접 인용하지 않았습니다.
