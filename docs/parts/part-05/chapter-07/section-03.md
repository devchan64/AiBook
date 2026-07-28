# P5-7.3 적응형 업데이트의 직관: Adam을 예로

> Section ID: `P5-7.3`
> Version: `v2026.07.26`

P5-7.2에서는 같은 gradient라도 learning rate에 따라 실제 update 보폭이 어떻게 달라지는지 보았습니다. 여기서 바로 다음 질문이 생깁니다. 그 보폭을 모든 파라미터에 언제나 같은 방식으로 적용해도 충분한가?

적응형 업데이트(adaptive update)는 바로 이 지점에서 나옵니다. 기본 직접 update가 `현재 gradient와 learning rate를 바탕으로 한 번 움직이는 방식`이라면, 적응형 업데이트는 여기에 최근 gradient 흐름과 파라미터 좌표별 차이까지 함께 보며 실제 이동량을 조절하려고 합니다.

이 절에서는 Adam(Adaptive Moment Estimation)을 대표 예로 삼아 그 직관을 읽습니다. 중심은 Adam이라는 이름 자체보다, `왜 update 규칙에 최근 흐름과 좌표별 조절이 들어가는가`입니다.

기본 업데이트와 적응형 업데이트의 차이가 다시 섞이면 개념사전의 [경사하강법(gradient descent)](../../../reference/concept-glossary-parts/01-giyeok.md#gradient-descent)과 [옵티마이저(optimizer)](../../../reference/concept-glossary-parts/08-ieung.md#optimizer) 항목을 함께 다시 봅니다.

## Adam이 적응형으로 보정하는 질문

- 적응형 업데이트는 기본적인 gradient update에 무엇을 더 보완하려는가?
- 최근 gradient 흐름과 좌표별 조절이라는 적응형 update의 핵심 직관은 무엇인가?
- Adam은 그 적응형 update 감각을 설명할 때 어떤 대표 예가 되는가?
- Adam이 실무에서 많이 언급되지만 왜 절대 우열로 외우면 안 되는가?

이 절에서는 optimizer 이름을 더 많이 늘어놓기보다, 적응형 update가 어떤 문제의식에서 나오는지 설명합니다. 여기서 읽어야 할 것은 `이미 계산된 gradient를 어떤 규칙으로 실제 update로 바꾸는가`, 그리고 왜 그 규칙에 최근 흐름과 좌표별 차이가 들어가는가입니다. Adam은 이 직관을 붙잡는 대표 예로 사용합니다. optimizer 계열 이름을 처음 구분하는 비교는 P5-7.5 보충학습에서, optimizer state와 parameter-wise update는 P5-7.7 보충학습에서 다시 이어집니다. regularization과 일반화의 관점은 P5-8.1, P5-8.2에서 다시 연결하고, adaptive optimization의 수렴 분석은 P5-7.4 보충학습으로 이어집니다.

| 지금 절에서 구분할 것 | 왜 중요한가 |
| --- | --- |
| 모델 구조 | CNN, RNN, Transformer처럼 입력 구조를 어떻게 표현할지 정하는 문제이기 때문입니다. |
| optimizer 절차 | 같은 구조라도 파라미터를 어떤 보폭과 어떤 누적 규칙으로 움직일지 정하는 문제이기 때문입니다. |
| regularization과의 차이 | optimizer는 `어떻게 움직일까`, regularization은 `어떤 해를 덜 선호할까`를 다루기 때문입니다. |

## gradient 이력과 보폭 조절의 판단 기준

- 적응형 업데이트를 `최근 gradient 흐름과 좌표별 조절을 반영하는 update 방식`으로 설명할 수 있습니다.
- 기본 직접 업데이트와 적응형 업데이트의 차이를 이해할 수 있습니다.
- Adam이 왜 적응형 update의 대표 예로 자주 언급되는지 말할 수 있습니다.
- 실행 가능한 Python 예제로 업데이트 감각 차이를 확인할 수 있습니다.

## 적응형 업데이트를 이해할 때 먼저 필요한 기준선

적응형 업데이트를 바로 공식으로 시작하면 초심자는 `무엇이 추가된 것인지`를 놓치기 쉽습니다. 그래서 먼저 가장 단순한 기준선부터 둡니다. 여기서 먼저 붙잡아야 할 것은 특정 optimizer 이름보다, `현재 gradient와 learning rate를 바탕으로 바로 한 번 움직인다`는 기본 감각입니다.

다음처럼 이해하면 충분합니다.

`현재 gradient가 가리키는 방향으로, 정해 둔 learning rate만큼 한 걸음 움직이는 방식이다.`

이 감각은 P5-7.2에서 본 `learning rate가 update 보폭을 정한다`는 설명을 그대로 이어받습니다. P5-7.2가 보폭 자체를 설명했다면, 여기서는 그 보폭을 `모든 파라미터에 같은 식으로 바로 적용하는 기본 update`를 기준선으로 삼습니다.

여기서 특정 optimizer 이름을 앞세우지 않는 이유도 분명합니다. 지금 필요한 것은 이름 구분이 아니라, 적응형 update가 무엇을 더 보완하는지 읽기 위한 가장 얇은 기준선이기 때문입니다.

- 직관이 분명합니다
- gradient descent의 핵심 아이디어가 드러납니다
- 업데이트 규칙을 가장 직접적으로 볼 수 있습니다

즉, 이 절의 기준선은 특정 optimizer 소개가 아니라, 적응형 업데이트를 설명하기 위한 `가장 단순한 직접 update 감각`입니다.

## 적응형 업데이트는 무엇을 더 보완하려 하는가

적응형 업데이트는 단순한 현재 gradient 기준 update보다 더 많은 정보를 사용합니다. Adam을 대표 예로 두고 보면 다음 정도로 이해하면 충분합니다.

- 최근 gradient의 방향을 누적해서 보고
- 좌표마다 변화 크기를 다르게 조절하려고 하며
- 초기 학습을 더 빠르고 안정적으로 만들려는 실용적 목적이 있습니다

즉, 적응형 업데이트는 `모든 파라미터를 같은 기준 보폭으로 움직이는 것`만으로는 놓치기 쉬운 정보를 함께 반영하려고 합니다.

한 문장으로 줄이면 다음과 같습니다.

`Adam은 gradient의 최근 흐름과 좌표별 크기 차이를 함께 참고해, 파라미터마다 더 적응적으로 움직이려는 optimizer이다.`

조금 더 직관적으로 바꾸면 다음처럼 읽을 수 있습니다.

- 단순 update 기준: `지금 보이는 경사 방향으로 같은 기준 보폭을 내딛는다`
- Adam: `최근 몇 걸음의 흔들림을 같이 보고, 좌표마다 보폭을 다르게 조절한다`

예를 들어 어떤 파라미터는 gradient가 계속 크게 흔들리고, 다른 파라미터는 아주 작고 안정적으로 움직인다고 해 보겠습니다. 기본 직접 update는 둘을 같은 learning rate 기준으로 함께 밀지만, Adam 같은 적응형 update는 `지금 이 좌표는 너무 크게 흔들리고 있지 않은가`, `이 좌표는 너무 느리게 움직이고 있지 않은가`를 함께 반영하려고 합니다. 그래서 적응형 업데이트는 `같은 한 걸음`보다 `좌표마다 다른 한 걸음`에 가깝게 느껴집니다.

## Adam을 예로 보면 적응형 업데이트의 무엇이 보이는가

입문 단계에서는 복잡한 수식보다 다음 표가 더 중요합니다.

| 항목 | 단순 update 기준 | Adam |
| --- | --- | --- |
| 기본 감각 | 단순한 한 걸음 업데이트 | 더 많은 누적 정보를 반영한 적응형 업데이트 |
| 장점 | 직관이 단순하고 기준점이 분명함 | 초반 학습이 빠르고 실무에서 다루기 편한 경우가 많음 |
| 주의점 | 학습률 설정에 민감할 수 있음 | 설정이 편해 보여도 항상 최종 일반화가 더 좋다고 단정할 수는 없음 |

이 표에서 핵심은 `어느 것이 절대적으로 우월한가`가 아닙니다. 오히려 다음처럼 이해하는 편이 안전합니다.

`Adam은 단순한 gradient update 기준에 최근 흐름과 좌표별 조절을 더해, 더 적응적인 update를 만들려는 대표적 예다.`

## 왜 Adam이 대표 예로 자주 언급되는가

실무에서는 Adam이 자주 언급됩니다. 여기서 독자가 오래 붙잡아야 할 것은 `많이 쓰인다`보다 `왜 적응형 update의 대표 예로 자주 선택되는가`입니다.

- 초기 설정으로도 비교적 잘 동작하는 경우가 많고
- 학습 초반 손실이 빠르게 줄어드는 경험을 주기 쉽고
- 큰 모델이나 복잡한 데이터에서 입문 장벽이 낮게 느껴질 수 있습니다

하지만 여기서 중요한 주의점이 있습니다.

`Adam이 자주 쓰인다고 해서, 모든 문제에서 무조건 더 좋은 최종 결과를 보장하는 것은 아니다.`

즉, Adam의 인기는 실용성과 편의성에서 오는 부분이 크며, 문제에 따라 다른 판단이 필요합니다.

여기까지를 한 번 압축하면, 적응형 업데이트는 `기본 직접 update 위에 최근 흐름과 좌표별 조절을 더하는 방식`이고, Adam은 그 직관을 읽기 좋은 대표 예입니다.

이 차이를 업데이트 규칙만 남겨 압축하면 다음과 같습니다.

```mermaid
--8<-- "assets/part-05/chapter-07/sgd-vs-adam-flow-ko.mmd"
```

이 도식에서 먼저 확인할 결과는, 기본 직접 update가 `현재 gradient에 같은 기준 보폭으로 반응`하는 감각에 가깝다면, Adam은 `최근 흐름과 좌표별 차이를 더 반영해 보폭을 조절`하는 감각에 가깝다는 점입니다.

## 연습 및 예제

이제 예제로 바로 넘어가면 됩니다. 이번 절의 예제는 `진짜 Adam 전체 구현`이 아니라, 적응형 업데이트의 핵심 직관을 분리해서 보는 단순화 예제입니다. 예제 데이터는 [optimizer-gradient-history.csv](../../../assets/part-05/chapter-07/optimizer-gradient-history.csv)에 있습니다. 이 파일에는 12개 step 동안 세 파라미터가 받은 gradient 흐름이 들어 있습니다. 하나는 큰 gradient가 꾸준히 줄어드는 좌표, 하나는 작은 gradient가 꾸준히 줄어드는 좌표, 하나는 방향이 계속 흔들리는 좌표입니다.

입력:

- 여러 step에서 기록된 파라미터별 gradient 흐름
- 파라미터 이름 `parameter_name`
- 학습 step `step`
- 각 step의 `gradient`

출력:

- 단순 직접 업데이트 방식의 파라미터별 이동 결과
- Adam-like 누적 평균과 second moment를 단순화한 업데이트 결과
- 파라미터별 평균 `direct_delta`와 `adam_like_delta`
- 큰 gradient, 작은 gradient, 흔들리는 gradient에서 이동 경로가 어떻게 달라지는지

문제 상황:

- 적응형 업데이트의 차이는 수식 이름보다 파라미터별 gradient 흐름이 어떤 step별 update로 바뀌는지로 보는 편이 직관적이다

확인할 개념:

- 단순 직접 업데이트는 현재 gradient에 바로 반응한다
- Adam류 방식은 최근 gradient 정보를 누적해 이동량을 조절한다
- Adam류 방식은 좌표별 gradient 크기 이력도 update 크기에 반영하려 한다

입력(input):

CSV에는 다음 세 좌표의 gradient 흐름이 들어 있습니다.

| 파라미터 | gradient 흐름 | 먼저 예상해 볼 일 |
| --- | --- | --- |
| `risk_weight` | 큰 음수 gradient가 꾸준히 작아짐 | 직접 update는 크게 움직이고, Adam-like는 크기 이력을 보며 보폭을 조절합니다. |
| `recovery_weight` | 작은 음수 gradient가 꾸준히 작아짐 | 직접 update는 거의 못 움직이고, Adam-like는 작은 좌표도 자기 이력 기준으로 조절합니다. |
| `noise_weight` | 음수와 양수가 번갈아 흔들림 | 직접 update는 방향이 계속 바뀌고, Adam-like는 최근 흐름을 누적해 흔들림을 줄입니다. |

이 표의 목적은 정확한 숫자를 미리 암기하는 데 있지 않습니다. 같은 learning rate를 쓰더라도 단순 직접 업데이트는 `지금 기울기`를 바로 반영하고, Adam-like는 `최근 흐름`과 `좌표별 크기 이력`을 함께 남기며 다른 이동 경로를 만들 수 있다는 점을 코드 전에 붙잡는 데 있습니다.

```python
# CSV gradient history를 읽어 direct update와 Adam-like update가 파라미터별 이동 경로를 어떻게 다르게 만드는지 비교하는 예제입니다.
from csv import DictReader
from pathlib import Path

DATA_PATH = Path("docs/assets/part-05/chapter-07/optimizer-gradient-history.csv")
PARAMETER_ORDER = ["risk_weight", "recovery_weight", "noise_weight"]


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return [
            {
                "step": int(row["step"]),
                "parameter_name": row["parameter_name"],
                "signal_group": row["signal_group"],
                "gradient": float(row["gradient"]),
            }
            for row in DictReader(f)
        ]


def simulate_updates(rows):
    learning_rate = 0.05
    beta1 = 0.8
    beta2 = 0.9
    epsilon = 1e-8
    state = {
        parameter_name: {
            "direct_weight": 1.0,
            "adam_like_weight": 1.0,
            "m": 0.0,
            "v": 0.0,
        }
        for parameter_name in PARAMETER_ORDER
    }
    simulated = []

    parameter_index = {
        parameter_name: index
        for index, parameter_name in enumerate(PARAMETER_ORDER)
    }
    for row in sorted(
        rows,
        key=lambda item: (item["step"], parameter_index[item["parameter_name"]]),
    ):
        parameter_name = row["parameter_name"]
        gradient = row["gradient"]
        parameter_state = state[parameter_name]

        direct_delta = -learning_rate * gradient
        parameter_state["direct_weight"] += direct_delta

        parameter_state["m"] = beta1 * parameter_state["m"] + (1 - beta1) * gradient
        parameter_state["v"] = (
            beta2 * parameter_state["v"]
            + (1 - beta2) * gradient * gradient
        )
        adam_like_delta = (
            -learning_rate
            * parameter_state["m"]
            / (parameter_state["v"] ** 0.5 + epsilon)
        )
        parameter_state["adam_like_weight"] += adam_like_delta

        simulated.append(
            {
                "step": row["step"],
                "parameter_name": parameter_name,
                "gradient": gradient,
                "direct_delta": direct_delta,
                "adam_like_delta": adam_like_delta,
                "direct_weight": parameter_state["direct_weight"],
                "adam_like_weight": parameter_state["adam_like_weight"],
            }
        )

    return simulated


rows = load_rows(DATA_PATH)
simulated = simulate_updates(rows)

print("[model input]")
print("rows =", len(rows))
print("parameters =", ", ".join(PARAMETER_ORDER))

print("\n[checkpoints]")
for item in simulated:
    if item["step"] in [1, 6, 12]:
        print(
            item["parameter_name"],
            "step =", item["step"],
            "gradient =", item["gradient"],
            "direct_delta =", round(item["direct_delta"], 3),
            "adam_like_delta =", round(item["adam_like_delta"], 3),
        )

print("\n[final weights]")
for parameter_name in PARAMETER_ORDER:
    last = [
        item for item in simulated
        if item["parameter_name"] == parameter_name
    ][-1]
    print(
        parameter_name,
        "direct_weight =", round(last["direct_weight"], 3),
        "adam_like_weight =", round(last["adam_like_weight"], 3),
    )
```

출력에서는 같은 CSV 입력에서도 단순 직접 업데이트와 Adam-like의 step별 update가 어떻게 달라지는지부터 비교하면 됩니다.

```text
[model input]
rows = 36
parameters = risk_weight, recovery_weight, noise_weight

[checkpoints]
risk_weight step = 1 gradient = -7.0 direct_delta = 0.35 adam_like_delta = 0.032
recovery_weight step = 1 gradient = -0.6 direct_delta = 0.03 adam_like_delta = 0.032
noise_weight step = 1 gradient = -3.0 direct_delta = 0.15 adam_like_delta = 0.032
risk_weight step = 6 gradient = -3.0 direct_delta = 0.15 adam_like_delta = 0.049
recovery_weight step = 6 gradient = -0.29 direct_delta = 0.014 adam_like_delta = 0.05
noise_weight step = 6 gradient = 1.2 direct_delta = -0.06 adam_like_delta = -0.001
risk_weight step = 12 gradient = -0.4 direct_delta = 0.02 adam_like_delta = 0.03
recovery_weight step = 12 gradient = -0.05 direct_delta = 0.003 adam_like_delta = 0.034
noise_weight step = 12 gradient = 0.3 direct_delta = -0.015 adam_like_delta = -0.0

[final weights]
risk_weight direct_weight = 2.87 adam_like_weight = 1.502
recovery_weight direct_weight = 1.171 adam_like_weight = 1.52
noise_weight direct_weight = 1.07 adam_like_weight = 1.063
```

같은 출력도 `입력 gradient -> step별 update -> 누적된 weight`로 나누어 보면 Adam-like가 무엇을 더 보완하려는지 더 분명합니다.

![파라미터별 gradient 흐름](../../../assets/part-05/chapter-07/adaptive-gradient-history-ko.png)

첫 단계의 입력은 optimizer가 아직 바꾸지 않은 gradient 흐름입니다. `risk_weight`는 큰 음수 gradient가 꾸준히 줄고, `recovery_weight`는 작은 음수 gradient가 꾸준히 줄며, `noise_weight`는 방향이 계속 바뀝니다. 단순 직접 업데이트와 Adam-like는 모두 이 같은 입력을 받습니다.

![좌표별 평균 update 크기](../../../assets/part-05/chapter-07/adaptive-delta-scale-ko.png)

delta 단계에서 차이가 생깁니다. 단순 직접 업데이트는 gradient 크기 차이를 update 크기 차이로 거의 그대로 옮깁니다. Adam-like는 최근 흐름과 좌표별 크기 이력을 함께 쓰기 때문에 큰 gradient 좌표는 상대적으로 눌리고, 작은 gradient 좌표도 자기 이력 기준으로 조절됩니다.

![update 규칙별 파라미터 이동 경로](../../../assets/part-05/chapter-07/adaptive-weight-trajectory-ko.png)

최종 파라미터 경로를 보면 이 차이가 누적됩니다. 큰 gradient가 꾸준한 `risk_weight`에서는 직접 update가 훨씬 멀리 움직이고, 작은 gradient가 꾸준한 `recovery_weight`에서는 Adam-like가 더 크게 반응합니다. 방향이 흔들리는 `noise_weight`에서는 두 경로 모두 크게 멀어지지 않습니다. 이 단계에서 달라지는 것은 `gradient를 새로 계산했다`가 아니라, optimizer 규칙이 같은 gradient 흐름을 실제 파라미터 경로로 바꾸는 방식입니다.

이 예제는 진짜 Adam 전체 공식을 구현한 것도 아니고, 단순 직접 업데이트와 Adam의 성능 우열을 판정하는 실험도 아닙니다. 여기서 읽어야 할 핵심은 다음입니다.

- 단순 직접 업데이트는 현재 `gradient`를 비교적 직접 반영합니다
- Adam류의 아이디어는 최근 방향과 좌표별 크기 이력을 누적해 step별 update를 다르게 만듭니다
- optimizer는 단순히 `감소시킨다`가 아니라, 같은 gradient를 `어떤 update 경로로 바꿀지`를 정합니다

이 예제를 읽으면 적응형 업데이트의 보완점이 두 축으로 나뉩니다.

| 보는 축 | 직접 확인할 변화 | 이 절에서 남길 문장 |
| --- | --- | --- |
| 시간축 | 최근 gradient가 moving average에 남아 step별 update가 매끈해진다 | 적응형 업데이트는 현재 gradient만 보지 않고 최근 흐름을 함께 볼 수 있다 |
| 좌표축 | 파라미터마다 자기 gradient 크기 이력을 따로 쌓아 보폭을 조절한다 | 적응형 업데이트는 모든 파라미터를 같은 기준 보폭으로만 밀지 않는다 |

이 표까지 읽고 나면 적응형 업데이트의 핵심을 `시간축 누적과 좌표축 조절을 update 규칙에 넣는 방식`으로 말할 수 있어야 합니다. 그리고 Adam은 그 방식을 대표적으로 보여 주는 예라고 정리하면 충분합니다.

## 언제 적응형 업데이트 관점을 먼저 꺼내는가

optimizer의 일반 역할을 이해한 뒤에는 `지금 기본 업데이트 감각만으로 충분한가, 아니면 적응형 업데이트 감각이 필요한가`를 나누어 읽는 편이 좋습니다.

| 먼저 보이는 문제 장면 | 먼저 떠올릴 optimizer 관점 | 이유 |
| --- | --- | --- |
| gradient 방향과 보폭의 가장 기본 구조를 설명해야 한다 | 단순 update 기준 | 현재 gradient에 직접 반응하는 기본 업데이트 감각을 가장 분명히 보여 줍니다. |
| 초반 학습이 너무 거칠거나 좌표별 스케일 차이가 크다 | 적응형 업데이트 | 누적 정보와 좌표별 적응을 반영하는 업데이트 감각이 더 중요해집니다. |
| 실무에서 왜 Adam이 자주 쓰이는지 설명해야 한다 | 적응형 업데이트를 먼저 떠올리고 Adam은 대표 예로 본다 | 편의성과 실용성은 크지만 대표 예를 곧바로 일반 원리와 혼동하면 감각이 흐려지기 때문입니다. |
| optimizer를 절대 우열로 외우려는 경향이 보인다 | 단순 기준과 적응형 업데이트를 나란히 둔다 | 속도, 안정성, 일반화를 분리해 읽어야 하기 때문입니다. |

## 체크리스트

- 적응형 업데이트가 기본 update에 무엇을 더 보완하려는지 설명할 수 있는가?
- 적응형 업데이트는 누적 정보와 좌표별 조절을 더 반영하는 방식이라는 점을 설명할 수 있는가?
- 단순 update 기준과 적응형 업데이트를 `현재 gradient에 바로 반응하는 방식`과 `누적 정보와 좌표별 차이를 더 반영하는 방식`의 차이로 설명할 수 있는가?
- CSV 예제에서 시간축 누적과 좌표축 조절을 함께 읽어야 한다는 점을 구분할 수 있는가?
- Adam은 적응형 업데이트의 대표 예일 뿐, 절대적으로 더 좋은 optimizer라고 단정할 수 없다는 점을 말할 수 있는가?

## 출처와 참고 자료

- Léon Bottou, `Large-Scale Machine Learning with Stochastic Gradient Descent`, COMPSTAT, 2010, 확인 날짜: 2026-07-19. [https://doi.org/10.1007/978-3-7908-2604-3_16](https://doi.org/10.1007/978-3-7908-2604-3_16){: target="_blank" rel="noopener noreferrer" }
- Diederik P. Kingma, Jimmy Ba, `Adam: A Method for Stochastic Optimization`, arXiv, 2014, 확인 날짜: 2026-07-19. [https://arxiv.org/abs/1412.6980](https://arxiv.org/abs/1412.6980){: target="_blank" rel="noopener noreferrer" }
- Sebastian Ruder, `An overview of gradient descent optimization algorithms`, arXiv, 2016, 확인 날짜: 2026-07-19. [https://arxiv.org/abs/1609.04747](https://arxiv.org/abs/1609.04747){: target="_blank" rel="noopener noreferrer" }
