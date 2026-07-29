# P3-6.4 요약 표의 모든 열이 왜 특징은 아닌가

> Section ID: `P3-6.4`
> Version: `v2026.07.25`

[요약 표(summary table)](../../../reference/concept-glossary-parts/03-digeut.md#data-modeling)에 열이 들어 있다는 사실과 그것이 [특징(feature)](../../../reference/concept-glossary-parts/12-tieut.md#glossary-feature)이라는 판단은 같은 말이 아닙니다. 요약 표에는 샘플 구조를 설명하는 특징도 들어가지만, 비교를 위한 열, 결과 후보 열, 식별과 문맥을 위한 열도 함께 들어갈 수 있습니다. 그래서 이 절에서 먼저 붙잡아야 할 구분은 `요약 표의 열`과 `모델 입력으로 읽을 특징`이 자동으로 일치하지는 않는다는 점입니다.

## 왜 이 구분이 필요한가

동작 1회 요약 표를 만들면 아래처럼 여러 종류의 열이 한 표 안에 함께 있을 수 있습니다.

| 열 이름 예시 | 바로 feature인가 | 더 자연스러운 역할 |
| --- | --- | --- |
| `mid_flow_mean` | 보통 예 | 샘플 구조를 설명하는 특징 |
| `late_minus_early` | 보통 예 | 변화 구조를 보여 주는 특징 |
| `baseline_mid_flow_mean` | 경우에 따라 다름 | 비교 기준 열 |
| `review_needed` | 아니오 | 결과 또는 목표 라벨 후보 |
| `event_id` | 아니오 | 식별 열 |
| `captured_at` | 아니오 | 시간 문맥 열 |

이 표가 중요한 이유는, `숫자 열이면 다 feature`라고 읽는 습관을 늦추게 해 주기 때문입니다. 어떤 열은 샘플의 구조를 설명하지만, 어떤 열은 비교를 위해 붙였고, 어떤 열은 나중에 맞히고 싶은 결과를 적어 둔 것일 수 있습니다.

## 한 표 안에 왜 여러 역할이 섞이는가

요약 표는 `동작 1회 샘플을 읽기 좋은 한 행`으로 바꾼 표입니다. 그런데 사람이 표를 읽을 때 필요한 정보와, 모델 입력으로 바로 쓸 정보는 완전히 같지 않을 수 있습니다.

예를 들어 아래처럼 한 표를 생각해 볼 수 있습니다.

| event_id | mid_flow_mean | late_minus_early | baseline_mid_flow_mean | review_needed |
| --- | ---: | ---: | ---: | ---: |
| A | 2.40 | -0.80 | 3.05 | 1 |
| B | 2.55 | -0.10 | 2.60 | 0 |

이 표를 보면 모두 숫자처럼 보이지만 역할은 다릅니다.

- `mid_flow_mean`, `late_minus_early`는 샘플의 구조를 설명합니다.
- `baseline_mid_flow_mean`는 평소와 비교하기 위해 붙인 기준 열입니다.
- `review_needed`는 나중에 맞히고 싶은 결과 후보일 수 있습니다.
- `event_id`는 샘플을 가리키는 이름입니다.

즉 한 표는 `사람이 읽기 위한 비교`와 `뒤에서 학습으로 넘길 입력`과 `결과 후보`를 잠시 함께 담고 있을 수 있습니다.

## 네 종류로 먼저 나누면 덜 헷갈린다

처음 읽을 때는 복잡하게 생각하기보다 열을 네 종류로 먼저 나누면 좋습니다.

| 열 종류 | 먼저 묻는 질문 | 예시 |
| --- | --- | --- |
| 특징 열 | 이 값이 샘플 구조를 설명하는가 | 평균, 기울기, 변동성 |
| 비교 열 | 이 값이 평소/최근 차이를 읽게 하는가 | 기준선 평균, 차이값 |
| 결과 열 후보 | 이 값이 나중에 맞히고 싶은 결과인가 | `review_needed`, `final_status` |
| 식별·문맥 열 | 이 값은 샘플을 구분하거나 시점을 설명하는가 | `event_id`, `captured_at` |

이 네 칸으로 나누면 같은 작업 표 안에 함께 있는 열들도 왜 서로 다른 역할을 맡는지 더 분명해집니다. 비교 열은 평소와 최근의 차이를 읽게 하고, 결과 열 후보는 나중에 맞히고 싶은 값을 따로 세우게 하며, 식별·문맥 열은 그 판단이 어떤 샘플과 시점에서 나왔는지 잃지 않게 합니다. 즉 지금 이 구분은 단순 분류표가 아니라, 한 표 안의 열들이 왜 같은 방식으로 읽히면 안 되는지 정리하는 기준입니다.

## 같은 숫자 열도 항상 feature는 아니다

특히 헷갈리기 쉬운 것은 `baseline_mid_flow_mean`나 `delta_from_baseline` 같은 열입니다. 숫자이기 때문에 feature처럼 보이지만, 그 열이 붙은 이유를 먼저 봐야 합니다.

| 숫자 열 | 바로 떠오르는 오해 | 먼저 확인할 것 |
| --- | --- | --- |
| `baseline_mid_flow_mean` | 숫자니까 feature겠지 | 기준선 그 자체인지, 입력 특징으로 쓸 값인지 |
| `delta_from_baseline` | 차이값이니까 무조건 feature겠지 | 비교 구조를 설명하는 열인지, 실제 입력으로 넘길지 |
| `review_score` | 숫자니까 feature겠지 | 결과 점수인지, 입력 설명값인지 |

즉 `숫자 열`이라는 형식보다 `왜 이 열을 만들었는가`가 먼저입니다.

## 작은 점검 표

이 절의 예시는 계산 실험보다 열 역할 분리가 더 중요합니다. 아래처럼 작업 표에 들어간 열을 `값의 형식`이 아니라 `열을 만든 목적`으로 다시 읽으면 됩니다.

| 열 이름 | 예시 값 | 먼저 읽을 역할 | 바로 모델 입력으로 쓰는가 | 판단 이유 |
| --- | ---: | --- | --- | --- |
| `event_id` | A | 문맥(context) | 아니오 | 샘플을 구분하는 식별자 |
| `mid_flow_mean` | 2.40 | 특징(feature) | 예 | 샘플 자체의 중간 구간 평균을 설명 |
| `late_minus_early` | -0.80 | 특징(feature) | 예 | 샘플 내부의 전후반 변화 구조를 설명 |
| `baseline_mid_flow_mean` | 3.05 | 비교(comparison) | 경우에 따라 다름 | 기준선 자체를 담은 열 |
| `delta_from_baseline` | -0.65 | 비교(comparison) | 경우에 따라 다름 | 기준선 대비 차이를 표현한 열 |
| `review_score` | 87 | 결과 후보(target candidate) | 아니오 | 나중에 맞히고 싶은 결과 점수일 수 있음 |
| `review_needed` | 1 | 결과 후보(target candidate) | 아니오 | 검토 필요 여부라는 결과 후보 |
| `captured_at` | 2026-07-08 09:10 | 문맥(context) | 아니오 | 샘플이 기록된 시점 |

이 표가 보여 주는 것은 대단한 분류 규칙이 아닙니다. 하나의 작업 표 안에 여러 종류의 열이 잠시 함께 있을 수 있고, 그 열을 역할별 근거와 함께 다시 읽어야 한다는 점이 핵심입니다. 특히 `baseline_mid_flow_mean`와 `delta_from_baseline`는 숫자 열이지만 먼저는 비교 열로 읽히고, `review_score`, `review_needed`는 숫자 열이지만 먼저는 결과 후보로 읽힙니다.

`경우에 따라 다름`이 붙은 이유도 여기서 드러납니다. 기준선 자체나 기준선 차이값은 비교 설명을 위해 만든 열이므로, 바로 입력 특징으로 넘길지 여부는 뒤에서 어떤 예측 문제를 만들지에 따라 다시 판단해야 하기 때문입니다.

이 구분을 특징 설계 바로 뒤에서 한 번 짚어 두어야 `어차피 다 feature 아닌가`라는 착각이 줄어듭니다. 요약 표는 feature만 모아 둔 표가 아니라, feature 후보, 비교 열, 결과 후보, 식별·문맥 열이 함께 잠시 놓일 수 있는 작업 표입니다. 이렇게 읽어 두면 뒤에서 기준선 비교 열과 target 후보 열을 다시 만날 때도 각 열의 역할이 덜 갑자기 바뀌어 보입니다.

이 절은 `어떤 숫자 열이 feature인가`만 따지는 문제가 아니라, [작업 표 안의 열 역할 분리(column-role separation in a working table)](../../../reference/concept-glossary-parts/03-digeut.md#data-modeling)의 문제로 다시 볼 수 있습니다.


따라서 `숫자 열이면 다 feature`라는 오해 대신, 각 열이 샘플을 설명하는지, 비교 기준을 담는지, 결과를 적어 둔 것인지, 맥락만 남기는지부터 따져야 합니다.

## 작은 도식으로 보기

이 절의 핵심은 작업 표의 모든 열을 한 종류로 읽지 않는 데 있습니다. 같은 표 안의 열도 특징 열, 비교 열, 결과 후보 열, 문맥 열로 나뉘며, 이 역할 구분이 먼저 있어야 합니다.

--8<-- "assets/part-03/chapter-06/p3-6-4-mermaid-01-ko.mmd"

## 출처와 참고 자료

- Google for Developers, `Machine Learning Glossary`의 `labeled example`. labeled example을 features와 label의 결합으로 설명하므로, 입력 설명 열과 결과 열 후보를 구분해야 한다는 기본 틀을 제공합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Google for Developers, `Machine Learning Glossary`의 `label leakage`. feature가 label의 proxy가 되는 설계 결함을 설명하므로, `review_needed`나 `review_score` 같은 결과 후보 열을 무심코 feature로 섞지 말아야 한다는 근거가 됩니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- W3C, `PROV-Overview`. provenance information을 별도로 기록하고 추적하는 표준 문맥을 제공하므로, `event_id`, `captured_at` 같은 식별·문맥 열은 샘플을 설명하는 feature와 다른 역할의 정보로 남길 수 있다는 일반 근거로 참고할 수 있습니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
