# 3.13 표본 수가 적을 때 무엇을 말하지 말아야 하는가

지금까지 우리는 샘플 단위, 요약 표, 특징, 기준선 비교 구조를 만들었습니다. 하지만 비교표가 있다고 해서 모든 차이를 같은 강도로 읽을 수 있는 것은 아닙니다. 특히 운영 데이터에서는 표본 수가 적고, 같은 변화가 반복되는지 여부가 불분명할 수 있습니다. 그래서 해석 단계에서는 `무엇이 달라졌는가`만이 아니라 `그 차이를 얼마나 믿을 수 있는가`도 함께 봐야 합니다.

표본 수가 적으면 평균, 변동성, 대표 패턴 같은 값이 쉽게 흔들립니다. 예를 들어 최근 2건의 평균과 기준선 차이 0.3은 인상적으로 보일 수 있습니다. 하지만 최근 20건의 평균과 기준선 차이 0.3과는 무게가 다릅니다. 수치가 같아도, 그 차이가 몇 건에서 나온 것인지에 따라 해석의 강도는 달라져야 합니다.

여기서 중요한 것은 `데이터가 적으면 아무 말도 하지 말아야 한다`가 아닙니다. 더 정확한 표현은 `데이터가 적을수록 덜 확신하며 말해야 한다`입니다. 즉 해석을 멈추는 것이 아니라, 해석의 강도를 조절해야 합니다.

반복성도 같은 이유로 중요합니다. 한 번 크게 튄 변화와, 여러 번 조금씩 같은 방향으로 움직이는 변화는 운영상 의미가 다를 수 있습니다. 때로는 단발성 급락보다 최근 여러 구간에서 반복적으로 나타나는 약한 하락이 더 중요합니다. 운영자가 보고 싶은 것은 종종 `한 번의 특이한 사례`보다 `상태가 달라지고 있는 징후`이기 때문입니다.

| 상황 | 해석할 때 조심할 점 |
| --- | --- |
| 표본 수가 적고 반복도 약함 | 우연일 가능성을 더 크게 본다 |
| 표본 수가 적지만 같은 방향 변화가 반복됨 | 강한 결론은 보류하되 주의 깊게 본다 |
| 표본 수가 충분하고 반복도 있음 | 더 신뢰할 만한 변화 신호로 읽을 수 있다 |

짧은 숫자 예시로 보면 왜 같은 차이도 다르게 읽어야 하는지 더 분명합니다.

```python
import pandas as pd

cases = pd.DataFrame(
    [
        {"window_id": "small-sample", "event_count": 2, "recent_mean": 2.10, "baseline_mean": 2.40},
        {"window_id": "large-sample", "event_count": 20, "recent_mean": 2.10, "baseline_mean": 2.40},
    ]
)
cases["diff"] = cases["recent_mean"] - cases["baseline_mean"]

print(cases)
```

예상 출력:

```text
       window_id  event_count  recent_mean  baseline_mean  diff
0   small-sample            2         2.10            2.4  -0.3
1   large-sample           20         2.10            2.4  -0.3
```

두 경우의 차이값은 모두 `-0.3`입니다. 하지만 첫 번째는 2건, 두 번째는 20건에서 나온 값입니다. 따라서 숫자는 같아도 해석 강도는 같을 수 없습니다. 이처럼 표본 수는 단순 부가 정보가 아니라, 비교 결과를 얼마나 강하게 말할 수 있는지를 바꾸는 조건입니다.

반복성도 비슷하게 볼 수 있습니다.

```python
repeatability = pd.DataFrame(
    [
        {"window_id": "single-drop", "direction_signals": [-1, 0, 0, 0]},
        {"window_id": "repeated-drop", "direction_signals": [-1, -1, -1, -1]},
    ]
)
repeatability["repeatability_score"] = repeatability["direction_signals"].apply(sum)

print(repeatability[["window_id", "repeatability_score"]])
```

예상 출력:

```text
        window_id  repeatability_score
0     single-drop                   -1
1   repeated-drop                   -4
```

여기서는 단순히 방향 신호를 더한 아주 작은 예시지만, 한 번의 하락과 반복적 하락이 다른 의미를 가질 수 있다는 감각을 주기에는 충분합니다.

이 절에서 초심자가 가져가야 할 문장은 다음과 같습니다. `표본 수가 적을수록 차이는 더 조심스럽게 읽어야 한다.` 그리고 `반복되는 변화는 단발성 변화와 다른 의미를 가질 수 있다.`
