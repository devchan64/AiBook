# P7-4.3 표현 정규화 연습

> Section ID: `P7-4.3`
> Version: `v2026.08.01`

표현 정규화 연습은 `raw_expression`, `normalized_expression`, `coverage_change`, `prediction_change`, `remaining_oov`, `review_decision`을 함께 남깁니다. 정규화가 늘 좋은 것이 아니라 어떤 신호를 살리고 잃는지 봐야 합니다.

`낯선 표현을 학습 때 본 표현으로 바꾸면 실제로 무엇이 달라지는가`를 직접 실험해 볼 차례입니다. 정규화 규칙 하나가 예측, coverage, 회고 우선순위를 어떻게 함께 바꾸는지 확인하는 연습입니다.

같은 고객 문의를 `정규화 전`과 `정규화 후`로 나누어 다시 실행하면 `캔슬`, `스케줄`, `하자`처럼 실제 운영에서 흔하지만 학습 어휘와 어긋나는 표현을 어떻게 다뤄야 하는지 보입니다. 기록에는 무엇을 바꿨고 무엇이 좋아졌는지가 남아야 합니다.

## 표현 정규화가 바꾸는 출력

- 표현 정규화(normalization)는 텍스트 분류 실습에서 무엇을 바꾸는가?
- 같은 문의를 정규화 전후로 비교하면 coverage와 예측은 어떻게 달라지는가?
- 어떤 표현을 먼저 사전에 추가할지 어떤 기준으로 정할 수 있는가?

핵심은 `동의어 또는 운영 표현을 학습 어휘에 가까운 표현으로 치환`했을 때 모델이 읽는 단어와 회고 문장이 어떻게 달라지는지 확인하는 데 있습니다. 여기서 먼저 봐야 할 것은 거대한 전처리 파이프라인이 아니라, 표현 하나의 차이가 coverage와 예측 해석을 얼마나 바꾸는가입니다.

## 판단 기준

- 정규화 전후 결과를 나란히 비교하는 실행 기록을 만들 수 있습니다.
- coverage 개선과 정답 개선이 항상 함께 움직이지는 않는다는 점을 설명할 수 있습니다.
- 어떤 표현을 우선 정규화할지 `오답 빈도`, `핵심 의도성`, `운영 영향` 기준으로 정리할 수 있습니다.

## 왜 연습 절로 분리하는가

P7-4.2까지 읽고 나면 `낮은 coverage 샘플은 다시 봐야 한다`는 판단은 이해할 수 있습니다. 하지만 실제 프로젝트에서는 거기서 멈추지 않고, `무엇을 어떻게 바꿔 볼 것인가`까지 바로 이어져야 합니다.

이 장면을 설명 절 안에 짧게 넣는 것만으로는 부족한 이유는 다음과 같습니다.

| 질문 | 설명 절만 읽을 때 | 연습 절까지 수행할 때 |
| --- | --- | --- |
| `캔슬`이 왜 문제인가 | OOV라고 이해함 | `취소`로 바꾸었을 때 점수와 예측이 어떻게 달라지는지 확인함 |
| `스케줄`은 왜 다시 봐야 하는가 | coverage가 낮다고 이해함 | 정답은 맞아도 정규화가 회고 우선순위를 낮출 수 있음을 확인함 |
| 무엇을 먼저 고칠 것인가 | 막연한 개선 아이디어만 남음 | 실제 비교표를 보고 우선순위를 정함 |

예를 들어 정규화 후 정확도가 `1.0`으로 올라가면, 빠르게는 `동의어 사전만 더 늘리면 텍스트 문제는 대부분 해결된다`고 적고 싶어질 수 있습니다. 하지만 더 안전한 다음 판단은 정확도 상승만 보는 것이 아니라, `평가-05`처럼 실제 오답을 만든 표현이 무엇이었는지, `평가-07`처럼 정답은 유지됐지만 coverage를 깎은 표현이 무엇인지, `정규화 뒤에도 남는 OOV`가 무엇인지를 먼저 나누는 것입니다. 그렇게 읽어야 `효과가 큰 규칙`과 `나중에 정리해도 되는 규칙`을 구분할 수 있습니다.

```mermaid
--8<-- "assets/part-07/chapter-04/p7-4-3-normalization-case-flow-ko.mmd"
```

즉, 이 연습의 역할은 `표현 문제를 알았다`에서 끝나지 않고, `표현 문제를 어떻게 실험으로 다룰 것인가`까지 손으로 닫는 데 있습니다.

## 입력 파일

- 파일 경로: [`p7-4-support-routing-dataset.csv`](../../../assets/part-07/chapter-04/p7-4-support-routing-dataset.csv){ .csv-preview }
- 한 행의 의미: `한 건의 고객 문의와 라우팅 정답`
- 이번 연습에서 특히 볼 평가 행: `평가-05`, `평가-07`

고객 문의를 `원문 문장`과 `정규화한 문장`으로 나눠 같은 평가 셋에서 비교합니다. 핵심은 입력 파일 재사용이 아니라, 표현 하나를 바꿨을 때 coverage와 예측이 어떤 식으로 함께 흔들리는지 확인하는 데 있습니다. 아래 코드는 `docs/` 폴더가 보이는 책 저장소 루트에서 실행합니다.

| 평가 샘플 | 원문 | 이번 연습에서 주목할 표현 |
| --- | --- | --- |
| 평가-05 | `캔슬 후 송장 남아 있어요` | `캔슬` |
| 평가-07 | `하자 제품 환불 스케줄 알고 싶어요` | `하자`, `스케줄` |

## 연습 흐름

```mermaid
--8<-- "assets/part-07/chapter-04/p7-4-3-normalization-workflow-ko.mmd"
```

이 흐름에서 중요한 점은 `정규화 규칙을 많이 만드는 것`이 아니라, `하나의 규칙이 어떤 샘플에서 어떤 변화를 만들었는지 분리해서 읽는 것`입니다.

## 실행 기록 기준

1. 정규화 규칙을 적용하지 않은 결과와 적용한 결과를 같은 평가 셋에서 비교합니다.
2. `coverage`, `예측 팀`, `정답 여부`, `남은 OOV`, `검토 결정`이 어떻게 바뀌는지 샘플별로 적습니다.
3. 바뀐 결과를 보고 `어떤 표현을 다음 데이터 정리 우선순위로 올릴지` 한 문단으로 정리합니다.

## Python 예제

예제는 `정규화 전후 비교표`를 바로 얻는 것입니다. 코드가 길어 보이더라도 실제로는 토큰화와 분류 흐름은 유지한 채, `정규화 규칙 적용` 단계가 coverage와 예측 해석을 어떻게 바꾸는지 드러내는 형태입니다.

- 문제 상황: 고객 문의의 낯선 표현이 라우팅 결과를 흔든다.
- 비교 대상: 원문 문장 vs 정규화 후 문장
- 기대 출력: 샘플별 coverage 변화, 예측 변화, 정규화 효과 요약
- 확인할 개념:
  - 정규화는 입력 표현을 학습 어휘에 더 가깝게 만드는 작업이다
  - coverage가 올라가도 예측이 그대로일 수 있다
  - 정규화 우선순위는 `오답을 만든 표현`부터 잡는 편이 실무적이다

```python
# 고객지원 문장의 표현 정규화 전후 coverage, OOV, 예측 팀 변화를 비교해 정규화 효과를 확인하는 예제입니다.
import csv
import numpy as np
import re
from pathlib import Path

data_path = Path("docs/assets/part-07/chapter-04/p7-4-support-routing-dataset.csv")
rows = list(csv.DictReader(data_path.open(encoding="utf-8")))
for row in rows:
    row["라벨"] = int(row["label"])

train_rows = [row for row in rows if row["split"] == "train"]
test_rows = [row for row in rows if row["split"] == "test"]

라벨_이름 = {0: "환불팀", 1: "배송팀"}

def tokenize(text):
    return text.split()

vocab = sorted({token for row in train_rows for token in tokenize(row["text"])})
token_to_index = {token: i for i, token in enumerate(vocab)}

normalization_map = {
    "캔슬": "취소",
    "스케줄": "일정",
    "하자": "불량",
}

def normalize_text(text):
    for raw_expression, normalized_expression in sorted(
        normalization_map.items(), key=lambda item: len(item[0]), reverse=True
    ):
        # 공백으로 나뉜 표현 경계에서만 바꿔 부분 문자열 치환을 피합니다.
        pattern = rf"(?<!\S){re.escape(raw_expression)}(?!\S)"
        text = re.sub(pattern, normalized_expression, text)
    return text

def vectorize(texts):
    X = np.zeros((len(texts), len(vocab)), dtype=float)
    token_lists = []
    oov_lists = []
    coverage_list = []

    for i, text in enumerate(texts):
        tokens = tokenize(text)
        token_lists.append(tokens)
        known = 0
        oov = []
        for token in tokens:
            if token in token_to_index:
                X[i, token_to_index[token]] += 1
                known += 1
            else:
                oov.append(token)
        oov_lists.append(oov)
        coverage_list.append(round(known / len(tokens), 3) if tokens else 0.0)

    return X, token_lists, oov_lists, coverage_list

X_train, _, _, _ = vectorize([row["text"] for row in train_rows])
y_train = np.array([row["라벨"] for row in train_rows])

class_profiles = np.vstack([
    X_train[y_train == 0].sum(axis=0),
    X_train[y_train == 1].sum(axis=0),
])

original_texts = [row["text"] for row in test_rows]
normalized_texts = [normalize_text(text) for text in original_texts]
y_test = np.array([row["라벨"] for row in test_rows])

X_original, _, original_oov, original_coverage = vectorize(original_texts)
X_normalized, _, normalized_oov, normalized_coverage = vectorize(normalized_texts)

def predict_labels(X):
    scores = X @ class_profiles.T
    predictions = np.argmax(scores, axis=1)
    has_signal = X.sum(axis=1) > 0
    has_single_winner = np.ptp(scores, axis=1) > 0
    # 근거가 없거나 팀 점수가 동률이면 첫 라벨을 정답처럼 내보내지 않습니다.
    return np.where(has_signal & has_single_winner, predictions, -1)

def display_prediction(prediction):
    return "판단 보류" if prediction == -1 else 라벨_이름[int(prediction)]

def evaluation_status(prediction, actual):
    if prediction == -1:
        return "판단 보류"
    return "정답" if prediction == actual else "오답"

def review_decision(original_prediction, normalized_prediction, actual, coverage_change):
    original_status = evaluation_status(original_prediction, actual)
    normalized_status = evaluation_status(normalized_prediction, actual)
    if original_status == "정답" and normalized_status != "정답":
        return "규칙 되돌리기 또는 재검토"
    if original_status != "정답" and normalized_status != "정답":
        return "규칙 또는 데이터 보강"
    if original_status != "정답" and normalized_status == "정답":
        return "우선 정규화"
    if coverage_change > 0:
        return "다음 정리 후보"
    return "추가 확인"

original_pred = predict_labels(X_original)
normalized_pred = predict_labels(X_normalized)

comparison_rows = []
for i, row in enumerate(test_rows):
    comparison_rows.append({
        "평가 샘플": row["sample_id"],
        "원문": original_texts[i],
        "정규화 후": normalized_texts[i],
        "원문 coverage": original_coverage[i],
        "정규화 후 coverage": normalized_coverage[i],
        "coverage 변화": round(normalized_coverage[i] - original_coverage[i], 3),
        "원문 OOV": original_oov[i],
        "남은 OOV": normalized_oov[i],
        "원문 예측": display_prediction(original_pred[i]),
        "정규화 후 예측": display_prediction(normalized_pred[i]),
        "예측 변화": (
            "변화 없음"
            if original_pred[i] == normalized_pred[i]
            else f"{display_prediction(original_pred[i])} -> {display_prediction(normalized_pred[i])}"
        ),
        "원문 정답 여부": evaluation_status(original_pred[i], y_test[i]),
        "정규화 후 정답 여부": evaluation_status(normalized_pred[i], y_test[i]),
        "실제 팀": 라벨_이름[y_test[i]],
        "검토 결정": review_decision(
            original_pred[i], normalized_pred[i], y_test[i],
            normalized_coverage[i] - original_coverage[i]
        ),
    })

summary = {
    "원문 정확도": round(float((original_pred == y_test).mean()), 3),
    "정규화 후 정확도": round(float((normalized_pred == y_test).mean()), 3),
    "coverage가 오른 샘플": [
        row["sample_id"]
        for i, row in enumerate(test_rows)
        if normalized_coverage[i] > original_coverage[i]
    ],
    "예측이 바뀐 샘플": [
        row["sample_id"]
        for i, row in enumerate(test_rows)
        if normalized_pred[i] != original_pred[i]
    ],
    "원문 판단 보류 샘플": [
        row["sample_id"]
        for i, row in enumerate(test_rows)
        if original_pred[i] == -1
    ],
    "정규화 후 판단 보류 샘플": [
        row["sample_id"]
        for i, row in enumerate(test_rows)
        if normalized_pred[i] == -1
    ],
}

print("정규화 비교 요약 =", summary)
print("핵심 샘플별 비교 =")
for row in comparison_rows:
    if row["평가 샘플"] in {"평가-05", "평가-07"}:
        print(row)
```

실행 결과 예시는 다음과 같습니다.

```text
정규화 비교 요약 = {'원문 정확도': 0.857, '정규화 후 정확도': 1.0, 'coverage가 오른 샘플': ['평가-05', '평가-07'], '예측이 바뀐 샘플': ['평가-05'], '원문 판단 보류 샘플': [], '정규화 후 판단 보류 샘플': []}
핵심 샘플별 비교 =
{'평가 샘플': '평가-05', '원문': '캔슬 후 송장 남아 있어요', '정규화 후': '취소 후 송장 남아 있어요', '원문 coverage': 0.2, '정규화 후 coverage': 0.4, 'coverage 변화': 0.2, '원문 OOV': ['캔슬', '후', '남아', '있어요'], '남은 OOV': ['후', '남아', '있어요'], '원문 예측': '배송팀', '정규화 후 예측': '환불팀', '예측 변화': '배송팀 -> 환불팀', '원문 정답 여부': '오답', '정규화 후 정답 여부': '정답', '실제 팀': '환불팀', '검토 결정': '우선 정규화'}
{'평가 샘플': '평가-07', '원문': '하자 제품 환불 스케줄 알고 싶어요', '정규화 후': '불량 제품 환불 일정 알고 싶어요', '원문 coverage': 0.333, '정규화 후 coverage': 0.667, 'coverage 변화': 0.334, '원문 OOV': ['하자', '스케줄', '알고', '싶어요'], '남은 OOV': ['알고', '싶어요'], '원문 예측': '환불팀', '정규화 후 예측': '환불팀', '예측 변화': '변화 없음', '원문 정답 여부': '정답', '정규화 후 정답 여부': '정답', '실제 팀': '환불팀', '검토 결정': '다음 정리 후보'}
```

## 결과를 어떻게 읽는가

이번 비교에서 먼저 읽어야 할 것은 `정확도 1.0`이 아니라, `어떤 표현을 바꿨더니 무엇이 달라졌는가`입니다.

| 샘플 | 정규화 전 | 정규화 후 | 검토 결정 |
| --- | --- | --- | --- |
| 평가-05 | coverage 0.2, 배송팀 오답 | coverage 0.4, 환불팀 정답 | `우선 정규화`: `캔슬`은 실제 오답을 만들었다 |
| 평가-07 | coverage 0.333, 환불팀 정답 | coverage 0.667, 환불팀 정답 유지 | `다음 정리 후보`: `하자`, `스케줄`은 coverage만 낮췄다 |

이 비교를 통해 다음 네 가지 정규화 판단 경우를 구분할 수 있습니다.

- `오답을 직접 만든 표현`: 먼저 고쳐야 합니다. 예제에서는 `캔슬`이 여기에 해당합니다.
- `정답은 유지됐지만 coverage를 낮춘 표현`: 다음 우선순위로 둘 수 있습니다. 예제에서는 `하자`, `스케줄`이 여기에 가깝습니다.
- `정답을 오답 또는 판단 보류로 바꾼 규칙`: coverage가 올라도 먼저 되돌리거나 다시 검토해야 합니다. 이 경우에는 `규칙 되돌리기 또는 재검토`로 기록합니다.
- `오답 또는 판단 보류가 그대로 남은 규칙`: coverage가 올라도 오류가 해결되지 않았으므로 `규칙 또는 데이터 보강`으로 기록합니다.

즉, 정규화 우선순위는 단순히 OOV 개수만으로 정하기보다 `실제 운영 판단을 틀리게 만들었는가`를 먼저 봐야 합니다. 특히 정규화 전에는 맞았는데 정규화 후에 틀리거나 보류가 된 샘플, 또는 정규화 뒤에도 오답·보류가 남은 샘플은 coverage 개선보다 앞서 확인합니다.

## 결과 해석 기준

- coverage가 올라갔는데도 예측이 안 바뀌는 샘플은 무엇인가?
- 예측이 바뀐 샘플은 어떤 단어 하나가 핵심 신호였는가?
- 정규화로 해결되지 않고 여전히 남는 OOV는 무엇인가?
- 다음 데이터 정리에서는 `동의어 사전 추가`, `학습 데이터 보강`, `토큰화 방식 변경` 중 무엇을 먼저 시도할 것인가?

## 프로젝트 기록 예시

실습 뒤에는 다음 형식으로 짧게 기록해 두는 편이 좋습니다.

| 항목 | 적을 내용 |
| --- | --- |
| 사실 | coverage 변화, 예측 변화, 원문·정규화 후 정답 여부는 무엇인가 |
| 해석 | 남은 OOV는 무엇이며 그 변화가 표현 불일치 때문이었는가, 점수 우연이었는가 |
| 다음 질문 | `우선 정규화`, `다음 정리 후보`, `규칙 또는 데이터 보강`, `규칙 되돌리기 또는 재검토` 중 무엇으로 기록할 것인가 |

한 문단으로 쓰면 예를 들어 다음처럼 정리할 수 있습니다.

> `캔슬 후 송장 남아 있어요`는 원문에서는 배송팀으로 잘못 분류됐지만, `캔슬`을 `취소`로 정규화하자 coverage가 0.2에서 0.4로 오르고 예측도 환불팀으로 바뀌었다. 반면 `하자 제품 환불 스케줄 알고 싶어요`는 정답은 유지됐지만 coverage가 0.333에서 0.667로 올라, 지금은 맞더라도 표현 정규화 가치가 있는 샘플임을 확인했다. 따라서 다음 반복에서는 실제 오답을 만든 동의어부터 우선 사전에 추가하고, 그 뒤에 low-coverage 정답 샘플을 정리하는 편이 적절하다.

## 직접 바꿔 보며 확인할 것

각 실습은 기본 CSV와 기본 `normalization_map`에서 시작하는 독립 실행입니다. 지시한 `sample_id` 행의 `text` 열 또는 정규화 규칙만 수정하고 실행한 뒤, 다음 실습 전에는 원래 문장과 규칙으로 되돌립니다.

1. `평가-05`를 `캔슬 후 남아 있어요`로 바꿔 다시 실행해 봅니다.
   관찰할 점: 원문 coverage는 `0.000`이고 예측은 `판단 보류`, 정규화 후 coverage는 `0.250`이고 예측은 환불팀 정답이 됩니다. 요약의 `원문 판단 보류 샘플`에는 `평가-05`가, 정규화 후 목록에는 아무것도 남지 않습니다. 원문에는 학습 어휘가 하나도 없어 두 팀 점수가 동률입니다. 이 예제는 그 동률을 첫 라벨의 정답처럼 처리하지 않으므로, `캔슬` 정규화가 모델에 환불 신호를 다시 제공했다는 사실을 분리해 읽을 수 있습니다.

2. `평가-07`에 새 표현 하나를 더 넣어 봅니다. 예를 들어 `하자 제품 환불 스케줄 ASAP`처럼 바꿔 봅니다.
   관찰할 점: 원문 coverage는 `0.400`, 정규화 후 coverage는 `0.800`이지만 `ASAP`는 정규화 뒤에도 OOV로 남습니다. 예측은 환불팀 정답으로 유지되므로, 이 표현은 즉시 오답을 고치기보다 사전 추가 또는 토큰화 검토 대상으로 기록합니다.

3. `평가-07`을 `하자 제품 환불 요청 스케줄 알고 싶어요`로 바꾸고, 정규화 규칙에 `"환불 요청": "환불"`을 추가해 봅니다.
   관찰할 점: 정규화 후 문장에서 `요청`이 사라지고 coverage가 `0.429`에서 `0.667`로 오르는가? 정규화 함수는 긴 표현부터 공백 경계에서 치환하므로, `환불 요청`은 한 표현으로 적용되고 `환불 요청서` 같은 더 긴 토큰 내부는 바꾸지 않습니다. 예측이 그대로라면 규칙 추가는 coverage 개선 기록으로 남기고, 실제 오답 감소는 별도 평가에서 확인합니다.

4. 기본 `평가-07`을 유지한 채, 정규화 규칙에 `"환불": "배송"`을 추가해 봅니다.
   관찰할 점: 원문 coverage `0.333`, 환불팀 정답이 정규화 뒤 coverage `0.667`, 배송팀 오답으로 바뀌는가? coverage가 올라도 `검토 결정`은 `규칙 되돌리기 또는 재검토`여야 합니다. 이 규칙은 의도적으로 잘못된 예이므로 실행 뒤 바로 제거합니다.

5. 기본 `평가-05`를 유지한 채, 정규화 규칙에 `"취소": "배송"`을 추가해 봅니다.
   관찰할 점: 원문 coverage `0.2`, 배송팀 오답이 정규화 뒤 coverage `0.4`, 배송팀 오답으로 남는가? coverage는 올랐지만 오류가 해결되지 않았으므로 `검토 결정`은 `규칙 또는 데이터 보강`이어야 합니다. 이 규칙도 의도적으로 잘못된 예이므로 실행 뒤 바로 제거합니다.

판단 기준은 coverage가 올랐다는 사실만이 아니라, 그 변화가 실제 오답을 줄였는지입니다. 먼저 정답이 오답·보류로 바뀐 규칙은 되돌리거나 다시 검토하고, 오답·보류가 남은 규칙은 데이터 또는 규칙을 보강합니다. 그다음 오답을 정답으로 바꾼 표현을 우선 정규화 후보로 올리고, 정답은 유지됐지만 coverage만 낮춘 표현은 다음 정리 우선순위로 둡니다.

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| 비교 조건 | 정규화 전후를 같은 평가 셋에서 나란히 실행했는가? |
| coverage | coverage 변화와 예측 변화를 함께 기록했는가? |
| 오류 표현 | 오답을 만든 표현과 low-coverage 정답 표현을 구분했는가? |
| 정답 회귀 | 정답이 정규화 뒤 오답 또는 판단 보류가 된 샘플을 되돌리기 또는 재검토 대상으로 표시했는가? |
| 오류 잔존 | 정규화 뒤에도 오답 또는 판단 보류가 남은 샘플을 규칙 또는 데이터 보강 대상으로 표시했는가? |
| 남은 위험 | 정규화 후에도 남는 OOV나 애매한 표현을 적었는가? |
| 다음 반복 | 무엇을 먼저 바꿀지 한 문장으로 정했는가? |

## 출처와 참고 자료

- 문의 데이터: [`p7-4-support-routing-dataset.csv`](../../../assets/part-07/chapter-04/p7-4-support-routing-dataset.csv){ .csv-preview }
- 이 문서는 자체 실습 예시를 사용했습니다. 외부 자료를 직접 인용하지 않았습니다.
