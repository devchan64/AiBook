# 2026-07-10 작은 코드 예시 점검 리포트

## 점검 범위

- 대상: `docs/parts/part-03` 안에서 `python` 코드 블록을 포함한 Section 21개
- 기준 문서:
  - `AGENTS.md`
  - `management/guidelines/manuscript-writing-workflow.md`
  - `management/guidelines/rules-and-guidelines-summary.md`

이번 점검은 Part 3 원고의 작은 Python 예시가 레포의 작성 원칙에 맞는지 확인하는 데 집중했다. 특히 아래 항목을 기준으로 보았다.

- 코드 앞에 `문제 상황`, `입력(input)`, `기대 출력(output)`, `확인할 개념`이 있는가
- `print` 등으로 독자가 바로 출력값을 읽을 수 있는가
- 코드 아래에 예상 출력이 있는가
- 예제가 현재 Section의 중심 질문과 직접 연결되는가

## Findings

### [P1] Part 3의 작은 Python 예시 21개 중 15개가 필수 프리앰블 없이 바로 코드로 들어간다

`management/guidelines/manuscript-writing-workflow.md`와 `management/guidelines/rules-and-guidelines-summary.md`는 Python 예제 앞에 `문제 상황`, `입력(input)`, `기대 출력(output)`, `확인할 개념`을 짧게 둘 것을 공통으로 요구한다. 그런데 Part 3의 작은 Python 예시 다수는 `예상 출력`과 `print`는 갖추고 있지만, 정작 코드 바로 앞 프리앰블이 없다. 이 상태에서는 독자가 예제를 스캔할 때 `무엇을 확인해야 하는지`를 코드 밖에서 즉시 회수하기 어렵고, 같은 예제를 번역본이나 후속 개정에서 재사용할 때도 구조 기준이 흐려진다.

대표 근거:

- `P3-2.1` [docs/parts/part-03/chapter-02/section-01.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-02/section-01.md:51)
- `P3-4.1` [docs/parts/part-03/chapter-04/section-01.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-04/section-01.md:79)
- `P3-4.2` [docs/parts/part-03/chapter-04/section-02.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-04/section-02.md:53)
- `P3-4.3` [docs/parts/part-03/chapter-04/section-03.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-04/section-03.md:76)
- `P3-4.4` [docs/parts/part-03/chapter-04/section-04.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-04/section-04.md:60)
- `P3-4.5` [docs/parts/part-03/chapter-04/section-05.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-04/section-05.md:79)
- `P3-5.1` [docs/parts/part-03/chapter-05/section-01.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-05/section-01.md:62)
- `P3-5.2` [docs/parts/part-03/chapter-05/section-02.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-05/section-02.md:55)
- `P3-5.5` [docs/parts/part-03/chapter-05/section-05.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-05/section-05.md:89)
- `P3-5.6` [docs/parts/part-03/chapter-05/section-06.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-05/section-06.md:42)
- `P3-5.7` [docs/parts/part-03/chapter-05/section-07.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-05/section-07.md:47)
- `P3-6.2` [docs/parts/part-03/chapter-06/section-02.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-06/section-02.md:40)
- `P3-6.5` [docs/parts/part-03/chapter-06/section-05.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-06/section-05.md:86)
- `P3-6.6` [docs/parts/part-03/chapter-06/section-06.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-06/section-06.md:95)
- `P3-9.6` [docs/parts/part-03/chapter-09/section-06.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-09/section-06.md:90)

반대로 아래 Section들은 같은 기준을 충족한다.

- `P3-2.2` [docs/parts/part-03/chapter-02/section-02.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-02/section-02.md:47)
- `P3-2.3` [docs/parts/part-03/chapter-02/section-03.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-02/section-03.md:83)
- `P3-3.1` [docs/parts/part-03/chapter-03/section-01.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-03/section-01.md:46)
- `P3-6.1` [docs/parts/part-03/chapter-06/section-01.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-06/section-01.md:40)
- `P3-6.4` [docs/parts/part-03/chapter-06/section-04.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-06/section-04.md:72)
- `P3-8.1` [docs/parts/part-03/chapter-08/section-01.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-08/section-01.md:46)

### [P2] 프리앰블이 빠진 예시들은 `작은 코드 예시`라는 제목만 두거나 제목조차 없이 시작해, 예제 경계와 학습 포인트가 약해진다

레포 원칙은 메타 문장을 줄이되, 예제에서는 오히려 `지금 왜 이 코드를 보는가`를 짧게 명시하도록 요구한다. 그런데 프리앰블이 빠진 Section들은 대개 `## 작은 코드 예시`만 남기거나, [P3-2.1](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-02/section-01.md:44)처럼 코드 블록이 표 설명 바로 뒤에 이어진다. 이 구조는 설명 문단 안에서 읽을 때는 버틸 수 있지만, 예제만 빠르게 훑는 독자나 번역/개정 과정에서는 `현재 확인할 개념`을 다시 주변 문단에서 찾아야 한다.

대표 근거:

- `P3-2.1` [docs/parts/part-03/chapter-02/section-01.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-02/section-01.md:44)
- `P3-4.4` [docs/parts/part-03/chapter-04/section-04.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-04/section-04.md:58)
- `P3-6.5` [docs/parts/part-03/chapter-06/section-05.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-06/section-05.md:84)
- `P3-9.6` [docs/parts/part-03/chapter-09/section-06.md](/Users/simchangbo/ws/AiBook/docs/parts/part-03/chapter-09/section-06.md:88)

## Pass 관찰

- Part 3의 Python 예시 21개 모두 `print(...)`를 사용해 독자가 바로 결과를 읽을 수 있게 했다.
- Part 3의 Python 예시 21개 모두 코드 아래에 `예상 출력`을 두었다.
- 예제 대부분이 `pandas.DataFrame`과 표 형태 입력을 사용해, 현재 Part 3의 데이터 모델링 질문과 잘 맞는 실제 데이터 형식 연결을 유지한다.

## 결론

Part 3의 작은 Python 예시는 실행 가능성, 출력 가시성, 현재 질문과의 내용 정합성 측면에서는 대체로 양호하다. 다만 구조 기준에서는 `코드 앞 프리앰블` 누락이 반복되고 있어, 현재 상태를 그대로 두면 레포가 정한 Python 예제 형식이 Section마다 들쭉날쭉해진다. 다음 수정에서는 위 15개 Section부터 `문제 상황`, `입력(input)`, `기대 출력(output)`, `확인할 개념`을 코드 바로 앞에 지역화하는 것이 우선이다.
