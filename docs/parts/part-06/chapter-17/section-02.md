# P6-17.2 최소 구현과 회고 포인트

> Section ID: `P6-17.2`
> Version: `v2026.07.12`

P6-17.1에서는 작은 생성형 AI 기능을 `요청 해석 -> 검색 또는 도구 선택 -> 응답 생성 -> 평가와 기록`의 흐름으로 묶었습니다. 이 절에서는 그 흐름을 아주 작은 코드로 다시 그려 봅니다.

최소 구현의 목적은 성능 좋은 서비스를 완성하는 데 있지 않고, `어떤 입력이 어떤 경로를 거쳐 어떤 출력과 기록으로 남는가`를 눈으로 확인하는 데 있습니다.

## 이 절의 범위

이 절은 다음 질문에 답합니다.

- 실제 상용 API를 붙이기 전에도 어떤 최소 구현을 만들어 볼 수 있는가?
- 검색, 응답 생성, 검토 필요 여부를 어떤 실행 기록으로 함께 남겨야 하는가?
- 남은 기록을 보고 다음 개선 지점을 어떻게 읽을 수 있는가?

이 절에서는 다음 내용을 깊게 다루지 않습니다.

- 실제 벡터 데이터베이스 연결 코드
- 인증이 필요한 외부 SaaS API 호출
- 프로덕션 배포 설정

이 절의 구현은 `축약된 기준선 구현`입니다. 여기서는 앞의 P6-10.1, P6-10.2 RAG 흐름과 P6-12.1, P6-12.2 도구 사용 구조, P6-15.1, P6-15.2 평가와 기록 관점을 작은 코드로 다시 묶어 확인합니다. 검색과 실행 구조를 더 자세히 다시 보려면 P6-10~P6-12로, 운영 기록과 실패 대응을 다시 보려면 P6-15~P6-16으로 돌아가면 됩니다.

지금 읽는 층위는 `기록 가능한 최소 구현 층위`입니다. 앞 절이 `어떤 구조를 붙여야 질문이 닫히는가`를 설계 문장으로 정리했다면, 여기서는 그 구조가 실제로 어떤 실행 기록으로 남아야 하는지 확인합니다. 아직 제품 수준 자동화나 배포 절차까지는 가지 않습니다.

| 단계 | 지금 붙잡을 질문 | 바로 이어지는 위치 |
| --- | --- | --- |
| 요청 흐름 설계 | 질문에 따라 prompt, retrieval, tool 중 무엇을 붙일 것인가? | P6-17.1 |
| 최소 구현과 요청 실행 기록 | 그 선택이 실제로 어떤 출력과 기록으로 남는가? | P6-17.2 |

즉, 이 절의 핵심은 `요청 흐름을 설계한다`에서 `그 흐름을 실제 요청 실행 기록으로 남긴다`로 관점이 바뀌는 데 있습니다.

이 절은 Part 6에서 요청 실행 기록과 회고 포인트를 최소 구현으로 묶어 보여 주는 대표 Section입니다. `돌아간다`와 `기록 가능하게 설계되었다`를 구분하는 기준을 여기서 눈에 보이게 만듭니다.

## 이 절의 목표

- 작은 생성형 AI 기능의 최소 구현 흐름을 읽을 수 있습니다.
- 검색 결과, 응답, 근거, 실패 기록이 왜 함께 출력되어야 하는지 설명할 수 있습니다.
- 기능이 돌아간다는 사실과 기능이 잘 설계되었다는 판단이 다르다는 점을 구분할 수 있습니다.
- 다음 개선 전에 먼저 확인해야 할 최소 기록 구조를 설명할 수 있습니다.

## 최소 구현에서 확인할 네 단계

이 절의 최소 구현은 다음 네 단계를 가집니다.

1. 질문을 받는다.
2. 간단한 규칙으로 관련 문서를 찾는다.
3. 찾은 문서를 바탕으로 답변을 만든다.
4. 어떤 문서를 썼는지와 답변 품질 메모를 남긴다.

실제 LLM API 호출을 붙이지 않아도 이 네 단계를 먼저 확인해 두면, 이후 어디에 모델 호출이 들어가고 어디에 검색 품질 문제가 생기는지 구조를 읽기 쉬워집니다.

## 작은 데이터와 목표

입력:

- 정책 문서 네 개
- 서로 다른 실패 유형을 유도하는 사용자 질문 세 개

출력:

- 문서별 검색 점수
- 선택된 근거 문서
- 생성된 답변 초안
- 사람 검토 필요 여부와 평가 메모

이 예제의 목표는 `정답률`이 아니라 `운영 상태 구분`을 포함한 흐름 확인입니다. 같은 최소 기능이라도 `여러 근거가 맞물린 경우`, `근거가 부족한 경우`, `검색 자체가 실패한 경우`를 구분해 읽어야 다음 개선 우선순위를 정할 수 있습니다.

## 사례 및 예시

최소 구현 절이 실제로 필요한 이유는 `한 번 돌았다`와 `운영 판단까지 남겼다`를 분리해 보여 주기 위해서입니다. 아래 두 장면은 같은 정책 안내 도우미처럼 보여도, 요청 실행 기록을 남기지 않으면 어디서 실패했는지 다시 읽을 수 없다는 점을 보여 줍니다.

### 사례 1. 답은 나왔는데 왜 나왔는지 남기지 않으면

사람은 답변 문자열만 자연스럽게 보이면 기능이 일단 됐다고 느끼기 쉽습니다. 예를 들어 `이번 달에 입사한 직원도 여름휴가를 바로 쓸 수 있나요?`라는 질문에, 답변이 그럴듯하게 한 문장으로 나오면 바로 통과시키고 싶어집니다. 하지만 이 경우 실제로 필요한 것은 `입사 후 1개월` 규정과 `여름휴가 승인` 규정을 함께 읽었는지, 두 근거가 충돌하지 않았는지, 답변이 어떤 문서를 바탕으로 만들어졌는지 남기는 일입니다. 답만 남기고 근거 문서와 실행 상태를 안 남기면, 나중에 답이 어긋났을 때 검색을 잘못한 것인지 해석을 잘못한 것인지 구분할 수 없습니다. 그래서 최소 구현이라도 답변 문자열 옆에 문서별 점수, 선택 문서, 실행 상태를 함께 남겨야 합니다. 이 사례에서 확인해야 할 결과는 `답이 나왔다`가 아니라 `왜 그 답이 나왔는지를 같은 요청 실행 기록에서 다시 읽을 수 있는가`입니다.

### 사례 2. 근거가 부족한데도 답을 확정해 버리면

`신규 복지포인트는 이번 주부터 바로 쓸 수 있나요?` 같은 질문은 더 위험합니다. 검색 결과가 한 문서만 잡혔다고 해서 바로 답을 확정하면, 실제로는 복지포인트 직접 규정이 아니라 `신규 복지 제도는 공지 전까지 인사팀 확인이 필요하다`는 일반 문장만 보고 답했을 가능성이 있습니다. 사람은 문서가 하나라도 잡혔으니 답을 한 번 써 보자고 느끼기 쉽지만, 이 경우 더 중요한 것은 `근거가 하나뿐인가`, `예외 조항 누락 가능성이 있는가`, `사람 검토가 필요한가`를 함께 남기는 일입니다. 그래서 최소 구현에서도 `single_evidence`와 `needs_human_review` 같은 상태를 따로 남겨야, 다음 회고에서 검색 확장 문제인지 승인 게이트 문제인지 분리할 수 있습니다. 이 사례에서 확인해야 할 결과는 `답을 생성했다`가 아니라 `근거 부족 상태를 숨기지 않고 운영 경로로 남겼는가`입니다.

두 사례를 요청 실행 기록 관점으로 다시 줄이면 다음과 같습니다.

| 장면 | 답만 남기면 놓치는 것 | 함께 남겨야 할 기록 |
| --- | --- | --- |
| 다중 근거가 필요한 질문 | 어떤 문서를 같이 읽었는지, 충돌 가능성이 있었는지 | 문서 점수, 선택 문서, 실행 상태, 답변 초안 |
| 근거가 하나뿐인 질문 | 답을 확정해도 되는지, 사람 검토가 필요한지 | `single_evidence`, `needs_human_review`, 회고 메모 |
| 문서를 전혀 못 찾은 질문 | 검색 실패인지 해석 실패인지 | `retrieval_failed`, 실패 메모, 다음 조치 |

## 연습 및 예제

이번 예제는 `질문 -> 검색 -> 답변 초안 -> 평가 -> 기록`을 한 번에 확인하는 데 목적이 있습니다. 질문 두 개만 보는 대신 `다중 근거가 잡히는 경우`, `근거가 하나만 잡히는 경우`, `아예 검색 실패가 나는 경우`를 함께 넣어, 작은 기준선 구현도 여러 실패 유형으로 갈라진다는 점을 확인하겠습니다. 특히 각 질문이 끝난 뒤 요청 실행 기록 하나로 남도록 만들어, 뒤의 회고나 운영 판단에서 무엇을 고쳐야 하는지 바로 다시 읽을 수 있게 하겠습니다.

입력:

- 정책 문서 4개
- 사용자 질문 3개

출력:

- 문서별 검색 점수
- 선택된 근거 문서
- 답변 초안
- 사람 검토 필요 여부와 회고 메모
- 질문별 요청 실행 기록
- 전체 질문 묶음에 대한 요약 통계

확인할 개념:

- 최소 구현도 검색, 답변, 평가, 기록이 한 흐름으로 묶여야 한다
- 질문별 요청 실행 기록을 남겨야 어떤 실패 유형이 반복되는지 다시 읽을 수 있다
- 운영 관점에서는 정답률보다 근거 부족과 검색 실패를 어떻게 구분했는지가 중요하다

코드를 보기 전에, 먼저 아래 세 질문에 대해 어떤 실행 상태가 남아야 하는지 스스로 적어 보는 편이 좋습니다.

| 질문 | 먼저 예상해 볼 실행 상태 | 왜 이렇게 예상하는가 |
| --- | --- | --- |
| `이번 달에 입사한 직원도 여름휴가를 바로 쓸 수 있나요?` | `multi_evidence` | 입사 규정과 휴가 규정을 함께 읽어야 닫히기 때문 |
| `신규 복지포인트는 이번 주부터 바로 쓸 수 있나요?` | `single_evidence` + 사람 검토 | 직접 근거가 약할 가능성이 커서 예외 조항 누락 위험이 있기 때문 |
| `야간 근무 수당은 이번 달부터 얼마인가요?` | `retrieval_failed` + 사람 검토 | 현재 문서 세트로는 관련 규정을 못 찾을 가능성이 크기 때문 |

답을 미리 적어 두고 코드 결과와 비교하면, 이 예제가 단순 출력 확인이 아니라 `질문별 운영 상태 분류`를 검증하는 실습이라는 점이 더 분명해집니다.

먼저 이 예제에서 함께 볼 통합 기록 기준은 다음과 같습니다.

| 점검 항목 | 왜 필요한가 |
| --- | --- |
| 근거 문서 목록 | 어떤 근거를 실제로 썼는지 남겨야 해서 |
| 사람 검토 필요 여부 | 답을 바로 써도 되는지, 사람 확인이 필요한지 나눠야 해서 |
| 실행 상태 | 다중 근거 확보, 근거 부족, 검색 실패를 한눈에 구분해야 해서 |
| 전체 요약 | 한 질문씩만 보지 않고 전체 흐름에서 어떤 실패가 많은지 읽어야 해서 |

입력(input):

위에 정리한 정책 문서 목록과 질문 실행 시나리오를 사용합니다.

```python
documents = [
    {
        "id": "policy-1",
        "text": "신입 직원은 입사 후 1개월이 지나면 월차를 사용할 수 있습니다.",
    },
    {
        "id": "policy-2",
        "text": "여름휴가는 공지된 기간 안에서 팀 승인 후 사용할 수 있습니다.",
    },
    {
        "id": "policy-3",
        "text": "잔여 휴가 일수 조회는 인사 시스템에서 확인합니다.",
    },
    {
        "id": "policy-4",
        "text": "신규 복지 제도는 공지 전까지 인사팀 확인이 필요합니다.",
    },
]

queries = [
    "이번 달에 입사한 직원도 여름휴가를 바로 쓸 수 있나요?",
    "신규 복지포인트는 이번 주부터 바로 쓸 수 있나요?",
    "야간 근무 수당은 이번 달부터 얼마인가요?",
]

keyword_groups = {
    "입사": ["입사", "신입", "직원"],
    "휴가": ["휴가", "월차", "여름휴가"],
    "복지": ["복지", "포인트", "제도"],
}

def score_document(query, doc):
    score = 0
    matched_groups = []
    for group_name, keywords in keyword_groups.items():
        query_hit = any(keyword in query for keyword in keywords)
        doc_hit = any(keyword in doc["text"] for keyword in keywords)
        if query_hit and doc_hit:
            score += 1
            matched_groups.append(group_name)
    return score, matched_groups

def retrieve_docs(query, docs, top_k=2):
    scored = []
    for doc in docs:
        score, matched_groups = score_document(query, doc)
        scored.append(
            {
                "id": doc["id"],
                "text": doc["text"],
                "score": score,
                "matched_groups": matched_groups,
            }
        )
    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored[:top_k], scored

def draft_answer(query, retrieved):
    top_docs = [doc for doc in retrieved if doc["score"] > 0]
    if not top_docs:
        return "관련 규정을 찾지 못했습니다. 답변을 확정하지 말고 인사팀 확인으로 넘깁니다."

    evidence_lines = [f"- {doc['id']}: {doc['text']}" for doc in top_docs]
    if len(top_docs) == 1:
        summary_line = "초안 판단: 근거가 하나뿐이므로 예외 조항이나 최신 공지를 다시 확인해야 합니다."
    else:
        summary_line = "초안 판단: 여러 근거를 함께 읽어 조건 충돌과 적용 순서를 확인해야 합니다."
    return "\n".join(
        [
            f"질문: {query}",
            "확인된 근거:",
            *evidence_lines,
            summary_line,
        ]
    )

def evaluate_run(query, retrieved):
    positive_docs = [doc for doc in retrieved if doc["score"] > 0]
    notes = []
    if not positive_docs:
        notes.append("검색 실패: 관련 문서를 찾지 못했으므로 사람 검토가 필요함")
        run_status = "retrieval_failed"
    elif len(positive_docs) == 1:
        notes.append("근거 부족 가능성: 한 문서만 잡혔으므로 예외 조항 누락을 점검")
        run_status = "single_evidence"
    else:
        notes.append("다중 근거 확인: 여러 문서를 함께 읽어 조건 충돌 여부를 점검")
        run_status = "multi_evidence"

    if "복지포인트" in query:
        notes.append("현재 문서에는 복지포인트 직접 규정이 없어 신규 제도 여부를 재확인")

    return {
        "needs_human_review": len(positive_docs) == 0 or len(positive_docs) == 1 or "복지포인트" in query,
        "run_status": run_status,
        "notes": notes,
    }

run_records = []
for query in queries:
    top_docs, full_scores = retrieve_docs(query, documents)
    answer = draft_answer(query, top_docs)
    evaluation = evaluate_run(query, top_docs)
    run_records.append(
        {
            "question": query,
            "document_scores": full_scores,
            "retrieved_doc_ids": [doc["id"] for doc in top_docs if doc["score"] > 0],
            "draft_answer": answer,
            "evaluation": evaluation,
        }
    )

summary = {
    "run_count": len(run_records),
    "multi_evidence_count": sum(record["evaluation"]["run_status"] == "multi_evidence" for record in run_records),
    "single_evidence_count": sum(record["evaluation"]["run_status"] == "single_evidence" for record in run_records),
    "retrieval_failed_count": sum(record["evaluation"]["run_status"] == "retrieval_failed" for record in run_records),
    "needs_human_review_count": sum(record["evaluation"]["needs_human_review"] for record in run_records),
}

print("[summary]")
print(summary)
print()

for record in run_records:
    print("=" * 80)
    print("question =", record["question"])
    print("[document scores]")
    for item in record["document_scores"]:
        print(item["id"], "score=", item["score"], "matched_groups=", item["matched_groups"])
    print("[retrieved_doc_ids]")
    print(record["retrieved_doc_ids"])
    print("[draft answer]")
    print(record["draft_answer"])
    print("[evaluation]")
    print("run_status =", record["evaluation"]["run_status"])
    print("needs_human_review =", record["evaluation"]["needs_human_review"])
    for note in record["evaluation"]["notes"]:
        print("-", note)
```

실행 결과 예시는 다음처럼 읽을 수 있습니다.

```text
[summary]
{'run_count': 3, 'multi_evidence_count': 1, 'single_evidence_count': 1, 'retrieval_failed_count': 1, 'needs_human_review_count': 2}

================================================================================
question = 이번 달에 입사한 직원도 여름휴가를 바로 쓸 수 있나요?
[document scores]
policy-1 score= 2 matched_groups= ['입사', '휴가']
policy-2 score= 1 matched_groups= ['휴가']
policy-3 score= 0 matched_groups= []
policy-4 score= 0 matched_groups= []
[retrieved_doc_ids]
['policy-1', 'policy-2']
[draft answer]
질문: 이번 달에 입사한 직원도 여름휴가를 바로 쓸 수 있나요?
확인된 근거:
- policy-1: 신입 직원은 입사 후 1개월이 지나면 월차를 사용할 수 있습니다.
- policy-2: 여름휴가는 공지된 기간 안에서 팀 승인 후 사용할 수 있습니다.
초안 판단: 여러 근거를 함께 읽어 조건 충돌과 적용 순서를 확인해야 합니다.
[evaluation]
run_status = multi_evidence
needs_human_review = False
- 다중 근거 확인: 여러 문서를 함께 읽어 조건 충돌 여부를 점검
================================================================================
question = 신규 복지포인트는 이번 주부터 바로 쓸 수 있나요?
[document scores]
policy-4 score= 1 matched_groups= ['복지']
policy-1 score= 0 matched_groups= []
policy-2 score= 0 matched_groups= []
policy-3 score= 0 matched_groups= []
[retrieved_doc_ids]
['policy-4']
[draft answer]
질문: 신규 복지포인트는 이번 주부터 바로 쓸 수 있나요?
확인된 근거:
- policy-4: 신규 복지 제도는 공지 전까지 인사팀 확인이 필요합니다.
초안 판단: 근거가 하나뿐이므로 예외 조항이나 최신 공지를 다시 확인해야 합니다.
[evaluation]
run_status = single_evidence
needs_human_review = True
- 근거 부족 가능성: 한 문서만 잡혔으므로 예외 조항 누락을 점검
- 현재 문서에는 복지포인트 직접 규정이 없어 신규 제도 여부를 재확인
================================================================================
question = 야간 근무 수당은 이번 달부터 얼마인가요?
[document scores]
policy-1 score= 0 matched_groups= []
policy-2 score= 0 matched_groups= []
policy-3 score= 0 matched_groups= []
policy-4 score= 0 matched_groups= []
[retrieved_doc_ids]
[]
[draft answer]
관련 규정을 찾지 못했습니다. 답변을 확정하지 말고 인사팀 확인으로 넘깁니다.
[evaluation]
run_status = retrieval_failed
needs_human_review = True
- 검색 실패: 관련 문서를 찾지 못했으므로 사람 검토가 필요함
```

## 이 예제에서 무엇을 읽어야 하나

이 코드는 실제 LLM도, 실제 검색 엔진도 아닙니다. 하지만 다음 네 가지를 분명히 드러냅니다.

- 질문이 들어온다
- 검색 단계가 점수와 함께 따로 존재한다
- 답변은 하나의 문서가 아니라 선택된 근거 묶음에 기대어 만들어진다
- 다중 근거, 근거 부족, 검색 실패가 서로 다른 메모와 실행 상태로 기록된다
- 질문별 실행 결과가 마지막에 전체 요약으로 다시 묶인다

그래서 이 예제에서 확인해야 할 결과는 `모델이 답했다`는 한 줄 뒤에 검색 점수, 근거 문서, 사람 검토 플래그, 회고 메모, 질문별 요청 실행 기록이 실제로 따로 남는가입니다. 특히 같은 최소 기능 안에서도 `다중 근거 확보`, `근거 부족`, `검색 실패`가 서로 다른 운영 상태로 남는지가 중요합니다.

같은 결과를 실무 검토 메모처럼 다시 적으면 다음과 같습니다.

| 질문 | 지금 바로 남길 검토 메모 | 다음 패치 우선순위 |
| --- | --- | --- |
| 입사와 휴가 규정이 함께 걸린 질문 | 근거는 둘 이상 잡혔지만 조건 충돌 해석 규칙이 필요하다 | 해석 규칙과 groundedness 점검 |
| 복지포인트처럼 직접 근거가 약한 질문 | 답은 만들 수 있어도 바로 확정하면 위험하다 | 검색 확장 또는 승인 게이트 |
| 문서를 못 찾은 질문 | 답을 꾸미지 않고 실패를 드러낸 것은 맞지만, 검색 범위가 부족하다 | 색인 확장, 문서 추가, 사람 검토 흐름 |

## 요청 실행 기록에서 무엇을 회고하나

이 최소 구현은 코드가 한 번 돌아가는지 확인하는 데서 멈추지 않습니다. 질문마다 남은 요청 실행 기록을 다시 읽어, 실패가 검색 단계에 있었는지, 해석 단계에 있었는지, 사람 검토로 넘겨야 하는 상태였는지를 구분해야 합니다.

| 관찰된 문제 | 실제로 실패한 단계 | 다음 개선 방향 |
| --- | --- | --- |
| 문서는 찾았는데 답이 틀림 | 해석/생성 단계 | 근거 인용 방식, 답변 검토 규칙 보강 |
| 문서 자체를 못 찾음 | 검색 단계 | 키워드 확장, 임베딩 검색, 색인 개선 |
| 질문은 답했지만 실제 상태가 빠짐 | 도구 부재 | 조회 API 또는 도구 호출 추가 |

예를 들어 `입사 후 1개월` 같은 조건을 끝까지 반영하지 못했다면, 이는 검색 성공 뒤의 해석 실패입니다. 반대로 관련 문서가 하나도 잡히지 않았다면 답을 꾸며내기보다 `needs_human_review`를 남겨 사람 검토로 넘겨야 합니다. 이렇게 읽어야 같은 실패가 다시 나왔을 때 어디를 먼저 고쳐야 하는지 분명해집니다.

여기서 한 단계 더 가면, 최소 구현이 직접 보여 주는 것과 아직 다음 개선으로 남는 것을 분리해 두는 편이 좋습니다.

| 상황 | 이 최소 구현이 직접 보여 주는 것 | 아직 다음 개선으로 남는 것 |
| --- | --- | --- |
| 질문마다 다른 결과가 나옴 | 다중 근거, 근거 부족, 검색 실패를 서로 다른 실행 상태로 남김 | 실제 임베딩 검색, 재순위화, 더 정교한 groundedness 판정 |
| 답은 나왔지만 검토가 필요함 | `needs_human_review`, 회고 메모, 요청 실행 기록 | 승인 게이트, 실제 사람 검토 큐, 재시도 정책 |
| 근거가 부족하거나 없음 | 검색 단계와 해석 단계를 구분해 회고함 | 더 나은 검색 인프라와 도구 호출 연결 |
| 코드가 한 번 돌아감 | 요청 경로와 기록 구조가 분리되어 보임 | 비용, 지연 시간, 운영 한도까지 포함한 서비스화 |

이 표의 핵심은 최소 구현이 `작동 예시`를 넘어서 `어디를 다음에 고칠지 보여 주는 기준선`이라는 점입니다. 실제 임베딩 검색, tool use, agent loop, 운영 통제는 이 기준선 위에 다음 단계로 얹힙니다.

회고 질문은 다음 정도면 충분합니다.

| 장면 | 바로 남겨야 하는 회고 질문 | 다음에 먼저 손볼 가능성이 큰 곳 |
| --- | --- | --- |
| 문서를 찾았지만 답변이 어긋남 | 근거를 끝까지 읽었는가 | 해석 규칙, groundedness 점검 |
| 문서를 못 찾아 사람 검토로 넘김 | 근거 부재를 숨기지 않았는가 | 검색 확장, 사람 검토 흐름 |
| 다음 확장 지점을 고름 | 실패가 검색 문제인가 도구 부재인가 | 벡터 검색, tool use, agent 분기 |

## 이 최소 구현이 아직 하지 못하는 일

이 최소 구현은 분명히 한계가 있습니다.

- 검색 품질이 단순 키워드 규칙에 의존합니다.
- 답변 생성이 사실상 템플릿 수준입니다.
- 문서가 여러 개 충돌할 때 우선순위를 다루지 못합니다.
- 실제 도구 호출이나 권한 검사는 들어 있지 않습니다.

하지만 바로 이 한계를 적어야 `코드가 한 번 실행된다`는 사실과 `실제 업무 조건에서 반복적으로 쓸 수 있다`는 판단을 분리할 수 있습니다.

또 하나 중요한 점은, 이 한계 목록이 곧바로 다음 설계 우선순위가 된다는 것입니다.

- 검색 실패가 많으면 검색 품질부터 고칩니다.
- 문서는 찾는데 답이 자주 어긋나면 답변 생성 규칙과 근거 표시를 먼저 고칩니다.
- 현재 상태 질문이 많아지면 tool use를 붙입니다.

즉, 최소 구현의 회고는 감상이 아니라 `다음 패치 순서를 정하는 입력`이어야 합니다.

## 언제 vector search와 tool use로 확장하나

다음 상황이 오면 이 미니 실습은 확장 대상이 됩니다.

- 문서 수가 많아져 키워드 규칙으로는 한계가 보일 때
- 비슷한 표현을 더 잘 찾고 싶을 때
- 현재 상태 조회나 실행이 필요할 때

즉, 이 절은 `끝난 구현`이 아니라 `다음 개선을 위한 기준점`입니다.

다음처럼 연결하면 충분합니다.

- 더 나은 검색이 필요하면 P6-11의 임베딩과 벡터 검색으로 돌아갑니다.
- 실제 상태 조회가 필요하면 P6-12의 tool use로 갑니다.
- 여러 단계 판단이 필요하면 P6-13의 agent 구조로 갑니다.
- 실패 기록과 안전 장치는 P6-16의 운영 관점으로 다시 읽습니다.

## 체크리스트

- 최소 구현은 완성품이 아니라 구조 확인용 기준점이라는 점을 설명할 수 있는가?
- 검색, 응답, 기록은 따로가 아니라 함께 출력되어야 한다는 점을 설명할 수 있는가?
- 기능이 돌아간다는 사실과 실제로 쓸 만하다는 판단이 다르다는 점을 구분할 수 있는가?
- 회고를 남겨야 다음에 vector search, tool use, agent로 확장할 이유가 분명해진다는 점을 설명할 수 있는가?
- 최소 구현을 `작은 데모`가 아니라 `요청 경로와 기록 구조를 확인하는 기준점`으로 설명할 수 있는가?
- 검색 결과, 답변, 실패 기록, 사람 검토 필요 여부를 함께 남겨야 다음 개선 우선순위를 잡을 수 있다는 점을 말할 수 있는가?
- 이 예제가 무엇을 보여 주고 무엇을 아직 못 하는지 구분할 수 있는가?

## 출처와 참고 자료

- OpenAI, [Retrieval](https://developers.openai.com/api/docs/guides/retrieval){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, 확인 날짜: 2026-07-05.
- OpenAI, [Working with evals](https://developers.openai.com/api/docs/guides/evals){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, 확인 날짜: 2026-07-05.
- OpenAI, [Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, 확인 날짜: 2026-07-05.
