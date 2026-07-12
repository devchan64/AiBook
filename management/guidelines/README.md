# 가이드라인 폴더 메모

이 디렉터리는 `management` 아래에 흩어져 있는 책 원고 세부 작성 규칙과 작업 가이드를 정리해 모으기 위한 준비 공간이다.

이 폴더에는 저장소 전체 운영 규칙이 아니라, 책 원고 세부 작성 전에 반복해서 확인하는 가이드라인만 둔다.

다음 성격의 문서는 여기로 모은다.

- 차트와 도식 작성 기준
- 집필 규칙 요약과 작업형 가이드
- 특정 작업 흐름별 세부 워크플로우 규칙

반대로 다음은 이 폴더의 대상이 아니다.

- 저장소 전체 운영 규칙
- Part별 작업 큐 문서
- 커리큘럼 조사 문서
- 개별 챕터 분석 메모
- 근거 검토 메모
- 일회성 감사 기록

현재 이관된 문서는 다음과 같다.

- `chart-guidelines.md`
- `chinese-translation-guidelines.md`
- `concept-glossary-guidelines.md`
- `english-translation-guidelines.md`
- `rules-and-guidelines-summary.md`
- `manuscript-writing-workflow.md`
- `python-example-guidelines.md`

함께 봐야 하지만 이 폴더 밖에서 관리하는 문서는 다음과 같다.

- `../release-notes/sections/README.md`
  - Section 버전 코드, 수정일 기준 버전 관리, 제목 앞 인덱스와 `Section ID` 일치 규칙, 번역본 동기화 메모, Section별 릴리즈노트 형식을 다룬다.
  - Section 본문을 실제로 수정했다면 이 문서를 따라 메타데이터와 릴리즈노트를 함께 갱신한다.

운영 원칙은 다음과 같다.

- `AGENTS.md`는 저장소 전체 규칙과 주요 업무 흐름의 인덱스를 맡는다.
- `management/README.md`는 `authoring/`, `guidelines/`, `release-notes/`의 역할 분담을 빠르게 찾는 인덱스를 맡는다.
- `management/guidelines/`는 특정 워크플로우를 실제로 수행할 때 다시 여는 세부 규칙 문서를 맡는다.
- `management/release-notes/sections/`는 Section 단위 변경 이력과 다국어 동기화 기준점을 맡는다.
- 원칙 문서와 가이드라인 문서는 별도 리비전노트를 두지 않고 문서 자체를 직접 갱신한다.
- 새 워크플로우 문서는 가능하면 `목적 -> 언제 보는가 -> 작업 전 확인 -> 작업 순서 -> 예외 -> 작업 후 검증 -> 함께 볼 문서` 순서를 따른다.
