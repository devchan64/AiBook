# P6-13.2 함수 호출(function calling)

> Section ID: `P6-13.2`
> Version: `v2026.07.21`

P6-13.1에서는 도구 사용(tool use)이 모델과 외부 기능을 연결하는 구조라는 점을 보았습니다. 그러면 이제 더 구체적인 질문이 나옵니다.

도구를 써야 한다는 판단을 시스템은 어떤 형식으로 주고받는가?

함수 호출(function calling)은 모델이 어떤 도구를 어떤 인자(arguments)로 호출해야 하는지 구조화된 형식으로 표현하게 하는 방식이다.

## 구조화된 호출이 다루는 질문

핵심 질문은 다음과 같습니다.

- 함수 호출은 왜 필요한가?
- 자연어 요청과 구조화된 도구 호출은 무엇이 다른가?
- 함수 이름과 인자를 나누는 것이 왜 중요한가?

먼저 닫을 문제는 함수 호출을 `도구 사용을 안정적으로 연결하기 위한 구조화된 실행 요청`으로 읽고, 자연어 요청이 왜 이름과 인자 구조로 바뀌어야 하는지 붙잡는 것입니다.

반복 작업을 이어 가는 실행 구조는 구조화된 호출을 여러 단계로 묶는 문제입니다. 함수 호출은 먼저 한 번의 실행 요청을 검증 가능한 형태로 만드는 데 집중합니다.

여기서는 function calling을 단순 제품 기능명이 아니라, `도구 사용을 안정적으로 연결하기 위한 구조화 방식`으로 읽습니다.

tool use가 `무엇을 실행할까`를 다뤘다면, function calling은 그 실행 판단을 어떤 이름과 인자 구조로 바꿔야 시스템이 검증하고 이어서 처리할 수 있는지 다룹니다. agent 구조에서는 이런 구조화된 호출을 여러 단계 목표 흐름 안에서 어떻게 이어 갈지로 질문이 더 커집니다.

function calling은 `구조화된 실행 요청`을 다루고, 그다음에는 구조화된 호출을 어떤 목표 흐름으로 이어 붙일지의 문제가 붙습니다.

후반 실행 구조를 같은 질문으로 다시 고정하면, 역할은 아래처럼 압축할 수 있습니다.

| 지금 부족한 것 | 붙이는 구조 | 아직 남는 문제 |
| --- | --- | --- |
| 도구를 써야 한다는 판단만으로는 시스템이 바로 실행할 수 없고, 어떤 필드가 빠졌는지도 확인하기 어렵다 | 함수 이름과 인자를 분리한 구조화된 실행 요청 | 여러 호출을 어떤 순서로 이어 갈지, 중간 관찰에 따라 어떻게 재계획할지는 아직 남아 있다 |

| 지금 단계의 관점 | 이어지는 질문 | 다른 층위로 남겨 둘 것 |
| --- | --- | --- |
| tool use 실행 필요 | 어떤 외부 기능이 필요한가? | 호출 스키마와 검증 |
| function calling 구조화 요청 | 그 기능 요청을 어떤 이름과 인자 구조로 넘길 것인가? | 계획, 행동, 관찰 루프 |
| agent 목표 흐름 | 이런 구조화된 호출을 어떤 순서로 이어 갈 것인가? | 하네스와 운영 제약 |

여기서는 `함수 호출(function calling)`을 `자연어로 실행을 지시한다`는 인상보다 `이름과 인자가 분리된 검증 가능한 호출 구조`로 읽는 기준을 잡습니다.

핵심은 `무엇을 실행할까`에서 `그 실행 요청을 어떻게 검증 가능한 구조로 바꿀까`로 관점이 바뀌는 데 있습니다. tool use가 `실행 필요성`을 열었다면, function calling은 그 실행을 `검증 가능한 구조`로 바꾸고, agent는 그런 구조들을 `목표 흐름` 안에서 이어 붙입니다. 이 차이가 보여야 함수 호출을 단순 제품 기능이 아니라, `실행 연결을 안정화하는 중간 층`으로 읽을 수 있습니다.

이 단계에서 먼저 남겨야 할 기록은 어떤 호출을 어떤 인자로 준비했는지를 보여 주는 함수 이름, 인자, 누락 필드 점검 결과와, 결과를 어떤 형식으로 기대했고 어디서 호출이 막혔는지를 보여 주는 결과 형식과 호출 실패 이유입니다. 이 기록이 있어야 자연어 요청과 실행 구조를 다시 맞춰 보고, 실행 실패와 후속 운영 실패를 구분할 수 있습니다. 뒤로 갈수록 이 기록은 P6-14.2의 plan/action 루프, P6-15.2의 tool call log, P6-16의 평가 입력, P6-17.2의 실패 대응에서 다시 읽힙니다.

## 여기서 남겨야 할 구분

- 함수 호출을 입문 수준에서 설명할 수 있습니다.
- 자연어 요청과 구조화된 호출의 차이를 말할 수 있습니다.
- 이름(name), 인자(arguments), 결과(result)를 나눠 보는 이유를 설명할 수 있습니다.
- 구조화된 호출이 여러 단계 목표 흐름으로 이어질 수 있음을 말할 수 있습니다.

## 구조화 전환을 보는 순서

구조화 전환은 다음 순서로 읽으면 흐름이 잘 잡힙니다.

1. 먼저 `왜 구조화가 필요한가`와 `자연어 요청과 무엇이 다른가`를 읽고, 사람에게는 자연스럽지만 시스템에는 모호한 요청이 구조화된 호출로 바뀌는 이유를 잡습니다.
2. 그다음 `함수 이름과 인자를 나누는 이유`, `결과도 구조화가 중요한가`, `함수 호출이 항상 정답은 아니다`를 읽으면서 검증 가능성과 통제 가능성이 왜 중요해지는지 확인합니다.
3. 마지막으로 사례와 Python 예제를 보면서, `자연어 요청 -> 함수 이름 + 인자 -> 누락 필드 검증 -> 실행 준비`라는 흐름이 실제로 어떻게 드러나는지 확인합니다.

## 왜 구조화가 필요한가

도구 사용을 자연어 문장만으로 처리하면 애매함이 큽니다.

예를 들어 모델이 이렇게 말한다고 가정해 봅시다.

`서울의 오늘 환율을 검색해서 알려 주세요.`

이 문장은 사람은 이해할 수 있지만, 시스템 입장에서는 다음이 모호할 수 있습니다.

- 어떤 도구를 써야 하는가?
- 인자는 무엇인가?
- 날짜 형식은 어떻게 되는가?
- 실패하면 무엇을 돌려줘야 하는가?

그래서 함수 호출 구조는 보통 다음을 분리합니다.

- 도구 이름
- 인자 이름
- 인자 값

즉, 자연어를 그대로 실행하는 것이 아니라 `실행 가능한 구조`로 바꾸는 것입니다.

## 자연어 요청과 무엇이 다른가

| 표현 방식 | 특징 |
| --- | --- |
| 자연어 요청 | 사람이 읽기 쉽지만 모호할 수 있음 |
| 구조화된 함수 호출 | 시스템이 해석하기 쉽고 검증이 가능함 |

`함수 호출은 모델의 의도를 시스템이 더 안전하게 실행할 수 있도록 문장을 구조로 바꾸는 방법이다.`

## 함수 이름과 인자를 나누는 이유

이 구분을 잡아야 시스템이 `어떤 기능을 부를지`와 `그 기능에 어떤 값을 넘길지`를 따로 검증하고 실패 원인을 나눠 볼 수 있습니다.

예를 들어:

- 함수 이름: `lookup_exchange_rate`
- 인자: `{"currency": "USD", "region": "KR", "date": "2026-06-29"}`

이렇게 나누면 시스템은 다음을 하기 쉬워집니다.

- 허용된 도구인지 확인
- 인자 형식 검증
- 빠진 인자 탐지
- 실행 전 승인 요구

즉, 함수 호출은 단순히 예쁘게 정리하는 것이 아니라, `검증 가능성`과 `통제 가능성`을 높이는 구조입니다.

## 결과도 구조화가 중요한가

그렇습니다. 도구를 호출한 뒤에도 결과가 다시 구조적으로 돌아오면:

- 모델이 다시 읽기 쉬워지고
- 앱이 후처리하기 쉬워지며
- 로그와 추적(trace)이 쉬워집니다

즉, 함수 호출은 보통 입력 구조화만이 아니라, 실행 결과를 다시 연결하는 흐름까지 포함하는 구조로 보는 편이 좋습니다.

## 함수 호출이 항상 정답은 아니다

함수 호출이 있다고 해서:

- 모델이 항상 올바른 도구를 고르는 것
- 인자를 완벽하게 채우는 것
- 잘못된 실행을 완전히 막는 것

이 보장되지는 않습니다.

따라서 실제 시스템은 보통:

- schema 검증
- 권한 확인
- 사용자 승인
- 실패 시 재시도 또는 오류 보고

같은 추가 구조를 둡니다.

## 아주 단순하게 그리면

```mermaid
--8<-- "assets/part-06/chapter-13/p6-c13-s02-function-call-flow-ko.mmd"
```

이 도식의 핵심은 `문장 -> 구조 -> 실행 -> 결과` 흐름으로 바뀐다는 점입니다.

## 사례 및 예시

### 사례 1. 환율 조회

`오늘 달러 환율 알려 줘`라는 질문을 생각해 볼 수 있습니다. 이런 질문은 사람끼리는 대충 통하니 시스템도 바로 처리할 수 있을 것이라고 생각하기 쉽습니다. 하지만 시스템은 `어느 통화쌍인지`, `어느 날짜 기준인지`, `어느 지역 환율인지`를 인자로 분리해야 실제 조회가 가능합니다. 예를 들어 사용자 의도가 `USD/KRW`인지 `달러 인덱스`인지부터 다를 수 있습니다. 이 구분이 없으면 조회는 성공해도 사용자가 원한 값이 아닌 다른 지표를 돌려줄 수 있습니다. 즉 `실행 성공`과 `의도 일치`는 같은 말이 아닙니다.

여기서 바뀌는 점은 `질문 뜻이 대충 통하는가`를 보던 기준에서 `실제 조회에 필요한 인자가 빠짐없이 구조화되는가`를 보는 기준으로 이동한다는 것입니다. 함수 호출 구조는 자연어 요청을 이런 명시적 필드로 바꾸어 실행 단계를 더 분명하게 만듭니다. 여기서 넘어가야 할 오해는 `말이 자연스럽게 이해되면 조회도 맞게 될 것`이라는 기대입니다. 그래서 이 사례에서 확인해야 할 결과는 질문 문장이 실제 조회 전에 `통화쌍`, `기준 날짜` 같은 인자로 분해되는가, 그리고 그 인자만 봐도 사용자의 원래 의도가 재확인되는가입니다.

### 사례 2. 일정 생성

자연어로는 `내일 오후 3시에 회의 잡아 줘`라고 말하면 충분해 보입니다. 사람도 이런 표현이면 서로 이해될 거라고 먼저 느끼기 쉽습니다. 하지만 실제 캘린더 API는 참석자, 시간대, 제목, 날짜 형식처럼 더 구조화된 인자를 받아야 합니다. 예를 들어 `내일`은 사용자 시간대가 바뀌면 다른 날짜가 될 수 있고, 참석자가 빠지면 회의 생성 자체가 불완전할 수 있습니다. 이 차이를 놓치면 모델이 말을 잘 이해해도 실행 단계에서 바로 막히거나 엉뚱한 시간에 일정이 생길 수 있습니다. 특히 `회의는 만들어졌으니 성공`이라고 보기 쉽지만, 잘못된 시각이나 빈 참석자 목록으로 생성된 일정은 운영 기준에서는 실패에 가깝습니다.

여기서 바뀌는 점은 `말이 충분히 구체적인가`를 보던 기준에서 `API가 요구하는 필드가 실제로 다 채워졌는가`를 보는 기준으로 이동한다는 것입니다. 함수 호출 구조는 이런 암묵적 정보를 명시적 인자 묶음으로 바꿔 줍니다. 그래서 이 사례에서 확인해야 할 결과는 회의 생성 전에 시간, 날짜, 제목, 참석자 같은 필드가 빠짐없이 구조화되는가, 그리고 누락 필드가 있으면 실행 전에 바로 드러나는가입니다.

### 사례 3. 코드 에이전트

코드 에이전트가 파일 읽기, 테스트 실행, 패치 적용을 번갈아 수행한다고 해 봅시다. 단순 자연어 설명만 남으면 어떤 작업이 언제 어떤 인자로 실행됐는지 다시 추적하기 어렵습니다. `파일을 읽고 테스트를 돌렸다`는 서술만 있어도 흐름이 충분히 설명됐다고 느끼기 쉽지만, 실제 운영에서는 어떤 파일을 읽고 어떤 테스트를 돌렸는지까지 남아야 실패를 재현할 수 있습니다. 예를 들어 같은 `테스트를 돌렸다`는 문장도 어느 디렉터리에서, 어떤 플래그로, 어떤 대상만 실행했는지에 따라 결과 해석이 완전히 달라집니다.

반대로 함수 호출 구조로 남기면 `read_file`, `run_tests`, `apply_patch` 같은 단계가 명시적으로 기록되어 실행 흐름을 더 쉽게 되짚을 수 있습니다. 여기서 바뀌는 점은 `무슨 작업을 했다`는 설명만 남기던 기준에서 `어떤 함수가 어떤 인자로 호출됐는가`까지 다시 추적할 수 있는가를 보는 기준으로 이동한다는 것입니다. 이 기록이 없으면 같은 실패가 다시 나와도 어느 단계 입력이 달랐는지 확인하기 어려워집니다. 즉, 함수 호출은 실행 성공뿐 아니라 로그와 재현성을 관리하는 데에도 직접 연결됩니다. 그래서 이 사례에서 확인해야 할 결과는 최종 성공 여부뿐 아니라 어떤 함수가 어떤 인자로 호출됐는지를 다시 추적할 수 있는가, 그리고 누락된 인자 때문에 어떤 단계가 막혔는지도 재구성할 수 있는가입니다.

세 사례를 구조화 관점으로 다시 묶으면 다음과 같습니다.

| 상황 | 자연어만 두면 모호한 것 | 함수 호출 구조가 분명하게 만드는 것 |
| --- | --- | --- |
| 환율 조회 | 어떤 값을 어느 기준으로 조회할지 | 통화쌍, 날짜, 지역 같은 인자 |
| 일정 생성 | `내일`, `오후` 같은 표현의 실행 기준 | 날짜, 시간, 시간대, 참석자 필드 |
| 코드 에이전트 | 무엇을 어떤 순서로 실행했는지 | 함수 이름, 인자, 실행 로그 |

같은 내용을 구조화된 실행 요청 흐름으로 다시 보면 다음처럼 읽을 수 있습니다.

```mermaid
--8<-- "assets/part-06/chapter-13/p6-c13-s02-function-call-boundary-ko.mmd"
```

핵심은 `구조화됐다`와 `바로 실행 가능하다`가 같은 말이 아니라는 점입니다.

## 바로 적용해 보면

함수 호출을 처음 읽을 때 가장 자주 헷갈리는 것은 `말이 이해된다`와 `실행 준비가 끝났다`를 같은 뜻으로 보는 점입니다. 하지만 실제로는 `어떤 기능을 부를지`, `어떤 필드가 필요한지`, `누락 없이 실행 가능한지`를 따로 봐야 합니다.

| 이런 장면이 보이면 | 먼저 확인할 것 | 왜 그 확인이 먼저 필요한가 |
| --- | --- | --- |
| 요청 뜻은 알겠는데 시스템이 어떤 도구를 써야 할지 애매함 | 함수 이름이 분명하게 정해졌는가 | 기능 이름이 모호하면 뒤 인자 검증 이전에 실행 대상부터 흔들리기 때문입니다. |
| 기능은 맞는 것 같은데 실행 직전에 자주 막힘 | 필수 인자가 누락 없이 채워졌는가 | 자연어로는 통하는 요청도 날짜, 시간대, 통화쌍 같은 필드가 비어 있으면 실제 호출은 실패하기 때문입니다. |
| 구조는 갖췄는데 결과가 여전히 불안정함 | 결과 형식과 실패 이유가 함께 기록되는가 | 호출 성공/실패를 다시 추적할 수 있어야 다음 단계 재시도나 수정이 가능하기 때문입니다. |

같은 기준을 더 짧은 실무 질문으로 바꾸면 다음처럼 읽을 수 있습니다.

| 이런 의심이 들면 | 먼저 던질 질문 |
| --- | --- |
| `무슨 작업을 하려는지는 알겠는데 호출이 흐릿하다` | 함수 이름 하나로 실행 대상을 분명히 했는가? |
| `요청은 구체적인데 왜 실행이 안 되지?` | 필수 인자가 빈칸 없이 채워졌는가? |
| `실패는 했는데 어디서 막혔는지 모르겠다` | 결과 형식과 실패 이유를 구조적으로 남겼는가? |

먼저 익혀야 하는 기준은 단순합니다. function calling은 `자연어를 보기 좋게 정리하는 일`이 아니라, `함수 이름`, `인자`, `결과`를 나눠 실행 전 검증과 실행 후 추적을 가능하게 만드는 구조입니다.

## 연습 및 예제

예제의 목표는 실제 캘린더 API를 부르는 것이 아니라, 자연어 요청이 함수 이름과 인자 구조로 바뀌고, 그 구조가 검증 가능한 형태가 된다는 점을 보는 것입니다. 한 요청만 보면 `구조화하면 된다` 수준에서 끝나기 쉬우므로, 여러 요청을 배치로 보면서 어떤 호출은 바로 실행 가능하고 어떤 호출은 필드 누락으로 막히는지도 함께 봅니다.

사용자는 자연어로 일정을 만들어 달라고 요청하지만, 시스템은 이 문장을 그대로 실행하지 않고 함수 이름과 인자를 분리해 받아야 합니다. 인자 누락 여부를 실행 전에 점검할 수 있어야 하므로, `구조화했다`와 `실행 준비가 끝났다`는 같은 말이 아닙니다.

아래 예제는 사용자 요청 여러 개와, 자연어 요청에서 함수 호출 초안을 만드는 간단한 변환 규칙을 사용합니다. 출력에서는 함수 이름과 인자 구조, 필수 인자 점검 결과, 어떤 호출이 바로 실행 가능하고 어떤 호출은 누락으로 막히는지에 대한 점검값을 확인합니다.

먼저 이 예제에서 같이 볼 항목은 다음과 같습니다.

| 점검 항목 | 왜 필요한가 |
| --- | --- |
| `function_name` | 어떤 기능을 부르려는지 분리해서 확인 |
| `missing_fields` | 실행 전에 어떤 인자가 비었는지 확인 |
| `is_valid` | 현재 구조로 바로 실행 가능한지 확인 |
| `provided_argument_keys` | 모델이 어떤 필드까지 채웠는지 확인 |

코드에서 확인할 핵심은 함수 호출형 도구 사용은 실행 전에 함수 이름, 인자, 누락 필드를 먼저 검증하는 단계가 필요하다는 점입니다.

```python
# 캘린더 일정 생성 요청에서 function call arguments가 필수 필드를 채웠는지 검증해 실행 가능성을 판단하는 예제입니다.
requests = [
    "내일 오후 3시에 서울 시간으로 디자인 리뷰 회의를 만들어 주세요.",
    "내일 오후에 서울 시간으로 팀 회의를 잡아 주세요.",
    "다음 주 월요일 오전 10시에 채용 인터뷰를 잡아 주세요.",
]

required_fields = ["title", "date", "time", "timezone"]

def build_function_call(user_request):
    if "디자인 리뷰" in user_request:
        title = "디자인 리뷰"
    elif "팀 회의" in user_request:
        title = "팀 회의"
    elif "채용 인터뷰" in user_request:
        title = "채용 인터뷰"
    else:
        title = ""

    if "내일" in user_request:
        date = "tomorrow"
    elif "다음 주 월요일" in user_request:
        date = "next_monday"
    else:
        date = ""

    if "오후 3시" in user_request:
        time = "15:00"
    elif "오전 10시" in user_request:
        time = "10:00"
    else:
        time = ""

    timezone = "Asia/Seoul" if "서울" in user_request else None

    return {
        "name": "create_calendar_event",
        "arguments": {
            "title": title,
            "date": date,
            "time": time,
            "timezone": timezone,
            "attendees": [],
        },
    }

def validate_function_call(function_call, required_fields):
    arguments = function_call["arguments"]
    missing = [
        field
        for field in required_fields
        if field not in arguments or arguments[field] in ("", None)
    ]
    return {
        "function_name": function_call["name"],
        "missing_fields": missing,
        "is_valid": len(missing) == 0,
    }

reports = []
for user_request in requests:
    function_call = build_function_call(user_request)
    validation = validate_function_call(function_call, required_fields)
    inspection = {
        "required_fields": required_fields,
        "provided_argument_keys": list(function_call["arguments"].keys()),
        "is_ready_to_execute": validation["is_valid"],
        "missing_count": len(validation["missing_fields"]),
    }
    reports.append(
        {
            "user_request": user_request,
            "function_call": function_call,
            "validation": validation,
            "inspection": inspection,
        }
    )

summary = {
    "valid_call_count": sum(report["validation"]["is_valid"] for report in reports),
    "invalid_call_count": sum(not report["validation"]["is_valid"] for report in reports),
    "calls_missing_time": sum("time" in report["validation"]["missing_fields"] for report in reports),
    "calls_missing_timezone": sum("timezone" in report["validation"]["missing_fields"] for report in reports),
    "valid_call_ratio": round(
        sum(report["validation"]["is_valid"] for report in reports) / len(reports),
        2,
    ),
    "invalid_call_ratio": round(
        sum(not report["validation"]["is_valid"] for report in reports) / len(reports),
        2,
    ),
}

print("[summary]")
print(summary)
print()

for report in reports:
    print("=" * 80)
    print("[user_request]")
    print(report["user_request"])
    print("[function_call]")
    print(report["function_call"])
    print("[validation]")
    print(report["validation"])
    print("[inspection]")
    print(report["inspection"])
```

실행 결과 예시는 다음처럼 읽을 수 있습니다.

```text
[summary]
{'valid_call_count': 1, 'invalid_call_count': 2, 'calls_missing_time': 1, 'calls_missing_timezone': 1, 'valid_call_ratio': 0.33, 'invalid_call_ratio': 0.67}

================================================================================
[user_request]
내일 오후 3시에 서울 시간으로 디자인 리뷰 회의를 만들어 주세요.
[function_call]
{'name': 'create_calendar_event', 'arguments': {'title': '디자인 리뷰', 'date': 'tomorrow', 'time': '15:00', 'timezone': 'Asia/Seoul', 'attendees': []}}
[validation]
{'function_name': 'create_calendar_event', 'missing_fields': [], 'is_valid': True}
[inspection]
{'required_fields': ['title', 'date', 'time', 'timezone'], 'provided_argument_keys': ['title', 'date', 'time', 'timezone', 'attendees'], 'is_ready_to_execute': True, 'missing_count': 0}
================================================================================
[user_request]
내일 오후에 서울 시간으로 팀 회의를 잡아 주세요.
[function_call]
{'name': 'create_calendar_event', 'arguments': {'title': '팀 회의', 'date': 'tomorrow', 'time': '', 'timezone': 'Asia/Seoul', 'attendees': []}}
[validation]
{'function_name': 'create_calendar_event', 'missing_fields': ['time'], 'is_valid': False}
[inspection]
{'required_fields': ['title', 'date', 'time', 'timezone'], 'provided_argument_keys': ['title', 'date', 'time', 'timezone', 'attendees'], 'is_ready_to_execute': False, 'missing_count': 1}
================================================================================
[user_request]
다음 주 월요일 오전 10시에 채용 인터뷰를 잡아 주세요.
[function_call]
{'name': 'create_calendar_event', 'arguments': {'title': '채용 인터뷰', 'date': 'next_monday', 'time': '10:00', 'timezone': None, 'attendees': []}}
[validation]
{'function_name': 'create_calendar_event', 'missing_fields': ['timezone'], 'is_valid': False}
[inspection]
{'required_fields': ['title', 'date', 'time', 'timezone'], 'provided_argument_keys': ['title', 'date', 'time', 'timezone', 'attendees'], 'is_ready_to_execute': False, 'missing_count': 1}
```

이 결과에서 먼저 봐야 할 것은 `valid_call_count`가 1이고 `invalid_call_count`가 2라는 점입니다. 즉, 자연어 요청을 함수 호출 구조로 바꿨다고 해서 모두 바로 실행 가능한 것은 아닙니다. `time`, `timezone`처럼 시스템이 실제 실행에 꼭 필요한 필드는 따로 검증해야 하고, 함수 호출 구조는 바로 그 누락을 실행 전에 드러내는 역할을 합니다.

그래서 이 예제에서 확인해야 할 결과는 두 가지입니다.

- 자연어 요청이 사라지는 것이 아니라, 시스템이 실행하기 쉬운 함수 이름과 인자 구조로 다시 표현된다.
- 함수 호출의 핵심 가치는 `구조화` 자체뿐 아니라, 실행 전에 누락 필드를 검증하고 실패 원인을 분리할 수 있다는 데 있다.

이 예제에서 독자가 직접 해 볼 수 있는 조정은 다음과 같습니다.

- `requests`에 제목 누락, 날짜 누락 사례를 더 넣어 어떤 필드가 자주 빠지는지 보기
- `build_function_call`에 참석자 메일 주소를 읽는 규칙을 추가해 일정 생성 인자가 어떻게 확장되는지 확인하기
- `required_fields`를 바꿔 도구마다 검증 규칙이 달라질 수 있음을 실험해 보기
- `date`를 자연어 그대로 두고 별도 정규화 단계를 상상해 보기

여기서 한 단계 더 가면, 함수 호출이 해결하는 문제와 아직 남는 문제를 분리해서 읽어야 합니다.

| 상황 | 함수 호출이 직접 해결하는 것 | 함수 호출만으로는 남는 것 |
| --- | --- | --- |
| 요청이 말로는 이해되지만 실행 입력이 모호함 | 함수 이름과 인자 구조를 분리해 실행 입력을 명시함 | 어떤 도구를 선택할지 자체의 판단 품질 |
| 실행 전에 빠진 필드를 잡고 싶음 | `missing_fields`처럼 누락 인자를 검증할 수 있음 | 사용자가 의도한 값이 맞는지에 대한 의미 해석 |
| 결과를 후속 단계에 다시 넘기고 싶음 | 결과 형식을 일정한 구조로 돌려주기 쉬움 | 여러 호출을 어떤 순서로 이어 갈지에 대한 계획 |
| 실패를 재현하고 로그로 남기고 싶음 | 어떤 함수가 어떤 인자로 호출됐는지 추적 가능 | 재시도, 대안 경로, 종료 기준 같은 운영 루프 |

이 표가 중요한 이유는 `function calling = agent`로 뭉개지지 않게 해 주기 때문입니다. 함수 호출은 실행 직전 요청을 구조화하는 층이고, 여러 호출을 이어 가는 계획과 재시도는 에이전트 층의 문제입니다.

## 이 예제를 구조화된 실행 요청 관점으로 다시 보면

앞의 예제는 함수 호출 전체를 구현하는 코드가 아니라, `사람이 말한 요청`과 `시스템이 실행할 구조`가 같은 문장이 아니라는 점을 가장 짧게 보여 주는 장면입니다. 여기서 중요한 것은 자연어를 없애는 일이 아니라, 실행 직전에 어떤 이름과 인자 구조로 다시 정리되어야 하는지를 읽는 데 있습니다.

차트로 보면 세 호출 중 바로 실행 가능한 호출은 하나뿐이고, 나머지 둘은 각각 `time`, `timezone` 누락으로 막힙니다. 따라서 함수 호출은 구조를 만들었다는 사실보다, 실행 전에 어떤 필드가 빠졌는지 드러내고 멈출 수 있게 한다는 점이 더 중요합니다.

![함수 호출 예제의 유효 호출과 누락 필드 감지 수](../../../assets/part-06/chapter-13/function-call-validation-ko.png)

## 여기까지를 한 줄로 묶으면

함수 호출의 핵심은 자연어를 없애는 것이 아니라, 실행 직전에 요청을 `이름과 인자가 분리된 검증 가능한 구조`로 바꾸는 데 있습니다.

더 중요하게 붙잡아야 할 점은 `잘 설명하는가`와 `실제로 실행 가능한 요청 구조를 넘기는가`가 같은 문제가 아니라는 것입니다. 그래서 함수 호출은 도구를 더 붙이는 장식이 아니라, 실행 직전에 요청을 검증 가능한 구조로 바꿔 tool use를 덜 불안정하게 만드는 대표 방식으로 읽는 편이 좋습니다.

이 구조화가 중요한 이유는 다음과 같습니다.

- tool use를 모호한 자연어 수준에 두지 않게 하고
- agent, MCP, harness를 이해하기 위한 구조화 감각을 주며
- 실행 가능한 AI 서비스가 왜 애플리케이션 계층을 필요로 하는지 설명해 주기 때문입니다

## 체크리스트
- 함수 호출을 `자연어 지시`가 아니라 `이름과 인자가 분리된 검증 가능한 호출 구조`로 설명할 수 있어야 합니다.
- `어떤 함수인가`와 `어떤 인자인가`를 나눠 봐야 검증과 실패 추적이 쉬워진다는 점을 말할 수 있어야 합니다.
- 구조화된 호출들을 목표 흐름 안에서 어떤 순서로 이어 갈지로 질문이 이동한다는 점을 잡고 있어야 합니다.

## 출처와 참고 자료

- OpenAI, [Function calling](https://developers.openai.com/api/docs/guides/function-calling){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, 확인 날짜: 2026-07-19.
- OpenAI, [Using tools](https://developers.openai.com/api/docs/guides/tools){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, 확인 날짜: 2026-07-19.
- Shunyu Yao et al., [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629){: target="_blank" rel="noopener noreferrer" }, arXiv, 2022, 확인 날짜: 2026-07-19.
