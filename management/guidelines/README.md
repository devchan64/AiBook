# 가이드라인 폴더 인덱스

이 디렉터리는 `AGENTS.md`의 전역 원칙을 실제 작업으로 옮길 때 다시 여는 세부 가이드라인을 모아 둔다.

이 폴더에는 저장소 전체 운영 규칙이 아니라, 책 원고 작성·수정·번역·도식화처럼 반복되는 작업의 실행 기준만 둔다. 전역 원칙은 `../../AGENTS.md`에 남기고, 이 폴더는 작업별 판단 절차와 예외 기준을 담당한다.

다음 성격의 문서는 여기로 모은다.

- 차트, 그래프, 도식 작성 기준
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
  - 세부 규칙 재서술 문서가 아니라, 어떤 원문을 먼저 열어야 하는지 빠르게 찾는 인덱스 문서로 유지한다.
- `section-metadata-guidelines.md`
  - Section ID, 제목 앞 인덱스, Version, 릴리즈노트 연결 같은 본문 메타데이터 관리 기준을 다룬다.
- `manuscript-writing-workflow.md`
- `python-example-guidelines.md`

함께 봐야 하지만 이 폴더 밖에서 관리하는 문서는 다음과 같다.

- `../release-notes/sections/README.md`
  - 릴리즈노트 파일 위치, 파일명, 항목 형식만 다룬다.
  - Section ID, Version, 본문 메타데이터 관리는 `section-metadata-guidelines.md`를 따른다.

문서 경계는 다음과 같이 잡는다.

- `../../AGENTS.md`는 저장소의 핵심 원칙, 문서 위치, 브랜치·배포 기준, 작업 전 확인할 가이드라인 인덱스를 맡는다.
- `management/README.md`는 `authoring/`, `guidelines/`, `release-notes/`의 역할 분담을 빠르게 찾는 인덱스를 맡는다.
- `management/guidelines/README.md`는 이 폴더에 둘 문서와 두지 않을 문서의 경계를 맡는다.
- `management/guidelines/rules-and-guidelines-summary.md`는 작업 유형별 참조 순서를 빠르게 찾는 문서이며, 원칙 원문이나 세부 규칙을 반복하지 않는다.
- 개별 가이드라인 문서는 특정 워크플로우를 실제로 수행할 때 필요한 세부 절차, 예외, 검증 기준을 맡는다.
- `management/glossary-indexes/`는 개념사전의 언어별 표제어 탐색과 용어 대응을 맡는 보조 관리 폴더이며, 최종 정의 원고는 `docs/reference/concept-glossary-terms/`의 단어별 파일에 둔다. 한국어 자음별, 영어 알파벳별, 중국어 병음별 페이지는 각 언어의 색인 구조를 유지하되 단어별 원고를 include해 공개 페이지를 조립한다.
- `management/release-notes/sections/`는 Section 단위 릴리즈노트 파일과 그 안의 변경 이력·다국어 동기화 메모를 맡는다.
- 원칙 문서와 가이드라인 문서는 별도 리비전노트를 두지 않고 문서 자체를 직접 갱신한다.
- 새 워크플로우 문서는 가능하면 `목적 -> 언제 보는가 -> 작업 전 확인 -> 작업 순서 -> 예외 -> 작업 후 검증 -> 함께 볼 문서` 순서를 따른다.
