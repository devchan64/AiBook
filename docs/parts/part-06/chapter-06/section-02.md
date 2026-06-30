# P6-6.2 권한과 로그 검토

P6-6.1에서는 agent를 목표, 도구, 관찰의 흐름으로 설명했습니다. 하지만 실제 agent 프로젝트는 여기서 바로 멈추면 위험합니다.

도구를 호출할 수 있다는 말은 곧 다음 질문을 뜻하기 때문입니다.

- 누구 권한으로 실행하는가?
- 실패하면 어디에 남는가?
- 같은 작업을 다시 추적할 수 있는가?

이 절은 agent 프로젝트의 `권한(permission)`과 `로그(log)`를 다룹니다.

이 절의 목적은 agent가 무엇을 할 수 있는가보다, 무엇을 해도 되는가와 무엇을 남겨야 하는가를 프로젝트 문서에 적는 것이다.

## 이 절의 범위

이 절은 다음 질문에 답합니다.

- agent 프로젝트에서 권한을 왜 먼저 적어야 하는가?
- 로그는 단순 디버그 출력이 아니라 무엇을 위한 기록인가?
- 승인(approval), 상태(state), 범위(scope)는 어떻게 프로젝트 문서에 남길 수 있는가?

이 절은 다음 내용은 깊게 다루지 않습니다.

- 감사 시스템(audit system)의 전체 설계
- 보안 정책 엔진
- 분산 tracing 인프라

이 절에서는 권한 범위와 로그 기록을 프로젝트 문서에 남기는 최소 기준만 다룹니다. 배포 이후 실패 추적과 운영 회고는 P6-7.1 배포와 모니터링 목표, P6-7.2 실패 기록과 개선 계획에서 다시 이어지며, 감사 시스템과 보안 정책 엔진 전체 설계는 현재 본편 범위 밖으로 둡니다.

## 이 절의 목표

- agent 실행에서 권한과 로그가 왜 중심 요소인지 설명할 수 있습니다.
- 단순 실행 성공 여부보다 `무슨 도구를 어떤 범위에서 썼는가`를 기록하는 법을 알 수 있습니다.
- 실패 대응 문서를 agent 실행 기록과 연결할 수 있습니다.

## 왜 권한이 먼저인가

도구를 쓰는 agent는 단순 텍스트 생성보다 훨씬 강한 행동력을 가질 수 있습니다.

예를 들어:

- 파일 읽기
- 파일 수정
- 빌드 실행
- 외부 API 호출

이 행동들은 모두 같은 위험도를 갖지 않습니다. 그래서 프로젝트 문서에는 최소 다음을 구분하는 편이 좋습니다.

먼저 다음 세 질문으로 읽으면 좋습니다.

| 질문 | 짧은 답 |
| --- | --- |
| 왜 권한을 먼저 적는가? | 도구마다 위험도가 다르기 때문 |
| 로그는 왜 필요한가? | 어떤 실행이 일어났는지 다시 보기 위해 |
| 최소 산출물은 무엇인가? | permission, approval, result가 들어간 실행 기록 |

| 항목 | 질문 |
| --- | --- |
| permission | 이 도구를 그냥 실행해도 되는가? |
| approval | 사람 승인이 필요한가? |
| scope | 어느 파일, 어느 디렉터리, 어느 시스템까지 허용되는가? |
| log | 실행 결과와 실패 원인은 어디에 남는가? |

## 왜 로그가 중요한가

로그는 단순 출력 저장이 아닙니다. agent 프로젝트에서는 다음 목적을 가집니다.

- 어떤 도구를 호출했는지 추적
- 어느 단계에서 실패했는지 확인
- 승인 여부 기록
- 나중에 회고할 근거 확보

즉, agent 로그는 `관찰(observation)의 역사`입니다.

이 표현은 중요합니다. 결과 한 줄만 남기면 agent 프로젝트는 재현과 회고가 거의 불가능해집니다.

## 작은 실행 기록 예제

이번 절에서는 toy agent가 다음 세 단계를 거쳤다고 가정해 봅니다.

1. `read_toc`
2. `check_build`
3. `write_report`

그런데 마지막 단계는 쓰기 권한이 필요합니다. 따라서 로그에는 단순 성공/실패가 아니라 `승인 필요 여부`도 남겨야 합니다.

## Python 예제

```python
planned_steps = [
    {"step": 1, "tool": "read_toc", "permission": "read", "scope": "docs/book/"},
    {"step": 2, "tool": "check_build", "permission": "execute", "scope": "mkdocs build"},
    {"step": 3, "tool": "write_report", "permission": "write", "scope": "management/report.md"},
]

execution_records = [
    {
        "step": 1,
        "tool": "read_toc",
        "permission": "read",
        "scope": "docs/book/",
        "approved": True,
        "result_status": "success",
        "observation": "table of contents was loaded",
        "next_action": "check_build",
    },
    {
        "step": 2,
        "tool": "check_build",
        "permission": "execute",
        "scope": "mkdocs build",
        "approved": True,
        "result_status": "success",
        "observation": "build finished without error",
        "next_action": "write_report",
    },
    {
        "step": 3,
        "tool": "write_report",
        "permission": "write",
        "scope": "management/report.md",
        "approved": False,
        "result_status": "blocked",
        "observation": "write action requires approval before continuing",
        "next_action": "request_approval",
    },
]

review_summary = {
    "step_count": len(execution_records),
    "approved_step_count": sum(entry["approved"] for entry in execution_records),
    "blocked_step_count": sum(
        entry["result_status"] == "blocked" for entry in execution_records
    ),
    "approval_required_tools": [
        entry["tool"] for entry in execution_records if not entry["approved"]
    ],
}

print("planned_steps =", planned_steps)
print("execution_records =")
for entry in execution_records:
    print(entry)
print("review_summary =", review_summary)
```

실행 결과 예시는 다음과 같습니다.

```text
planned_steps = [{'step': 1, 'tool': 'read_toc', 'permission': 'read', 'scope': 'docs/book/'}, {'step': 2, 'tool': 'check_build', 'permission': 'execute', 'scope': 'mkdocs build'}, {'step': 3, 'tool': 'write_report', 'permission': 'write', 'scope': 'management/report.md'}]
execution_records =
{'step': 1, 'tool': 'read_toc', 'permission': 'read', 'scope': 'docs/book/', 'approved': True, 'result_status': 'success', 'observation': 'table of contents was loaded', 'next_action': 'check_build'}
{'step': 2, 'tool': 'check_build', 'permission': 'execute', 'scope': 'mkdocs build', 'approved': True, 'result_status': 'success', 'observation': 'build finished without error', 'next_action': 'write_report'}
{'step': 3, 'tool': 'write_report', 'permission': 'write', 'scope': 'management/report.md', 'approved': False, 'result_status': 'blocked', 'observation': 'write action requires approval before continuing', 'next_action': 'request_approval'}
review_summary = {'step_count': 3, 'approved_step_count': 2, 'blocked_step_count': 1, 'approval_required_tools': ['write_report']}
```

## 결과를 어떻게 읽는가

이 출력에서 중요한 것은 마지막 줄입니다.

- agent는 계획을 세웠습니다.
- 하지만 모든 계획이 자동 실행 가능한 것은 아닙니다.
- `write_report`는 기능적으로 가능해 보여도, 권한 정책상 보류될 수 있습니다.
- `review_summary`는 몇 단계가 승인 없이 진행되었고, 어떤 도구가 approval을 요구했는지 한 번에 보여 줍니다.

즉, 좋은 agent 프로젝트는 `할 수 있는가`만이 아니라 `해도 되는가`를 함께 다룹니다.

이 결과를 다음 세 줄로 요약할 수 있으면 충분합니다.

- 계획이 있어도 승인 없이는 멈출 수 있다
- permission, scope, next_action이 함께 있어야 blocked 상태를 운영적으로 해석할 수 있다
- blocked는 단순 실패와 다른 상태다
- agent 문서에는 결과뿐 아니라 권한 판단도 남겨야 한다

## 운영 관점의 연결

이 권한과 로그 구조는 결국 운영 문제와 직결됩니다.

- 잘못된 쓰기 권한은 사고로 이어질 수 있습니다.
- 로그가 없으면 실패 원인을 설명하기 어렵습니다.
- 승인 정책이 없으면 agent 행동 범위가 불명확해집니다.

따라서 agent 프로젝트 회고 문서에는 다음을 함께 남길 수 있습니다.

- 어떤 도구는 자동 실행 허용
- 어떤 도구는 사람 승인 필요
- 어떤 실패는 재시도 가능
- 어떤 실패는 즉시 중단해야 함

이 절은 Part 6 전체 흐름에서 `실행 가능한 프로젝트는 권한과 로그 없이는 운영 관점이 빠진 상태`라는 점을 고정합니다.

## 다음 프로젝트와의 연결

이제 Part 6의 마지막 주제는 배포와 운영입니다. 사실 agent 프로젝트의 권한과 로그는 이미 운영 주제의 일부입니다. 다음 장에서는 이를 GitHub Pages 배포와 기본 모니터링, 실패 기록으로 확장합니다.

## 이 절에서 기억할 관점

- agent 프로젝트는 권한과 로그 없이 완성되지 않습니다.
- 승인(approval)은 기능 부족이 아니라 운영 안전장치입니다.
- 로그는 관찰의 역사이며, 회고의 근거입니다.
- `할 수 있는가`와 `해도 되는가`는 다른 질문입니다.

## 체크리스트

- 도구별 permission과 approval 필요 여부를 적을 수 있는가?
- 실행 로그에 최소 step/tool/result를 남겼는가?
- blocked 상태를 실패와 구분해 기록할 수 있는가?
- 권한 정책이 왜 운영 문제와 연결되는지 설명할 수 있는가?

## 출처와 참고 자료

- OpenAI, `Function calling`, OpenAI API Docs, 확인 날짜: 2026-06-29. [https://developers.openai.com/api/docs/guides/function-calling](https://developers.openai.com/api/docs/guides/function-calling){: target="_blank" rel="noopener noreferrer" }
- Model Context Protocol, `What is MCP?`, 확인 날짜: 2026-06-29. [https://modelcontextprotocol.io/docs/getting-started/intro](https://modelcontextprotocol.io/docs/getting-started/intro){: target="_blank" rel="noopener noreferrer" }
