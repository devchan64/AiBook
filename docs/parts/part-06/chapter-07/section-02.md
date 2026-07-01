# P6-7.2 실패 기록과 개선 계획

배포 프로젝트의 마지막 단계는 배포 성공 화면을 보고 끝내는 일이 아닙니다. 실제로는 `무엇이 실패할 수 있었고, 무엇을 다음에 먼저 개선할 것인가`를 남겨야 프로젝트가 닫힙니다.

이번 절은 그 회고 문서를 다룹니다.

이 절의 목적은 배포가 끝난 뒤 성공 화면만 남기는 것이 아니라, 실패 유형과 다음 조치를 분리해 기록하는 것이다.

## 이 절의 범위

이 절은 다음 질문에 답합니다.

- 정적 사이트 프로젝트에서 어떤 실패를 기록해야 하는가?
- 배포 실패와 콘텐츠 실패를 왜 구분해야 하는가?
- 개선 계획은 어떻게 우선순위를 붙이면 좋은가?

이 절은 다음 내용은 깊게 다루지 않습니다.

- 본격 incident management 시스템
- 장기 비용 분석
- 팀 단위 SLO 설계

이 절은 작은 문서 배포 프로젝트의 실패 유형과 우선순위 기록에 집중합니다. 대규모 incident management나 팀 단위 SLO 설계는 이 책의 현재 프로젝트 입문 범위 밖으로 두고, 대신 `실패를 원인 추정과 다음 조치로 남기는 습관`까지를 이 절의 회수 범위로 삼습니다.

## 이 절의 목표

- 배포 프로젝트의 실패 유형을 몇 가지 범주로 정리할 수 있습니다.
- 실패 기록을 `원인 추정`과 `다음 조치`까지 연결해 적을 수 있습니다.
- 작은 문서 프로젝트에도 운영 회고가 필요하다는 점을 설명할 수 있습니다.

## 실패 유형을 나누어 보기

정적 문서 배포 프로젝트에서 흔한 실패는 크게 네 가지로 나눌 수 있습니다.

| 실패 유형 | 예시 |
| --- | --- |
| build failure | MkDocs 설정 오류, 링크 문법 오류 |
| deploy failure | Actions workflow 실패, publishing source 문제 |
| content failure | 최신 수정이 누락됨, 제목/섹션 배치 오류 |
| runtime failure | 공개 URL은 열리지만 링크가 깨짐, 404 발생 |

이 구분이 중요한 이유는 해결 책임과 다음 행동이 다르기 때문입니다.

- build failure는 로컬 재현이 중요합니다.
- deploy failure는 CI 로그 확인이 중요합니다.
- content failure는 문서 검토가 중요합니다.
- runtime failure는 공개 페이지 실제 확인이 중요합니다.

먼저 다음 세 질문으로 읽으면 좋습니다.

| 질문 | 짧은 답 |
| --- | --- |
| 왜 실패를 나누는가? | 같은 실패처럼 보여도 대응이 다르기 때문 |
| 무엇을 같이 적어야 하는가? | category, likely cause, next action |
| 최소 산출물은 무엇인가? | 실패 기록 표와 우선순위 목록 |

## 작은 실패 기록 예시

이번 절에서는 프로젝트 회고 문서를 다음 형식으로 남기는 예를 듭니다.

| date | issue | category | likely cause | next action |
| --- | --- | --- | --- | --- |
| 2026-06-29 | 최신 섹션이 배포 페이지에 보이지 않음 | deploy/content | main 미반영 또는 workflow 지연 | Actions 로그 확인, main 반영 상태 재확인 |
| 2026-06-29 | 내부 링크 404 | runtime | nav와 실제 경로 불일치 | mkdocs nav와 파일 경로 재검토 |
| 2026-06-29 | 수식 렌더링 누락 | content/runtime | JS 로드 또는 문법 문제 | 브라우저 확인, 수식 블록 점검 |

이 표는 단순하지만 회고 문서로 충분히 유용합니다.

이 표는 Part 6의 배포 프로젝트에서 사실상 `운영 회고 템플릿` 역할을 합니다.

## 바로 쓰는 실패 기록 템플릿

배포 프로젝트를 마친 뒤 바로 채울 수 있는 최소 템플릿은 다음 정도면 충분합니다.

```text
### incident record
- date:
- issue:
- category:
- likely_cause:
- user_impact:
- priority:
- next_action:

### review summary
- 가장 먼저 고칠 문제:
- 이번 반복에서 미루는 문제:
- 다음 배포 전에 추가할 점검:
```

이 템플릿의 핵심은 `실패했다`에서 멈추지 않는 것입니다. 적어도 `어떤 종류의 실패였는가`, `독자에게 어떤 영향이 있었는가`, `다음에 무엇을 먼저 할 것인가`까지는 같이 적어야 합니다.

예를 들어 내부 링크가 404였던 경우는 다음처럼 바로 채울 수 있습니다.

```text
### incident record
- date: 2026-06-29
- issue: 내부 링크 404
- category: runtime
- likely_cause: mkdocs nav와 실제 파일 경로 불일치
- user_impact: 독자 흐름이 끊긴다
- priority: 1
- next_action: nav와 target 경로를 함께 다시 확인한다

### review summary
- 가장 먼저 고칠 문제: 독자가 바로 만나게 되는 404 링크
- 이번 반복에서 미루는 문제: 수식 렌더링 미세 조정
- 다음 배포 전에 추가할 점검: 공개 URL에서 핵심 링크 3개 직접 클릭
```

## Python 예제

이번 예제의 목적은 실패 표를 실제 회고 기록 구조로 바꾸는 것입니다.

- 문제 상황: 배포 이후 생긴 문제를 다시 읽고 다음 조치를 정리한다.
- 입력(input): 실패 항목 목록
- 기대 출력(output): 우선순위가 붙은 incident 기록과 개선 계획
- 확인할 개념:
  - 실패는 category별로 나누어 남겨야 한다
  - likely cause와 next action이 함께 있어야 한다
  - 우선순위가 붙어야 다음 반복으로 이어진다

```python
incident_records = [
    {
        "date": "2026-06-29",
        "issue": "latest section missing on deployed page",
        "category": "deploy/content",
        "likely_cause": "main branch not updated or workflow still pending",
        "user_impact": "readers cannot see the newest section",
        "priority": 1,
        "next_action": "check Actions run and confirm main branch status",
    },
    {
        "date": "2026-06-29",
        "issue": "internal link returns 404",
        "category": "runtime",
        "likely_cause": "nav path and actual file path do not match",
        "user_impact": "reader flow is interrupted",
        "priority": 1,
        "next_action": "review mkdocs nav and target file paths",
    },
    {
        "date": "2026-06-29",
        "issue": "math rendering is missing on one page",
        "category": "content/runtime",
        "likely_cause": "script load or markdown syntax problem",
        "user_impact": "equation explanation becomes unclear",
        "priority": 2,
        "next_action": "recheck browser rendering and math block syntax",
    },
]

incident_records.sort(key=lambda row: (row["priority"], row["date"]))

improvement_plan = []
for row in incident_records:
    if row["priority"] == 1:
        action_bucket = "fix_immediately"
    elif row["priority"] == 2:
        action_bucket = "fix_next_cycle"
    else:
        action_bucket = "track_for_later"

    improvement_plan.append({
        "issue": row["issue"],
        "action_bucket": action_bucket,
        "next_action": row["next_action"],
    })

review_summary = {
    "incident_count": len(incident_records),
    "priority_1_count": sum(row["priority"] == 1 for row in incident_records),
    "priority_2_count": sum(row["priority"] == 2 for row in incident_records),
    "categories": sorted({row["category"] for row in incident_records}),
}

print("review_summary =", review_summary)
print("incident_records =")
for row in incident_records:
    print(row)
print("improvement_plan =")
for row in improvement_plan:
    print(row)
```

실행 결과 예시는 다음과 같습니다.

```text
review_summary = {'incident_count': 3, 'priority_1_count': 2, 'priority_2_count': 1, 'categories': ['content/runtime', 'deploy/content', 'runtime']}
incident_records =
{'date': '2026-06-29', 'issue': 'latest section missing on deployed page', 'category': 'deploy/content', 'likely_cause': 'main branch not updated or workflow still pending', 'user_impact': 'readers cannot see the newest section', 'priority': 1, 'next_action': 'check Actions run and confirm main branch status'}
{'date': '2026-06-29', 'issue': 'internal link returns 404', 'category': 'runtime', 'likely_cause': 'nav path and actual file path do not match', 'user_impact': 'reader flow is interrupted', 'priority': 1, 'next_action': 'review mkdocs nav and target file paths'}
{'date': '2026-06-29', 'issue': 'math rendering is missing on one page', 'category': 'content/runtime', 'likely_cause': 'script load or markdown syntax problem', 'user_impact': 'equation explanation becomes unclear', 'priority': 2, 'next_action': 'recheck browser rendering and math block syntax'}
improvement_plan =
{'issue': 'latest section missing on deployed page', 'action_bucket': 'fix_immediately', 'next_action': 'check Actions run and confirm main branch status'}
{'issue': 'internal link returns 404', 'action_bucket': 'fix_immediately', 'next_action': 'review mkdocs nav and target file paths'}
{'issue': 'math rendering is missing on one page', 'action_bucket': 'fix_next_cycle', 'next_action': 'recheck browser rendering and math block syntax'}
```

## 이 출력은 어떻게 읽는가

이 예제에서 중요한 점은 세 가지입니다.

1. `incident_records`  
   실패를 단순 사건 메모가 아니라 `category`, `likely_cause`, `user_impact`, `priority`가 있는 운영 기록으로 남깁니다.

2. `improvement_plan`  
   같은 실패 목록이라도 `fix_immediately`, `fix_next_cycle`처럼 행동 구간으로 나누면 다음 반복이 쉬워집니다.

3. `review_summary`  
   우선순위 1 문제가 몇 개인지 바로 보여 주므로, 무엇을 먼저 고쳐야 하는지 한눈에 읽을 수 있습니다.

즉, 회고 문서는 과거 설명이 아니라 다음 반복을 여는 작업 목록이어야 합니다.

## 왜 postmortem 습관이 필요한가

Google SRE 책은 postmortem culture를 failure에서 배우는 문화로 다룹니다. 이 책의 Part 6 프로젝트 수준에서는 거대한 조직 절차까지 갈 필요는 없지만, 핵심 태도는 그대로 가져올 수 있습니다.

- 실패를 숨기지 않는다.
- 원인을 단정하기보다 가능한 설명을 적는다.
- 다음 반복에서 바꿀 것을 남긴다.

즉, 회고는 책임 추궁이 아니라 `반복 가능한 개선 메모`입니다.

이 문장은 Part 6 전체를 마무리하는 태도이기도 합니다. 작은 프로젝트라도 실패를 남겨야 다음 반복이 쉬워집니다.

## 개선 계획 우선순위 붙이기

개선 계획은 많아질수록 오히려 실행되지 않기 쉽습니다. 그래서 작은 프로젝트에서는 다음처럼 우선순위를 붙이는 편이 좋습니다.

1. 다시 발생하면 바로 보이는 문제  
   예: broken link, build failure
2. 독자 경험을 직접 해치는 문제  
   예: 최신 내용 미반영, 모바일 가독성 저하
3. 나중에 구조적으로 키워야 할 문제  
   예: 배포 자동 검증 강화, 모니터링 항목 추가

이렇게 나누면 회고가 단순 희망사항 목록으로 끝나지 않습니다.

이 우선순위를 다음 세 줄로 요약할 수 있으면 충분합니다.

- 먼저 다시 보이는 실패를 고친다
- 다음으로 독자 경험을 해치는 문제를 고친다
- 그다음 구조적 개선을 계획한다

## 나쁜 실패 기록과 좋은 실패 기록

실패 기록도 자주 너무 짧거나 너무 감정적으로 끝납니다. 다음 정도로 대비해 보면 기준이 분명해집니다.

| 구분 | 예시 |
| --- | --- |
| 나쁜 기록 | `배포가 좀 이상했다. 나중에 확인 필요.` |
| 좋은 기록 | `최신 섹션이 배포 페이지에 보이지 않았다. category는 deploy/content로 보고, main 미반영 또는 workflow 지연 가능성을 먼저 확인한다. 독자는 최신 내용을 읽을 수 없으므로 priority는 1로 둔다.` |

좋은 기록은 완벽한 원인 분석이 없어도 괜찮습니다. 대신 `관찰된 현상`, `현재 가능한 원인 추정`, `다음 조치`, `우선순위`가 함께 남아 있어야 다음 반복에서 바로 다시 잡을 수 있습니다.

## 프로젝트 회고 문장 예시

> 이번 정적 문서 배포 프로젝트는 로컬 빌드와 GitHub Pages 배포를 분리해 확인하는 구조를 정리했다. 그러나 배포 성공 여부만으로는 충분하지 않았고, 최신 문서 반영, 내부 링크 정상 동작, 실제 공개 페이지 확인이 별도 단계로 필요했다. 다음 반복에서는 배포 후 점검 체크리스트를 더 짧고 명확하게 만들고, 링크 점검과 최근 수정 반영 여부를 우선 확인 항목으로 두는 것이 적절하다.

## 이 책 전체와의 연결

Part 6의 마지막 회고는 사실 이 책 전체의 학습 방식과도 연결됩니다.

- 개념을 배웠다.
- 작은 프로젝트로 다시 해 봤다.
- 실패와 한계를 기록했다.
- 다음 반복 계획을 남겼다.

이 흐름이 있어야 재학습 저장소가 단순 메모가 아니라 `계속 갱신되는 학습 시스템`이 됩니다.

이 절은 Part 6 전체 흐름에서 `프로젝트의 끝은 구현 완료가 아니라 회고와 다음 계획 작성`이라는 점을 고정합니다.

## 이 절에서 기억할 관점

- 배포 프로젝트에도 실패 기록이 필요합니다.
- build, deploy, content, runtime 실패를 구분하면 회고가 더 선명해집니다.
- 개선 계획은 우선순위를 붙여야 실제 행동으로 이어집니다.
- 작은 프로젝트의 회고 습관이 큰 운영 문화의 출발점입니다.

## 체크리스트

- 실패를 유형별로 나눠 기록할 수 있는가?
- likely cause와 next action을 함께 적었는가?
- 독자 경험에 직접 영향을 주는 문제를 우선순위로 올렸는가?
- 회고가 다음 반복 계획으로 이어지는가?

## 출처와 참고 자료

- GitHub Docs, `Creating a GitHub Pages site`, 확인 날짜: 2026-06-29. [https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site){: target="_blank" rel="noopener noreferrer" }
- Google, `Monitoring Distributed Systems`, Site Reliability Engineering Book, 확인 날짜: 2026-06-29. [https://sre.google/sre-book/monitoring-distributed-systems/](https://sre.google/sre-book/monitoring-distributed-systems/){: target="_blank" rel="noopener noreferrer" }

이 절의 실패 기록 표는 Part 6 프로젝트 회고를 위해 구성한 자체 예시입니다.
