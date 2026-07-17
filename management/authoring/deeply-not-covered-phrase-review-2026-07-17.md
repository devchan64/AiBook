# `깊게 다루지 않습니다` 문구 전수 점검 리포트

작성일: 2026-07-17

## 목적

`이 절에서는 다음 내용을 깊게 다루지 않습니다.`와 그 변형 문장이 현재 책 본문 전체에서 어떻게 쓰이고 있는지 점검하고, 초심자용 책이라는 원칙에 맞는지 검토한다.

이 리포트는 문구 자체의 존재 여부만 세지 않는다. 해당 문구 뒤에 오는 후속 내용이 다음 중 어느 패턴에 가까운지도 함께 본다.

- 후속 Section, 보충학습, 범위 밖과 연결되는가
- 단순 생략 목록만 남기고 끝나는가
- 본문 핵심 설명으로 곧바로 이어지는가
- 메타 안내가 본문보다 앞에 서는가

## 점검 기준

이번 점검은 다음 가이드 문구를 기준으로 삼았다.

- [AGENTS.md](/home/cbsim/ws/AiBook/AGENTS.md)
  - 초심자 기준으로 원고를 작성한다.
  - 초반 도입에서는 진행 멘트보다 문제 상황과 핵심 개념으로 바로 들어가는 문장을 우선한다.
  - 본문에서는 집필 의도를 메타 문장으로 드러내기보다 설명 자체가 바로 이해되게 쓰는 쪽을 우선한다.
- [management/guidelines/manuscript-writing-workflow.md](/home/cbsim/ws/AiBook/management/guidelines/manuscript-writing-workflow.md)
  - `여기서는 다루지 않습니다` 같은 문장은 단독으로 끝내지 않는다.
  - `깊게 다루지 않는 항목`을 2개 이상 적었다면 각 항목의 회수 위치를 개별적으로 확인한다.
  - 진행 순서나 집필 행동을 설명하는 메타 표현은 경계한다.

## 점검 범위와 방법

- 범위: `docs/` 아래 공개 본문 전체
- 제외: `management/authoring/part-05-archive-2026-07-16-pre-restructure/` 같은 아카이브, 릴리즈노트, 관리 메모
- 검색 기준: `깊게 다루지 않습니다`를 포함한 문장 전체
- 후속 내용 분류 기준:
  - `list_with_recovery`: 바로 아래 목록이 있고, 가까운 문맥 안에 `다시 다룹`, `보충학습`, `범위 밖`, `Part`, `Section ID` 수준의 회수 표지가 있음
  - `inline_with_recovery`: 인라인 문장형이지만 바로 이어 회수 위치나 범위 밖 안내가 있음
  - `list_only`: 목록은 있으나 가까운 문맥에 회수 위치가 드러나지 않음
  - `inline_only`: 인라인 문장형이고 회수 위치도 바로 드러나지 않음

## 전수 수치

전체 발생 수: `192`

Part별 발생 수:

- `part-01`: 23
- `part-02`: 37
- `part-04`: 39
- `part-05`: 35
- `part-06`: 43
- `part-07`: 15

후속 패턴별 발생 수:

- `list_with_recovery`: 160
- `inline_with_recovery`: 19
- `list_only`: 9
- `inline_only`: 4

## 전체 판단

전체 책 기준으로 보면 이 문구는 이미 `예외적 범위 조정`이 아니라 `반복적 도입 습관`에 가까운 수준까지 퍼져 있다.

다만 전수 수치만으로 바로 부정적으로 볼 필요는 없다. `192`건 중 `179`건은 회수 위치나 범위 구분이 함께 드러나는 `list_with_recovery` 또는 `inline_with_recovery` 패턴이었다. 즉, 현재 원고는 대체로 가이드가 요구한 `어디로 넘기는가`를 같이 적으려는 방향을 가지고 있다.

문제는 다음 두 가지다.

1. 초심자 기준에서는 `회수 위치가 있다`는 사실만으로 충분하지 않다.
   - 같은 절의 핵심 개념 설명보다 생략 목록이 먼저 강하게 보이면 메타 표현이 앞자리를 차지한다.
   - 특히 Part 4, 5, 6처럼 개념 설명 밀도가 높은 파트에서는 이런 도입이 반복되면 독자가 `무엇을 배웠는가`보다 `무엇을 안 하는가`를 먼저 읽게 된다.
2. 소수이지만 `list_only`와 `inline_only` 패턴이 남아 있다.
   - 이 경우는 가이드의 `각 항목 회수 위치를 개별적으로 확인한다` 기준에 직접 걸릴 가능성이 높다.

따라서 책 전체 수준의 결론은 다음과 같다.

- 현재 사용은 `전면 삭제`보다 `강한 축소와 선택적 유지`가 맞다.
- 초심자 본문 Section에서는 기본값을 `삭제`로 두고, 정말 필요한 경우에만 남기는 편이 가이드 방향과 더 가깝다.
- 남길 때는 `회수 위치가 분명한 한 문장` 또는 `오버뷰 문서에서의 범위 안내` 수준이 적절하다.

## 허용 가능한 패턴

### 1. 회수 위치가 바로 붙는 목록형

대표 예시:

- [docs/parts/part-04/chapter-11/section-02.md](/home/cbsim/ws/AiBook/docs/parts/part-04/chapter-11/section-02.md)
- [docs/parts/part-06/chapter-05/section-01.md](/home/cbsim/ws/AiBook/docs/parts/part-06/chapter-05/section-01.md)

이 패턴은 다음 조건을 만족하면 유지 가능하다.

- 절의 중심 질문이 이미 분명하다
- 생략 항목이 현재 절 이해를 돕는 범위 조정 역할만 한다
- 각 항목이 후속 절, 보충학습, 범위 밖 중 어디로 가는지 바로 드러난다

다만 이런 패턴도 반복 빈도가 너무 높으면 메타 두께가 커진다. 특히 같은 Chapter 안에서 여러 절이 모두 같은 리듬으로 시작하면 압축이 필요하다.

### 2. 인라인 문장형 + 회수 위치 연결

대표 예시:

- [docs/parts/part-02/chapter-07/section-01.md](/home/cbsim/ws/AiBook/docs/parts/part-02/chapter-07/section-01.md)
- [docs/parts/part-01/chapter-06/section-02.md](/home/cbsim/ws/AiBook/docs/parts/part-01/chapter-06/section-02.md)

이 패턴은 `여기서는 설치법을 단계별로 안내하지 않습니다. ...에서 다시 봅니다.`처럼 현재 절의 역할을 곧바로 분명히 해 준다. 초심자 독해 흐름도 비교적 덜 끊는다.

책 전체 기준으로는 이 형식이 목록형보다 더 안전하다.

## 주의가 필요한 패턴

### 1. `list_only`

이 패턴은 목록은 있지만 가까운 문맥에서 회수 위치가 드러나지 않는다. 가이드 기준상 우선 점검 대상이다.

대표 사례:

- [docs/parts/part-01/chapter-02/section-02.md](/home/cbsim/ws/AiBook/docs/parts/part-01/chapter-02/section-02.md)
- [docs/parts/part-02/chapter-04/section-03.md](/home/cbsim/ws/AiBook/docs/parts/part-02/chapter-04/section-03.md)
- [docs/parts/part-02/chapter-04/section-04.md](/home/cbsim/ws/AiBook/docs/parts/part-02/chapter-04/section-04.md)
- [docs/parts/part-02/chapter-14/section-02.md](/home/cbsim/ws/AiBook/docs/parts/part-02/chapter-14/section-02.md)
- [docs/parts/part-04/chapter-12/section-03.md](/home/cbsim/ws/AiBook/docs/parts/part-04/chapter-12/section-03.md)
- [docs/parts/part-04/chapter-15/section-02.md](/home/cbsim/ws/AiBook/docs/parts/part-04/chapter-15/section-02.md)
- [docs/parts/part-04/chapter-15/section-03.md](/home/cbsim/ws/AiBook/docs/parts/part-04/chapter-15/section-03.md)
- [docs/parts/part-05/chapter-07/section-03.md](/home/cbsim/ws/AiBook/docs/parts/part-05/chapter-07/section-03.md)
- [docs/parts/part-06/chapter-03/section-02.md](/home/cbsim/ws/AiBook/docs/parts/part-06/chapter-03/section-02.md)

이 경우의 권장 조치는 둘 중 하나다.

- 회수 위치를 짧게 붙여 정합성을 맞춘다
- 초심자에게 불필요하면 목록 자체를 걷어낸다

### 2. `inline_only`

이 패턴은 상대적으로 덜 문제적일 수 있다. 다만 `깊게 다루지 않는다`는 말만 하고 회수 위치가 없거나, 그 문장이 현재 절의 핵심 설명을 밀어내면 삭제를 우선 검토하는 편이 낫다.

대표 사례:

- [docs/parts/part-01/chapter-04/section-03.md](/home/cbsim/ws/AiBook/docs/parts/part-01/chapter-04/section-03.md)
- [docs/parts/part-01/chapter-08/section-01.md](/home/cbsim/ws/AiBook/docs/parts/part-01/chapter-08/section-01.md)
- [docs/parts/part-02/chapter-04/section-01.md](/home/cbsim/ws/AiBook/docs/parts/part-02/chapter-04/section-01.md)
- [docs/parts/part-02/chapter-07/section-02.md](/home/cbsim/ws/AiBook/docs/parts/part-02/chapter-07/section-02.md)

이 패턴은 삭제 후에도 설명 흐름이 자연스럽다면 삭제 쪽이 더 낫다.

## Part별 메모

### Part 1

- 도입부 성격의 절이 많아 `무엇을 안 하는가` 목록이 자주 붙는다.
- 큰 그림 소개 파트라는 점을 감안해도 반복 빈도가 높다.
- `list_only`와 `inline_only`가 모두 남아 있어 우선 점검 가치가 높다.

### Part 2

- 선행지식 복구 파트라 `여기서는 ... 다시 본다`형 안내가 비교적 유효하다.
- 다만 수학 입문 절에서 목록형 범위 안내가 반복되면 독자가 핵심 수학 직관보다 생략 항목을 먼저 읽게 된다.
- Part 2는 `인라인 한 문장형`으로 줄이는 것이 특히 잘 맞을 가능성이 높다.

### Part 4

- 평가 파트는 비교 대상이 많아 생략 목록이 붙기 쉽다.
- 현재는 `회수 위치가 있다`는 이유로 유지된 절이 많지만, 초심자 기준에서는 밀도를 다시 줄일 여지가 크다.
- [docs/parts/part-04/chapter-15/section-02.md](/home/cbsim/ws/AiBook/docs/parts/part-04/chapter-15/section-02.md), [docs/parts/part-04/chapter-15/section-03.md](/home/cbsim/ws/AiBook/docs/parts/part-04/chapter-15/section-03.md) 같은 곳은 우선 점검 후보다.

### Part 5

- 리뉴얼 이후에도 이 습관이 많이 남아 있다.
- 다만 최근 수정된 [docs/parts/part-05/chapter-05/section-02.md](/home/cbsim/ws/AiBook/docs/parts/part-05/chapter-05/section-02.md)는 이 목록을 제거했고, 이는 초심자용 책이라는 현재 원칙과 더 잘 맞는다.
- 이 리뉴얼 방향을 Part 5의 다른 절에도 확장할 수 있다.

### Part 6

- 발생 수가 가장 많다.
- LLM/생성형 AI 파트 특성상 빠르게 변하는 주제, 범위 밖 구현, 벤더 차이를 잘라내려는 의도가 강하게 보인다.
- 그렇더라도 `이 절에서는 다음 내용을 깊게 다루지 않습니다`가 거의 표준 도입문처럼 굳어질 위험이 있다.
- Part 6은 회수 위치를 남기되, 가능한 한 `현재 절의 중심 질문을 먼저 세운 뒤` 필요한 경우에만 짧게 붙이는 방식으로 줄이는 것이 좋다.

### Part 7

- 프로젝트 파트 특성상 범위 조정 문장이 많다.
- 오버뷰 성격이 강한 절에서는 어느 정도 허용되지만, 각 절이 모두 같은 형식으로 시작하면 프로젝트 장면보다 관리 문장이 먼저 보일 수 있다.

## 우선순위 제안

### 1순위: 회수 위치가 없는 `list_only`

위에 적은 9개 파일부터 우선 점검한다.

판단 기준:

- 정말 필요한 범위 조정인가
- 회수 위치를 붙일 수 있는가
- 붙여도 초심자에게 이득이 없는가

셋째에 가깝다면 삭제가 기본값이다.

### 2순위: 메타 두께가 큰 Part 6, 7

`회수 위치가 있다`는 이유만으로 유지된 범위 목록이 많다. 절 시작의 리듬이 과도하게 비슷해지는지 함께 점검할 필요가 있다.

### 3순위: Part 1 도입부

책의 첫인상에 해당하므로, 범위 안내보다 문제 장면과 핵심 개념이 먼저 나오도록 정리할 가치가 크다.

## 권장 편집 원칙

이 리포트 기준으로는 다음 순서를 책 전체 기본값으로 권한다.

1. 본문 Section에서는 `깊게 다루지 않습니다` 목록을 기본적으로 쓰지 않는다.
2. 정말 필요하면 인라인 한 문장형으로 줄인다.
3. 여러 항목을 남겨야 한다면 각 항목의 회수 위치를 바로 붙인다.
4. 회수 위치를 붙일 수 없고 초심자 이해에도 직접 도움이 없으면 삭제한다.
5. Part 시작 페이지나 오버뷰 문서에서만 상대적으로 넓은 범위 안내를 허용한다.

## 결론

이 책은 이미 초심자용 책으로 정리되어 있다. 따라서 `무엇을 안 하는가`를 반복해 경계 짓는 방식보다 `지금 무엇을 이해하면 되는가`를 먼저 세우는 편이 전체 원고 원칙과 더 잘 맞는다.

현재 본문의 `깊게 다루지 않습니다` 문구는 대부분 회수 위치를 동반하고 있어 전면적인 규칙 위반 상태는 아니다. 그러나 발생 수가 `192`건에 이르고, 일부는 회수 위치 없이 남아 있으며, 특히 Part 6과 7에서는 절 도입 습관으로 굳어질 위험이 보인다.

따라서 전체 책 차원의 권고는 단순하다.

- `회수 없는 목록형`은 우선 정리한다.
- `회수 있는 목록형`도 초심자 독해를 방해하면 인라인 문장형이나 삭제로 줄인다.
- 앞으로 새 원고에서는 이 문구를 기본 구조처럼 반복하지 않는다.
