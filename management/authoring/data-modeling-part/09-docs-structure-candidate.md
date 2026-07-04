# 새 데이터 모델링 Part의 docs 구조와 더미 파일 목록

## 목적

이 문서는 현재 관리 설계안을 실제 `docs/parts/part-03/` 구조와 대조하기 위해 만든다.

현재는 Chapter와 Section의 더미 파일이 이미 생성되어 있으므로, 이 문서는 `후보 구조`만 적는 문서가 아니라 `현재 파일 목록 점검 기준`으로도 사용한다.

## 배치 원칙

- 새 Part는 실제로 `Part 3`에 들어간다.
- 이후 머신러닝, 딥러닝, LLM, 프로젝트는 각각 `Part 4`부터 `Part 7`로 한 칸씩 밀린다.
- 여기서는 더 이상 임시 이름이 아니라 실제 경로 `part-03`을 기준으로 적는다.

## 현재 더미 파일 목록 점검

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

현재 점검 결과, 위 파일들은 모두 실제로 존재한다. 즉 Part 3의 현재 더미 골격은 `index + summary + 6개 chapter + 12개 section`으로 내려가 있다.

다만 현재 설계 기준은 초심자용 전개를 위해 `9개 chapter + 18개 section`으로 확장하는 쪽으로 업데이트되었다. 따라서 이 문서는 `현재 존재하는 더미 파일`과 `권장 목표 구조`를 구분해서 봐야 한다.

## 권장 목표 구조

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
docs/parts/part-03/chapter-07/section-01.md
docs/parts/part-03/chapter-07/section-02.md
docs/parts/part-03/chapter-08/section-01.md
docs/parts/part-03/chapter-08/section-02.md
docs/parts/part-03/chapter-09/section-01.md
docs/parts/part-03/chapter-09/section-02.md
```

## 파일 역할 기준

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
- 저장 구조와 분석 구조의 차이
- 데이터 생애주기에서의 위치

### `chapter-02`

- 데이터셋 환상 깨기
- 원천데이터와 분석용 구조의 차이

### `chapter-03`

- 샘플 단위
- 측정값과 샘플의 차이

### `chapter-04`

- 원시 로그
- 요약 표와 집계 표

### `chapter-05`

- 특징과 중간 표현
- 세그먼트와 토큰화 표현

### `chapter-06`

- 기준선 비교
- 비교표 읽기

### `chapter-07`

- 표본 수와 반복성
- 변화 신호와 해석 경계

### `chapter-08`

- 경고 후보, 검토 큐, 라벨 예측 문제의 구분
- 비교 리포트로 남겨야 하는 운영 문제

### `chapter-09`

- 머신러닝 Part로 넘기는 handoff 정리
- feature, target, split, evaluation 전제

## Part 번호 검토 메모

현재 책 구조상 새 Part가 실제로 들어가면 이후 Part 번호를 다시 밀어야 할 수 있다.

선택지는 두 가지다.

1. 기존 Part 번호를 전부 한 칸씩 뒤로 민다.
2. 새 Part를 별도 보간 방식으로 넣는다.

현재 저장소 규칙과 독자 가독성을 생각하면, 결국은 `정식 번호 재배치`가 더 깔끔할 가능성이 크다. 다만 실제 반영 전에 `mkdocs.yml`, 내부 링크, Part별 인덱스 문서를 함께 점검해야 한다.

## 점검 메모

- 현재 파일 수는 과거 설계 문서의 `6개 Chapter, 12개 Section` 구조와 일치한다.
- 최신 설계 기준은 `9개 Chapter, 18개 Section`이다.
- 따라서 다음 단계의 중심 작업은 두 가지다.
  - 기존 더미 파일의 역할을 최신 구조에 맞게 다시 정렬한다.
  - `chapter-07`, `chapter-08`, `chapter-09` 더미 파일을 추가할지 결정한다.
- 최신 기준에서 `chapter-01`은 역할 지도, `chapter-02`는 데이터셋 환상 깨기, `chapter-03`은 샘플 정의, `chapter-04`는 표 구조 변환, `chapter-05`는 특징 설계, `chapter-06`은 비교 구조 읽기, `chapter-07`은 해석 경계, `chapter-08`은 문제 유형 구분, `chapter-09`는 handoff를 맡아야 한다.

## 현재 결론

새 데이터 모델링 Part는 이미 `docs/parts/part-03/` 수준으로 1차 더미 파일 골격이 준비된 상태다. 다음 단계는 `6개 Chapter 더미 구조`를 `9개 Chapter 목표 구조`로 확장할지 결정하고, 그 기준에 맞춰 더미 파일과 본문 초안을 차례대로 정렬하는 일이다.
