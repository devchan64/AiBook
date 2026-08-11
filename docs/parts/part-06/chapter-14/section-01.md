# P6-15.1 중간 결과에 따라 다음 작업을 바꾸는 AI 에이전트

> Section ID: `P6-15.1`
> Version: `v2026.07.31`

AI 에이전트 흐름은 `goal`, `current_state`, `next_action`, `tool_result`, `observation`, `updated_plan`을 분리해 기록합니다. 이 기록이 있어야 단일 답변 생성과 중간 결과에 따라 다음 행동을 바꾸는 목표 흐름이 구분됩니다.

P6-14.2에서는 함수 호출(function calling)이 도구 사용을 구조화된 형식으로 표현하는 방식이라는 점을 보았습니다. 이제 질문은 도구 호출이 한 번으로 끝나지 않고, 여러 단계 작업을 이어 가야 할 때 무엇이라고 보아야 하는가로 커집니다.

AI 에이전트(AI agent)는 목표를 받고, 필요한 하위 작업을 이어 가며, 도구 사용과 관찰을 반복해 결과를 만드는 작업 구조다.

## 단일 호출과 목표 흐름의 차이

에이전트를 이해할 때 닫아야 할 문제는 `목표를 여러 단계로 이어 가는 실행 구조`와 단일 도구 호출을 구분하는 것입니다. 앞 장의 tool use가 `무엇을 한 번 조회하거나 실행할까`를 다뤘다면, agent는 여러 도구 호출과 문서 읽기 결과를 어떤 순서로 이어 붙이고 언제 멈추거나 다시 시도할지를 다룹니다.

따라서 agent를 넓은 제품 이름으로 잡기보다 `중간 결과를 보고 다음 행동이 바뀌는 목표 흐름`으로 읽는 편이 안전합니다. P6-14.2의 function calling이 한 번의 실행 요청을 검증 가능한 구조로 넘기는 문제였다면, agent는 여러 호출과 읽기를 어떤 순서로 이어 갈지와 상태 관리를 다룹니다. 루프가 실제로 어떻게 계획, 행동, 관찰로 움직이는지는 P6-15.2에서 더 자세히 봅니다.

여기서 남겨야 할 기록은 단계 계획, 중간 관찰 메모, 다음 단계입니다. 이 기록이 있어야 다음 행동이 왜 바뀌었는지, 흐름 단위 실패가 어디서 생겼는지 나중에 다시 읽을 수 있습니다. 어디서 멈추고 사람 검토로 넘길지는 바로 다음 P6-15.2에서 더 구체적으로 봅니다.

## 에이전트로 읽어야 하는 장면

여기서 고정할 구분은 agent를 새로운 제품 이름처럼 외우는 일이 아니라, 어떤 장면에서 `도구를 여러 개 썼다`와 `중간 결과를 보고 다음 행동이 바뀐다`를 갈라 읽는 일입니다. 한 번의 답변이 길다고 해서 곧바로 agent가 되는 것은 아닙니다. 반대로 출력은 짧아도, 그 출력에 이르기까지 검색 결과를 보고 다시 찾고, 도구 실행 결과를 보고 다른 도구를 고르고, 실패하면 멈추거나 사람에게 넘기는 흐름이 있으면 AI 에이전트 구조에 가까워집니다.

| 먼저 보인 장면 | agent로 먼저 읽어야 하는가 | 왜 이렇게 갈라지는가 |
| --- | --- | --- |
| 조회나 실행 한 번으로 답이 거의 닫힘 | 보통 아니다 | 한 번의 tool use나 RAG로도 충분할 수 있기 때문입니다. |
| 중간 결과를 보고 검색어, 도구, 다음 단계가 바뀜 | 그렇다 | 다음 행동 선택 자체가 문제로 떠오르기 때문입니다. |
| 실패 뒤에 재시도, 멈춤, handoff 기준까지 같이 정해야 함 | 그렇다 | 답 한 번보다 목표 흐름과 상태 관리가 더 중요해지기 때문입니다. |

이 표를 잡고 아래의 agent 설명, 상태(state), 사례를 읽으면, agent를 `도구를 많이 쓰는 것`보다 `다음 단계 선택이 계속 바뀌는 목표 흐름`으로 더 쉽게 붙잡을 수 있습니다.

## 읽기와 실행을 목표 순서로 묶는 구조

프롬프트(prompt)는 입력을 설계합니다. RAG는 외부 문서를 찾아 답변 근거로 붙입니다. Tool use는 외부 기능을 호출합니다. Function calling은 그 호출을 이름과 인자 구조로 정리합니다.

에이전트에서 새로 중요해지는 것은 이 요소들을 `목표 흐름` 안에 배치하는 일입니다. 한 번의 도구 호출과 달리 중간 결과를 보고 다음 행동을 바꾸며, 중심도 한 번의 답변에서 목표 중심 워크플로우로 이동합니다. 그래서 agent를 이해할 때는 `무엇을 한 번 실행했는가`보다 `현재 상태를 보고 다음에 무엇을 하기로 골랐는가`를 먼저 봐야 합니다.

예를 들어 어떤 목표가:

- 정보를 찾고
- 필요한 도구를 고르고
- 중간 결과를 읽고
- 다음 행동을 바꾸고
- 실패하면 다시 시도하고
- 최종 결과를 정리하는

흐름으로 이어진다면, 이것은 단순 단발 요청보다 AI 에이전트 구조에 가깝습니다.

즉, 에이전트는 `한 번의 응답`보다 `목표를 향한 작업 흐름`에 중심이 있습니다.

## 대화 인터페이스와 작업 조율 구조의 차이

종종 agent를 `더 똑똑한 챗봇` 정도로 이해합니다. 하지만 더 안전한 설명은 다음과 같습니다.

`에이전트는 대화형 인터페이스를 가질 수 있지만, 핵심은 대화 자체가 아니라 목표를 위해 작업 단계를 이어 가는 실행 구조에 있다.`

예를 들어 에이전트는 다음을 할 수 있습니다.

- 질문을 다시 분해하기
- 문서를 검색하기
- 파일을 읽기
- 테스트를 실행하기
- 실패 원인을 보고 다시 시도하기

이런 흐름은 단순한 한 번의 답변보다 `작업 조율 구조`에 더 가깝습니다.

## 프롬프트·RAG·tool use·agent의 층위

| 구조 | 먼저 다루는 대상 | 바로 필요한 판단 | 결과가 닫히는 방식 |
| --- | --- | --- | --- |
| 프롬프트(prompt) | 사용자 입력과 지시 | 어떻게 물을까 | 한 번의 모델 응답 |
| RAG | 문서와 근거 | 어떤 문서를 붙일까 | 근거가 붙은 답변 |
| tool use | 외부 기능 | 어떤 기능을 호출할까 | 조회값, 계산값, 실행 결과 |
| function calling | 도구 호출 형식 | 어떤 이름과 인자로 넘길까 | 검증 가능한 호출 요청 |
| AI agent | 여러 단계 상태 | 다음에 무엇을 하고 언제 멈출까 | 목표를 향해 이어지는 작업 흐름 |

이 표의 핵심은 agent가 단순히 도구를 더 많이 붙인 버전이 아니라, `다음 단계 선택` 자체를 중심 문제로 바꾼다는 점입니다. 그래서 agent 설명은 기능 목록을 늘리는 일이 아니라, 앞의 읽기와 실행을 `목표 기준 순서 결정`으로 다시 묶는 일입니다.

Chapter 12~14의 최소 차이는 아래 표처럼 다시 고정할 수 있습니다.

| 현재 층위 | 핵심 질문 | 이어지는 중심 |
| --- | --- | --- |
| tool use | 무엇을 실제로 조회하거나 실행할까? | 실행 요청을 어떤 이름과 인자 구조로 넘길까 |
| function calling | 그 실행 요청을 어떻게 검증 가능한 구조로 만들까? | 여러 호출을 어떤 목표 순서로 이어 갈까 |
| AI agent | 여러 읽기와 실행을 어떤 목표 흐름으로 이어 갈까? | 그 흐름을 어떤 공통 연결 형식과 실행 기록 안에 둘까 |
| MCP / harness | 연결을 어떤 형식으로 드러내고 실행을 어떤 기록으로 남길까? | 남긴 기록을 어떤 평가와 운영 판단으로 읽을까 |

## 상태(state)가 없으면 다음 행동도 흔들린다

여러 단계 작업을 이어 가려면 시스템은 중간 상태를 알아야 합니다.

예를 들어:

- 이미 어떤 문서를 읽었는가
- 어떤 도구 호출이 성공했는가
- 어떤 오류가 발생했는가
- 다음에 무엇을 해야 하는가

이런 정보가 없으면 에이전트는 매 단계마다 맥락을 잃고 같은 실수를 반복할 수 있습니다.

따라서 agent는 단순한 출력 생성보다 `상태를 가진 실행`에 더 가깝습니다.

이 점 때문에 agent 설명에서는 `왜?`라는 질문에 답하기 위해 현재 단계, 이전 결과, 남은 목표를 함께 봐야 합니다.

## 실무 요청이 단일 답변을 넘어설 때

구분해야 할 점은 `설명을 한 번 돌려주는 일`과 `여러 단계 작업을 끝까지 이어 가는 일`이 같은 문제가 아니라는 것입니다. 그래서 agent가 필요한 장면은 보통 다음처럼 `중간 결과를 보고 다음 행동을 다시 골라야 하는가`로 드러납니다.

- 단순 설명을 넘어서
- 실제 자료를 모으고
- 도구를 사용하고
- 결과를 다시 정리하고
- 끝까지 처리해 주는 흐름

즉, 요청이 한 번의 답변으로 닫히지 않고 `읽기 -> 실행 -> 확인 -> 다음 행동 선택`으로 이어지기 시작하면, 그 장면은 단일 응답보다 AI 에이전트 구조로 읽는 편이 더 정확합니다.

예를 들어:

- 개발 보조
- 리서치 보조
- 문서 처리 자동화
- 고객 대응 워크플로우

같은 곳에서 AI 에이전트 구조가 두드러집니다.

## 목표 흐름이 늘리는 운영 복잡도

이 점도 반드시 같이 넣어야 합니다.

에이전트가 있다고 해서:

- 항상 올바른 계획을 세우는 것
- 무한 반복을 피하는 것
- 잘못된 도구 호출을 모두 막는 것
- 비용과 지연 시간을 자동으로 최적화하는 것

을 자동으로 해결하는 것은 아닙니다. 그래서 계속 확인해야 할 결과는 `여러 단계를 이어 갈 수 있는가`만이 아니라, `어디서 멈추고 다시 계획하며 사람에게 넘겨야 하는가`까지 구조 안에 드러나는가입니다.

오히려 단계가 늘어나면:

- 실패 지점이 늘고
- 로그가 더 필요하며
- 승인과 권한 관리가 중요해지고
- 평가와 재현성이 더 어려워질 수 있습니다

즉, agent는 능력을 넓히는 동시에 운영 복잡도도 크게 키웁니다.

## 목표에서 관찰로 이어지는 기본 흐름

```mermaid
--8<-- "assets/part-06/chapter-14/p6-c14-s01-agent-flow-ko.mmd"
```

이 도식의 핵심은 agent가 `질문 -> 답변` 한 번으로 끝나는 구조가 아니라, `목표 -> 단계 선택 -> 실행 -> 관찰`의 반복 구조라는 점입니다.

## 중간 관찰이 행동을 바꾸는 사례

### 사례 1. 코딩 에이전트

사용자가 `로그인 오류를 고쳐 달라`고 요청하면, 사람은 `원인 설명 한 번`이나 `수정 코드 한 조각`을 기대하기 쉽습니다. 하지만 실제 코딩 에이전트는 관련 파일을 찾고 오류 지점을 읽은 뒤 패치를 적용하고 테스트를 다시 실행합니다.

예를 들어 첫 수정 후 테스트가 다른 인증 예외를 새로 드러내면, 거기서 멈추지 않고 다음 수정으로 이어 가야 합니다. 사람이 중간 결과를 확인해 보듯이, 에이전트도 테스트 실패나 새 오류 메시지를 보고 다음 행동을 바꿉니다. 이 관찰을 무시하면 원래 오류 하나는 줄여도 다른 회귀를 남긴 채 끝날 수 있습니다.

여기서 바뀌는 기준은 `수정 코드 한 번을 내놓는가`에서 `테스트 결과를 보고 다음 행동을 바꾸는 흐름이 있는가`로 이동합니다. 이런 구조는 `답변 한 번`이 아니라 `읽기-수정-실행-재확인`이 이어지는 작업 흐름이므로 agent라고 부릅니다. 이 사례에서 확인해야 할 결과는 수정 코드 한 번으로 끝나는 것이 아니라, 테스트 결과를 보고 다음 행동이 실제로 바뀌는가입니다.

| 단계 | 중간 관찰 | 다음에 실제로 바뀌어야 하는 것 |
| --- | --- | --- |
| 파일 읽기 | 인증 로직 위치 확인 | 어디를 먼저 수정할지 |
| 패치 적용 | 코드 변경 완료 | 어떤 테스트를 돌릴지 |
| 테스트 실행 | 새 오류, 회귀, 실패 로그 | 다음 패치 방향과 재검증 순서 |

### 사례 2. 문서 조사 에이전트

사용자가 `최신 환불 정책을 근거와 함께 정리해 달라`고 요청하면, 검색 한 번으로 바로 답이 끝날 것처럼 느끼기 쉽습니다. 하지만 문서 조사 에이전트는 관련 공지와 규정 문서를 찾고, 사람이 수작업으로 조사할 때처럼 문서 날짜와 근거 수준을 확인한 뒤 부족하면 검색어를 바꾸거나 다른 출처를 더 읽습니다.

검색 첫 결과가 작년 공지라면 거기서 바로 요약하지 않고 최신 개정 문서를 다시 찾아야 합니다. 반대로 최신 공지는 찾았지만 세부 조건이 별도 규정 PDF에 있으면, 공지 하나만으로 끝내지 않고 그 PDF까지 다시 열어 근거를 보강해야 할 수 있습니다. 그렇지 않으면 겉보기에는 출처가 붙어 있어도 실제로는 오래된 근거를 붙이거나 핵심 조건을 빠뜨린 답이 됩니다.

여기서 바뀌는 기준은 `검색 결과 하나가 나왔는가`에서 `날짜와 근거 수준을 확인하며 재탐색하는가`로 이동합니다. 검색, 읽기, 요약, 출처 정리, 재탐색이 한 목표 아래에서 이어지기 때문에 단순 검색기보다 에이전트에 가깝습니다. 이 사례에서 확인해야 할 결과는 첫 검색 결과를 바로 요약하는 대신, 날짜와 근거 수준을 다시 확인하며 최신 문서를 끝까지 찾는가입니다.

| 단계 | 중간 관찰 | 다음에 실제로 바뀌어야 하는 것 |
| --- | --- | --- |
| 첫 검색 | 작년 공지, 불충분한 출처 | 검색어와 날짜 필터 |
| 문서 읽기 | 세부 조건 누락 | 추가 PDF나 규정 원문 열람 |
| 요약 직전 점검 | 출처는 있으나 최신성 불확실 | 재탐색 여부와 인용 근거 보강 |

### 사례 3. 업무 자동화 에이전트

사용자가 `오늘 접수된 긴급 문의를 찾아 담당자 캘린더까지 확인해 달라`고 요청할 수 있습니다. 사람은 이 요청을 문장 하나로 말하더라도, 실제 시스템에서는 메일함 조회, 긴급 여부 분류, 담당자 검색, 캘린더 확인, 결과 기록을 차례로 이어 가야 합니다.

긴급 문의로 분류된 항목이 세 개라면 담당자마다 다른 캘린더를 다시 조회하고, 일정이 겹치면 우선순위까지 다시 정해야 할 수 있습니다. 각 단계는 개별 도구 호출이지만, 핵심은 그 호출들을 하나의 업무 목표로 연결하고 중간 결과에 따라 다음 순서를 바꾸는 데 있습니다.

중간 결과를 보지 않고 처음 순서만 밀어붙이면, 긴급도가 낮은 건을 먼저 처리하거나 담당자 일정 충돌을 놓칠 수 있습니다. 여기서 바뀌는 기준은 `도구를 차례로 호출하는가`에서 `중간 결과에 따라 실제 순서와 우선순위가 바뀌는가`로 이동합니다. 이 사례에서 확인해야 할 결과는 도구 호출 목록을 나열하는 데 그치지 않고, 중간 결과에 따라 실제 작업 순서와 우선순위가 바뀌는가입니다.

사례를 작업 구조로 다시 펴 보면 다음처럼 읽을 수 있습니다.

| 상황 | 시작 목표 | 중간에 바뀌는 것 | agent로 읽어야 하는 이유 |
| --- | --- | --- | --- |
| 코딩 보조 | 오류 수정 | 테스트 로그에 따라 다음 패치 방향 | 한 번의 코드 제안이 아니라 재시도 루프가 필요해서 |
| 문서 조사 | 최신 근거 정리 | 검색어, 날짜 필터, 읽기 우선순위 | 첫 검색 결과로 바로 끝내면 오래된 근거가 남을 수 있어서 |
| 업무 자동화 | 긴급 문의 처리 | 우선순위, 담당자, 일정 충돌 처리 | 여러 시스템 결과를 보고 순서를 계속 바꿔야 해서 |

## 도구 개수보다 관찰에 따른 변화

AI 에이전트를 처음 읽을 때 가장 자주 놓치는 것은 `도구를 여러 개 쓴다`는 사실만 보고도 곧바로 agent라고 부르는 점입니다. 하지만 핵심은 도구 개수가 아니라 `중간 결과를 보고 다음 행동이 실제로 바뀌는가`에 있습니다.

먼저 던질 질문은 단순합니다. 검색하고 끝내는 한 번의 답변처럼 보인다면 중간 결과 뒤에 다음 선택이 실제로 생기는지 봅니다. 도구를 여러 개 쓰지만 순서가 항상 고정돼 있다면 관찰 결과에 따라 순서나 다음 단계가 바뀌는지 봅니다. 실패가 났을 때는 같은 순서를 밀어붙이는지, 아니면 다시 찾기나 재시도 같은 다른 행동으로 바뀌는지 봅니다.

먼저 익혀야 하는 기준은 `도구가 많은 시스템인가`가 아니라 `중간 관찰이 다음 행동 선택을 바꾸는가`입니다. 멈춤과 사람 검토의 세부 기준은 P6-15.2에서 계획, 행동, 관찰 루프와 함께 더 자세히 봅니다.

같은 내용을 작업 흐름 구조로 다시 보면 다음처럼 읽을 수 있습니다.

```mermaid
--8<-- "assets/part-06/chapter-14/p6-c14-s01-agent-state-loop-ko.mmd"
```

핵심은 `답변 한 번`이 아니라 `상태를 갱신하며 다음 행동을 다시 고르는 반복`입니다.

## 모델 제안과 guard 최종 행동 비교

예제의 목표는 실제 에이전트 프레임워크 전체를 구현하는 것이 아닙니다. 여기서 확인할 것은 관찰 결과가 달라지면 다음 행동도 달라져야 한다는 점입니다. 코딩 보조, 문서 조사, 업무 자동화는 서로 다른 작업이지만 agent 관점에서는 모두 현재 상태를 보고 다음 행동을 고르는 문제로 다시 읽을 수 있습니다. 관련 맥락을 못 찾은 상태, 오래된 맥락만 있는 상태, 근거가 부족한 상태, 실행이 실패한 상태, 사람 검토가 필요한 상태는 서로 다른 다음 행동을 요구합니다.

아래 예제는 관찰 상태 CSV [p6-14-1-agent-observation-states.csv](../../../assets/part-06/chapter-14/p6-14-1-agent-observation-states.csv){ .csv-preview }를 사용합니다. 한 행은 코딩 보조, 문서 조사, 업무 자동화 같은 작업에서 에이전트가 중간에 본 현재 상태를 뜻합니다. CSV의 `model_observation_en`은 모델에 넘기는 영어 관찰 문장이고, `found_context`, `current_context`, `detail_missing`, `conflict_found`, `action_failed`, `approval_needed`, `sources_attached`는 애플리케이션이 모델 제안을 점검할 때 쓰는 상태 신호입니다.

코드에서 확인할 핵심은 모델이 관찰 문장을 읽고 다음 행동을 제안하되, 애플리케이션이 그 제안을 그대로 믿지 않고 상태 신호로 다시 점검한다는 점입니다. 실행 전에 Ollama를 설치하고 모델을 받을 필요가 있습니다. 예를 들어 `ollama pull qwen2.5:1.5b`를 실행한 뒤 Ollama가 켜진 상태에서 코드를 실행합니다. 다른 모델을 쓰려면 `AIBOOK_OLLAMA_MODEL=모델명`처럼 환경 변수를 바꿉니다. 모델에 넘기는 프롬프트와 관찰 문장은 영어로 둡니다.

```python
from collections import Counter, defaultdict
from pathlib import Path
import csv
import json
import os
import urllib.request

CSV_PATH = Path("docs/assets/part-06/chapter-14/p6-14-1-agent-observation-states.csv")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/chat")
OLLAMA_MODEL = os.environ.get("AIBOOK_OLLAMA_MODEL", "qwen2.5:1.5b")

NEXT_ACTIONS = {
    "search_or_inspect",
    "refine_search_or_reload",
    "collect_supporting_context",
    "retry_with_changed_step",
    "compare_evidence",
    "handoff_for_review",
    "attach_sources",
    "finish",
}

ACTION_GUIDE = {
    "search_or_inspect": "no relevant context has been found yet",
    "refine_search_or_reload": "context exists but is stale or not current",
    "collect_supporting_context": "current context exists but important detail is missing",
    "retry_with_changed_step": "the previous action failed and needs a changed retry",
    "compare_evidence": "available evidence conflicts and must be compared",
    "handoff_for_review": "approval, permission, or risk requires human review",
    "attach_sources": "enough context exists but final evidence is not attached",
    "finish": "the task is already complete with evidence attached",
}

def as_bool(value):
    return value.strip().lower() == "true"

def guard_next_action(state):
    # guard는 정답표가 아니라, 모델 제안을 현재 상태 신호로 다시 점검하는 안전층입니다.
    if state["approval_needed"]:
        return "handoff_for_review"
    if state["action_failed"]:
        return "retry_with_changed_step"
    if state["conflict_found"]:
        return "compare_evidence"
    if not state["found_context"]:
        return "search_or_inspect"
    if not state["current_context"]:
        return "refine_search_or_reload"
    if state["detail_missing"]:
        return "collect_supporting_context"
    if not state["sources_attached"]:
        return "attach_sources"
    return "finish"

def build_prompt(observation):
    labels = "\n".join(f"- {label}: {description}" for label, description in ACTION_GUIDE.items())
    return f"""
You are choosing the next action for a small LLM AI agent workflow.
Return exactly one label and no explanation.

Allowed labels:
{labels}

Observation:
{observation}
""".strip()

def ask_ollama(prompt):
    payload = {
        "model": OLLAMA_MODEL,
        "stream": False,
        "messages": [{"role": "user", "content": prompt}],
        "options": {"temperature": 0},
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        result = json.loads(response.read().decode("utf-8"))
    return result["message"]["content"].strip()

def model_next_action(state):
    prompt = build_prompt(state["model_observation_en"])
    try:
        raw = ask_ollama(prompt)
    except Exception as error:
        return {"model_action": None, "model_raw": error.__class__.__name__}

    action = next((label for label in NEXT_ACTIONS if label in raw), None)
    return {"model_action": action, "model_raw": raw[:100]}

rows = []
with CSV_PATH.open(encoding="utf-8", newline="") as file:
    for row in csv.DictReader(file):
        state = {
            "case_id": row["case_id"],
            "domain": row["domain"],
            "observation_signal": row["observation_signal"],
            "model_observation_en": row["model_observation_en"],
            "found_context": as_bool(row["found_context"]),
            "current_context": as_bool(row["current_context"]),
            "detail_missing": as_bool(row["detail_missing"]),
            "conflict_found": as_bool(row["conflict_found"]),
            "action_failed": as_bool(row["action_failed"]),
            "approval_needed": as_bool(row["approval_needed"]),
            "sources_attached": as_bool(row["sources_attached"]),
        }
        model_hint = model_next_action(state)
        state["model_action"] = model_hint["model_action"]
        state["model_raw"] = model_hint["model_raw"]
        state["guard_action"] = guard_next_action(state)
        state["guard_changed_model_action"] = state["model_action"] != state["guard_action"]
        rows.append(state)

guard_counts = Counter(row["guard_action"] for row in rows)
model_counts = Counter(row["model_action"] or "model_unavailable" for row in rows)
domain_counts = defaultdict(Counter)
for row in rows:
    domain_counts[row["domain"]][row["guard_action"]] += 1

print("[model]")
print(
    {
        "model": OLLAMA_MODEL,
        "model_hint_count": sum(row["model_action"] is not None for row in rows),
        "guard_changed_model_action_count": sum(row["guard_changed_model_action"] for row in rows),
    }
)

print("\n[guard action counts]")
for action, count in guard_counts.most_common():
    print(f"{action}: {count}")

print("\n[model action counts]")
for action, count in model_counts.most_common():
    print(f"{action}: {count}")

print("\n[sample decisions]")
for row in rows[:8]:
    print(
        row["case_id"],
        row["observation_signal"],
        "model=",
        row["model_action"],
        "guard=",
        row["guard_action"],
        "changed=",
        row["guard_changed_model_action"],
    )

print("\n[domain split]")
for domain, counts in domain_counts.items():
    print(domain, dict(counts))
```

실행 결과 예시는 다음처럼 읽을 수 있습니다.

```text
[model]
{'model': 'qwen2.5:1.5b', 'model_hint_count': 36, 'guard_changed_model_action_count': 10}

[guard action counts]
handoff_for_review: 6
attach_sources: 6
finish: 6
refine_search_or_reload: 4
retry_with_changed_step: 4
compare_evidence: 4
search_or_inspect: 3
collect_supporting_context: 3

[model action counts]
attach_sources: 12
handoff_for_review: 7
search_or_inspect: 6
refine_search_or_reload: 3
collect_supporting_context: 3
retry_with_changed_step: 3
compare_evidence: 2

[sample decisions]
coding-01 no_related_file model= search_or_inspect guard= search_or_inspect changed= False
coding-02 old_error_log model= refine_search_or_reload guard= refine_search_or_reload changed= False
coding-03 missing_test_context model= collect_supporting_context guard= collect_supporting_context changed= False
coding-04 new_test_failure model= retry_with_changed_step guard= retry_with_changed_step changed= False
coding-05 security_sensitive_change model= handoff_for_review guard= handoff_for_review changed= False
coding-06 patch_ready_without_test_note model= attach_sources guard= attach_sources changed= False
coding-07 verified_patch_with_notes model= attach_sources guard= finish changed= True
coding-08 conflicting_test_results model= compare_evidence guard= compare_evidence changed= False

[domain split]
coding {'search_or_inspect': 1, 'refine_search_or_reload': 1, 'collect_supporting_context': 1, 'retry_with_changed_step': 2, 'handoff_for_review': 2, 'attach_sources': 2, 'finish': 2, 'compare_evidence': 1}
research {'search_or_inspect': 1, 'refine_search_or_reload': 2, 'collect_supporting_context': 1, 'compare_evidence': 1, 'handoff_for_review': 2, 'attach_sources': 2, 'finish': 2, 'retry_with_changed_step': 1}
workflow {'search_or_inspect': 1, 'refine_search_or_reload': 1, 'collect_supporting_context': 1, 'retry_with_changed_step': 1, 'compare_evidence': 2, 'handoff_for_review': 2, 'attach_sources': 2, 'finish': 2}
```

이 결과에서 먼저 봐야 할 것은 모델이 모든 관찰 상태에 대해 다음 행동을 제안했다는 점입니다. 하지만 `guard_changed_model_action_count`가 10이라는 점도 같이 봐야 합니다. 예를 들어 `verified_patch_with_notes`에서는 모델이 `attach_sources`를 제안했지만, 상태 신호에는 이미 `sources_attached`가 표시되어 있으므로 guard는 `finish`로 닫았습니다. 즉, agent 흐름에서는 모델의 제안 자체보다 `모델 제안`, `현재 상태`, `최종 다음 행동`을 함께 기록하는 구조가 중요합니다.

같은 이유로 `old_error_log`나 `stale_policy_notice`처럼 현재 기준이 아닌 근거가 보이면 다시 찾거나 다시 읽어야 합니다. `new_test_failure`나 `calendar_api_failed`처럼 실행 자체가 실패하면 같은 순서를 밀어붙이는 것이 아니라 다른 단계로 재시도해야 합니다. `security_sensitive_change`나 `manager_approval_required`처럼 권한 또는 승인 경계가 보이면 agent가 혼자 계속 진행하지 않고 사람 검토로 넘겨야 합니다.

![agent 다음 행동 분기](../../../assets/part-06/chapter-14/agent-state-progress-ko.png)

이 차트는 모델 제안과 guard 최종 행동의 차이를 보여 줍니다. 모델은 `attach_sources`를 비교적 자주 제안하지만, guard는 상태 신호를 다시 확인해 이미 근거가 붙은 사례를 `finish`로 닫습니다. 반대로 권한, 실패, 충돌 신호가 있으면 guard는 모델 제안과 별도로 사람 검토, 재시도, 근거 비교 쪽으로 최종 행동을 고정할 수 있습니다.

따라서 이 차트에서 읽어야 할 것은 모델이 틀렸다는 단순 결론이 아닙니다. agent 흐름에서는 모델이 다음 행동 후보를 제안하고, 애플리케이션이 현재 상태와 기록 기준으로 그 제안을 다시 좁힌다는 구조가 보인다는 점입니다.

그래서 이 예제에서 확인해야 할 결과는 두 가지입니다.

- 모델은 관찰 문장을 읽고 다음 행동을 제안하지만, 그 제안은 상태 신호와 함께 다시 점검되어야 한다.
- 에이전트의 핵심은 도구를 많이 쓰는 것이 아니라, `현재 상태를 보고 다음 행동을 다시 고르는 목표 흐름`을 기록하는 데 있다.

이 예제에서 독자가 직접 해 볼 수 있는 조정은 다음과 같습니다.

- CSV에서 `current_context`를 `false`로 바꿔 오래된 근거가 보일 때 다음 행동이 어떻게 바뀌는지 보기
- `action_failed`를 `true`로 바꿔 실패 뒤에 같은 순서 진행이 아니라 재시도가 선택되는지 보기
- `approval_needed`를 `true`로 바꿔 agent가 계속 진행하지 않고 사람 검토로 넘어가는지 보기
- `sources_attached`를 `true`로 바꿔 더 진행할 필요가 없는 사례가 `finish`로 닫히는지 보기
- `AIBOOK_OLLAMA_MODEL`을 바꿔 모델 제안과 guard 보정 차이가 어떻게 달라지는지 보기

이 지점에서 한 번 더 분리해 두면, agent가 직접 해결하려는 것은 다음 행동 선택과 순서 재조정입니다. 하지만 각 호출을 어떤 형식으로 표현할지, 권한 경계를 어떻게 기록할지, 실행 trace를 어떻게 남길지는 별도 층위의 문제로 남습니다. 호출 형식 검증은 P6-14.2, 공통 연결 규칙은 P6-16.1, 실행 기록과 재현은 P6-16.2에서 더 구체화됩니다.

## 관찰 신호가 만드는 다음 행동

앞의 예제는 agent 전체를 구현하는 코드가 아니라, 중간 관찰이 다음 행동을 어떻게 갈라놓는지 보여 주는 작은 점검 장면입니다. 여기서 읽어야 할 핵심은 단계 수를 세는 일이 아닙니다. 같은 목표라도 `관련 맥락 없음`, `오래된 맥락`, `세부 근거 부족`, `실행 실패`, `권한 경계`, `출처 부착 완료`처럼 현재 상태가 달라지면 다음 행동도 달라져야 한다는 점입니다.

이 예제에서 읽어야 할 핵심은 다음입니다.

- 목표는 하나여도 현재 상태는 여러 모습으로 갈라질 수 있고
- 상태가 달라지면 다음 행동도 달라져야 하며
- 그 선택과 이유가 기록되어야 agent 흐름을 나중에 다시 점검할 수 있다는 점입니다

## 여러 호출을 목표 흐름으로 읽는 이유

에이전트의 핵심은 도구를 많이 쓰는 데 있지 않고, 목표를 여러 단계로 나누고 현재 상태를 보며 다음 행동을 계속 다시 고르는 실행 흐름을 만드는 데 있습니다.

더 중요하게 붙잡아야 할 점은 `답을 한 번 잘하는가`와 `중간 결과를 보며 일을 계속 이어 가는가`가 같은 문제가 아니라는 것입니다. 그래서 agent는 도구를 더 붙인 버전이 아니라, 여러 단계 상태를 보며 다음 행동을 다시 고르는 실행 흐름으로 읽는 편이 좋습니다.

이 실행 흐름이 중요한 이유는 다음과 같습니다.

- 바로 앞의 P6-14.1 도구 사용과 P6-14.2 함수 호출을 `한 번의 호출`이 아니라 `여러 단계를 잇는 실행 구조` 안에 다시 놓게 하고
- P6-15.2의 계획, 행동, 관찰 루프를 이해할 준비를 만들며
- 뒤의 P6-16.1 MCP, P6-16.2 하네스, P6-17.1 평가를 왜 함께 봐야 하는지 준비시키기 때문입니다

## 체크리스트
- 에이전트를 `더 똑똑한 챗봇`이 아니라 `여러 읽기와 실행을 목표 흐름으로 이어 가는 작업 구조`로 설명할 수 있어야 합니다.
- RAG, tool use, function calling이 각각 읽기·실행·구조화라면, agent는 `다음 단계 선택`을 중심에 두는 상위 흐름이라는 점을 말할 수 있어야 합니다.
- agent 흐름은 다시 계획, 행동, 관찰의 반복 루프로 더 구체화된다는 점을 잡고 있어야 합니다.

## 출처와 참고 자료

- Shunyu Yao et al., [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629){: target="_blank" rel="noopener noreferrer" }, arXiv, 2022, 확인 날짜: 2026-07-19.
- OpenAI, [Agents SDK](https://developers.openai.com/api/docs/guides/agents){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, 확인 날짜: 2026-07-19.
- OpenAI, [Using tools](https://developers.openai.com/api/docs/guides/tools){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, 확인 날짜: 2026-07-19.
