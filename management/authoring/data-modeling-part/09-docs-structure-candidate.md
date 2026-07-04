# 새 데이터 모델링 Part의 docs 구조 후보

## 목적

이 문서는 현재 관리 설계안을 실제 `docs/parts/` 구조로 옮길 때 어떤 디렉터리와 파일 배치를 쓰면 좋을지 미리 정리하기 위해 만든다.

아직 실제 `docs/` 편집은 시작하지 않는다. 여기서는 후보 구조만 고정한다.

## 배치 원칙

- 새 Part는 실제로 `Part 3`에 들어간다.
- 이후 머신러닝, 딥러닝, LLM, 프로젝트는 각각 `Part 4`부터 `Part 7`로 한 칸씩 밀린다.
- 여기서는 더 이상 임시 이름이 아니라 실제 경로 `part-03`을 기준으로 적는다.

## 디렉터리 구조 후보

```text
docs/parts/part-03/
docs/parts/part-03/index.md
docs/parts/part-03/summary.md
docs/parts/part-03/chapter-01/section-01.md
docs/parts/part-03/chapter-01/section-02.md
docs/parts/part-03/chapter-02/section-01.md
docs/parts/part-03/chapter-02/section-02.md
docs/parts/part-03/chapter-03/section-01.md
docs/parts/part-03/chapter-03/section-02.md
docs/parts/part-03/chapter-04/section-01.md
docs/parts/part-03/chapter-04/section-02.md
docs/parts/part-03/chapter-05/section-01.md
docs/parts/part-03/chapter-05/section-02.md
docs/parts/part-03/chapter-06/section-01.md
docs/parts/part-03/chapter-06/section-02.md
```

## 파일 역할 후보

### `index.md`

- 이 Part의 목적
- 왜 이 Part가 필요한가
- 주요 질문
- 범위와 비범위
- Part 2와의 연결
- Part 4와의 연결

### `summary.md`

- 이 Part의 핵심 흐름 요약
- 반드시 기억할 개념
- 오해하기 쉬운 지점
- Part 4로 넘어가기 전 확인 질문

### `chapter-01`

- 데이터 모델링의 정의
- 저장 구조와 문제 표현 구조의 차이

### `chapter-02`

- 샘플 단위
- 측정값과 샘플의 차이

### `chapter-03`

- 원시 로그
- 요약 표와 집계 표

### `chapter-04`

- 특징과 중간 표현
- 세그먼트와 토큰화 표현

### `chapter-05`

- 기준선 비교
- 변화 신호와 원인 확정의 분리

### `chapter-06`

- 표본 수와 반복성
- 경고 후보, 검토 큐, 라벨 예측 문제의 구분

## Part 번호 검토 메모

현재 책 구조상 새 Part가 실제로 들어가면 이후 Part 번호를 다시 밀어야 할 수 있다.

선택지는 두 가지다.

1. 기존 Part 번호를 전부 한 칸씩 뒤로 민다.
2. 새 Part를 별도 보간 방식으로 넣는다.

현재 저장소 규칙과 독자 가독성을 생각하면, 결국은 `정식 번호 재배치`가 더 깔끔할 가능성이 크다. 다만 실제 반영 전에 `mkdocs.yml`, 내부 링크, Part별 인덱스 문서를 함께 점검해야 한다.

## 현재 결론

새 데이터 모델링 Part는 이미 `docs/parts/part-03/` 수준으로 실제 경로에 내려간 상태다. 다음 단계는 더미 파일을 본문 초안으로 바꾸고, 밀린 Part들의 숫자 연결을 더 정교하게 다듬는 일이다.
