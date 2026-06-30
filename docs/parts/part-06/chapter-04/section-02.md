# P6-4.2 토큰화와 평가

P6-4.1에서는 공백 기준 토큰화로 아주 작은 텍스트 분류기를 만들었습니다. 그런데 텍스트 프로젝트는 정확도 숫자만으로 끝내기 어렵습니다.

왜냐하면 텍스트는 `무슨 단어를 알고 있었는가`, `무슨 단어를 몰랐는가`, `토큰 coverage가 어느 정도였는가`에 따라 결과 해석이 크게 달라지기 때문입니다.

이 절의 목적은 정확도 숫자 하나를 보는 대신, 모델이 실제로 어떤 단어를 읽을 수 있었는지까지 같이 기록하는 것이다.

## 이 절의 범위

이 절은 다음 질문에 답합니다.

- 토큰화(tokenization)는 프로젝트 성능 해석에 왜 직접 영향을 주는가?
- OOV(out-of-vocabulary) 토큰이 많은 문장은 왜 위험한가?
- 텍스트 분류 프로젝트에서 정확도 외에 무엇을 같이 기록해야 하는가?

이 절은 다음 내용은 깊게 다루지 않습니다.

- subword tokenizer의 병합 규칙
- BPE, WordPiece, SentencePiece의 내부 비교
- 정밀도(precision), 재현율(recall), F1의 심화 계산

이 절에서는 coverage와 OOV를 프로젝트 문서에 남기는 최소 감각만 다룹니다. 토크나이저 내부 비교는 Part 5의 P5-1.3 보충학습에서 이미 다시 읽을 수 있고, 정밀도·재현율·F1 같은 추가 평가 축은 Part 3의 P3-6장 평가 지표와 다시 연결됩니다.

## 이 절의 목표

- 토큰화와 평가를 분리하지 않고 함께 읽어야 하는 이유를 설명할 수 있습니다.
- OOV 토큰과 coverage 비율을 프로젝트 문서에 기록할 수 있습니다.
- 정확도는 같아도 입력 coverage가 낮으면 해석이 달라진다는 점을 이해할 수 있습니다.

## 왜 coverage를 봐야 하나

텍스트 분류 모델이 예측을 잘했다는 말은, 적어도 어떤 단어 구조를 읽고 분류했는지와 함께 나와야 합니다.

예를 들어 다음 두 문장은 정확히 같은 길이여도 모델 입장에서는 매우 다를 수 있습니다.

- `great support thank you`
- `excellent item arrived today`

첫 번째 문장은 학습 어휘에 있는 단어가 많을 수 있고, 두 번째 문장은 거의 다 낯선 단어일 수 있습니다. 이 차이를 기록하지 않으면 결과 해석이 부정확해집니다.

먼저 다음 세 질문으로 읽으면 좋습니다.

| 질문 | 짧은 답 |
| --- | --- |
| 왜 coverage를 보아야 하는가? | 모델이 실제로 읽은 단어 비율을 알아야 해서 |
| 무엇이 낮으면 위험한가? | known token coverage |
| 그래서 문서에 무엇을 남기는가? | OOV, coverage, 틀린 문장 사례 |

## 이번 프로젝트의 확장 평가

이번 절에서는 평가 문장 하나를 일부러 바꿉니다.

- 기존 praise 문장 대신 `excellent item arrived today`를 넣습니다.
- 이 문장에는 학습 어휘에 없던 단어가 많이 들어 있습니다.

즉, 프로젝트 질문은 이렇게 바뀝니다.

> 정확도뿐 아니라, 각 문장이 학습 어휘를 얼마나 많이 포함하는지도 함께 기록해야 하지 않는가?

## Python 예제

이번 예제의 목적은 각 test 문장의 토큰 목록과 known token coverage를 함께 출력하는 것입니다. 이번에는 단순히 coverage 한 줄만 출력하지 않고, `evaluation_records`, `review_summary`, `oov_tokens`를 함께 남겨서 어떤 문장을 다음 회고 대상으로 삼아야 하는지 바로 보이게 하겠습니다.

- 문제 상황: 문장 분류 결과를 coverage와 함께 읽는다.
- 입력(input): 학습 문장 6개, 평가 문장 4개
- 확인할 개념:
  - 토큰화 결과가 그대로 프로젝트 해석 자료가 된다
  - OOV 토큰이 많으면 예측 신뢰가 약해질 수 있다
  - review 대상 문장을 명시적으로 남겨야 다음 개선 계획이 쉬워진다

```python
import numpy as np

train_rows = [
    {"sample_id": "train-01", "text": "refund delay angry", "label": 0},
    {"sample_id": "train-02", "text": "broken product complaint", "label": 0},
    {"sample_id": "train-03", "text": "thank you fast delivery", "label": 1},
    {"sample_id": "train-04", "text": "love this product great", "label": 1},
    {"sample_id": "train-05", "text": "refund request not working", "label": 0},
    {"sample_id": "train-06", "text": "happy with quick support", "label": 1},
]
train_texts = [row["text"] for row in train_rows]
y_train = np.array([row["label"] for row in train_rows])
label_names = {0: "complaint", 1: "praise"}

vocab = sorted({token for text in train_texts for token in text.split()})
token_to_index = {token: i for i, token in enumerate(vocab)}

def vectorize(texts):
    X = np.zeros((len(texts), len(vocab)), dtype=float)
    token_lists = []
    known_counts = []
    total_counts = []
    oov_tokens_per_text = []

    for i, text in enumerate(texts):
        tokens = text.split()
        token_lists.append(tokens)
        total_counts.append(len(tokens))
        known = 0
        oov_tokens = []

        for token in tokens:
            if token in token_to_index:
                X[i, token_to_index[token]] += 1
                known += 1
            else:
                oov_tokens.append(token)

        known_counts.append(known)
        oov_tokens_per_text.append(oov_tokens)

    return X, token_lists, known_counts, total_counts, oov_tokens_per_text

X_train, _, _, _, _ = vectorize(train_texts)
class_centroids = np.vstack([
    X_train[y_train == 0].mean(axis=0),
    X_train[y_train == 1].mean(axis=0),
])

test_rows = [
    {"sample_id": "test-01", "text": "refund for broken product", "label": 0},
    {"sample_id": "test-02", "text": "great support thank you", "label": 1},
    {"sample_id": "test-03", "text": "delay but quick refund", "label": 0},
    {"sample_id": "test-04", "text": "excellent item arrived today", "label": 1},
]
test_texts = [row["text"] for row in test_rows]
y_test = np.array([row["label"] for row in test_rows])

X_test, token_lists, known_counts, total_counts, oov_tokens_per_text = vectorize(test_texts)

predictions = []
evaluation_records = []
for index, x in enumerate(X_test):
    distances = np.linalg.norm(class_centroids - x, axis=1)
    pred_label = int(np.argmin(distances))
    predictions.append(pred_label)
    coverage = known_counts[index] / total_counts[index] if total_counts[index] else 0.0
    evaluation_records.append({
        "sample_id": test_rows[index]["sample_id"],
        "text": test_rows[index]["text"],
        "tokens": token_lists[index],
        "oov_tokens": oov_tokens_per_text[index],
        "known_token_coverage": round(coverage, 3),
        "pred_label_name": label_names[pred_label],
        "true_label_name": label_names[y_test[index]],
        "correct": bool(pred_label == y_test[index]),
        "needs_token_review": bool(coverage < 0.5 or pred_label != y_test[index]),
    })

predictions = np.array(predictions)

review_summary = {
    "vocab_size": len(vocab),
    "tokenization_rule": "whitespace split",
    "test_accuracy": round(float((predictions == y_test).mean()), 3),
    "review_target_ids": [
        row["sample_id"] for row in evaluation_records if row["needs_token_review"]
    ],
    "low_coverage_count": sum(
        row["known_token_coverage"] < 0.5 for row in evaluation_records
    ),
}

print("review_summary =", review_summary)
print("evaluation_records =")
for row in evaluation_records:
    print(row)
```

실행 결과 예시는 다음과 같습니다.

```text
review_summary = {'vocab_size': 20, 'tokenization_rule': 'whitespace split', 'test_accuracy': 0.75, 'review_target_ids': ['test-04'], 'low_coverage_count': 1}
evaluation_records =
{'sample_id': 'test-01', 'text': 'refund for broken product', 'tokens': ['refund', 'for', 'broken', 'product'], 'oov_tokens': ['for'], 'known_token_coverage': 0.75, 'pred_label_name': 'complaint', 'true_label_name': 'complaint', 'correct': True, 'needs_token_review': False}
{'sample_id': 'test-02', 'text': 'great support thank you', 'tokens': ['great', 'support', 'thank', 'you'], 'oov_tokens': [], 'known_token_coverage': 1.0, 'pred_label_name': 'praise', 'true_label_name': 'praise', 'correct': True, 'needs_token_review': False}
{'sample_id': 'test-03', 'text': 'delay but quick refund', 'tokens': ['delay', 'but', 'quick', 'refund'], 'oov_tokens': ['but'], 'known_token_coverage': 0.75, 'pred_label_name': 'complaint', 'true_label_name': 'complaint', 'correct': True, 'needs_token_review': False}
{'sample_id': 'test-04', 'text': 'excellent item arrived today', 'tokens': ['excellent', 'item', 'arrived', 'today'], 'oov_tokens': ['excellent', 'item', 'arrived', 'today'], 'known_token_coverage': 0.0, 'pred_label_name': 'complaint', 'true_label_name': 'praise', 'correct': False, 'needs_token_review': True}
```

## 결과를 어떻게 읽는가

가장 중요한 사례는 마지막 문장입니다.

- `excellent item arrived today`
- known token coverage = `0.0`
- 예측은 `complaint`
- 실제 라벨은 `praise`

이 사례는 정확도 0.75라는 숫자보다 더 많은 정보를 줍니다. `review_summary`가 `test-04`를 review 대상으로 바로 가리키고, `evaluation_records`는 OOV 토큰이 네 개 모두였다는 점을 한 줄로 보여 줍니다.

`모델이 틀린 이유는 단지 분류 규칙이 약해서가 아니라, 학습 어휘에 없는 단어가 너무 많아 입력 표현 자체가 빈약해졌기 때문일 수 있다.`

즉, 텍스트 프로젝트에서는 `틀렸다`와 함께 `왜 이 문장을 잘 읽지 못했는가`를 토큰 수준에서 남기는 것이 중요합니다.

독자는 이 사례를 다음 세 줄로 요약할 수 있으면 충분합니다.

- 마지막 문장은 어휘에 없는 단어가 너무 많았다
- coverage가 0.0이면 예측 해석이 더 조심스러워져야 한다
- review 대상 문장과 OOV 목록을 함께 남겨야 다음 tokenizer 개선으로 이어진다
- 따라서 정확도 하락은 분류 규칙뿐 아니라 입력 표현 문제일 수도 있다

## 평가 문서에 추가할 항목

텍스트 분류 프로젝트라면 정확도 외에 다음 항목을 함께 적어 두는 편이 좋습니다.

| 항목 | 왜 필요한가 |
| --- | --- |
| vocabulary size | 모델이 어떤 어휘 범위를 보고 있는지 보여 줍니다. |
| tokenization rule | 공백 기준인지, subword인지 기록해야 해석이 가능합니다. |
| known token coverage | test 문장이 훈련 어휘를 얼마나 공유하는지 보여 줍니다. |
| wrong example | 실제로 어떤 문장을 틀렸는지 봐야 개선 방향이 나옵니다. |

이 표는 Part 6의 텍스트 프로젝트에서 사실상 `평가 기록 템플릿` 역할을 합니다.

## 프로젝트 회고 예시

이번 프로젝트의 회고를 한 문단으로 적으면 다음처럼 쓸 수 있습니다.

> 이번 장난감 텍스트 분류 프로젝트는 공백 기준 토큰화와 count vector만으로도 기본 분류 흐름을 재현했다. 그러나 `excellent item arrived today` 문장은 학습 어휘에 포함된 토큰이 하나도 없어 coverage가 0.0이었고, 결과적으로 praise 문장을 complaint로 잘못 분류했다. 따라서 이번 결과는 단순 정확도 0.75보다 `어휘 범위가 좁을 때 입력 표현이 무너질 수 있다`는 점을 더 잘 보여 준다. 다음 반복에서는 어휘를 넓히거나 subword tokenizer를 도입하는 방향을 검토할 수 있다.

이 문단에서 독자가 익혀야 할 형식은 다음과 같습니다.

- 어떤 문장이 틀렸는가
- coverage는 어땠는가
- 오류를 규칙 문제로 볼지 표현 문제로 볼지
- 다음 개선을 어디서 시작할지

## Part 5와의 연결

이 절은 Part 5의 토큰(token), 토큰화(tokenization), OOV, 임베딩(embedding) 설명과 직접 이어집니다.

LLM 시대에는 더 정교한 tokenizer를 쓰더라도, 기본 질문은 그대로 남습니다.

- 입력이 어떻게 쪼개졌는가?
- 모델이 실제로 읽은 단위는 무엇인가?
- 어휘 밖 표현이 얼마나 있었는가?

즉, 텍스트 분류의 작은 실습은 LLM 입력 해석의 기초 감각을 다시 훈련하는 효과도 있습니다.

이 절은 Part 6 전체 흐름에서 `텍스트 프로젝트는 정확도 경쟁이 아니라 입력 해석과 평가 기록까지 포함해야 한다`는 기준을 고정합니다.

## 이 절에서 기억할 관점

- 텍스트 프로젝트에서는 정확도만으로 해석이 부족합니다.
- 토큰화 규칙과 vocabulary 범위를 함께 기록해야 합니다.
- OOV 토큰이 많은 문장은 예측 해석이 더 조심스러워야 합니다.
- 잘못 분류된 문장을 토큰 수준으로 다시 읽는 습관이 중요합니다.

## 체크리스트

- 토큰화 규칙을 한 문장으로 적을 수 있는가?
- vocabulary size와 coverage를 기록했는가?
- 틀린 문장을 토큰 수준으로 다시 보여 줄 수 있는가?
- 다음 개선 방향을 어휘 확장 / tokenizer 변경 / 데이터 추가로 나누어 적을 수 있는가?

## 출처와 참고 자료

- NumPy Developers, `NumPy documentation`, 확인 날짜: 2026-06-29. [https://numpy.org/doc/stable/](https://numpy.org/doc/stable/){: target="_blank" rel="noopener noreferrer" }

이 절의 텍스트 데이터는 프로젝트 실습을 위해 만든 자체 장난감 문장입니다.
