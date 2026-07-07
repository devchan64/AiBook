# P3-6.4 요약 표의 모든 열이 왜 특징은 아닌가

> Section ID: `P3-6.4`
> Version: `v2026.07.07`

Chapter 5에서 원시 로그를 요약 표로 바꾸고, Chapter 6 앞 절에서 어떤 구조를 특징(feature)으로 남길지 보았습니다. 그런데 여기서 자주 다시 멈춥니다. `요약 표를 만들었으면, 그 안에 있는 열은 전부 feature 아닌가?` Part 3이 어렵게 느껴지는 이유 중 하나가 바로 이 지점입니다. 요약 표에는 특징도 들어가지만, 비교를 위한 열, 결과 후보 열, 식별과 문맥을 위한 열도 함께 들어갈 수 있기 때문입니다.

`요약 표에 있다`와 `특징이다`는 같은 말이 아닙니다.

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

이 네 칸으로 나누면 뒤의 Chapter가 왜 갈라지는지도 더 분명해집니다.

- Chapter 7은 비교 열을 더 본격적으로 읽습니다.
- Chapter 9는 결과 열 후보를 어디까지 예측 문제로 올리고, 뒤 Part로 무엇을 넘길지 함께 다룹니다.
- Part 4로 넘어갈 때는 특징 열과 결과 열 후보를 다시 가릅니다.

즉 지금 이 구분은 단순 분류표가 아니라, Part 3 전체 구조를 다시 정렬하는 기준입니다.

## 같은 숫자 열도 항상 feature는 아니다

특히 헷갈리기 쉬운 것은 `baseline_mid_flow_mean`나 `delta_from_baseline` 같은 열입니다. 숫자이기 때문에 feature처럼 보이지만, 그 열이 붙은 이유를 먼저 봐야 합니다.

| 숫자 열 | 바로 떠오르는 오해 | 먼저 확인할 것 |
| --- | --- | --- |
| `baseline_mid_flow_mean` | 숫자니까 feature겠지 | 기준선 그 자체인지, 입력 특징으로 쓸 값인지 |
| `delta_from_baseline` | 차이값이니까 무조건 feature겠지 | 비교 구조를 설명하는 열인지, 실제 입력으로 넘길지 |
| `review_score` | 숫자니까 feature겠지 | 결과 점수인지, 입력 설명값인지 |

즉 `숫자 열`이라는 형식보다 `왜 이 열을 만들었는가`가 먼저입니다.

## 작은 코드 예시

```python
import pandas as pd

summary = pd.DataFrame(
    [
        {
            "event_id": "A",
            "mid_flow_mean": 2.40,
            "late_minus_early": -0.80,
            "baseline_mid_flow_mean": 3.05,
            "review_needed": 1,
        }
    ]
)

feature_cols = ["mid_flow_mean", "late_minus_early"]
comparison_cols = ["baseline_mid_flow_mean"]
target_candidate_cols = ["review_needed"]
context_cols = ["event_id"]

print("feature cols:", feature_cols)
print("comparison cols:", comparison_cols)
print("target candidate cols:", target_candidate_cols)
print("context cols:", context_cols)
```

예상 출력:

```text
feature cols: ['mid_flow_mean', 'late_minus_early']
comparison cols: ['baseline_mid_flow_mean']
target candidate cols: ['review_needed']
context cols: ['event_id']
```

이 예시가 보여 주는 것은 대단한 분류 규칙이 아닙니다. 같은 요약 표 안의 열도 역할을 먼저 나누어 읽어야 한다는 점입니다.

## 왜 Chapter 6에 이 절이 필요한가

이 절이 뒤 Part 연결 직전에만 나오면, Chapter 6과 Chapter 7을 읽는 동안 계속 `어차피 다 feature 아닌가`라는 착각을 안고 가게 됩니다. 하지만 실제로는 특징 설계 바로 뒤에서 이 구분을 한 번 짚어 두어야, 다음 장의 기준선 비교와 뒤 장의 target 후보 구분이 덜 갑자기 이어집니다.

즉 Chapter 6의 끝에서는 다음 문장이 서 있어야 합니다.

`요약 표는 feature만 모아 둔 표가 아니라, feature 후보, 비교 열, 결과 후보, 식별·문맥 열이 함께 잠시 놓일 수 있는 작업 표다.`

이 문장이 서면 Part 3의 중반부터 후반까지의 연결이 더 부드러워집니다.

## 짧은 점검

- 왜 `요약 표에 있다`와 `바로 feature다`가 같은 뜻이 아닌지 설명할 수 있는가
- `baseline_mid_flow_mean` 같은 열이 왜 비교 열로 먼저 읽힐 수 있는지 말할 수 있는가
- `review_needed`가 왜 결과 열 후보이지 입력 특징이 아닐 수 있는지 설명할 수 있는가
- 현재 보고 있는 요약 표의 열을 `특징`, `비교`, `결과 후보`, `식별·문맥`으로 나눌 수 있는가

## 언제 이 관점을 먼저 떠올려야 하는가

- 요약 표를 만들고 나서 모든 숫자 열을 한꺼번에 feature처럼 읽기 시작할 때 이 절을 먼저 떠올립니다.
- 기준선 비교 열과 결과 후보 열이 특징 열과 섞여 보일 때 이 절로 돌아옵니다.
- Chapter 7의 비교 구조와 Chapter 9의 뒤 Part 연결 구간이 왜 같은 요약 표에서 다른 방향으로 갈라지는지 다시 설명해야 할 때 이 절이 기준이 됩니다.
