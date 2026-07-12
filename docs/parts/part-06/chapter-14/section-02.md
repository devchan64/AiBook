# P6-14.2 하네스(harness)

> Section ID: `P6-14.2`
> Version: `v2026.07.12`

P6-14.1에서는 MCP가 모델과 외부 도구, 데이터 사이의 연결을 더 일관되게 만드는 인터페이스 관점이라는 점을 보았습니다. 하지만 연결만으로는 충분하지 않습니다. 이 절에서는 에이전트 실행을 안정적으로 감싸고, 로그와 평가를 남기며, 반복 가능하게 관리하는 구조를 봅니다.

Part 6에서 `하네스(harness)`, `에이전트 실행을 감싸는 운영 장치`, `연결 표준과 실행 관리의 구분`에 대한 첫 상세 설명은 이 절에서 잡습니다. 뒤 절에서는 현재 맥락에 필요한 최소 설명만 남기고, 실행 관리 환경의 기본 뜻은 이 절과 개념사전을 기준으로 다시 연결합니다.

하네스(harness)는 에이전트나 모델 실행을 감싸서 입력, 도구 호출, 결과, 로그, 평가를 관리하는 실행 환경 또는 운영 장치에 가깝다.

## 이 절의 범위

이 절은 다음 질문에 답합니다.

- 하네스는 무엇을 감싸는가?
- 왜 에이전트 실행에는 하네스 같은 운영 장치가 필요한가?
- 하네스를 DevOps 도구 하나처럼 보면 왜 혼동이 생기는가?

이 절에서는 다음 내용을 깊게 다루지 않습니다.

- 테스트 프레임워크 세부 구현
- 관측성(observability) 스택 전체
- 배포 파이프라인 전체 설계

하네스의 역할은 여기서 큰 그림으로 잡고, 품질 점검은 뒤의 P6-15.1 LLM 평가와 P6-15.2 자동 평가와 사람 평가에서 다시 회수합니다. 운영 제약과 실패 대응은 P6-16.1, P6-16.2에서 다시 이어지며, 특정 관측성 스택과 배포 파이프라인 구현은 현재 본편 범위 밖으로 둡니다.

이 절에서는 harness를 단일 제품명처럼 보지 않고, `실행을 통제하고 기록하고 평가하는 감싸는 구조`로 설명합니다.

지금 읽는 층위는 `실행 관리에서 평가 입력으로 넘어가는 경계 층위`입니다. 앞 절까지가 연결과 실행 구조를 만드는 쪽이었다면, 여기서는 그 실행에서 남긴 trace, log, replay 정보가 왜 바로 다음 장의 평가 기준이 되는지 읽습니다. 즉, 좋은 실행 기록은 운영 부록이 아니라 `무엇을 기준으로 괜찮다고 판정할까`를 떠받치는 입력입니다.

하네스는 제품 이름보다 `무엇을 어떤 trace와 replay로 남겨야 하는가`, `이 기록이 왜 바로 다음 장의 평가 입력이 되는가`, `MCP와 하네스가 각각 연결과 관리 중 무엇을 맡는가`라는 세 질문으로 읽으면 됩니다.

| 지금 단계의 관점 | 바로 다음에 이어질 질문 | 뒤에서 본격적으로 다시 읽는 위치 |
| --- | --- | --- |
| MCP 연결 형식 | 무엇과 어떤 형식으로 연결했는가? | P6-14.1 |
| harness 실행 기록 | 그 연결을 쓴 실행을 어떤 trace, replay, approval 기록으로 남길 것인가? | P6-14.2 |
| 평가와 운영 판정 | 남긴 기록을 어떤 통과 기준과 서비스 통제로 이어 갈 것인가? | P6-15.1, P6-15.2, P6-16.1, P6-16.2 |

이 절은 Part 6에서 `하네스(harness)`를 대표로 설명하는 Section입니다. `도구 하나`라는 인상을 `실행을 감싸고 기록과 평가 입력을 남기는 운영 장치`로 바꾸는 기준선을 여기서 세웁니다.

즉, 하네스는 `실행 흔적을 남기는 층`, 평가는 `그 흔적을 품질 판단으로 바꾸는 층`, 운영은 `그 판단을 실제 서비스 통제와 실패 대응으로 이어 붙이는 층`입니다. 지금 장의 핵심은 `연결을 잘했는가`에서 `그 연결을 쓴 실행을 다시 설명하고 비교할 수 있는가`로 관점이 바뀌는 데 있습니다. 이 차이가 보여야 하네스를 평가 절차나 운영 정책과 같은 말처럼 섞어 읽지 않게 됩니다.

MCP, 하네스, 평가, 운영의 최소 차이는 아래 표처럼 다시 고정할 수 있습니다.

| 지금 읽는 장 | 가장 먼저 붙잡을 질문 | 바로 다음 장으로 넘어갈 때 바뀌는 중심 |
| --- | --- | --- |
| MCP | 무엇과 어떤 공통 형식으로 연결할까? | 그 연결을 쓴 실행을 어떤 trace와 replay로 남길까 |
| harness | 실행을 어떻게 감싸고 기록할까? | 남긴 기록을 어떤 품질 기준으로 읽을까 |
| evaluation | 어떤 실행을 괜찮다고 통과시킬까? | 통과한 실행을 비용, 지연 시간, 실패 통제로 어떻게 운영할까 |
| operations | 어떤 실패를 어디서 멈추고 복구할까? | 그 판단을 요청 흐름과 요청 실행 기록으로 어떻게 남길까 |

## 이 절의 목표

- 하네스를 입문 수준에서 설명할 수 있습니다.
- MCP와 하네스의 역할 차이를 말할 수 있습니다.
- trace, log, eval, replay 같은 운영 요구가 왜 중요한지 설명할 수 있습니다.
- 다음 장의 평가와 운영 문제로 자연스럽게 넘어갈 수 있습니다.

## 이 절을 읽는 순서

이 절은 다음 순서로 읽으면 흐름이 자연스럽습니다.

1. 먼저 하네스가 `무엇을 감싸는가`를 읽습니다.
2. 그다음 MCP와 하네스를 구분해 `연결 문제`와 `실행 관리 문제`를 나눕니다.
3. 사례와 Python 예제에서는 `최종 답이 아니라 실행 기록이 왜 운영 판단 기준이 되는가`를 확인합니다.

## 하네스는 무엇을 감싸나

하네스는 다음 역할 묶음으로 보면 범위를 더 분명하게 잡을 수 있습니다.

하네스는 보통:

- 어떤 입력으로 실행했는지
- 어떤 도구를 호출했는지
- 어떤 결과가 나왔는지
- 중간에 어떤 실패가 있었는지
- 다시 재현할 수 있는지

를 관리하는 역할을 합니다.

즉, 하네스는 `모델이 무엇을 말했는가`만 보는 것이 아니라, `그 실행 전체를 어떻게 감싸고 관리할 것인가`를 다룹니다.

한 번 더 단순화하면 다음과 같습니다.

```mermaid
--8<-- "assets/part-06/chapter-14/p6-c14-s02-diagram-01-ko.mmd"
```

이 그림의 핵심은 하네스가 결과 문장만 남기는 것이 아니라, 그 결과에 이르기까지의 실행과 점검 단계를 함께 남긴다는 점입니다.

## 왜 agent 시대에 필요해졌나

단일 질의응답에서는 로그 한 줄로 끝날 수 있습니다. 하지만 에이전트는:

- 여러 단계 계획을 만들고
- 도구를 호출하고
- 중간 실패를 겪고
- 다시 시도하고
- 최종 결과를 냅니다

이 구조에서는 `최종 답변`만 보면 무엇이 잘됐고 무엇이 틀렸는지 알기 어렵습니다.

그래서 다음이 중요해집니다.

- trace: 어떤 순서로 움직였는가
- log: 어떤 입력과 결과가 오갔는가
- eval: 결과가 괜찮았는가
- replay: 같은 흐름을 다시 재현할 수 있는가

이 요구를 감싸는 구조가 바로 harness에 가깝습니다.

## MCP와 무엇이 다른가

이 차이도 분리해야 합니다.

| 구조 | 중심 역할 |
| --- | --- |
| MCP | 도구와 데이터 연결 인터페이스를 정리한다 |
| harness | 실행을 감싸고 기록하고 평가한다 |

즉:

- MCP는 `무엇과 어떻게 연결할까`에 가깝고
- harness는 `그 연결을 써서 실행한 흐름을 어떻게 관리할까`에 가깝습니다

둘은 함께 쓰일 수 있지만 같은 층위의 개념은 아닙니다.

## 왜 DevOps 도구 하나처럼 보면 혼동이 생기나

하네스를 단일 제품이나 특정 도구 하나로 이해하면 범위가 너무 좁아집니다. 더 안전한 설명은 다음입니다.

`하네스는 실행을 둘러싼 운영 패턴 또는 환경이라는 관점이 더 가깝다.`

즉, harness는:

- 테스트 러너일 수도 있고
- 평가 환경일 수도 있고
- trace 수집 구조일 수도 있고
- 승인과 권한 체크를 포함한 실행 래퍼일 수도 있습니다

핵심은 특정 브랜드보다 `실행을 감싸는 역할`입니다.

## 왜 평가와 재현성이 같이 중요해지나

agent 시스템은 한 번 잘 돌아가는 것처럼 보여도, 다음 번에는 다른 행동을 할 수 있습니다. 따라서 운영에서는 다음이 중요해집니다.

- 어떤 입력에서 실패했는가
- 어떤 도구 호출이 원인이었는가
- 어떤 설정에서 재현되는가
- 수정 후 실제로 나아졌는가

이 질문들은 harness 없이는 다루기 어렵습니다.

즉, harness는 단순 기록이 아니라 `디버깅과 개선의 기반`입니다.

## 아주 단순하게 그리면

```mermaid
--8<-- "assets/part-06/chapter-14/p6-c14-s02-diagram-02-ko.mmd"
```

이 도식의 핵심은 harness가 실행을 둘러싸서 `관찰 가능성`과 `개선 가능성`을 만들고, 필요하면 사람 검토나 정책 차단으로 넘기는 구조라는 점입니다.

## 사례 및 예시

이 사례들의 초점은 `실패했는가`보다 `어디까지 기록되어 있어야 같은 실패를 다시 설명할 수 있는가`입니다.

### 사례 1. 코딩 에이전트

코딩 에이전트가 여러 파일을 고친 뒤 테스트가 실패했다고 해 봅시다. 결과만 보면 `실패했다`는 사실은 알 수 있지만, 어떤 파일을 먼저 읽었고 어떤 패치를 넣었으며 어느 테스트에서 처음 문제가 났는지는 금방 사라집니다. 사람이 수동으로 되짚으면 가능한 일이지만, 반복 실험이 많아질수록 기억과 복기에 의존하게 됩니다. 예를 들어 마지막 실패는 로그인 테스트에서 보였지만, 실제 원인은 그 전에 바꾼 공용 유틸 함수 한 줄일 수 있습니다. 이 경로가 남지 않으면 원인 추적보다 같은 실험을 다시 하는 시간이 더 길어질 수 있습니다. harness가 있으면 읽은 파일, 적용한 변경, 실행한 테스트와 결과가 trace로 남아 문제 지점을 다시 추적하기 쉬워집니다. 여기서 바뀌는 점은 `최종 결과가 성공인가 실패인가`만 보던 기준에서 `어떤 실행 경로를 거쳐 실패했는가`를 다시 추적할 수 있는가를 보는 기준으로 이동한다는 것입니다. 그래서 이 사례에서 확인해야 할 결과는 최종 실패 한 줄만 남는 것이 아니라, 어떤 파일 변경 뒤 어떤 테스트가 처음 깨졌는지가 실제로 다시 추적되는가입니다.

이 사례가 실무 장면인 이유는 코딩 에이전트의 출력이 대개 한 파일이 아니라 여러 파일, 여러 명령, 여러 검증 단계를 거치기 때문입니다. 사람이 직접 수정할 때도 `어느 커밋에서 망가졌는가`를 찾는 일이 오래 걸리는데, 에이전트가 짧은 시간에 여러 패치를 연속으로 넣으면 경로를 기억만으로 복기하기 더 어려워집니다. 그래서 하네스의 가치는 `실패를 막아 준다`보다 `실패를 다시 설명하게 해 준다`에 가깝습니다. 테스트 실패 한 줄만 있으면 고장 사실은 알 수 있지만, 어떤 읽기와 어떤 수정이 그 실패를 만들었는지는 남지 않습니다.

같은 실패라도 기록 수준에 따라 운영자가 할 수 있는 판단은 크게 달라집니다.

| 남은 기록 | 겉으로는 어떻게 보이나 | 실제로 다시 판단할 수 있는 것 |
| --- | --- | --- |
| 최종 테스트 실패 한 줄 | 실패는 확인됨 | 어느 변경이 회귀를 만들었는지 거의 추적 불가 |
| 수정 파일 목록 + 최종 실패 | 수정 범위는 보임 | 어떤 파일 순서와 어떤 테스트가 처음 문제였는지는 불분명 |
| 읽은 파일 + 패치 순서 + 테스트 trace | 복잡해 보일 수 있음 | 최초 회귀 지점, 불필요한 수정, 검증 누락을 분리 가능 |

이 표에서 초심자가 붙잡아야 할 기준은 `로그가 많으면 번거롭다`가 아니라 `로그가 없으면 같은 실패를 다시 실험해야 한다`는 점입니다. 코딩 에이전트에서 하네스는 디버깅을 대신하는 마법이 아니라, 디버깅을 가능한 상태로 만드는 최소 기록 장치입니다.

### 사례 2. 문서 조사 에이전트

문서 조사 에이전트가 정책 변경 요약을 냈는데 내용이 틀렸다고 해 봅시다. 사람이 최종 문장만 보면 에이전트가 잘못 요약했는지, 애초에 엉뚱한 문서를 검색했는지 구분하기 어렵습니다. 실제 개선은 이 둘을 나누어 봐야 시작할 수 있는데, 실행 기록이 없으면 둘 다 추측으로만 남습니다. 예를 들어 작년 공지를 읽고 정확히 요약한 것과, 최신 공지를 읽고도 잘못 요약한 것은 완전히 다른 실패입니다. 이 구분이 안 되면 검색 로직을 고쳐야 할지 요약 프롬프트를 고쳐야 할지 판단도 흔들립니다. harness는 어떤 문서를 검색했는지, 어떤 문단을 읽었는지, 어떤 요약 단계를 거쳤는지를 함께 남겨 문제를 단계별로 나눠 보게 합니다. 여기서 바뀌는 점은 `답이 틀렸는가`만 보던 기준에서 `검색 단계와 요약 단계 중 어디서 틀렸는가`를 구분할 수 있는가를 보는 기준으로 이동한다는 것입니다. 그래서 이 사례에서 확인해야 할 결과는 틀린 답이 나왔을 때 `검색 실패`와 `요약 실패`가 실제로 서로 다른 원인으로 분리되어 보이는가입니다.

이 장면도 실제 운영에서 자주 생깁니다. 조사 에이전트는 보통 `문서를 찾는 일`과 `찾은 문서를 정리하는 일`을 한 흐름 안에서 처리합니다. 그런데 최종 요약만 남기면 사람은 둘을 쉽게 섞어 봅니다. `답이 틀렸다`는 결과만으로는 검색 단계가 오래된 문서를 골랐는지, 최신 문서를 읽고도 해석을 잘못했는지 구분되지 않기 때문입니다. 이 차이는 개선 방향을 완전히 바꿉니다. 전자는 검색 우선순위나 최신성 필터 문제이고, 후자는 요약 규칙이나 인용 구조 문제입니다.

같은 오답이라도 하네스가 남겨 주는 기록은 다음처럼 역할이 다릅니다.

| 오답 장면 | 하네스가 없으면 남는 해석 | 하네스가 있으면 분리되는 원인 |
| --- | --- | --- |
| 작년 공지를 읽고 정확히 요약함 | `요약을 못했다`로 뭉뚱그려짐 | 검색 실패, 최신 문서 선택 실패 |
| 최신 공지를 읽고 핵심 조항을 빠뜨림 | `문서를 잘못 찾았나?`로 추측만 남음 | 요약 실패, 핵심 정보 보존 실패 |
| 여러 문서를 읽었지만 구버전과 신버전을 섞음 | `결론이 이상하다`만 남음 | 문서 선택 문제와 충돌 정리 실패를 분리 가능 |

이 사례에서 초심자가 넘어가야 할 오해는 `틀린 답은 다 같은 종류의 실패`라는 감각입니다. 하네스가 필요한 이유는 오답을 더 빨리 만드는 것이 아니라, 오답의 원인을 검색 층과 해석 층으로 갈라서 다음 수정 우선순위를 정하게 만드는 데 있습니다.

### 사례 3. 고객 지원 에이전트

고객 지원 에이전트가 환불 불가 답변을 냈는데 실제 최신 정책은 환불 가능이었다고 해 봅시다. 이때 사람이 먼저 확인해야 할 것은 `정책 문서를 오래된 것으로 읽었는가`, `읽은 내용은 맞았지만 응답 규칙이 잘못 적용되었는가`, `승인 단계 없이 바로 전송되었는가` 같은 흐름입니다. 하지만 실행 기록이 없으면 잘못된 답 하나만 남고, 어디서 틀렸는지 조직적으로 설명하기가 어려워집니다. 예를 들어 정책 해석은 맞았지만 승인 단계를 건너뛰어 바로 발송했다면, 문제는 모델 지식이 아니라 운영 통제 실패일 수 있습니다. 이런 차이가 보이지 않으면 같은 답변 오류를 다시 막기 위한 통제도 설계하기 어렵습니다. harness는 읽은 정책, 사용한 도구, 승인 여부, 평가 상태를 함께 남겨 감사와 재현을 가능하게 합니다. 여기서 바뀌는 점은 `답변이 틀렸는가`만 보던 기준에서 `오류가 어떤 운영 단계에서 발생했는가`를 보는 기준으로 이동한다는 것입니다. 그래서 이 사례에서 확인해야 할 결과는 답변 오류가 났을 때 오래된 문서 참조, 규칙 적용 오류, 승인 누락 중 어느 단계에서 문제가 났는지가 실제로 다시 설명되는가입니다.

세 사례를 운영 관점으로 다시 묶으면 다음과 같습니다.

| 상황 | 하네스가 남겨야 하는 핵심 기록 | 기록이 없으면 생기는 문제 |
| --- | --- | --- |
| 코딩 에이전트 | 읽은 파일, 패치 순서, 테스트 실패 지점 | 어느 변경이 회귀를 만들었는지 추적이 어려움 |
| 문서 조사 에이전트 | 검색 문서, 읽은 문단, 요약 단계 | 검색 실패와 요약 실패를 구분하기 어려움 |
| 고객 지원 에이전트 | 사용한 정책 문서, 승인 여부, 발송 경로 | 답변 오류가 지식 문제인지 운영 통제 문제인지 흐려짐 |

세 사례를 하네스 판단 기준으로 다시 묶으면 다음과 같습니다.

| 상황 | 하네스가 먼저 드러내야 하는 것 | 그 기록으로 분리해 볼 수 있는 실패 |
| --- | --- | --- |
| 코딩 에이전트 | 어느 파일과 테스트를 거쳤는가 | 패치 문제와 검증 누락 |
| 문서 조사 에이전트 | 어떤 문서를 읽고 어떤 문단을 근거로 삼았는가 | 검색 실패와 해석 실패 |
| 고객 지원 에이전트 | 어떤 정책과 승인 경로를 거쳤는가 | 지식 오류와 운영 통제 오류 |

즉, 여기까지의 핵심은 `실행을 더 많이 시킨다`가 아닙니다. 실행 기록을 남겨야만 바로 다음 장에서 `무엇을 기준으로 괜찮다고 볼 것인가`, `어느 실패를 검색 문제로 보고 어느 실패를 승인 문제로 볼 것인가`를 나눠 읽을 수 있다는 점이 더 중요합니다.

이 연결을 가장 짧게 잡으면 다음과 같습니다.

| 하네스에서 남기는 것 | 바로 다음 장에서 읽는 평가 질문 | 그다음 운영 장에서 이어지는 조치 |
| --- | --- | --- |
| 검색 문서와 trace | 답이 어떤 근거 위에서 나왔는가 | 검색 품질 보정, 근거 문서 교체 |
| tool call log와 승인 상태 | 실행 경로가 안전하고 적절했는가 | 승인 게이트 추가, 호출 제한 조정 |
| replay ID와 실행 설정 | 같은 실패를 다시 재현해 비교할 수 있는가 | 수정 전후 비교, 회귀 점검 |

즉, P6-15에서는 하네스를 `평가 입력`으로 읽고, P6-16에서는 같은 기록을 `운영 통제와 실패 대응 입력`으로 다시 읽습니다.

## 연습 및 예제

이번 예제의 목표는 실제 하네스 전체를 구현하는 것이 아니라, 여러 실행 기록을 보고 `무엇이 잘못되었는지`뿐 아니라 `그래서 다음 운영 조치를 무엇으로 잡아야 하는지`까지 읽는 것입니다. 단순히 기록 항목이 있나 없나만 보면 하네스가 체크리스트처럼 보일 수 있으므로, 이번에는 실행별로 운영 판단을 내려 보겠습니다.

문제 상황:

- 고객 지원 에이전트가 환불 정책을 읽고 답변 초안을 만듦
- 어떤 실행은 최신 정책을 읽었고, 어떤 실행은 오래된 문서를 읽었으며, 어떤 실행은 승인 없이 바로 전송됨
- 최종 답만 보면 세 경우가 모두 `답변 품질 문제`처럼 보이지만 실제 원인은 다름

입력:

- 여러 번의 agent 실행 기록
- 각 실행에서 사용한 도구, 읽은 문서, 승인 여부, 재현 식별자

출력:

- 실행별 run report
- 어떤 실행이 검색 실패, 승인 실패, 재현 가능성 부족으로 분리되는지에 대한 점검값
- 각 실행에서 바로 취해야 할 운영 후속 조치

먼저 이 예제에서 함께 볼 운영 점검 기준은 다음과 같습니다.

| 점검 항목 | 왜 필요한가 |
| --- | --- |
| `used_latest_policy` | 틀린 답의 원인이 오래된 근거 문서인지 분리해야 해서 |
| `approval_completed` | 지식 오류와 운영 통제 오류를 구분해야 해서 |
| `replay_ready` | 같은 실패를 다시 재현해 수정 전후를 비교해야 해서 |
| `root_issue` | 검색, 승인, 기록 중 어디가 먼저 흔들렸는지 바로 읽어야 해서 |
| 다음 운영 조치 | 문제가 보였을 때 바로 어떤 운영 조치를 취할지 정해야 해서 |

문제 상황:

- 운영 사고를 분석할 때는 단순 실패 여부보다 최신 근거 사용, 승인 흐름, 재현 가능성을 함께 봐야 원인을 분리할 수 있다

입력(input):

위에 정리한 실행 run 기록 목록을 사용합니다.

확인할 개념:

- 하네스와 실행 로그는 실패를 재현 가능하게 남겨야 원인 분리와 다음 운영 조치를 동시에 정할 수 있다

```python
from pprint import pprint

runs = [
    {
        "run_id": "run-2026-06-30-001",
        "goal": "최신 환불 정책을 찾아 답변 초안을 만든다",
        "tools_used": ["search_policy_docs", "read_file", "request_approval"],
        "documents_read": ["refund_policy_2026_06_29"],
        "trace": [
            {"step": 1, "action": "search_policy_docs", "status": "ok"},
            {"step": 2, "action": "read_file", "status": "ok"},
            {"step": 3, "action": "request_approval", "status": "approved"},
        ],
        "draft_answer": "최신 정책 기준으로 환불 가능",
        "trace_saved": True,
        "eval_status": "passed",
        "approval_completed": True,
        "replay_id": "run-2026-06-30-001",
    },
    {
        "run_id": "run-2026-06-30-002",
        "goal": "최신 환불 정책을 찾아 답변 초안을 만든다",
        "tools_used": ["search_policy_docs", "read_file", "request_approval"],
        "documents_read": ["refund_policy_2025_12_01"],
        "trace": [
            {"step": 1, "action": "search_policy_docs", "status": "ok"},
            {"step": 2, "action": "read_file", "status": "ok"},
            {"step": 3, "action": "request_approval", "status": "approved"},
        ],
        "draft_answer": "환불 불가",
        "trace_saved": True,
        "eval_status": "failed",
        "approval_completed": True,
        "replay_id": "run-2026-06-30-002",
    },
    {
        "run_id": "run-2026-06-30-003",
        "goal": "최신 환불 정책을 찾아 답변 초안을 만든다",
        "tools_used": ["search_policy_docs", "read_file", "send_reply"],
        "documents_read": ["refund_policy_2026_06_29"],
        "trace": [
            {"step": 1, "action": "search_policy_docs", "status": "ok"},
            {"step": 2, "action": "read_file", "status": "ok"},
            {"step": 3, "action": "send_reply", "status": "sent_without_approval"},
        ],
        "draft_answer": "최신 정책 기준으로 환불 가능",
        "trace_saved": False,
        "eval_status": "needs_review",
        "approval_completed": False,
        "replay_id": None,
    },
]

def inspect_run(record):
    used_latest_policy = any("2026_06_29" in doc for doc in record["documents_read"])
    replay_ready = record["trace_saved"] and record["replay_id"] is not None

    if not used_latest_policy:
        root_issue = "stale_reference"
    elif not record["approval_completed"]:
        root_issue = "approval_gap"
    elif not replay_ready:
        root_issue = "replay_gap"
    else:
        root_issue = "healthy_run"

    next_action_map = {
        "healthy_run": "keep_as_reference_run",
        "stale_reference": "fix_retrieval_source_and_compare_again",
        "approval_gap": "insert_approval_gate_before_send",
        "replay_gap": "save_trace_and_assign_replay_id",
    }

    return {
        "run_id": record["run_id"],
        "tool_count": len(record["tools_used"]),
        "trace_steps": len(record["trace"]),
        "used_latest_policy": used_latest_policy,
        "approval_completed": record["approval_completed"],
        "has_eval_status": "eval_status" in record,
        "has_replay_id": record["replay_id"] is not None,
        "replay_ready": replay_ready,
        "root_issue": root_issue,
        "next_action": next_action_map[root_issue],
    }

reports = []
for run in runs:
    inspection = inspect_run(run)
    reports.append({"run": run, "inspection": inspection})

summary = {
    "healthy_run_count": sum(report["inspection"]["root_issue"] == "healthy_run" for report in reports),
    "stale_reference_count": sum(report["inspection"]["root_issue"] == "stale_reference" for report in reports),
    "approval_gap_count": sum(report["inspection"]["root_issue"] == "approval_gap" for report in reports),
    "replay_gap_count": sum(report["inspection"]["root_issue"] == "replay_gap" for report in reports),
    "replay_ready_count": sum(report["inspection"]["replay_ready"] for report in reports),
    "approval_completed_ratio": round(
        sum(report["inspection"]["approval_completed"] for report in reports) / len(reports), 2
    ),
    "replay_ready_ratio": round(
        sum(report["inspection"]["replay_ready"] for report in reports) / len(reports), 2
    ),
}

print("[summary]")
pprint(summary)
print()

for report in reports:
    print("=" * 80)
    print("[run_id]")
    print(report["run"]["run_id"])
    print("[inspection]")
    pprint(report["inspection"])
    print("[trace]")
    pprint(report["run"]["trace"])
    print("[documents_read]")
    pprint(report["run"]["documents_read"])
```

실행 결과 예시는 다음처럼 읽을 수 있습니다.

```text
[summary]
{'approval_completed_ratio': 0.67,
 'approval_gap_count': 1,
 'healthy_run_count': 1,
 'replay_gap_count': 0,
 'replay_ready_count': 2,
 'replay_ready_ratio': 0.67,
 'stale_reference_count': 1}

================================================================================
[run_id]
run-2026-06-30-001
[inspection]
{'approval_completed': True,
 'has_eval_status': True,
 'has_replay_id': True,
 'next_action': 'keep_as_reference_run',
 'replay_ready': True,
 'root_issue': 'healthy_run',
 'run_id': 'run-2026-06-30-001',
 'tool_count': 3,
 'trace_steps': 3,
 'used_latest_policy': True}
[trace]
[{'action': 'search_policy_docs', 'status': 'ok', 'step': 1},
 {'action': 'read_file', 'status': 'ok', 'step': 2},
 {'action': 'request_approval', 'status': 'approved', 'step': 3}]
[documents_read]
['refund_policy_2026_06_29']
================================================================================
[run_id]
run-2026-06-30-002
[inspection]
{'approval_completed': True,
 'has_eval_status': True,
 'has_replay_id': True,
 'next_action': 'fix_retrieval_source_and_compare_again',
 'replay_ready': True,
 'root_issue': 'stale_reference',
 'run_id': 'run-2026-06-30-002',
 'tool_count': 3,
 'trace_steps': 3,
 'used_latest_policy': False}
[trace]
[{'action': 'search_policy_docs', 'status': 'ok', 'step': 1},
 {'action': 'read_file', 'status': 'ok', 'step': 2},
 {'action': 'request_approval', 'status': 'approved', 'step': 3}]
[documents_read]
['refund_policy_2025_12_01']
================================================================================
[run_id]
run-2026-06-30-003
[inspection]
{'approval_completed': False,
 'has_eval_status': True,
 'has_replay_id': False,
 'next_action': 'insert_approval_gate_before_send',
 'replay_ready': False,
 'root_issue': 'approval_gap',
 'run_id': 'run-2026-06-30-003',
 'tool_count': 3,
 'trace_steps': 3,
 'used_latest_policy': True}
[trace]
[{'action': 'search_policy_docs', 'status': 'ok', 'step': 1},
 {'action': 'read_file', 'status': 'ok', 'step': 2},
 {'action': 'send_reply', 'status': 'sent_without_approval', 'step': 3}]
[documents_read]
['refund_policy_2026_06_29']
```

이 예제에서 먼저 봐야 할 것은 `stale_reference_count`, `approval_gap_count`, `replay_ready_ratio`가 서로 다른 운영 축을 보여 준다는 점입니다. 즉, 답변 오류처럼 보여도 실제로는 `오래된 문서 참조`, `승인 누락`, `재현 정보 부족`이 따로 분리되고, 각 축마다 다음 조치도 달라집니다. 하네스가 없다면 이 세 경우는 모두 `최종 답이 이상함`이라는 한 문장으로 뭉개지기 쉽습니다.

그래서 이 예제에서 확인해야 할 결과는 결과 텍스트 하나만 남는 것이 아니라, 사용한 도구, 읽은 문서, 실행 trace, 평가 상태, replay 식별자까지 함께 추적되어 실패 원인을 실제 운영 단계로 나눠 볼 수 있다는 점입니다.

이 예제에서 독자가 직접 해 볼 수 있는 조정은 다음과 같습니다.

- `run-2026-06-30-002`의 문서 이름을 최신 정책으로 바꿔 `stale_reference_count`가 어떻게 줄어드는지 보기
- `run-2026-06-30-003`에 `request_approval` 단계를 추가해 승인 누락과 재현 가능성 문제가 어떻게 분리되는지 보기
- `trace_saved`와 `replay_id`를 따로 바꿔 재현 준비가 왜 단일 플래그 하나로 끝나지 않는지 확인하기

여기서 한 단계 더 나가면, 하네스가 직접 해결하는 것과 평가나 운영에서 다시 판단해야 하는 것을 분리해 읽는 편이 좋습니다.

| 먼저 보인 신호 | 하네스 층에서 바로 남겨야 하는 것 | 그다음 평가/운영에서 이어지는 판단 |
| --- | --- | --- |
| 최종 답은 틀렸는데 원인이 불명확함 | 읽은 문서, tool call trace, approval 기록 | 검색 실패인지 해석 실패인지 운영 통제 실패인지 구분 |
| 수정 전후를 비교해야 함 | replay ID, 실행 설정, trace 저장 여부 | 회귀가 줄었는지 같은 조건에서 재평가 |
| 승인 없이 실행이 나감 | approval 상태와 실제 전송 경로 | 승인 게이트 추가, 자동 차단 정책 보강 |
| 특정 실패가 다시 재현되지 않음 | 입력, 도구 호출, 중간 상태 기록 | 재현 불가 상태를 운영 리스크로 볼지 판단 |

이 표의 핵심은 하네스가 `좋다/나쁘다를 판정하는 층`이 아니라, 그 판정을 가능하게 만드는 기록 층이라는 점입니다. 평가 장은 이 기록을 품질 기준으로 읽고, 운영 장은 같은 기록을 통제와 복구 조치로 읽습니다.

## 이 예제를 운영 기록 관점으로 다시 보면

앞의 예제는 실제 하네스를 구현하는 코드가 아니라, `좋은 결과가 나왔는가`보다 먼저 `무슨 실행이 있었고 무엇이 남아야 하는가`를 점검하는 최소 장면입니다. 여기서 중요한 것은 기록 항목을 많이 나열하는 일이 아니라, 결과 문장 하나로는 운영 개선이 불가능하고, 서로 다른 실패를 서로 다른 운영 원인으로 분리해야 한다는 점을 짧게 체감하는 데 있습니다.

여기까지를 한 줄로 묶으면, 하네스 관점은 `답변 결과를 저장하는 장치`가 아니라 `같은 실패를 다시 설명하고 다음 운영 조치를 정하게 만드는 실행 기록 구조`입니다.

이 절에서 더 중요하게 붙잡아야 할 점은 `답변이 괜찮은가`와 `그 답에 이르기까지의 실행을 다시 설명하고 통제할 수 있는가`가 같은 문제가 아니라는 것입니다. 그래서 하네스는 실행 결과를 저장하는 부속 장치가 아니라, trace, replay, approval 같은 기록으로 tool use와 agent를 운영 가능한 구조로 바꾸는 패턴으로 읽는 편이 좋습니다.

커리큘럼 관점에서 이 절이 중요한 이유는 다음과 같습니다.

- tool use와 agent를 운영 가능성 관점으로 확장해 읽게 하고
- 이후 평가(evaluation), 비용, 실패 대응, 서비스 제약 장으로 자연스럽게 연결하며
- Part 7 프로젝트에서 `단순 동작`보다 `관리 가능한 동작`을 설계하게 만들기 때문입니다

바로 이 지점에서 실행 기록은 다음 장의 평가 입력으로 바뀝니다. 답변 문장만 보면 `괜찮다/이상하다` 정도만 말하기 쉽지만, trace와 approval 기록, replay 정보까지 함께 보면 `검색 근거가 낡았는가`, `승인 경계가 비었는가`, `같은 실행을 다시 비교할 수 있는가`처럼 평가 축을 분리할 수 있습니다.

## 체크리스트

| 상황 | 먼저 떠올릴 관점 | 왜 중요한가 |
| --- | --- | --- |
| 최종 답만 보고는 왜 실패했는지 설명하기 어려울 때 | 실행 기록을 감싸는 관리 환경이 먼저 필요하다는 점 | 어떤 입력, 어떤 도구 호출, 어떤 승인 경계를 거쳤는지 남겨야 실패 원인을 단계별로 나눠 볼 수 있습니다. |
| 같은 작업을 다시 재현하거나 수정 전후를 비교해야 할 때 | trace, replay, approval 기록이 기준선이라는 점 | 실행 흔적이 없으면 개선이 아니라 추측만 반복하게 됩니다. |
| 다음 장의 평가가 무엇을 근거로 판단하는지 감이 오지 않을 때 | 하네스가 평가 입력을 남기는 층위라는 점 | 평가 절은 추상 판정이 아니라, 하네스가 남긴 실행 기록을 기준으로 품질을 읽는 단계입니다. |

| 지금 이 절에서 정리한 것 | 바로 다음에 붙는 질문 | 이 용어가 맡는 층위 |
| --- | --- | --- |
| 하네스는 실행을 감싸고 trace, replay, approval을 남기는 실행 관리 환경이다 | 이 기록으로 무엇이 좋은 답과 좋은 실행인지 어떻게 판정할까 | `연결을 써서 실제 실행을 어떻게 관리할까`를 다루는 운영 입력 층위 |

- 하네스는 에이전트 실행을 감싸고 기록하고 평가하는 운영 장치에 가깝습니다.
- MCP는 연결 인터페이스, harness는 실행 관리 구조라는 점에서 다릅니다.
- trace, log, eval, replay는 실행 기록을 남기고, 같은 실패를 재현하고, 수정 전후 차이를 비교하게 해 주는 운영 기준선입니다.
- harness를 통해 같은 실행을 다시 재생하고 승인 경계를 남기며 수정 전후 차이를 비교할 수 있어, 운영 개선의 기준선이 됩니다.

하네스는 실행을 감싸고 `trace`, `replay`, `approval` 기록을 남기는 실행 관리 구조입니다. MCP가 연결을 다룬다면 하네스는 그 연결을 쓴 실행 흐름의 기록과 비교를 다룹니다.

- 하네스를 `도구 하나`가 아니라 `실행을 감싸고 기록하고 평가 입력을 남기는 운영 장치`로 설명할 수 있어야 합니다.
- MCP가 연결을 다루고 하네스가 실행 관리와 재현 기준을 다룬다는 차이를 말할 수 있어야 합니다.
- 다음 장의 평가는 하네스와 별개로 떠 있는 추상 판단이 아니라, 여기서 남긴 기록을 품질 기준으로 읽는 단계라는 점을 잡고 있어야 합니다.

## 출처와 참고 자료

- OpenAI, [Integrations and observability](https://developers.openai.com/api/docs/guides/agents/integrations-observability){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, 확인 날짜: 2026-07-05.
- OpenAI, [Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, 확인 날짜: 2026-07-05.
- OpenAI, [Agents SDK](https://developers.openai.com/api/docs/guides/agents){: target="_blank" rel="noopener noreferrer" }, OpenAI API Docs, 확인 날짜: 2026-07-05.
