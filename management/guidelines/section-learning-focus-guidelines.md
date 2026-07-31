# Section별 중심 학습 산출물 추적 가이드라인

이 문서는 각 Section이 독자에게 남겨야 할 중심 학습 산출물을 어디에, 어떤 형식으로 관리할지 다룬다. `Section ID`와 `Version` 형식은 `section-metadata-guidelines.md`, 본문 구성과 소제목 규칙은 `manuscript-writing-workflow.md`를 따른다.

## 목적

- 각 Section의 중심 질문과 중심 학습 산출물을 `Section ID` 기준으로 추적한다.
- 본문 수정, 번역 동기화, 개념사전 연결 작업에서 학습 초점이 흔들렸는지 확인한다.
- 학습 산출물 추적을 작업 로그, 품질 상태표, 릴리즈노트, 본문 진행 메타와 섞지 않는다.

## 관리 위치

실제 항목은 Part별 체크포인트 노트의 `목차 기준 체크포인트` 구간에서 관리한다.

| 범위 | 기준 문서 |
| --- | --- |
| Part 1 | `management/authoring/part-01-open-checklist.md` |
| Part 2 | `management/authoring/part-02-open-checklist.md` |
| Part 3 | `management/authoring/part-03-open-checklist.md` |
| Part 4 | `management/authoring/part-04-open-checklist.md` |
| Part 5 | `management/authoring/part-05-open-checklist.md` |
| Part 6 | `management/authoring/part-06-open-checklist.md` |
| Part 7 | `management/authoring/part-07-open-checklist.md` |

이 문서는 항목 작성 기준만 관리한다. Section별 실제 목록은 이 파일에 누적하지 않는다.

## 중심 학습 산출물의 의미

- 중심 학습 산출물은 해당 Section을 읽은 독자가 무엇을 구분하거나 판단할 수 있어야 하는지를 한 줄로 적은 관리 기준이다.
- 한 Section에는 중심 학습 산출물을 하나만 둔다.
- 중심 학습 산출물은 본문 소제목이 아니며, 본문에 `중심 학습 산출물`이라는 제목으로 노출하지 않는다.
- 중심 질문은 본문 작성 방향을 잡고, 중심 학습 산출물은 작업 후 본문이 남긴 결과를 점검한다.

## 항목 작성 기준

Part 체크포인트 노트의 Section별 항목은 다음 기준을 따른다.

- 파일 경로나 제목이 아니라 `Section ID`로 시작한다.
- `무엇을 설명한다`보다 `독자가 무엇을 구분하거나 판단할 수 있어야 하는가`를 우선한다.
- 예제, 표, 도식, 참고 자료 목록을 항목 안에 길게 누적하지 않는다.
- 완료 여부, 작업 날짜, 품질 상태, 번역 상태는 적지 않는다.

권장 문장형:

```md
- `P6-15.1`: MCP를 도구와 자원을 공통 형식으로 연결하는 인터페이스 층으로 설명해야 합니다.
```

피해야 할 문장형:

```md
- `P6-15.1`: MCP 정의, 사례, 표, 참고문헌 추가 완료. 영어판 번역 필요.
```

## 갱신 시점

다음 작업을 하면 대응 Part 체크포인트 노트의 Section별 중심 학습 산출물을 확인한다.

- Section의 중심 질문이나 결론이 바뀐 경우
- Chapter 또는 Section 순서를 바꾼 경우
- Section을 새로 만들거나 나눈 경우
- 기존 Section을 합친 경우
- 개념사전의 중심 Section을 옮긴 경우
- 번역본에서 원문과 다른 학습 초점이 생긴 경우
- 진행 메타 소제목을 내용형 소제목으로 바꾸면서 Section의 설명 순서나 강조점이 달라진 경우

본문 문장만 다듬고 Section의 중심 학습 산출물이 바뀌지 않았다면 체크포인트 항목을 억지로 갱신하지 않는다.

## 다른 문서와의 경계

- 본문 메타데이터는 `Section ID`와 `Version`만 관리한다. 중심 학습 산출물을 본문 메타데이터 줄에 추가하지 않는다.
- 릴리즈노트는 `언제 무엇을 왜 고쳤는가`를 관리한다. 중심 학습 산출물을 릴리즈노트 항목으로 대체하지 않는다.
- 본문 소제목, Section 경계, 진행 메타 소제목 정리는 `manuscript-writing-workflow.md`를 따른다.
- 진행 메타 소제목의 현재 잔여 위치와 변경 제안은 `../authoring/progress-meta-heading-audit.md`와 `../authoring/progress-meta-heading-proposal.md`에서 확인한다.

## 점검 절차

1. 수정 대상 Section의 `Section ID`를 확인한다.
2. 대응 Part 체크포인트 노트의 `목차 기준 체크포인트` 구간에서 같은 Section ID 항목을 찾는다.
3. 현재 본문이 그 항목의 중심 학습 산출물을 실제로 설명하는지 확인한다.
4. 본문 초점이 바뀌었다면 체크포인트 항목을 짧게 갱신한다.
5. Section 분리나 병합이 있었다면 새 Section ID와 사라진 Section ID를 목차, 본문, 릴리즈노트 기준으로 함께 맞춘다.

## 함께 볼 문서

- `section-metadata-guidelines.md`
- `manuscript-writing-workflow.md`
- `../release-notes/sections/README.md`
- `../authoring/progress-meta-heading-audit.md`
- `../authoring/progress-meta-heading-proposal.md`
