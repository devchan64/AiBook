# P7-5.3 질문-근거 경계 연습

> Section ID: `P7-5.3`
> Version: `v2026.07.31`

`같은 문서 집합에서도 질문 문구를 어떻게 쓰느냐에 따라 왜 답변 상태가 달라지는가`를 직접 연습할 차례입니다. 질문 문구 하나가 `근거 부족`, `답변 과장 위험`, `근거 기반 답변`을 어떻게 가르는지 손으로 확인하는 데 초점을 둡니다.

질문 문구와 멈춤 규칙은 같은 프로젝트의 근거 기록을 직접 바꿉니다. 검색기가 똑같더라도 질문이 문서 범위를 직접 묻는지, 과장된 일반화를 요구하는지, 문서에 없는 개념을 끌고 오는지에 따라 결과가 달라집니다.

## 질문 경계가 바꾸는 답변 상태

- 질문 문구가 바뀌면 왜 같은 문서 집합에서도 답변 상태가 달라지는가?
- `근거 부족`과 `답변 과장 위험`은 어떤 질문에서 갈리는가?
- 문서 범위 안 질문과 범위 밖 질문을 어떻게 다시 써야 하는가?

핵심은 질문 재작성(rewrite)과 멈춤 기준(stop rule)을 통해 같은 문서 집합에서도 답변 상태가 어떻게 달라지는지 확인하는 데 있습니다. 검색기 자체를 바꾸기보다 질문을 덜 과장되게 쓰는 편이 언제 더 강한 개선이 되는지 먼저 봅니다.

## 판단 기준

- 질문 문구를 바꿔 답변 상태를 의도적으로 바꿔 볼 수 있습니다.
- `근거 부족`과 `답변 과장 위험`을 서로 다른 검토 대상으로 기록할 수 있습니다.
- 문서 범위 밖 질문을 문서 범위 안 질문으로 다시 쓰는 기본 연습을 할 수 있습니다.

## 왜 이 연습 절이 필요한가

P7-5.2까지 읽으면 독자는 보통 이렇게 생각하기 쉽습니다. `문서가 있으면 답하고, 없으면 멈추면 된다.` 하지만 실제 RAG 프로젝트에서는 그 경계가 그렇게 단순하지 않습니다.

문제가 되는 장면은 대체로 세 가지입니다.

| 장면 | 겉보기에는 비슷해 보이지만 실제로는 다른 점 |
| --- | --- |
| 문서에 없는 개념을 묻는 질문 | 검색 자체가 비어 있거나 억지 관련 문서를 끌고 온다 |
| 문서에 있는 주제를 과하게 일반화한 질문 | 검색은 되지만 답변을 강하게 단정하면 근거 밖으로 나간다 |
| 문서 표현과 맞닿게 다시 쓴 질문 | 같은 주제라도 문서 범위 안 답변으로 돌아온다 |

예를 들어 질문을 다시 썼더니 두 건이 `근거 기반 답변`으로 바뀌면, 빠르게는 `검색기를 손대지 않아도 질문만 잘 쓰면 다 해결된다`고 적고 싶어질 수 있습니다. 하지만 더 안전한 다음 판단은 재작성 성공만 보는 것이 아니라, `원래 질문이 문서 범위 밖이었는가`, `과장 표현 때문에 위험했던 것인가`, `재작성 뒤에도 여전히 근거 부족으로 남는 질문은 무엇인가`를 먼저 나누는 것입니다. 그렇게 읽어야 `질문 재작성으로 풀리는 문제`와 `문서 자체를 늘려야 하는 문제`를 구분할 수 있습니다.

```mermaid
--8<-- "assets/part-07/chapter-05/p7-5-3-rewrite-risk-flow-ko.mmd"
```

즉, RAG 품질은 문서와 검색기만의 문제가 아니라 `질문 문구`와 `멈춤 규칙`의 문제이기도 합니다.  역할은 바로 이 지점을 독자가 직접 흔들어 보는 데 있습니다.

## 입력 파일

- 문서 파일: [`p7-5-rag-documents.csv`](../../../assets/part-07/chapter-05/p7-5-rag-documents.csv) · [CSV 미리보기](../../../assets/part-07/chapter-05/p7-5-rag-documents.csv){ .csv-preview }
- 연습 질문 파일: [`p7-5-boundary-cases.csv`](../../../assets/part-07/chapter-05/p7-5-boundary-cases.csv) · [CSV 미리보기](../../../assets/part-07/chapter-05/p7-5-boundary-cases.csv){ .csv-preview }
- 문서 파일의 한 행 의미: `검색 가능한 문서 조각 하나`
- 연습 질문 파일의 한 행 의미: `질문-근거 경계를 시험하는 질문 한 개`

P7-5.1, P7-5.2와 같은 문서 집합을 그대로 사용합니다. 대신 질문 파일을 별도로 두어, 같은 지식베이스 위에서 질문 문구와 기대 상태만 바꾸며 결과를 비교합니다. 즉, 다른 프로젝트를 새로 여는 것이 아니라 같은 RAG 프로젝트 기록에서 `질문 경계`가 어떻게 품질 판정을 바꾸는지 더 분명히 드러내는 실습입니다.

| case_id | question | expected_state | focus |
| --- | --- | --- | --- |
| 연습-02 | `MCP는 왜 필요한가?` | 근거 부족 | 문서 범위 밖 질문 |
| 연습-03 | `문서 분할 재정렬만 있으면 모든 환각이 해결되는가?` | 답변 과장 위험 | 과한 일반화 |
| 연습-04 | `문서 분할과 재정렬은 검색 품질에 어떤 도움을 줄 수 있는가?` | 근거 기반 답변 | 더 보수적인 질문 재작성 |

## 연습 흐름

```mermaid
--8<-- "assets/part-07/chapter-05/p7-5-3-question-boundary-flow-ko.mmd"
```

이 흐름에서 중요한 점은 `검색 점수`만 보는 것이 아니라, `질문을 어떻게 다시 썼더니 상태가 바뀌는가`까지 함께 읽는 것입니다.

## 실행 기록 기준

1. 같은 문서 집합 위에서 여러 질문을 돌려 답변 상태를 비교합니다.
2. `근거 부족` 질문과 `답변 과장 위험` 질문을 각각 한 개씩 골라 다시 씁니다.
3. 다시 쓴 질문이 `근거 기반 답변`으로 바뀌는지 기록합니다.

## Python 예제

예제는 질문 재작성 전후를 바로 비교하는 것입니다. 코드가 길어 보이더라도 실제로는 P7-5.2의 평가 구조를 유지한 채, `expected_state`와 `rewritten_question` 비교만 하나 더 넣은 형태입니다.

- 문제 상황: 질문 문구를 바꾸며 RAG의 멈춤 규칙을 직접 시험한다.
- 입력: 문서 조각 6개, 연습 질문 6개
- 기대 출력: 질문별 상태 판정, 기대 상태와 실제 상태 비교, 재작성 결과
- 확인할 개념:
  - 문서에 없는 질문은 억지 답변보다 `근거 부족`으로 멈추는 편이 낫다
  - 강한 일반화 질문은 검색이 되어도 `답변 과장 위험`이 될 수 있다
  - 질문을 더 좁히거나 문서 표현에 맞추면 상태가 바뀔 수 있다

```python
# RAG 연습 질문을 재작성하기 전후로 근거 기반 답변 가능 상태와 상위 후보가 어떻게 바뀌는지 비교하는 예제입니다.
import csv
from pathlib import Path

document_path = Path("docs/assets/part-07/chapter-05/p7-5-rag-documents.csv")
case_path = Path("docs/assets/part-07/chapter-05/p7-5-boundary-cases.csv")

document_rows = list(csv.DictReader(document_path.open(encoding="utf-8")))
case_rows = list(csv.DictReader(case_path.open(encoding="utf-8")))
대표_문서_ids = {f"문서-{index}" for index in range(1, 7)}
대표_case_ids = {f"연습-{index:02d}" for index in range(1, 7)}
document_rows = [row for row in document_rows if row["doc_id"] in 대표_문서_ids]
case_rows = [row for row in case_rows if row["case_id"] in 대표_case_ids]
documents = {row["doc_id"]: row["text"] for row in document_rows}

rewrite_map = {
    "MCP는 왜 필요한가?": "최신 규칙이 필요한 서비스에서 검색 단계가 먼저 필요한 이유를 문서 범위 안에서 설명할 수 있는가?",
    "문서 분할 재정렬만 있으면 모든 환각이 해결되는가?": "문서 분할과 재정렬은 검색 품질에 어떤 도움을 줄 수 있는가?",
}

def clean_token(token):
    token = token.replace("?", "").replace(".", "")
    for keyword in ["RAG", "MCP"]:
        if token.startswith(keyword):
            return keyword
    return token

def tokenize(text):
    return {clean_token(token) for token in text.split()}

def evaluate_question(question):
    question_tokens = tokenize(question)
    ranked = []
    for doc_id, text in documents.items():
        overlap = len(question_tokens & tokenize(text))
        domain_bonus = sum(
            phrase in question and phrase in text
            for phrase in ["문서 분할", "재정렬", "검색 후보", "선택 근거", "최신 규칙"]
        )
        direct_bonus = 1 if overlap > 0 and ("기록" in text or "구분" in text or "질문에 더 직접 답하는" in text) else 0
        ranked.append({
            "doc_id": doc_id,
            "score": overlap + domain_bonus + direct_bonus,
            "overlap": overlap,
            "text": text,
        })
    ranked.sort(key=lambda row: (row["score"], row["overlap"]), reverse=True)
    top = ranked[0]

    if top["score"] == 0:
        state = "근거 부족"
        reason = "문서 범위 밖 질문"
    elif "모든" in question or "항상" in question:
        state = "답변 과장 위험"
        reason = "검색은 됐지만 단정 표현이 문서 근거를 넘어간다"
    else:
        state = "근거 기반 답변"
        reason = "현재 문서 범위 안에서 보수적으로 답할 수 있다"

    return {
        "question": question,
        "state": state,
        "reason": reason,
        "top_doc": top["doc_id"],
        "top_score": top["score"],
        "candidates": ranked[:3],
    }

exercise_records = []
for row in case_rows:
    before = evaluate_question(row["question"])
    rewritten_question = rewrite_map.get(row["question"])
    after = evaluate_question(rewritten_question) if rewritten_question else None
    expected_state = "근거 부족" if row["expected_state"] == "문서 범위 밖" else row["expected_state"]

    exercise_records.append({
        "case_id": row["case_id"],
        "focus": row["focus"],
        "expected_state": expected_state,
        "before": before,
        "rewritten_question": rewritten_question,
        "after": after,
    })

summary = {
    "연습 수": len(exercise_records),
    "기대 상태와 일치한 수": sum(
        record["before"]["state"] == record["expected_state"]
        for record in exercise_records
    ),
    "재작성으로 상태가 바뀐 수": sum(
        record["after"] is not None and record["after"]["state"] != record["before"]["state"]
        for record in exercise_records
    ),
    "다시 쓸 가치가 큰 질문": [
        record["case_id"]
        for record in exercise_records
        if record["before"]["state"] != "근거 기반 답변"
    ],
}

print("연습 요약 =", summary)
print("읽은 문서 파일 =", str(document_path))
print("읽은 연습 질문 파일 =", str(case_path))
핵심_case_ids = {"연습-02", "연습-03"}
print("핵심 연습 기록 =")
for row in exercise_records:
    if row["case_id"] in 핵심_case_ids:
        print(row)
```

실행 결과 예시는 다음과 같습니다.

```text
연습 요약 = {'연습 수': 6, '기대 상태와 일치한 수': 6, '재작성으로 상태가 바뀐 수': 2, '다시 쓸 가치가 큰 질문': ['연습-02', '연습-03', '연습-06']}
읽은 문서 파일 = docs/assets/part-07/chapter-05/p7-5-rag-documents.csv
읽은 연습 질문 파일 = docs/assets/part-07/chapter-05/p7-5-boundary-cases.csv
핵심 연습 기록 =
{'case_id': '연습-02', 'focus': '현재 문서 집합에 없는 주제를 멈추는 경우', 'expected_state': '근거 부족', 'before': {'question': 'MCP는 왜 필요한가?', 'state': '근거 부족', 'reason': '문서 범위 밖 질문', 'top_doc': '문서-1', 'top_score': 0, 'candidates': [{'doc_id': '문서-1', 'score': 0, 'overlap': 0, 'text': 'RAG는 외부 문서를 검색해 모델 입력에 넣고 그 근거 위에서 답변을 구성하는 구조다.'}, {'doc_id': '문서-2', 'score': 0, 'overlap': 0, 'text': '프롬프트만으로는 최신 문서 근거를 보장할 수 없으므로 최신 규칙이 필요한 서비스에서는 검색 단계가 먼저 필요하다.'}, {'doc_id': '문서-3', 'score': 0, 'overlap': 0, 'text': '검색 후보 점수가 높아도 질문에 직접 답하지 않는 문장이 섞일 수 있으므로 선택 근거를 따로 남겨야 한다.'}]}, 'rewritten_question': '최신 규칙이 필요한 서비스에서 검색 단계가 먼저 필요한 이유를 문서 범위 안에서 설명할 수 있는가?', 'after': {'question': '최신 규칙이 필요한 서비스에서 검색 단계가 먼저 필요한 이유를 문서 범위 안에서 설명할 수 있는가?', 'state': '근거 기반 답변', 'reason': '현재 문서 범위 안에서 보수적으로 답할 수 있다', 'top_doc': '문서-2', 'top_score': 9, 'candidates': [{'doc_id': '문서-2', 'score': 9, 'overlap': 8, 'text': '프롬프트만으로는 최신 문서 근거를 보장할 수 없으므로 최신 규칙이 필요한 서비스에서는 검색 단계가 먼저 필요하다.'}, {'doc_id': '문서-5', 'score': 3, 'overlap': 3, 'text': '문서 분할 chunking 은 검색 범위를 세밀하게 만들지만 너무 잘게 나누면 문맥이 끊길 수 있다.'}, {'doc_id': '문서-4', 'score': 3, 'overlap': 2, 'text': 'RAG 프로젝트 기록에는 질문 검색 후보 선택 근거 최종 답변을 분리해 남겨야 검색 실패와 답변 실패를 나중에 구분할 수 있다.'}]}}
{'case_id': '연습-03', 'focus': '검색은 됐지만 단정이 근거 밖인 경우', 'expected_state': '답변 과장 위험', 'before': {'question': '문서 분할 재정렬만 있으면 모든 환각이 해결되는가?', 'state': '답변 과장 위험', 'reason': '검색은 됐지만 단정 표현이 문서 근거를 넘어간다', 'top_doc': '문서-5', 'top_score': 3, 'candidates': [{'doc_id': '문서-5', 'score': 3, 'overlap': 2, 'text': '문서 분할 chunking 은 검색 범위를 세밀하게 만들지만 너무 잘게 나누면 문맥이 끊길 수 있다.'}, {'doc_id': '문서-2', 'score': 1, 'overlap': 1, 'text': '프롬프트만으로는 최신 문서 근거를 보장할 수 없으므로 최신 규칙이 필요한 서비스에서는 검색 단계가 먼저 필요하다.'}, {'doc_id': '문서-6', 'score': 1, 'overlap': 0, 'text': '재정렬 reranking 은 상위 후보의 순서를 다시 바꾸어 질문에 더 직접 답하는 근거를 앞으로 당기는 단계다.'}]}, 'rewritten_question': '문서 분할과 재정렬은 검색 품질에 어떤 도움을 줄 수 있는가?', 'after': {'question': '문서 분할과 재정렬은 검색 품질에 어떤 도움을 줄 수 있는가?', 'state': '근거 기반 답변', 'reason': '현재 문서 범위 안에서 보수적으로 답할 수 있다', 'top_doc': '문서-5', 'top_score': 4, 'candidates': [{'doc_id': '문서-5', 'score': 4, 'overlap': 3, 'text': '문서 분할 chunking 은 검색 범위를 세밀하게 만들지만 너무 잘게 나누면 문맥이 끊길 수 있다.'}, {'doc_id': '문서-2', 'score': 3, 'overlap': 3, 'text': '프롬프트만으로는 최신 문서 근거를 보장할 수 없으므로 최신 규칙이 필요한 서비스에서는 검색 단계가 먼저 필요하다.'}, {'doc_id': '문서-4', 'score': 3, 'overlap': 2, 'text': 'RAG 프로젝트 기록에는 질문 검색 후보 선택 근거 최종 답변을 분리해 남겨야 검색 실패와 답변 실패를 나중에 구분할 수 있다.'}]}}
```

## 결과를 어떻게 읽는가

이번 연습의 핵심은 `검색기가 좋아졌다`가 아니라 `질문을 다시 썼더니 상태가 바뀌었다`는 점입니다.

| 질문 | 재작성 전 | 재작성 후 | 읽어야 할 점 |
| --- | --- | --- | --- |
| `MCP는 왜 필요한가?` | 근거 부족 | 근거 기반 답변 | 문서 범위 밖 질문을 문서 표현에 맞추면 답할 수 있는 질문이 된다 |
| `문서 분할 재정렬만 있으면 모든 환각이 해결되는가?` | 답변 과장 위험 | 근거 기반 답변 | 강한 일반화 표현을 걷어내면 보수적 답변이 가능해진다 |

이 차이를 통해 독자는 두 가지를 잡아야 합니다.

- `근거 부족`은 문서에 없는 것을 억지로 답하지 않는 상태입니다.
- `답변 과장 위험`은 문서는 있지만 질문의 강도가 문서 근거보다 더 센 상태입니다.

즉, 둘 다 `멈춤`이 필요할 수 있지만, 다음 수정 방향은 서로 다릅니다.

- `근거 부족`: 문서 추가, 질문 범위 축소, 범위 밖 안내가 필요합니다.
- `답변 과장 위험`: 질문 표현 완화, 답변 단정도 조절, 근거 문장 재선택이 필요합니다.

## 결과 해석 기준

- 같은 주제라도 질문 강도를 낮추면 상태가 어떻게 바뀌는가?
- 문서 표현과 가까운 질문은 어떤 문서를 더 쉽게 상위 후보로 끌어오는가?
- `항상`, `모든` 같은 단어가 들어가면 왜 과장 위험이 늘어나는가?
- 재작성 뒤에도 여전히 `근거 부족`으로 남는 질문은 무엇인가?

## 프로젝트 기록 예시

실습 뒤에는 다음 형식으로 짧게 기록해 두는 편이 좋습니다.

| 항목 | 적을 내용 |
| --- | --- |
| 원래 질문 | 왜 멈춤이 필요했는가 |
| 원래 상태 | 근거 부족 / 답변 과장 위험 |
| 다시 쓴 질문 | 무엇을 줄이거나 좁혔는가 |
| 바뀐 상태 | 근거 기반 답변으로 바뀌었는가 |
| 다음 질문 | 문서를 늘릴지, 질문을 더 고칠지 |

한 문단으로 쓰면 예를 들어 다음처럼 정리할 수 있습니다.

> `문서 분할 재정렬만 있으면 모든 환각이 해결되는가?`는 검색 후보는 있었지만 `모든`이라는 표현이 문서 근거보다 더 강해 `답변 과장 위험`으로 남았다. 같은 주제를 `문서 분할과 재정렬은 검색 품질에 어떤 도움을 줄 수 있는가?`로 다시 쓰자, 같은 문서 집합 안에서도 `근거 기반 답변` 상태로 바뀌었다. 따라서 다음 반복에서는 강한 일반화 질문을 그대로 답하기보다, 문서 범위에 맞는 질문으로 다시 쓰거나 답변 강도를 낮추는 규칙을 먼저 붙이는 편이 적절하다.

## 직접 바꿔 보며 확인할 것

1. `항상`, `모든`, `완전히` 같은 표현을 연습 질문에 하나씩 넣어 봅니다.
   관찰할 점: 검색 점수는 비슷해도 답변 상태가 `답변 과장 위험`으로 더 자주 이동하는가?

2. `MCP는 왜 필요한가?`를 다른 방식으로 다시 써 봅니다.
   관찰할 점: 질문을 문서 범위 안으로 옮기면 어떤 문서가 상위 후보로 올라오는가?

3. 연습 파일에 문서에 전혀 없는 새 질문을 하나 더 추가해 봅니다.
   관찰할 점: `근거 부족` 상태를 안전하게 유지하는 것이 왜 실패가 아니라 정상 동작인지 설명할 수 있는가?

판단 기준은 질문을 다시 쓰면 항상 답할 수 있는가가 아닙니다. 문서 표현과 어긋난 질문은 재작성으로 줄일 수 있지만, 문서 집합에 근거가 전혀 없는 질문은 문서를 늘리거나 `근거 부족`으로 멈추는 편이 더 안전합니다.

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| 원래 질문 | 문서 범위 밖 질문과 과장 질문을 구분해 기록했는가? |
| 재작성 | 질문 재작성 전후의 상태 변화를 남겼는가? |
| 상태 구분 | `근거 부족`과 `답변 과장 위험`의 다음 수정 방향을 따로 적었는가? |
| 멈춤 규칙 | 억지 답변보다 멈춤 규칙이 더 안전한 경우를 설명했는가? |
| 다음 질문 | 문서를 늘릴지, 질문을 더 고칠지 선택했는가? |

## 출처와 참고 자료

- 문서 집합: [`p7-5-rag-documents.csv`](../../../assets/part-07/chapter-05/p7-5-rag-documents.csv){ .csv-preview }
- 경계 사례 질문: [`p7-5-boundary-cases.csv`](../../../assets/part-07/chapter-05/p7-5-boundary-cases.csv){ .csv-preview }
- 이 문서는 자체 실습 예시를 사용했습니다. 외부 자료를 직접 인용하지 않았습니다.
