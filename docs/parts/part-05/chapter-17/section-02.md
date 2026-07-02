# P5-17.2 최소 구현과 회고 포인트

P5-17.1에서는 작은 생성형 AI 기능을 `요청 해석 -> 검색 또는 도구 선택 -> 응답 생성 -> 평가와 기록`의 흐름으로 묶었습니다. 이 절에서는 그 흐름을 아주 작은 코드로 다시 그려 봅니다.

최소 구현의 목적은 성능 좋은 서비스를 완성하는 데 있지 않고, `어떤 입력이 어떤 경로를 거쳐 어떤 출력과 기록으로 남는가`를 눈으로 확인하는 데 있습니다.

## 이 절의 범위

이 절은 다음 질문에 답합니다.

- 실제 상용 API를 붙이기 전에도 어떤 최소 구현을 만들어 볼 수 있는가?
- 검색, 응답 생성, 기록 남기기를 작은 코드로 어떻게 흉내 낼 수 있는가?
- 이 최소 구현에서 무엇을 회고해야 하는가?

이 절에서는 다음 내용을 깊게 다루지 않습니다.

- 실제 벡터 데이터베이스 연결 코드
- 인증이 필요한 외부 SaaS API 호출
- 프로덕션 배포 설정

이 절의 구현은 `개념 확인용 장난감 흐름`입니다. 여기서는 앞의 P5-10.1, P5-10.2 RAG 흐름과 P5-12.1, P5-12.2 도구 사용 구조, P5-15.1, P5-15.2 평가와 기록 관점을 아주 작은 코드로 다시 묶어 확인합니다. 실제 RAG 검증 구조는 P6-5.1, P6-5.2에서 다시 회수하고, 에이전트 도구 연결과 운영 기록은 P6-6.1, P6-6.2에서 다시 회수합니다.

이 절은 `이론 설명 -> 곧바로 대형 프로젝트` 사이에 놓인 첫 중간 다리 역할을 합니다.

지금 읽는 층위는 `기록 가능한 최소 구현 층위`입니다. 앞 절이 `어떤 구조를 붙여야 질문이 닫히는가`를 설계 문장으로 정리했다면, 여기서는 `그 구조가 실제로 어떤 실행 기록으로 남아야 하는가`로 질문이 바뀝니다. 아직 제품 수준 자동화나 배포 절차까지는 가지 않고, 뒤의 Part 6에서는 이 최소 기록을 프로젝트 문서와 회고 산출물로 더 크게 확장합니다.

이 차이를 먼저 잡아 두면, 최소 구현 예제를 `작은 데모 코드`로만 읽지 않게 됩니다. 여기서 중요한 것은 코드 길이가 아니라 `질문 -> 근거 -> 답변 -> 평가 -> 기록`이 실제로 분리되어 남는가입니다.

| 지금 단계의 손잡이 | 바로 앞에서 본 질문 | 지금 가장 먼저 봐야 하는 질문 | 바로 다음에 이어질 위치 |
| --- | --- | --- | --- |
| 요청 흐름 설계 | 질문에 따라 prompt, retrieval, tool 중 무엇을 붙일 것인가? | P5-17.1 |
| 최소 구현과 run record | 그 선택이 실제로 어떤 출력과 기록으로 남는가? | P5-17.2 |
| 프로젝트 문서와 회고 산출물 | 이 기록을 더 큰 프로젝트 문서와 개선 계획으로 어떻게 키울 것인가? | P6-5.1, P6-5.2, P6-6.1, P6-6.2 |

처음 읽을 때는 이 절을 `설계 문장을 실제 run record로 바꾸는 자리` 정도로만 잡아도 충분합니다.

그래서 Part 5 안에서는 Chapter 17이 실제로 Part 6 회고 문서로 넘어가는 마지막 본류 다리 역할을 맡습니다. 여기서 남기는 `retrieved_doc_ids`, `needs_human_review`, `run_status`, `summary` 같은 기록은 뒤의 Part 6에서 `review_summary`, `incident_records`, `improvement_plan`으로 더 또렷하게 자라나며, 바로 다음 프로젝트 문서의 입력으로 다시 쓰이게 됩니다.

## 이 절의 목표

- 작은 생성형 AI 기능의 최소 구현 흐름을 읽을 수 있습니다.
- 검색 결과, 응답, 근거, 실패 기록이 왜 함께 출력되어야 하는지 설명할 수 있습니다.
- 기능이 돌아간다는 사실과 기능이 잘 설계되었다는 판단이 다르다는 점을 구분할 수 있습니다.
- Part 6에서 더 큰 프로젝트로 넘어갈 준비를 할 수 있습니다.

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

## 실행 가능한 Python 예제로 보기

이번 예제는 `질문 -> 검색 -> 답변 초안 -> 평가 -> 기록`을 한 번에 확인하는 데 목적이 있습니다. 이번에는 질문 두 개만 보는 대신, `다중 근거가 잡히는 경우`, `근거가 하나만 잡히는 경우`, `아예 검색 실패가 나는 경우`를 함께 넣어 최소 기능도 여러 실패 유형으로 갈라진다는 점을 확인하겠습니다. 특히 각 질문이 끝난 뒤 `run record` 하나로 남도록 만들어, 나중에 무엇을 고쳐야 하는지 한눈에 다시 읽을 수 있게 하겠습니다.

문제 상황:

- 같은 최소 기능이라도 다중 근거 확보, 근거 부족, 검색 실패를 구분해 기록해야 한다

입력:

- 정책 문서 4개
- 사용자 질문 3개

출력:

- 문서별 검색 점수
- 선택된 근거 문서
- 답변 초안
- 사람 검토 필요 여부와 회고 메모
- 질문별 run record
- 전체 질문 묶음에 대한 요약 통계

확인할 개념:

- 최소 구현도 검색, 답변, 평가, 기록이 한 흐름으로 묶여야 한다
- 질문별 run record를 남겨야 어떤 실패 유형이 반복되는지 다시 읽을 수 있다
- 운영 관점에서는 정답률보다 근거 부족과 검색 실패를 어떻게 구분했는지가 중요하다

먼저 이 예제에서 함께 볼 통합 기록 기준은 다음과 같습니다.

| 점검 항목 | 왜 필요한가 |
| --- | --- |
| `retrieved_doc_ids` | 어떤 근거를 실제로 썼는지 남겨야 해서 |
| `needs_human_review` | 답을 바로 써도 되는지, 사람 확인이 필요한지 나눠야 해서 |
| `run_status` | 다중 근거 확보, 근거 부족, 검색 실패를 한눈에 구분해야 해서 |
| `summary` | 한 질문씩만 보지 않고 전체 흐름에서 어떤 실패가 많은지 읽어야 해서 |

문제 상황:

- 정책형 QA 운영에서는 어떤 근거를 썼는지와 사람 검토 필요 여부를 실행 로그로 남겨야 전체 품질 흐름을 볼 수 있다

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
- 다중 근거, 근거 부족, 검색 실패가 서로 다른 메모와 `run_status`로 기록된다
- 질문별 실행 결과가 마지막에 `summary`로 다시 묶인다

그래서 이 예제에서 확인해야 할 결과는 `모델이 답했다`는 한 줄 뒤에 검색 점수, 근거 문서, 사람 검토 플래그, 회고 메모, 질문별 run record가 실제로 따로 남는가입니다. 특히 같은 최소 기능 안에서도 `다중 근거 확보`, `근거 부족`, `검색 실패`가 서로 다른 운영 상태로 남고, 마지막 summary에서 어떤 유형이 몇 번 나왔는지 다시 집계되는지가 중요합니다.

## 실패 유형으로 다시 묶기

이 최소 구현은 코드 실행 결과만 보는 것보다, 실제로 어떤 실패 장면이 생기는지와 다음 확장 방향을 함께 읽을 때 더 유용합니다. 여기서는 새 기능 사례를 더 늘리기보다, 방금 본 최소 구현이 운영에서 어떤 방식으로 흔들릴 수 있는지와 그 흔들림을 어떻게 분류해야 하는지를 봅니다.

### 사례 1. 문서를 찾았지만 답변이 어긋나는 경우

질문과 관련된 정책 문서는 찾았는데, 답변 초안이 첫 번째 문장만 보고 섣불리 단정할 수 있습니다. 사람이 규정을 읽을 때도 흔히 `키워드가 맞는 문서를 찾았으니 답도 맞겠지`라고 넘기기 쉽지만, 실제로는 예외 조건이나 적용 범위가 뒤 문장에 숨어 있을 수 있습니다. 예를 들어 `신입 직원도 월차 사용 가능`이라는 문장만 보고 답했는데, 바로 뒤에 `입사 후 1개월 이후`라는 조건이 붙어 있을 수 있습니다. 이때 사람은 `검색은 성공했지만 해석은 실패했다`는 사실을 구분해서 봐야 합니다. 그래서 이 사례에서 확인해야 할 결과는 관련 문서를 찾았더라도 예외 조건과 적용 범위를 끝까지 반영했는가, 아니면 첫 문장만 보고 답을 닫아 버렸는가입니다.

### 사례 2. 문서를 못 찾아 사람 검토로 넘기는 경우

질문에 맞는 문서가 하나도 잡히지 않으면, 잘 모르는 상태로 그럴듯한 답을 만드는 것보다 사람 검토가 필요하다고 표시하는 편이 안전합니다. 사람이 수작업으로 응대할 때도 근거 문서를 못 찾으면 보통 담당 부서에 다시 확인을 요청하지, 빈 기억만으로 규정을 단정하지는 않습니다. 예를 들어 새로 생긴 복지 제도 질문이 들어왔는데 문서 저장소에 아직 반영되지 않았다면, `답을 못 찾았음`을 드러내는 것이 틀린 답을 꾸며내는 것보다 낫습니다. 이 장난감 구현에서 `needs_human_review`를 따로 남기는 이유도 바로 여기에 있습니다. 그래서 이 사례에서 확인해야 할 결과는 문서를 못 찾았을 때 답을 꾸며내지 않고, 실패 상태를 명시한 채 실제로 사람 검토 단계로 넘기는가입니다.

### 사례 3. 다음 확장 지점을 고르는 경우

문서가 몇 개 안 될 때는 키워드 규칙만으로도 돌아가지만, 비슷한 표현이 늘어나면 금방 한계가 드러날 수 있습니다. 사람이 직접 운영하면 보통 `같은 질문이 다른 표현으로 들어왔을 때 왜 못 찾았는가`, `문서는 찾았는데 왜 엉뚱한 답을 했는가`를 사건별로 나눠 봅니다. 예를 들어 `육아휴직 순서`는 찾는데 `출산 후 휴직 절차`는 놓친다면, 다음 개선은 답변 템플릿보다 검색 확장일 가능성이 큽니다. 반대로 문서는 잘 찾는데 실제 잔여 일수 질문이 계속 들어오면, 그때는 도구 호출이 더 시급할 수 있습니다. 그래서 이 사례에서 확인해야 할 결과는 실패 유형을 검색 문제, 해석 문제, 도구 부재 문제로 나눠 보고 다음 확장 우선순위를 실제로 다르게 잡을 수 있는가입니다.

위 세 사례를 운영 관점으로 다시 묶으면 다음처럼 읽을 수 있습니다.

| 관찰된 문제 | 실제로 실패한 단계 | 다음 개선 방향 |
| --- | --- | --- |
| 문서는 찾았는데 답이 틀림 | 해석/생성 단계 | 근거 인용 방식, 답변 검토 규칙 보강 |
| 문서 자체를 못 찾음 | 검색 단계 | 키워드 확장, 임베딩 검색, 색인 개선 |
| 질문은 답했지만 실제 상태가 빠짐 | 도구 부재 | 조회 API 또는 도구 호출 추가 |

세 사례를 회고 질문으로 다시 묶으면 다음과 같습니다.

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

## 회고에서는 무엇을 남겨야 하나

이 절의 미니 실습에서는 다음 정도의 회고를 남기면 충분합니다. 앞의 실패 장면을 막연한 느낌으로 남기지 않고, 실제로 어느 단계를 먼저 고칠지 결정할 수 있을 만큼만 남기는 것이 목적입니다.

| 회고 항목 | 예시 질문 |
| --- | --- |
| 검색 품질 | 필요한 문서를 놓치지 않았는가? |
| 답변 품질 | 문서를 가져왔지만 잘못 해석하지 않았는가? |
| 실패 처리 | 문서를 못 찾았을 때 사람 검토로 넘기는가? |
| 확장 포인트 | 이후 vector search나 tool use가 필요한가? |

이 네 가지를 따로 남겨야 `검색을 고칠지`, `답변 해석 규칙을 고칠지`, `사람 검토 흐름을 넣을지`, `vector search나 tool use로 확장할지`를 실제 개선 계획으로 나눌 수 있습니다.

## 언제 vector search와 tool use로 확장하나

다음 상황이 오면 이 미니 실습은 확장 대상이 됩니다.

- 문서 수가 많아져 키워드 규칙으로는 한계가 보일 때
- 비슷한 표현을 더 잘 찾고 싶을 때
- 현재 상태 조회나 실행이 필요할 때

즉, 이 장은 `끝난 구현`이 아니라 `다음 개선을 위한 기준점`입니다.

다음처럼 연결하면 충분합니다.

- 더 나은 검색이 필요하면 P5-11의 임베딩과 벡터 검색으로 돌아갑니다.
- 실제 상태 조회가 필요하면 P5-12의 tool use로 갑니다.
- 여러 단계 판단이 필요하면 P5-13의 agent 구조로 갑니다.
- 실패 기록과 안전 장치는 P5-16의 운영 관점으로 다시 읽습니다.

## Part 5를 여기서 어떻게 닫아야 하나

이제 Part 5의 학습 흐름을 다음 순서로 다시 묶을 수 있습니다.

1. 토큰과 Transformer를 이해합니다.
2. 다음 토큰 예측과 생성 과정을 이해합니다.
3. 검색, 도구, 에이전트, 평가, 운영을 붙입니다.
4. 마지막으로 작은 기능 흐름으로 다시 확인합니다.

이 마지막 단계가 들어가야 앞에서 배운 개념들이 `한 번의 요청이 실제로 어떤 경로를 거치는가`라는 질문으로 닫힙니다.

## 다음 절과의 연결

이 미니 실습까지 마쳤다면, 이제 다음 질문은 더 자연스럽습니다.

- 이 구조를 더 긴 프로젝트 문서로 어떻게 확장할 것인가?
- baseline, 개선, 실패 기록을 한 프로젝트 산출물로 어떻게 남길 것인가?

이 질문은 Part 6 프로젝트에서 본격적으로 이어집니다.

## 이 절에서 기억할 관점

- 최소 구현은 완성품이 아니라 구조 확인용 기준점입니다.
- 검색, 응답, 기록은 따로가 아니라 함께 출력되어야 합니다.
- 기능이 돌아간다는 사실과 실제로 쓸 만하다는 판단은 다릅니다.
- 회고를 남겨야 다음에 vector search, tool use, agent로 확장할 이유가 분명해집니다.

## 체크리스트

- 작은 생성형 AI 기능의 최소 구현 흐름을 설명할 수 있는가?
- 검색 결과, 답변, 실패 기록을 왜 함께 남겨야 하는지 말할 수 있는가?
- 이 예제가 무엇을 보여 주고 무엇을 아직 못 하는지 구분할 수 있는가?
- Part 6 프로젝트로 넘어갈 때 무엇을 더 확장해야 하는지 설명할 수 있는가?

## 출처와 참고 자료

이 문서는 Part 5의 통합 미니 실습을 위한 자체 구성 문서입니다. 외부 자료를 직접 인용하지 않았습니다.
