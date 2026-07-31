# Section별 중심 학습 산출물 추적 가이드라인

이 문서는 Section별 중심 학습 산출물을 어디에서 어떤 기준으로 추적할지 정리한다. 실제 Section별 항목은 Part별 체크포인트 노트의 `목차 기준 체크포인트` 구간에서 관리한다.

## 목적

- 각 Section이 독자에게 남겨야 할 핵심 학습 산출물을 `Section ID` 기준으로 추적한다.
- 본문 수정, 번역 동기화, 개념사전 연결 작업에서 Section의 중심 질문과 학습 산출물이 흐트러졌는지 빠르게 확인한다.
- 작업 로그, 품질 상태표, 릴리즈노트, 본문 진행 메타와 중심 학습 산출물 추적을 섞지 않는다.

## 본문 소제목과의 경계

`중심 학습 산출물`은 관리 문서에서만 쓰는 점검 용어다. 본문 Section의 소제목으로 쓰지 않는다.

본문에서는 다음 제목을 진행 메타 소제목으로 보고, 정밀 수정 때 내용형 제목으로 바꾼다.

- `주요 학습내용`
- `세부 학습내용`
- `세부 학습내용 보충`
- `먼저 연결할 개념`
- `이 절의 목표`
- `이 절의 범위`
- `이 절을 읽는 순서`
- `사례 및 예시`
- `연습 및 예제`

반대로 `체크리스트`와 `출처와 참고 자료`는 유지 소제목 구조다. 두 제목은 각각 Section 말미의 자기 확인과 근거 표시를 맡으므로 내용형 제목으로 바꾸지 않는다.

대체 제목은 현재 문단이 실제로 설명하는 개념, 오해, 비교 대상, 판단 기준을 드러내야 한다. 예를 들어 `세부 학습내용` 대신 `평균이 가리는 차이`, `입력과 라벨이 만드는 학습 신호`, `MCP가 연결 형식을 분리하는 이유`처럼 독자가 지금 읽을 대상을 바로 볼 수 있게 쓴다.

## 기준 원천

Section별 중심 학습 산출물의 기준 원천은 다음 문서다.

| 범위 | 기준 문서 |
| --- | --- |
| Part 1 | `management/authoring/part-01-open-checklist.md` |
| Part 2 | `management/authoring/part-02-open-checklist.md` |
| Part 3 | `management/authoring/part-03-open-checklist.md` |
| Part 4 | `management/authoring/part-04-open-checklist.md` |
| Part 5 | `management/authoring/part-05-open-checklist.md` |
| Part 6 | `management/authoring/part-06-open-checklist.md` |
| Part 7 | `management/authoring/part-07-open-checklist.md` |

각 Part 체크포인트 노트에서는 `P6-15.1`처럼 Section ID를 기준으로 한 줄 설명을 유지한다. 이 한 줄은 해당 Section의 중심 학습 산출물로 본다.

## 항목 작성 기준

Part 체크포인트 노트의 Section별 항목은 다음 기준을 따른다.

- 파일 경로나 제목이 아니라 `Section ID`로 시작한다.
- `무엇을 설명한다`보다 `독자가 무엇을 구분하거나 판단할 수 있어야 하는가`를 우선한다.
- 한 Section에는 중심 학습 산출물을 하나만 둔다.
- 예제, 표, 도식, 참고 자료 목록을 항목 안에 길게 누적하지 않는다.
- 완료 여부, 작업 날짜, 품질 상태, 번역 상태는 이 항목에 적지 않는다.

권장 문장형:

```md
- `P6-15.1`: MCP를 도구와 자원을 공통 형식으로 연결하는 인터페이스 층으로 설명해야 합니다.
```

피해야 할 문장형:

```md
- `P6-15.1`: MCP 정의, 사례, 표, 참고문헌 추가 완료. 영어판 번역 필요.
```

## 갱신 시점

다음 작업을 하면 대응 Part 체크포인트 노트의 Section별 중심 학습 산출물도 함께 확인한다.

- Section의 중심 질문이나 결론이 바뀐 경우
- Chapter 또는 Section 순서를 바꾼 경우
- Section을 새로 만들거나 나눈 경우
- 기존 Section을 합친 경우
- 개념사전의 중심 Section을 옮긴 경우
- 번역본에서 원문과 다른 학습 초점이 생긴 경우
- 진행 메타 소제목을 내용형 소제목으로 바꾸면서 Section의 설명 순서나 강조점이 달라진 경우

본문 문장만 다듬고 Section의 중심 학습 산출물이 바뀌지 않았다면 체크포인트 항목을 억지로 갱신하지 않는다.

## 릴리즈노트와의 경계

- 중심 학습 산출물 추적은 `무엇을 배우게 할 것인가`를 관리한다.
- 릴리즈노트는 `언제 무엇을 왜 고쳤는가`를 관리한다.
- 본문 메타데이터는 `Section ID`와 `Version`만 관리한다.

따라서 중심 학습 산출물을 본문 메타데이터 줄에 추가하지 않는다. Section 본문을 수정했다면 릴리즈노트는 기존 규칙대로 갱신하고, 학습 초점이 바뀐 경우에만 Part 체크포인트 노트를 함께 고친다.

## 점검 절차

1. 수정 대상 Section의 `Section ID`를 확인한다.
2. 대응 Part 체크포인트 노트의 `목차 기준 체크포인트` 구간에서 같은 Section ID 항목을 찾는다.
3. 현재 본문이 그 항목의 중심 학습 산출물을 실제로 설명하는지 확인한다.
4. 진행 메타 소제목이 남아 있으면 내용형 소제목으로 바꿀 후보를 잡는다.
5. 본문 초점이 바뀌었다면 체크포인트 항목을 짧게 갱신한다.
6. Section 분리나 병합이 있었다면 새 Section ID와 사라진 Section ID를 목차, 본문, 릴리즈노트 기준으로 함께 맞춘다.

## 함께 볼 문서

- `../authoring/progress-meta-heading-audit.md`
- `../README.md`
- `README.md`
- `manuscript-writing-workflow.md`
- `section-metadata-guidelines.md`
- `../release-notes/sections/README.md`
