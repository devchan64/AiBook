# P7-7.5 재현 가능한 프로젝트 패키지 만들기

Section ID: `P7-7.5`
Version: `v2026.07.23`

Part 7의 여러 실습을 끝냈다고 해서 프로젝트가 곧바로 다시 실행 가능한 상태가 되는 것은 아닙니다. 좋은 결과표, 모델 출력, RAG 검색 기록, agent 실행 로그가 있어도 다른 사람이 같은 조건에서 다시 돌릴 수 없다면 학습 기록은 금방 흩어집니다.

재현 가능한 프로젝트 패키지(reproducible project package)는 거창한 배포 묶음이 아닙니다. 최소한 `질문`, `입력`, `코드`, `환경`, `실행 명령`, `출력`, `오류 사례`, `한계`, `다음 조치`가 서로 이어져 있어야 합니다. 이 절에서는 Part 7에서 만든 여러 실습 결과를 다시 펼쳐, 어떤 패키지는 바로 재현 가능하고 어떤 패키지는 아직 보강이 필요한지 점검합니다.

## 재현 패키지가 가르는 질문

- 프로젝트를 다시 실행하려면 무엇이 반드시 남아 있어야 하는가?
- 코드와 출력이 있어도 왜 환경, 명령, 한계 기록이 빠지면 재현성이 흔들리는가?
- 다음 사람이 바로 이어서 볼 수 있게 하려면 어떤 항목부터 보강해야 하는가?

핵심은 `결과가 있다`와 `재현 가능하다`를 구분하는 데 있습니다. 결과표가 있어도 어떤 입력 파일을 썼는지, 어떤 패키지가 필요했는지, 어떤 명령으로 돌렸는지, 어떤 한계를 남겼는지 모르면 다음 실행은 추측이 됩니다.

## 판단 기준

- 프로젝트 산출물을 재현에 필요한 항목으로 나누어 볼 수 있습니다.
- 필수 항목과 선택 항목을 구분하고, 빠진 필수 항목이 재현 가능성을 어떻게 깨뜨리는지 설명할 수 있습니다.
- `재현 가능`, `검토 필요`, `재현 불가` 상태를 다음 보강 행동과 함께 기록할 수 있습니다.

## 왜 마지막에 재현성을 확인해야 하나

Part 7 앞 절들은 서로 다른 실행 장면을 다룹니다. P7-2에서는 비교 실험, P7-4에서는 학습 로그, P7-5에서는 RAG 검색 근거, P7-6에서는 agent 실행 기록, P7-7 앞 절에서는 배포와 운영 회고를 다뤘습니다. 그런데 실제 프로젝트에서는 이 기록들이 한 폴더나 문서 묶음 안에서 다시 실행 가능해야 합니다.

재현 패키지에서 흔히 빠지는 항목은 다음과 같습니다.

| 빠진 항목 | 바로 생기는 문제 |
| --- | --- |
| 입력 파일 경로 | 어떤 데이터로 만든 결과인지 알 수 없다 |
| 실행 환경 | 같은 코드라도 패키지 버전이나 실행 도구가 달라질 수 있다 |
| 실행 명령 | 코드가 있어도 어떤 순서로 돌렸는지 추측해야 한다 |
| 기준점과 오류 사례 | 출력 숫자만 남아 다음 수정 방향이 사라진다 |
| 한계와 다음 조치 | 성공처럼 보이는 결과가 과장된 결론으로 굳는다 |

따라서 프로젝트 마무리는 `결과를 저장했다`가 아니라 `다시 실행할 수 있게 묶었다`로 닫아야 합니다.

## 입력 파일

- 재현성 점검 파일: [`p7-7-reproducibility-items.csv`](../../../assets/part-07/chapter-07/p7-7-reproducibility-items.csv){ .csv-preview }
- 한 행의 의미: `하나의 프로젝트 패키지에서 재현성에 필요한 점검 항목 하나`
- 핵심 열: `package_id`, `category`, `status`, `required`, `next_action`

이 파일은 Part 7의 대표 실습 패키지 세 개를 합성한 점검표입니다. 실제 프로젝트 파일 목록을 그대로 복제한 것이 아니라, 어떤 항목이 빠지면 재현성이 깨지는지 보여 주기 위해 만든 자체 예시입니다.

## 연습 흐름

1. `package_id`별로 항목을 묶습니다.
2. `required=yes`인 필수 항목 중 `missing`, `partial`, `stale` 상태를 찾습니다.
3. 필수 항목이 모두 준비됐는지 보고 패키지 상태를 나눕니다.
4. 재현 불가 패키지에서는 먼저 보강할 항목과 다음 조치를 적습니다.

## 실행 기록 기준

- 전체 항목 수보다 필수 항목 준비율을 먼저 봅니다.
- `missing`과 `partial`을 같은 실패로 뭉치지 않고, 어떤 범주가 빠졌는지 확인합니다.
- 선택 항목이 낡은 경우와 필수 항목이 빠진 경우를 구분합니다.
- 재현 불가 상태에는 반드시 다음 조치를 붙입니다.

## Python 예제

예제는 프로젝트 패키지별 재현 가능성을 점검합니다. 필수 항목이 빠졌거나 부분 준비 상태면 재현이 끊기는 위치를 먼저 찾고, 다음 보강 항목을 출력합니다.

```python
# Part 7 대표 프로젝트 패키지의 질문, 입력, 코드, 환경, 실행 명령, 결과 기록을 점검해 재현 가능성을 분류하는 예제입니다.
import csv
from collections import Counter, defaultdict
from pathlib import Path

data_path = Path("docs/assets/part-07/chapter-07/p7-7-reproducibility-items.csv")
rows = list(csv.DictReader(data_path.open(encoding="utf-8")))

not_ready_statuses = {"missing", "partial", "stale"}
critical_categories = {
    "question",
    "input",
    "code",
    "environment",
    "command",
    "result",
    "release_note",
}

packages = defaultdict(list)
for row in rows:
    packages[row["package_id"]].append(row)

def package_state(items):
    required_items = [item for item in items if item["required"] == "yes"]
    not_ready_required = [
        item for item in required_items if item["status"] in not_ready_statuses
    ]
    critical_not_ready = [
        item for item in not_ready_required if item["category"] in critical_categories
    ]
    if critical_not_ready:
        return "재현 불가"
    if not_ready_required:
        return "검토 필요"

    optional_stale = [
        item
        for item in items
        if item["required"] == "no" and item["status"] in not_ready_statuses
    ]
    if optional_stale:
        return "재현 가능, 보강 권장"
    return "재현 가능"

package_records = []
for package_id, items in sorted(packages.items()):
    required_items = [item for item in items if item["required"] == "yes"]
    not_ready_required = [
        item for item in required_items if item["status"] in not_ready_statuses
    ]
    status_counts = Counter(item["status"] for item in items)
    package_records.append({
        "패키지": package_id,
        "전체 항목 수": len(items),
        "필수 항목 수": len(required_items),
        "준비 완료 필수 항목 수": len(required_items) - len(not_ready_required),
        "준비율": round(
            (len(required_items) - len(not_ready_required)) / len(required_items),
            2,
        ),
        "상태": package_state(items),
        "상태 분포": dict(status_counts),
        "먼저 보강할 항목": [
            f"{item['item_id']}:{item['category']}:{item['status']}"
            for item in not_ready_required[:3]
        ],
    })

next_actions = []
for row in rows:
    if row["required"] == "yes" and row["status"] in not_ready_statuses:
        next_actions.append({
            "패키지": row["package_id"],
            "항목": row["item_id"],
            "범주": row["category"],
            "상태": row["status"],
            "다음 조치": row["next_action"],
        })

summary = {
    "패키지 수": len(package_records),
    "재현 가능 패키지 수": sum(
        record["상태"].startswith("재현 가능") for record in package_records
    ),
    "재현 불가 패키지 수": sum(
        record["상태"] == "재현 불가" for record in package_records
    ),
    "필수 보강 항목 수": len(next_actions),
}

print("재현성 점검 요약 =", summary)
print("패키지별 기록 =")
for record in package_records:
    print(record)
print("필수 보강 항목 =")
for action in next_actions:
    print(action)
```

실행 결과 예시는 다음과 같습니다.

```text
재현성 점검 요약 = {'패키지 수': 3, '재현 가능 패키지 수': 1, '재현 불가 패키지 수': 2, '필수 보강 항목 수': 5}
패키지별 기록 =
{'패키지': 'agent-ops', '전체 항목 수': 12, '필수 항목 수': 11, '준비 완료 필수 항목 수': 7, '준비율': 0.64, '상태': '재현 불가', '상태 분포': {'ready': 7, 'missing': 3, 'partial': 2}, '먼저 보강할 항목': ['item-04:environment:missing', 'item-05:command:missing', 'item-07:evaluation:partial']}
{'패키지': 'baseline-churn', '전체 항목 수': 12, '필수 항목 수': 11, '준비 완료 필수 항목 수': 11, '준비율': 1.0, '상태': '재현 가능', '상태 분포': {'ready': 12}, '먼저 보강할 항목': []}
{'패키지': 'rag-vector-db', '전체 항목 수': 12, '필수 항목 수': 11, '준비 완료 필수 항목 수': 10, '준비율': 0.91, '상태': '재현 불가', '상태 분포': {'ready': 10, 'partial': 1, 'stale': 1}, '먼저 보강할 항목': ['item-04:environment:partial']}
필수 보강 항목 =
{'패키지': 'rag-vector-db', '항목': 'item-04', '범주': 'environment', '상태': 'partial', '다음 조치': 'requirements와 설치 버전 차이를 점검한다'}
{'패키지': 'agent-ops', '항목': 'item-04', '범주': 'environment', '상태': 'missing', '다음 조치': '표준 라이브러리만 쓰는지 명시한다'}
{'패키지': 'agent-ops', '항목': 'item-05', '범주': 'command', '상태': 'missing', '다음 조치': '본문 코드 블록 재실행 명령을 남긴다'}
{'패키지': 'agent-ops', '항목': 'item-07', '범주': 'evaluation', '상태': 'partial', '다음 조치': '자동 실행 가능과 즉시 보류 기준을 연결한다'}
{'패키지': 'agent-ops', '항목': 'item-12', '범주': 'release_note', '상태': 'missing', '다음 조치': 'P7-6.2 또는 P7-6.3 릴리즈노트 상태를 확인한다'}
```

## 결과를 어떻게 읽는가

`baseline-churn`은 바로 재현 가능한 패키지입니다. 질문, 입력, 코드, 환경, 명령, 결과, 오류 사례, 한계, 다음 조치가 모두 준비되어 있습니다. 이런 상태라면 다른 독자가 같은 파일을 열어 실행하고, 결과가 같은지 확인한 뒤 다음 실험으로 넘어갈 수 있습니다.

`rag-vector-db`는 결과와 코드는 있지만 환경 항목이 `partial`입니다. 특히 ChromaDB와 scikit-learn을 쓰는 예제는 의존성 버전이 달라지면 실행 메시지나 일부 API 동작이 달라질 수 있습니다. 따라서 결과가 있어도 `어떤 환경에서 다시 실행할 것인가`를 명확히 남기기 전에는 재현 가능하다고 단정하지 않습니다.

`agent-ops`는 실행 로그 자체는 있지만 환경, 실행 명령, 릴리즈노트 연결이 빠져 있습니다. 이 상태에서는 읽을 수는 있어도 다시 실행하거나 인수인계하기 어렵습니다. 운영 기록은 특히 `무엇이 완료됐고 무엇이 blocked였는가`를 남기는 것만으로 끝나지 않고, 다음 사람이 같은 판단을 다시 확인할 수 있게 실행 조건을 닫아야 합니다.

## 결과 해석 기준

| 관찰 | 읽어야 할 뜻 |
| --- | --- |
| `baseline-churn` 준비율이 1.0이다 | 질문, 입력, 실행, 결과, 한계가 한 묶음으로 닫혀 있다 |
| `rag-vector-db`는 준비율이 높아도 재현 불가다 | 필수 환경 항목이 부분 준비라 실제 재실행 조건이 닫히지 않았다 |
| `agent-ops`는 필수 보강 항목이 4개다 | 실행 로그는 있지만 다른 사람이 같은 조건으로 다시 확인하기 어렵다 |
| 필수 보강 항목이 바로 출력된다 | 회고가 막연한 반성이 아니라 다음 작업 목록으로 바뀐다 |

## 프로젝트 기록 예시

```text
프로젝트 패키지:
질문:
입력 파일:
실행 코드 또는 스크립트:
실행 환경:
실행 명령:
결과 요약:
오류 사례:
한계:
다음 조치:
재현 상태:
먼저 보강할 항목:
```

## 회고 문장으로 닫기

재현성 점검 뒤에는 다음처럼 회고를 남길 수 있습니다.

> `baseline-churn` 패키지는 질문, 입력, 코드, 실행 명령, 결과, 오류 사례, 한계 기록이 모두 준비되어 있어 바로 재현 가능한 상태다. 반면 `rag-vector-db`는 ChromaDB와 scikit-learn 의존성 조건이 부분 준비 상태라, 실행 환경을 더 명확히 남긴 뒤 재현 가능으로 볼 수 있다. `agent-ops`는 실행 로그는 있지만 환경과 명령, 릴리즈노트 연결이 빠져 있어 현재는 재현 불가로 분류한다. 다음 보강은 결과를 다시 쓰는 것이 아니라, 누락된 필수 항목을 채워 같은 실행을 다시 확인할 수 있게 만드는 데 둔다.

이 문장에서 중요한 것은 성공과 실패를 감정적으로 나누지 않는 것입니다. 재현 불가는 나쁜 프로젝트라는 뜻이 아니라, 아직 다음 사람이 같은 실행을 반복할 조건이 닫히지 않았다는 뜻입니다.

## 직접 바꿔 보며 확인할 것

1. `rag-vector-db`의 `environment` 상태를 `ready`로 바꿔 봅니다.
   - 관찰할 점: 준비율과 패키지 상태가 어떻게 바뀌는가?

2. `agent-ops`의 `command`, `environment`, `release_note` 상태를 차례로 `ready`로 바꿔 봅니다.
   - 관찰할 점: 어떤 항목이 마지막까지 재현 불가를 유지하게 만드는가?

3. `baseline-churn`의 `result` 상태를 `stale`로 바꿔 봅니다.
   - 관찰할 점: 결과 파일이 낡으면 전체 패키지를 바로 재현 가능으로 볼 수 있는가?

4. `required=no`인 `handoff` 항목만 `stale`로 바꿔 봅니다.
   - 관찰할 점: 선택 항목 보강 권장과 필수 항목 누락은 어떻게 다르게 읽어야 하는가?

핵심은 항목 수가 많다는 사실이 아니라, 필수 항목이 닫혀 있는지입니다. 재현성 점검은 문서 정리가 아니라 다음 실행의 실패 지점을 미리 줄이는 일입니다.

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| 질문 | 무엇을 다시 실행하려는지 한 문장으로 남겼는가? |
| 입력 | 데이터, 문서, 로그 파일 경로가 실제로 열리는가? |
| 환경 | 필요한 패키지와 실행 환경이 적혀 있는가? |
| 명령 | 다른 사람이 같은 명령으로 다시 실행할 수 있는가? |
| 결과 | 출력 요약과 오류 사례가 함께 남았는가? |
| 한계 | synthetic 데이터, mock 로그, 로컬 실행 같은 제한을 적었는가? |
| 다음 조치 | 재현 불가 항목이 다음 작업 목록으로 바뀌었는가? |

## 출처와 참고 자료

- 재현성 점검 파일: [`p7-7-reproducibility-items.csv`](../../../assets/part-07/chapter-07/p7-7-reproducibility-items.csv){ .csv-preview }
- 이 문서는 자체 합성 데이터와 자체 실습 예시를 사용했습니다. 외부 자료를 직접 인용하지 않았습니다.
