# P6-14.1 조회·계산·실행을 모델 밖으로 넘기는 도구 사용

> Section ID: `P6-14.1`
> Version: `v2026.07.31`

도구 사용 요청은 `model_request`, `tool_name`, `tool_input`, `tool_output`, `execution_status`, `model_summary`를 나누어 기록합니다. 이 구분을 남기면 모델이 설명을 생성한 부분과 실제 조회·계산·실행이 도구에서 일어난 부분이 분리됩니다.

P6-13.2에서는 벡터 검색에서 인덱스가 검색 속도와 품질의 균형을 만드는 구조라는 점을 보았습니다. 하지만 검색은 외부 세계와 연결되는 한 가지 방식일 뿐입니다. 이제 더 넓은 질문이 나옵니다.

모델이 문서를 읽는 것을 넘어, 외부 기능을 실제로 호출해야 한다면 어떻게 해야 하는가?

에이전트 도구 사용(tool use)은 모델이 텍스트만 생성하는 데서 멈추지 않고, 계산기, 검색기, 데이터베이스, API 같은 외부 기능을 연결해 쓰는 구조다.

## 실행 연결이 필요한 요청

핵심 질문은 다음과 같습니다.

- 도구 사용은 왜 필요한가?
- RAG와 도구 사용은 무엇이 다른가?
- 어떤 상황에서 모델 단독 답변보다 도구 호출이 더 적합한가?

먼저 닫을 문제는 도구 사용을 `모델이 외부 기능과 실제로 연결되는 실행 구조`로 읽고, RAG의 문서 읽기와 무엇이 다른지 붙잡는 것입니다.

여기서는 먼저 `문서만 읽으면 되는 요청`과 `외부 기능을 실제로 호출해야 닫히는 요청`을 가릅니다. 실행 요청을 이름과 인자로 나누는 문제는 P6-14.2에서, 여러 실행을 이어 가는 문제는 P6-14에서 따로 봅니다.

tool use는 `모델이 갑자기 실행 능력을 가진다`는 뜻이 아니라, `애플리케이션이 모델과 외부 기능을 연결하는 구조`입니다. 앞의 RAG가 외부 문서를 읽어 근거를 붙이는 구조였다면, tool use는 외부 기능을 실제로 호출해 결과를 가져오는 구조로 한 단계 더 나아갑니다. 호출 이름과 인자를 어떻게 검증 가능한 형식으로 만들지는 P6-14.2에서, 여러 호출을 어떤 순서로 이어 갈지는 P6-14에서 이어서 봅니다.

도구 이름을 많이 외우기보다 `지금 필요한 것이 문서 읽기인가 실제 실행인가`, `무엇을 조회하거나 계산하거나 실행해야 하는가`, `그 실행 결과를 어떤 호출 구조로 넘길 것인가`라는 세 질문으로 먼저 읽으면 됩니다.

이 단계에서 먼저 확인할 것은 단순합니다. 답이 문서 설명으로 닫히는지, 현재 상태 조회나 계산 결과가 필요한지, 실제 예약·수정처럼 외부 세계를 바꾸는 실행까지 필요한지 구분해야 합니다. 이 구분이 서야 다음 Section의 함수 호출 구조도 제품 기능명이 아니라 실행 요청을 안정화하는 형식으로 읽을 수 있습니다.

## 설명 생성과 실제 실행 연결의 구분

- 도구 사용을 입문 수준에서 설명할 수 있습니다.
- RAG와 도구 사용의 차이를 말할 수 있습니다.
- 계산, 조회, 실행 같은 작업에서 왜 도구가 필요한지 설명할 수 있습니다.
- 실행 요청을 함수 호출(function calling) 구조로 바꿔야 하는 이유를 말할 수 있습니다.

먼저 가를 장면은 아래처럼 정리할 수 있습니다.

| 먼저 보인 막힘 | 먼저 떠올릴 질문 | 왜 이 질문이 먼저 필요한가 |
| --- | --- | --- |
| 관련 규정은 읽었는데 지금 상태값은 아직 모른다 | 문서 읽기보다 실시간 조회가 먼저 필요한가? | 현재 값이 없으면 설명은 자연스러워도 실제 상태와 어긋난 답이 되기 쉽기 때문입니다. |
| 설명은 가능하지만 숫자 정확도가 핵심이다 | 추정 대신 계산 도구 결과를 먼저 가져와야 하는가? | 계산은 말투보다 수치 정확성이 먼저라서, 추측 답변으로는 바로 틀어질 수 있기 때문입니다. |
| 실행 결과가 있어야 답이 닫히는데 아직 행동은 하지 않았다 | 실제 실행 도구를 호출해야 질문이 끝나는가? | 파일 수정, 예약, 전송처럼 외부 세계를 바꾸는 작업은 설명만으로 완료되지 않기 때문입니다. |
| 문서를 읽을지, 도구를 부를지, 둘을 함께 쓸지 헷갈린다 | 지금 필요한 것이 근거 문서인가, 조회값인가, 실행 결과인가? | 읽기와 실행을 섞어 보면 RAG로 닫힐 질문과 tool use가 필요한 질문을 잘못 고르기 쉽기 때문입니다. |

이 표를 기준으로 삼으면, tool use를 `도구 이름 모음`보다 `문서 읽기에서 실제 조회·계산·실행으로 넘어가는 기준`으로 더 직접 읽을 수 있습니다.

## 왜 도구 사용이 필요한가

LLM은 텍스트 생성에 강하지만, 말만으로는 정확한 계산, 조회, 실행을 처리하기 어렵거나 위험한 작업이 있습니다. 도구 사용에서 추가되는 것은 외부 기능 호출 단계이고, 그래서 바뀌는 것은 답을 추측하는 대신 실제 결과를 가져오는 구조입니다.

- 정확한 계산
- 데이터베이스 조회
- 일정 예약
- 이메일 전송
- 파일 읽기와 수정
- 실시간 API 호출

이런 작업은 단순히 `답처럼 보이는 문장`을 만드는 것과 다릅니다. 실제로 외부 세계에 영향을 주거나, 검증 가능한 결과를 가져와야 합니다.

따라서 도구 사용은 보통 다음 목적 때문에 등장합니다.

- 모델의 약한 계산 능력을 보완하기 위해
- 실시간 정보에 접근하기 위해
- 실제 시스템 동작으로 이어지게 하기 위해

서비스 구조 관점으로 다시 말하면, RAG가 `근거 문서 읽기`를 붙였다면 tool use는 `실제 기능 실행`을 붙이는 단계입니다.

## RAG와 무엇이 다른가

이 차이를 먼저 분리해 두어야 지금 필요한 것이 `문서 근거 추가`인지 `실제 기능 실행`인지 구조를 잘못 고르지 않게 됩니다.

| 구조 | 중심 역할 |
| --- | --- |
| RAG | 관련 문서를 찾아서 답변 근거로 붙인다 |
| 에이전트 도구 사용(tool use) | 외부 기능을 호출해 실제 결과를 가져오거나 실행한다 |

예를 들어:

- 문서 검색 후 설명하는 것은 RAG에 가깝습니다
- 환율 API를 호출해 최신 값을 가져오는 것은 도구 사용에 가깝습니다
- 계산기로 정확한 합계를 구하는 것도 도구 사용에 가깝습니다

즉, RAG는 주로 `읽기(read)` 중심이고, tool use는 `조회(query)`, `계산(compute)`, `실행(act)`까지 포함하는 더 넓은 구조입니다.

이 차이를 현재 Part 6 본류 기준으로 가장 짧게 압축하면 다음과 같습니다.

| 구조 | 먼저 붙는 것 | 중심 질문 | 대표 결과 |
| --- | --- | --- | --- |
| RAG | 관련 문서 | 무엇을 근거로 답할까? | 문서 근거가 붙은 답변 |
| 에이전트 도구 사용(tool use) | 외부 기능 호출 | 무엇을 실제로 조회하거나 실행할까? | 계산값, 조회값, 실행 결과 |
| AI agent | 여러 단계 연결 | 어떤 순서로 계속 진행할까? | 상태를 갱신하며 이어지는 작업 흐름 |

이 표의 핵심은 `문서를 읽는 일`, `기능을 실행하는 일`, `여러 단계를 이어 가는 일`이 서로 다른 층위라는 점입니다. 그래서 RAG 위에 tool use가 붙을 수 있고, 그 둘을 다시 agent가 하나의 목표 흐름으로 묶을 수 있습니다.

여기까지는 아직 `요청 하나에 대해 어떤 외부 기능을 붙일 것인가`를 읽는 단계입니다. 예를 들어 `사내 환불 규정을 요약해 줘`는 먼저 문서 근거를 찾는 RAG 문제에 가깝고, `지금 환율로 300달러를 원화로 계산해 줘`는 현재 값 조회와 계산 도구가 필요한 tool use 문제에 가깝습니다. `내일 비어 있는 회의실을 찾아 예약까지 해 줘`처럼 조회와 실행이 이어지면 이후 AI 에이전트(AI agent) 구조에서 다시 다룹니다.

즉, 이 Section에서는 `무엇을 읽을까`에서 `무엇을 실제로 조회·계산·실행할까`로 넘어가는 지점을 먼저 닫습니다. 그 실행 요청을 어떤 이름과 인자 구조로 안정화할지는 P6-14.2의 함수 호출(function calling)에서, 여러 실행을 어떤 순서로 이어 갈지는 P6-14의 AI 에이전트 구조에서 이어서 봅니다.

## 모델이 직접 도구를 쓰는가

여기서 `모델이 스스로 API를 때리는가?`라는 오해를 하곤 합니다. 더 안전한 설명은 다음입니다.

`모델은 보통 어떤 도구가 필요할지에 대한 출력을 만들고, 실제 호출은 애플리케이션이나 실행 환경이 맡는다.`

즉, 도구 사용은:

- 모델이 요청 구조를 제안하고
- 시스템이 그 요청을 해석해
- 실제 도구를 호출하고
- 그 결과를 다시 모델이나 사용자에게 연결하는

협업 구조에 가깝습니다.

여기서 `모델이 어떤 실행을 제안하는가`와 `시스템이 그것을 실제로 수행하는가`를 분리해서 봐야, 실패가 판단 단계 문제인지 실행 단계 문제인지 나눌 수 있습니다.

## 어떤 상황에서 특히 유용한가

도구 사용은 다음 상황에서 매우 실용적입니다.

- 숫자 계산이 정확해야 할 때
- 최신 외부 시스템 조회가 필요할 때
- 파일이나 데이터 조작이 필요할 때
- 실행 결과를 다시 요약해야 할 때

`도구 사용은 모델이 잘 말하는 능력과, 시스템이 실제로 하는 능력을 연결하는 구조다.`

같은 요청 흐름으로 다시 정리하면 다음과 같습니다.

- 프롬프트: 질문 방식 조정
- RAG: 답하기 전 근거 문서 연결
- 도구 사용: 답하기 전 또는 답하는 중 실제 기능 호출

## 도구 사용도 만능은 아니다

도구 사용이 있다고 해서:

- 항상 올바른 도구를 고르는 것
- 필요한 인자를 정확히 구성하는 것
- 권한 없는 작업을 자동으로 막는 것
- 잘못된 실행 결과를 스스로 모두 교정하는 것

이 자동 보장되지는 않습니다.

즉, 도구 사용은 능력을 넓히지만, 동시에 다음 문제가 생깁니다.

- 권한(permission)
- 승인(approval)
- 실패 처리(error handling)
- 로그(trace)
- 재현성(reproducibility)

이 문제들은 뒤 장의 AI 에이전트와 하네스(harness) 구조로 이어집니다.

## 아주 단순하게 그리면

```mermaid
--8<-- "assets/part-06/chapter-13/p6-c13-s01-tool-use-flow-ko.mmd"
```

## 설명만으로 닫히지 않는 실행 요청

### 사례 1. 계산기 도구

사용자가 `13.7%를 세 번 연속 할인하면 최종 가격이 얼마인가요?`라고 묻는다고 해 봅시다. 사람은 설명을 잘하는 모델이면 계산도 비슷하게 잘할 것이라고 느끼기 쉽습니다. 하지만 긴 계산 과정에서는 중간 곱셈이나 반올림에서 작은 산술 오류가 바로 생길 수 있습니다. 예를 들어 할인율을 단순 합산해 버리면 말은 그럴듯해도 결과가 바로 틀어집니다.

이때 중요한 것은 더 그럴듯한 설명이 아니라 정확한 계산 결과입니다. 계산이 조금만 틀려도 할인 금액, 세금, 최종 청구액까지 연쇄적으로 어긋날 수 있습니다. 여기서 바뀌는 점은 `설명을 잘하는가`를 먼저 보던 기준에서 `정확한 계산은 외부 계산 도구로 확인하는가`를 먼저 보게 되는 기준으로 이동한다는 것입니다. 도구 사용 구조가 있으면 모델은 직접 숫자를 짐작하기보다 계산기 도구를 호출해 결과를 받아 설명할 수 있습니다. 그래서 이 사례에서 확인해야 할 결과는 설명 말투가 아니라 최종 수치와 중간 계산이 일치하는가입니다.

같은 질문이라도 아래처럼 판단 기준이 달라집니다.

| 질문 장면 | 설명만 볼 때 생기기 쉬운 오판 | 도구 사용 관점에서 먼저 확인할 것 |
| --- | --- | --- |
| 연속 할인 계산 | 설명이 단계적이니 결과도 맞을 것 같음 | 중간 곱셈과 반올림이 실제 계산 결과와 일치하는가 |
| 세금 포함 최종가 계산 | 결론 숫자만 그럴듯하면 통과시키기 쉬움 | 세전·세후 값과 적용 순서가 모두 계산 도구 결과와 맞는가 |
| 환율/할인/수수료가 섞인 계산 | 장문 reasoning이 있으면 더 신뢰하기 쉬움 | 최종 수치뿐 아니라 각 단계 숫자도 외부 계산 결과로 검증됐는가 |

이 표에서 넘어가야 할 오해는 `설명이 좋아 보이면 계산도 거의 맞다`는 기대입니다. 계산기 도구 사례의 핵심은 설명과 계산을 분리하고, 계산 쪽은 별도 실행 결과를 기준으로 확인하는 데 있습니다.

### 사례 2. 일정 조회

사용자가 `내일 오후 비어 있는 회의실이 있나요?`라고 묻는 장면을 생각해 볼 수 있습니다. 사람은 먼저 관련 안내 문서나 일반 규칙을 떠올리기 쉽지만, 이 질문은 정책 문서를 검색한다고 해결되지 않고 현재 일정 시스템의 실제 상태를 조회해야 닫힙니다. 예를 들어 예약 규칙은 문서에 있어도, 지금 3층 회의실이 실제로 비어 있는지는 문서가 아니라 캘린더 상태값에 들어 있습니다.

사람이 여기서 먼저 구분해야 하는 것은 `문서 지식이 필요한가`가 아니라 `실시간 상태 값이 필요한가`입니다. 만약 조회 없이 일반 규칙만 답하면, 사용자는 실제로는 이미 예약된 회의실을 비어 있다고 오해할 수 있습니다. 반대로 캘린더 도구를 조회하면 `3층 소회의실 A는 비어 있고, B는 15:00~16:00 예약됨`처럼 현재 시점 기준 결과가 바로 돌아올 수 있습니다. 여기서 바뀌는 점은 `규칙을 알고 있는가`에서 `현재 상태를 실제로 조회했는가`로 기준이 이동한다는 것입니다. 도구 사용 구조가 있으면 모델은 캘린더나 예약 시스템을 조회한 뒤 그 결과를 바탕으로 답할 수 있습니다. 그래서 이 사례에서 확인해야 할 결과는 답변이 일반 규칙 요약이 아니라, 실제 비어 있는 회의실 목록이나 불가 상태를 현재 시점 기준으로 돌려주는가입니다.

이 차이를 운영 메모처럼 줄이면 다음과 같습니다.

| 사용자 질문 | 문서 설명만으로 닫히는가 | 실제로 조회해야 하는 대상 |
| --- | --- | --- |
| `회의실 예약 규칙이 뭐예요?` | 대체로 가능 | 규칙 문서 |
| `내일 오후 3층 회의실이 비었나요?` | 불가 | 캘린더의 현재 예약 상태 |
| `A회의실이 비면 바로 예약해 줘` | 설명만으로는 더 부족함 | 상태 조회 + 실행 도구 |

이 사례에서 붙잡아야 할 기준은 `관련 정보를 알고 있는가`보다 `지금 필요한 정보가 문서 안에 있는가, 시스템 상태 안에 있는가`입니다. 일정 조회 사례는 바로 이 분기에서 도구 사용 필요가 결정된다는 점을 보여 줍니다.

### 사례 3. 파일 수정

코드 도우미가 `이 함수 이름을 새 규칙에 맞게 바꿔 주세요`라는 요청을 받는다고 해 봅시다. 사람은 종종 `어떻게 바꿀지 설명만 해도 충분하겠지`라고 생각하기 쉽지만, 실제 파일은 그 설명만으로 달라지지 않습니다. 더구나 함수 이름 하나를 바꾸면 선언부, 호출부, 테스트 코드까지 같이 찾아 수정해야 할 수 있습니다. 예를 들어 선언부만 바꾸고 테스트 호출부를 놓치면 답변은 그럴듯해도 저장소는 바로 깨집니다.

이 경우 필요한 것은 설명 능력보다 파일을 읽고 수정하고 저장하는 실행 능력입니다. 실제 수정 없이 설명만 남기면 사용자는 다시 수동 작업을 해야 하고, 중간 누락이 생길 가능성도 커집니다. 여기서 바뀌는 점은 `수정 방법을 설명하는가`에서 `실제 파일 상태를 바꾸고 연결된 위치까지 함께 수정하는가`로 기준이 이동한다는 것입니다. 도구 사용 구조가 있으면 모델은 수정 제안에 머무르지 않고 실제 파일 작업 도구를 호출할 수 있습니다. 그래서 이 사례에서 확인해야 할 결과는 설명문이 아니라 선언부, 호출부, 테스트가 함께 바뀌고 저장소가 계속 동작하는가입니다.

이 도식의 핵심은 모델이 혼자 끝내는 것이 아니라, 외부 시스템과 왕복이 생긴다는 점입니다.

세 사례를 실행 판단 기준으로 다시 묶으면 다음과 같습니다.

| 상황 | 모델 설명만으로는 부족한 것 | 실제로 확인하거나 바꿔야 하는 대상 |
| --- | --- | --- |
| 계산기 도구 | 숫자를 그럴듯하게 말하는 것 | 정확한 계산 결과 |
| 일정 조회 | 예약 규칙을 설명하는 것 | 현재 시점의 실제 일정 상태 |
| 파일 수정 | 수정 방법을 말로 설명하는 것 | 실제 파일 내용과 연결 위치 |

같은 내용을 실행 위임 구조로 다시 보면 다음처럼 읽을 수 있습니다.

```mermaid
--8<-- "assets/part-06/chapter-13/p6-c13-s01-tool-delegation-ko.mmd"
```

핵심은 `답변` 전에 `실행 준비 구조`가 따로 생긴다는 점입니다.

## 실행 연결이 필요한 장면

도구 사용을 처음 읽을 때 가장 자주 헷갈리는 것은 `외부 정보가 필요하다`는 말을 모두 같은 문제로 보는 점입니다. 하지만 실제로는 `문서를 읽으면 되는가`, `현재 상태를 조회해야 하는가`, `실제로 뭔가를 바꿔야 하는가`를 먼저 갈라야 다음 구조가 맞아집니다.

| 이런 장면이 보이면 | 먼저 확인할 것 | 왜 그 분리가 중요한가 |
| --- | --- | --- |
| 규정이나 매뉴얼을 설명하면 될 것 같음 | 문서 근거만으로 닫히는 질문인가 | 현재 상태 조회나 실행이 필요 없으면 RAG 쪽이 먼저 맞기 때문입니다. |
| 할인율, 세금, 환율처럼 숫자 정확도가 바로 결과를 바꿈 | 추정 문장 대신 실제 계산값을 가져와야 하는가 | 설명이 자연스러워도 계산은 쉽게 틀릴 수 있어, 외부 계산 결과를 기준으로 확인해야 하기 때문입니다. |
| 지금 비어 있는 회의실, 현재 환율처럼 시점 값이 중요함 | 실시간 상태 조회가 필요한가 | 문서 설명이 아니라 현재 시스템 값이 답의 출발점이기 때문입니다. |
| 파일 수정, 예약 생성처럼 세계 상태를 바꿔야 함 | 실제 실행과 승인 구조가 필요한가 | 설명만으로는 작업이 끝나지 않고, 권한과 실패 처리까지 함께 따라오기 때문입니다. |

같은 기준을 더 짧은 실무 질문으로 바꾸면 다음처럼 읽을 수 있습니다.

| 이런 의심이 들면 | 먼저 던질 질문 |
| --- | --- |
| `이건 문서만 읽어도 답할 수 있나?` | 필요한 것이 규정 설명인가, 현재 값 조회인가? |
| `설명은 그럴듯한데 숫자가 맞는지 불안하다` | 추정 대신 계산 도구 결과를 먼저 가져와야 하는가? |
| `답은 할 수 있겠지만 믿기 어렵다` | 추정 문장 대신 실제 조회값이나 계산값을 가져와야 하는가? |
| `설명은 충분한데 작업은 아직 안 끝났다` | 실제 파일·예약·상태를 바꾸는 실행 단계가 필요한가? |

먼저 익혀야 하는 기준은 단순합니다. tool use는 `외부 정보를 더 붙이는 방법`이 아니라, `조회`, `계산`, `실행`처럼 문서 읽기 밖의 결과를 실제로 가져오거나 발생시키는 연결 구조입니다.

## 요청 분기를 실행 기록으로 확인하기

예제의 목표는 실제 외부 API를 붙이는 것이 아니라, `사용자 요청`, `도구 필요 판단`, `도구 호출 계획`, `도구 실행 결과`, `최종 답변`이 서로 다른 단계라는 점을 눈으로 확인하는 것입니다. 한 요청만 보면 `환율 조회 = 도구 필요` 정도로 끝나기 쉬우므로, 여러 요청을 한 번에 돌려 어떤 요청은 설명만으로 닫히고, 어떤 요청은 조회·계산·실행 위임으로 갈라지는지 같이 봅니다.

어떤 요청은 실시간 조회가 필요해 도구를 써야 하고, 어떤 요청은 일반 설명이므로 도구 없이도 답할 수 있습니다. 또 어떤 요청은 실제 예약처럼 외부 상태를 바꾸므로 바로 실행하지 않고 승인 대기 상태로 멈춰야 합니다. 따라서 먼저 `도구가 필요한가`를 판단하고, 필요한 경우에도 조회인지 계산인지 실행인지, 실행해도 되는지까지 나누어야 합니다.

아래 예제는 사용자 요청 CSV, 로컬 LLM의 분기 제안, 애플리케이션 guard의 최종 판단, 도구가 돌려주는 조회·계산 결과, 실행 승인 대기 상태를 사용합니다. `ollama`가 설치되어 있고 `AIBOOK_OLLAMA_MODEL` 환경 변수로 지정한 모델이 준비되어 있으면 모델이 먼저 요청 유형을 제안합니다. 모델에 넘기는 프롬프트와 `model_request_en`은 영어로 둡니다. 이렇게 하면 작은 로컬 모델의 분기 안정성이 좋아질 뿐 아니라, 한국어·영어·중국어 번역본에서도 같은 실행 기준을 유지하기 쉽습니다. 로컬 모델이 없거나 모델 출력이 흔들려도 애플리케이션 guard가 최종 실행 route를 확정하므로 같은 코드를 실행할 수 있습니다. 출력에서는 요청별 모델 제안, guard 보정 여부, 도구 호출 구조, 실행 결과, 최종 답변을 확인합니다.

입력 CSV [p6-13-1-tool-use-requests.csv](../../../assets/part-06/chapter-13/p6-13-1-tool-use-requests.csv){ .csv-preview }는 18개의 요청을 담습니다. `user_request_ko`는 독자에게 보여 줄 한국어 원문이고, `model_request_en`은 모델 판단용 영어 요청입니다. `request_signal`은 애플리케이션이 실행 전 guard에서 확인하는 최소 신호입니다. 이 신호는 모델에게 줄 정답표가 아니라, 실제 서비스 코드가 실행 전에 확인해야 하는 정보 부족, 상태 변경, 계산 필요 여부를 단순화한 입력입니다.

먼저 이 예제에서 같이 볼 항목을 표로 정리하면 다음과 같습니다.

| 점검 항목 | 왜 필요한가 |
| --- | --- |
| `model_route` | 모델이 어떤 실행 방향을 먼저 제안했는지 확인 |
| `guard_changed_model_route` | 모델 제안을 애플리케이션이 실행 전에 바로잡았는지 확인 |
| `needs_tool` | 어떤 요청이 실행 단계로 넘어가야 하는지 판단 |
| `tool_selected` | 필요한 기능을 맞게 골랐는지 확인 |
| `tool_result_used` | 실제 실행 결과가 최종 답에 반영됐는지 확인 |
| `skipped_tool_when_not_needed` | 도구가 필요 없는 요청에 불필요한 호출을 하지 않는지 확인 |
| `approval_required` | 외부 상태를 바꾸는 요청을 바로 실행하지 않고 멈추는지 확인 |
| `missing_info` | 도구가 필요해도 필수 정보가 없으면 질문을 되돌리는지 확인 |

코드에서 확인할 핵심은 모델 제안만으로 바로 실행하지 않고, 실행 전 guard를 거쳐 호출 필요 여부와 승인 필요 여부를 확정한다는 점입니다. 호출했다면 실행 결과가 최종 답에 반영되어야 합니다.

```python
import csv
import os
import re
import subprocess
from pathlib import Path

CSV_PATH = Path("docs/assets/part-06/chapter-13/p6-13-1-tool-use-requests.csv")

with CSV_PATH.open(encoding="utf-8", newline="") as csv_file:
    requests = list(csv.DictReader(csv_file))

ROUTE_LABELS = {
    "no_tool": "일반 설명",
    "lookup": "외부 조회",
    "lookup_compute": "외부 조회 뒤 계산",
    "compute": "계산",
    "action_pending": "승인 필요한 실행",
    "needs_info": "정보 부족",
}

OLLAMA_MODEL = os.environ.get("AIBOOK_OLLAMA_MODEL", "qwen2.5:1.5b")

def clean_ollama_output(raw):
    return re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", raw).strip()

def ask_ollama_for_route(request):
    prompt = f"""
Classify the request into exactly one route label.
Return only one label, with no explanation.

Labels:
- no_tool: general explanation only
- lookup: current value or external state lookup
- lookup_compute: lookup a current value and then compute from it
- compute: calculation only
- action_pending: external state change that needs approval before execution
- needs_info: missing required date, target, amount, or other execution detail

Decision rules:
- If the request asks "what is it" or asks for a concept explanation, use no_tool.
- If the request asks for today's exchange rate, use lookup.
- If the request asks to calculate money using today's exchange rate, use lookup_compute.
- If the request asks for repeated discount calculation, use compute.
- If the request asks to check room availability, use lookup.
- If the request asks to reserve, send, write, or modify something, use action_pending.
- If the request asks for an exchange rate but gives no date such as today, use needs_info.
- If the request lacks the room, amount, file, recipient, or date needed for execution, use needs_info.

Request: {request["model_request_en"]}
""".strip()

    try:
        completed = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL, prompt],
            text=True,
            capture_output=True,
            timeout=45,
            check=True,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.CalledProcessError) as error:
        return {"model_route": None, "model_raw": error.__class__.__name__}

    raw = clean_ollama_output(completed.stdout)
    route = next((token for token in re.split(r"[\s,;:]+", raw) if token in ROUTE_LABELS), None)
    if route not in ROUTE_LABELS:
        route = None
    return {"model_route": route, "model_raw": raw[:80]}

def guard_route(request):
    signal = request["request_signal"]
    if signal == "concept_only":
        return {"route": "no_tool", "guard_reason": "개념 설명만으로 답할 수 있습니다."}
    if signal in {"current_exchange_rate", "calendar_lookup", "mixed_lookup"}:
        return {"route": "lookup", "guard_reason": "현재 값이나 외부 상태 조회가 필요합니다."}
    if signal == "exchange_rate_conversion":
        return {"route": "lookup_compute", "guard_reason": "오늘 환율 조회와 금액 계산이 함께 필요합니다."}
    if signal == "pure_calculation":
        return {"route": "compute", "guard_reason": "외부 조회 없이 계산 도구로 확인할 수 있습니다."}
    if signal == "state_change":
        return {"route": "action_pending", "guard_reason": "외부 상태를 바꾸는 실행 요청입니다."}
    if signal in {"missing_date", "missing_target", "missing_amount"}:
        return {"route": "needs_info", "guard_reason": "도구 실행에 필요한 정보가 부족합니다."}
    return {"route": "needs_info", "guard_reason": "분기 기준을 확정할 정보가 부족합니다."}

def propose_route(request):
    model_hint = ask_ollama_for_route(request)
    guarded = guard_route(request)
    return {
        "route": guarded["route"],
        "route_label": ROUTE_LABELS[guarded["route"]],
        "route_source": f"app_guard_after_ollama:{OLLAMA_MODEL}",
        "guard_reason": guarded["guard_reason"],
        "model_route": model_hint["model_route"],
        "model_raw": model_hint["model_raw"],
        "guard_changed_model_route": model_hint["model_route"] != guarded["route"],
    }

def build_tool_call(request, route_proposal):
    signal = request["request_signal"]
    route = route_proposal["route"]
    base = {
        "route": route,
        "route_label": route_proposal["route_label"],
        "route_source": route_proposal["route_source"],
        "guard_reason": route_proposal["guard_reason"],
        "model_route": route_proposal["model_route"],
        "model_raw": route_proposal["model_raw"],
        "guard_changed_model_route": route_proposal["guard_changed_model_route"],
    }

    if route == "action_pending":
        tool_name = {
            "state_change": "external_action_request",
        }.get(signal, "external_action_request")
        return {
            **base,
            "tool": tool_name,
            "arguments": {"action_request": request["model_request_en"]},
            "approval_required": True,
        }
    if route == "needs_info":
        missing_by_signal = {
            "missing_date": ["date"],
            "missing_target": ["room", "date", "time"],
            "missing_amount": ["amount", "discount_rate"],
        }
        return {
            **base,
            "tool": None,
            "arguments": {},
            "missing_info": missing_by_signal.get(signal, ["required_detail"]),
            "approval_required": False,
        }
    if route == "lookup_compute":
        return {
            **base,
            "tool": "exchange_rate_lookup",
            "arguments": {"base_currency": "USD", "quote_currency": "KRW", "date": "today", "amount": 300},
            "approval_required": False,
        }
    if route == "lookup" and signal == "calendar_lookup":
        return {
            **base,
            "tool": "calendar_lookup",
            "arguments": {"floor": "3층", "date": "tomorrow", "time": "afternoon"},
            "approval_required": False,
        }
    if route == "lookup" and signal == "mixed_lookup":
        return {
            **base,
            "tool": "combined_lookup",
            "arguments": {"queries": ["exchange_rate_lookup", "calendar_lookup"]},
            "approval_required": False,
        }
    if route == "lookup":
        return {
            **base,
            "tool": "exchange_rate_lookup",
            "arguments": {"base_currency": "USD", "quote_currency": "KRW", "date": "today"},
            "approval_required": False,
        }
    if route == "compute":
        return {
            **base,
            "tool": "discount_calculator",
            "arguments": {"discount_rate": 0.137, "repeat": 3},
            "approval_required": False,
        }
    return {**base, "tool": None, "arguments": {}, "approval_required": False}

def execute_tool(tool_call):
    # 예제에서는 실제 API 대신 고정된 실행 결과를 돌려줍니다.
    if tool_call["approval_required"] or tool_call["tool"] is None:
        return None
    if tool_call["tool"] == "exchange_rate_lookup":
        rate = 1382.4
        amount = tool_call["arguments"].get("amount")
        return {
            "rate": rate,
            "converted_krw": round(amount * rate, 1) if amount else None,
            "as_of": "2026-06-30 10:00 KST",
        }
    if tool_call["tool"] == "discount_calculator":
        remaining_ratio = (1 - tool_call["arguments"]["discount_rate"]) ** tool_call["arguments"]["repeat"]
        return {"remaining_ratio": round(remaining_ratio, 4)}
    if tool_call["tool"] == "calendar_lookup":
        return {"available_rooms": ["3층 B회의실"], "checked_at": "2026-06-30 10:00 KST"}
    if tool_call["tool"] == "combined_lookup":
        return {
            "rate": 1382.4,
            "available_rooms": ["3층 B회의실"],
            "checked_at": "2026-06-30 10:00 KST",
        }
    return {"error": "unknown tool"}

def compose_final_answer(request, tool_call, tool_result=None):
    text = request["user_request_ko"]
    if tool_call["route"] == "no_tool":
        return "환율은 한 통화가 다른 통화와 교환될 때 적용되는 비율입니다."
    if tool_call["route"] == "needs_info":
        return "조회 기준 날짜가 필요합니다. 오늘 기준인지 특정 날짜 기준인지 알려 주세요."
    if tool_call["route"] == "action_pending":
        return "회의실 예약은 외부 일정을 변경하므로 승인 후 실행해야 합니다."
    if tool_call["tool"] == "exchange_rate_lookup" and tool_result["converted_krw"] is not None:
        return f"300달러는 {tool_result['converted_krw']}원입니다. 기준 시각은 {tool_result['as_of']}입니다."
    if tool_call["tool"] == "exchange_rate_lookup":
        return f"오늘 USD/KRW 환율은 {tool_result['rate']}원입니다. 기준 시각은 {tool_result['as_of']}입니다."
    if tool_call["tool"] == "discount_calculator":
        return f"세 번 할인 뒤 남는 비율은 {tool_result['remaining_ratio']}입니다."
    if tool_call["tool"] == "calendar_lookup":
        return f"조회 결과 사용 가능한 회의실은 {', '.join(tool_result['available_rooms'])}입니다."
    if tool_call["tool"] == "combined_lookup":
        return f"오늘 USD/KRW 환율은 {tool_result['rate']}원이고, 사용 가능한 회의실은 {', '.join(tool_result['available_rooms'])}입니다."
    return text

def result_value_used(tool_result, final_answer):
    if tool_result is None:
        return False
    for value in tool_result.values():
        if isinstance(value, list) and any(str(item) in final_answer for item in value):
            return True
        if value is not None and not isinstance(value, list) and str(value) in final_answer:
            return True
    return False

reports = []
for request in requests:
    route_proposal = propose_route(request)
    tool_call = build_tool_call(request, route_proposal)
    tool_result = execute_tool(tool_call)
    final_answer = compose_final_answer(request, tool_call, tool_result)
    inspection = {
        "route": tool_call["route"],
        "route_source": tool_call["route_source"],
        "model_route": tool_call["model_route"],
        "guard_changed_model_route": tool_call["guard_changed_model_route"],
        "needs_tool": tool_call["tool"] is not None,
        "tool_selected": tool_call["tool"],
        "tool_executed": tool_result is not None,
        "tool_result_used": result_value_used(tool_result, final_answer),
        "skipped_tool_when_not_needed": tool_call["route"] == "no_tool" and tool_result is None,
        "approval_required": tool_call["approval_required"],
        "missing_info": tool_call["route"] == "needs_info",
    }
    reports.append(
        {
            "id": request["id"],
            "request": request,
            "tool_call": tool_call,
            "tool_result": tool_result,
            "final_answer": final_answer,
            "inspection": inspection,
        }
    )

route_counts = {}
for report in reports:
    route = report["inspection"]["route"]
    route_counts[route] = route_counts.get(route, 0) + 1

summary = {
    "needs_tool_count": sum(report["inspection"]["needs_tool"] for report in reports),
    "tool_executed_count": sum(report["inspection"]["tool_executed"] for report in reports),
    "tool_result_used_count": sum(report["inspection"]["tool_result_used"] for report in reports),
    "skipped_tool_count": sum(report["inspection"]["skipped_tool_when_not_needed"] for report in reports),
    "approval_pending_count": sum(report["inspection"]["approval_required"] for report in reports),
    "missing_info_count": sum(report["inspection"]["missing_info"] for report in reports),
    "model_hint_count": sum(report["inspection"]["model_route"] is not None for report in reports),
    "guard_changed_model_route_count": sum(report["inspection"]["guard_changed_model_route"] for report in reports),
    "route_counts": route_counts,
    "route_sources": sorted({report["inspection"]["route_source"] for report in reports}),
}

print("[summary]")
print(summary)
print()

for report in reports:
    if report["id"] not in {"R01", "R06", "R12", "R15", "R18"}:
        continue
    print("=" * 80)
    print("[request_id]")
    print(report["id"])
    print("[user_request]")
    print(report["request"]["user_request_ko"])
    print("[model_request]")
    print(report["request"]["model_request_en"])
    print("[tool_call]")
    print(report["tool_call"])
    print("[tool_result]")
    print(report["tool_result"])
    print("[final_answer]")
    print(report["final_answer"])
    print("[inspection]")
    print(report["inspection"])
```

실행 결과 예시는 다음처럼 읽을 수 있습니다. 아래 출력은 CSV 18행을 `qwen2.5:1.5b`로 한 번 실제 실행해 확인한 결과입니다.

```text
[summary]
{'needs_tool_count': 12, 'tool_executed_count': 9, 'tool_result_used_count': 9, 'skipped_tool_count': 3, 'approval_pending_count': 3, 'missing_info_count': 3, 'model_hint_count': 18, 'guard_changed_model_route_count': 4, 'route_counts': {'no_tool': 3, 'lookup': 5, 'lookup_compute': 2, 'compute': 2, 'action_pending': 3, 'needs_info': 3}, 'route_sources': ['app_guard_after_ollama:qwen2.5:1.5b']}

================================================================================
[request_id]
R01
[user_request]
환율이 무엇인지 한 문단으로 설명해 주세요.
[model_request]
Explain what an exchange rate is in one paragraph.
[tool_call]
{'route': 'no_tool', 'route_label': '일반 설명', 'route_source': 'app_guard_after_ollama:qwen2.5:1.5b', 'guard_reason': '개념 설명만으로 답할 수 있습니다.', 'model_route': 'no_tool', 'model_raw': 'no_tool', 'guard_changed_model_route': False, 'tool': None, 'arguments': {}, 'approval_required': False}
[tool_result]
None
[final_answer]
환율은 한 통화가 다른 통화와 교환될 때 적용되는 비율입니다.
[inspection]
{'route': 'no_tool', 'route_source': 'app_guard_after_ollama:qwen2.5:1.5b', 'model_route': 'no_tool', 'guard_changed_model_route': False, 'needs_tool': False, 'tool_selected': None, 'tool_executed': False, 'tool_result_used': False, 'skipped_tool_when_not_needed': True, 'approval_required': False, 'missing_info': False}
================================================================================
[request_id]
R06
[user_request]
오늘 환율로 300달러가 원화로 얼마인지 계산해 주세요.
[model_request]
Using today's exchange rate, calculate how much 300 USD is in KRW.
[tool_call]
{'route': 'lookup_compute', 'route_label': '외부 조회 뒤 계산', 'route_source': 'app_guard_after_ollama:qwen2.5:1.5b', 'guard_reason': '오늘 환율 조회와 금액 계산이 함께 필요합니다.', 'model_route': 'lookup_compute', 'model_raw': 'lookup_compute', 'guard_changed_model_route': False, 'tool': 'exchange_rate_lookup', 'arguments': {'base_currency': 'USD', 'quote_currency': 'KRW', 'date': 'today', 'amount': 300}, 'approval_required': False}
[tool_result]
{'rate': 1382.4, 'converted_krw': 414720.0, 'as_of': '2026-06-30 10:00 KST'}
[final_answer]
300달러는 414720.0원입니다. 기준 시각은 2026-06-30 10:00 KST입니다.
[inspection]
{'route': 'lookup_compute', 'route_source': 'app_guard_after_ollama:qwen2.5:1.5b', 'model_route': 'lookup_compute', 'guard_changed_model_route': False, 'needs_tool': True, 'tool_selected': 'exchange_rate_lookup', 'tool_executed': True, 'tool_result_used': True, 'skipped_tool_when_not_needed': False, 'approval_required': False, 'missing_info': False}
================================================================================
[request_id]
R12
[user_request]
내일 오후 3층 A회의실을 예약해 주세요.
[model_request]
Reserve meeting room A on the third floor for tomorrow afternoon.
[tool_call]
{'route': 'action_pending', 'route_label': '승인 필요한 실행', 'route_source': 'app_guard_after_ollama:qwen2.5:1.5b', 'guard_reason': '외부 상태를 바꾸는 실행 요청입니다.', 'model_route': 'action_pending', 'model_raw': 'action_pending', 'guard_changed_model_route': False, 'tool': 'external_action_request', 'arguments': {'action_request': 'Reserve meeting room A on the third floor for tomorrow afternoon.'}, 'approval_required': True}
[tool_result]
None
[final_answer]
회의실 예약은 외부 일정을 변경하므로 승인 후 실행해야 합니다.
[inspection]
{'route': 'action_pending', 'route_source': 'app_guard_after_ollama:qwen2.5:1.5b', 'model_route': 'action_pending', 'guard_changed_model_route': False, 'needs_tool': True, 'tool_selected': 'external_action_request', 'tool_executed': False, 'tool_result_used': False, 'skipped_tool_when_not_needed': False, 'approval_required': True, 'missing_info': False}
================================================================================
[request_id]
R15
[user_request]
USD 환율을 알려 주세요.
[model_request]
Tell me the USD exchange rate.
[tool_call]
{'route': 'needs_info', 'route_label': '정보 부족', 'route_source': 'app_guard_after_ollama:qwen2.5:1.5b', 'guard_reason': '도구 실행에 필요한 정보가 부족합니다.', 'model_route': 'lookup', 'model_raw': 'lookup', 'guard_changed_model_route': True, 'tool': None, 'arguments': {}, 'missing_info': ['date'], 'approval_required': False}
[tool_result]
None
[final_answer]
조회 기준 날짜가 필요합니다. 오늘 기준인지 특정 날짜 기준인지 알려 주세요.
[inspection]
{'route': 'needs_info', 'route_source': 'app_guard_after_ollama:qwen2.5:1.5b', 'model_route': 'lookup', 'guard_changed_model_route': True, 'needs_tool': False, 'tool_selected': None, 'tool_executed': False, 'tool_result_used': False, 'skipped_tool_when_not_needed': False, 'approval_required': False, 'missing_info': True}
================================================================================
[request_id]
R18
[user_request]
오늘 환율과 회의실 예약 가능 여부를 둘 다 확인해 주세요.
[model_request]
Check today's exchange rate and meeting room availability.
[tool_call]
{'route': 'lookup', 'route_label': '외부 조회', 'route_source': 'app_guard_after_ollama:qwen2.5:1.5b', 'guard_reason': '현재 값이나 외부 상태 조회가 필요합니다.', 'model_route': 'lookup_compute', 'model_raw': 'lookup_compute, lookup', 'guard_changed_model_route': True, 'tool': 'combined_lookup', 'arguments': {'queries': ['exchange_rate_lookup', 'calendar_lookup']}, 'approval_required': False}
[tool_result]
{'rate': 1382.4, 'available_rooms': ['3층 B회의실'], 'checked_at': '2026-06-30 10:00 KST'}
[final_answer]
오늘 USD/KRW 환율은 1382.4원이고, 사용 가능한 회의실은 3층 B회의실입니다.
[inspection]
{'route': 'lookup', 'route_source': 'app_guard_after_ollama:qwen2.5:1.5b', 'model_route': 'lookup_compute', 'guard_changed_model_route': True, 'needs_tool': True, 'tool_selected': 'combined_lookup', 'tool_executed': True, 'tool_result_used': True, 'skipped_tool_when_not_needed': False, 'approval_required': False, 'missing_info': False}
```

먼저 볼 것은 `route_counts`입니다. CSV에는 설명만으로 닫히는 요청 3개, 외부 조회 요청 5개, 조회 뒤 계산 요청 2개, 순수 계산 요청 2개, 승인 전 대기해야 하는 실행 요청 3개, 정보가 부족해 되물어야 하는 요청 3개가 들어 있습니다. 그래서 한두 개 예제로는 보이지 않던 `도구 호출`, `호출 보류`, `정보 보강 요청`, `승인 대기`의 차이가 한 번에 드러납니다.

다음으로 볼 것은 `model_route`와 `guard_changed_model_route`입니다. 모델 판단용 요청을 영어로 두면 R01의 개념 설명, R06의 조회 뒤 계산, R12의 예약 대기 같은 분기가 안정적으로 나옵니다. 그래도 R15처럼 기준 날짜가 없는 환율 요청은 모델이 조회로 보낼 수 있고, R18처럼 조회가 여러 개 섞인 요청은 모델이 `lookup_compute, lookup`처럼 두 후보를 함께 낼 수 있습니다. 그래서 애플리케이션 guard가 최종 route를 다시 확정합니다. tool use에서 모델 출력은 실행 제안이지, 곧바로 실행해도 되는 명령이 아니라는 점이 여기서 드러납니다.

그래서 이 예제에서 확인해야 할 결과는 세 가지입니다.

- 모델 출력이 곧바로 최종 답 문장이 아니라, 외부 기능 실행을 위한 구조화된 요청이 먼저 나오고 실제 실행 결과를 받은 뒤에야 최종 답변이 만들어진다.
- tool use에서는 `도구가 필요한 요청을 골라내는 판단`, `도구를 실제로 실행해도 되는지의 판단`, `실행 결과를 최종 답에 반영하는 단계`를 분리해서 봐야 한다.
- 정보가 부족하거나 승인이 필요한 요청은 도구 사용 구조 안에서도 바로 실행하지 않고 멈추는 것이 올바른 처리일 수 있다.

이 예제에서 독자가 직접 해 볼 수 있는 조정은 다음과 같습니다.

- CSV에 `내일 도쿄 기준 JPY 환율` 같은 요청 행을 추가해 정보 부족과 조회 분기가 어떻게 달라지는지 보기
- `model_request_en`의 영어 표현을 바꿔 모델 제안이 얼마나 안정적으로 유지되는지 보기
- `request_signal`을 바꿔 애플리케이션 guard가 최종 route를 어떻게 다시 확정하는지 보기
- `execute_tool`에 오류 응답을 넣어 실패 처리 흐름을 확인해 보기
- `compose_final_answer`를 바꿔 숫자뿐 아니라 출처나 경고 문구까지 함께 넣어 보기

이 예제에서 여기서 읽어야 할 핵심은 다음입니다.

- 사용자 요청과
- 도구 필요 판단과
- 도구 호출 구조와
- 실제 실행 결과와
- 최종 답변이 분리되어 있다는 점입니다

즉, tool use는 `대답` 이전에 `실행 준비 구조`를 만들고, 실행 결과를 다시 받아 최종 답으로 연결하는 단계라고 볼 수 있습니다.

요약 통계를 차트로 보면 도구 사용의 핵심 분기가 더 분명합니다. 왼쪽은 CSV 18행이 최종적으로 어떤 route로 확정됐는지 보여 주고, 오른쪽은 실제 실행 단계에서 어떤 일이 일어났는지 보여 줍니다. `도구 실행`은 9건이지만, `설명으로 종료`, `승인 대기`, `정보 부족`도 각각 3건씩 남습니다. 또 `guard 보정` 4건은 모델의 첫 제안과 애플리케이션의 최종 판단이 달랐던 요청입니다. tool use는 모든 요청을 외부 기능으로 보내는 일이 아니라, 실행이 필요한 요청과 멈춰야 하는 요청을 먼저 가르는 구조로 읽어야 합니다.

![도구 사용 예제의 요청 처리 분기 유형 비교](../../../assets/part-06/chapter-13/tool-use-decision-check-ko.png)

## 실행 위임에서 갈리는 요청 유형

이 예제는 모델이 직접 모든 일을 처리하는 것이 아니라, 어떤 순간에는 `설명`보다 `실행을 위임하는 구조`가 더 중요하다는 점을 보여 줍니다. 그래서 이후 AI 에이전트와 MCP 절을 읽을 때도 핵심은 말 잘하는 모델이 아니라, 언제 외부 기능으로 넘겨야 하는지를 판단하는 구조입니다.

## 도구 사용이 바꾸는 책임 경계

도구 사용의 핵심은 모델이 더 많은 사실을 아는 것이 아니라, 필요한 순간에 외부 기능으로 실행을 위임하고 그 결과를 다시 답변으로 연결하는 데 있습니다.

초기 LLM 사용 경험은 주로 `잘 말하는 모델`에 집중되어 있었습니다. 하지만 실서비스로 가면 곧 한계가 드러났습니다.

- 최신성 부족
- 계산 오류
- 실제 시스템과 단절

더 중요하게 붙잡아야 할 점은 `최신 문서를 읽는 일`과 `계산·조회·수정 같은 실제 기능을 실행하는 일`이 같은 문제가 아니라는 것입니다. 그래서 도구 사용은 답변을 더 길게 만드는 보강이 아니라, 프롬프트와 RAG만으로 닫히지 않는 실행 문제를 별도 연결 구조로 넘기는 단계로 읽는 편이 좋습니다.

이 구조가 중요한 이유는 다음과 같습니다.

- RAG와 도구 사용을 섞지 않게 하고
- 이후 함수 호출, AI 에이전트, MCP를 이해할 준비를 시키며
- `LLM은 혼자 일하지 않는다`는 서비스 구조 관점을 강화하기 때문입니다

## 체크리스트
- 도구 사용을 `모델이 스스로 실행한다`가 아니라 `애플리케이션이 외부 기능을 연결해 실제 결과를 가져오는 구조`로 설명할 수 있어야 합니다.
- RAG가 문서 근거를 붙이는 구조이고, tool use는 조회·계산·실행을 붙이는 구조라는 차이를 말할 수 있어야 합니다.
- 실행 요청은 다시 함수 이름과 인자 구조로 더 구체화된다는 점을 잡고 있어야 합니다.

## 출처와 참고 자료

- Shunyu Yao et al., [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629){: target="_blank" rel="noopener noreferrer" }, arXiv, 2022, 확인 날짜: 2026-07-19.
- OpenAI, [Using tools](https://developers.openai.com/api/docs/guides/tools){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, 확인 날짜: 2026-07-19.
- OpenAI, [Function calling](https://developers.openai.com/api/docs/guides/function-calling){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, 확인 날짜: 2026-07-19.
