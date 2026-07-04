# 데이터 모델링을 AI 활용 관점으로 가르치기 위한 모듈 설계

## 이 디렉터리의 목적

이 디렉터리는 `데이터 모델링`을 데이터베이스 저장 구조 설명에만 묶지 않고, AI가 활용할 수 있는 샘플, 특징, 기준선, 비교 구조를 설계하는 관점으로 책에 반영하기 위한 관리 문서 묶음이다.

이 디렉터리는 공개용 책 본문이 아니라 집필과 구조 설계를 위한 관리 자료다.

## 왜 별도 디렉터리가 필요한가

기존 `brewing-shot-ai-notes`는 특정 사례를 일반화해 책에 흡수하는 데 집중한다.

반면 여기서는 그 사례를 넘어, 책 전체에서 재사용 가능한 `데이터 모델링 교육 모듈` 자체를 정리한다.

즉 중심 질문이 다르다.

- 사례 노트: 이 사례를 어디에 어떻게 흡수할 것인가
- 현재 디렉터리: 데이터 모델링을 AI 활용 관점으로 어떤 모듈로 가르칠 것인가

## 이 디렉터리에서 다루는 범위

- 샘플 단위 정의
- 원시 로그와 요약 표의 차이
- 특징과 중간 표현 설계
- 기준선과 최근 구간 비교
- 표본 수, 반복성, 경고 해석
- 규칙 기반에서 학습 기반으로 올라가는 모델링 사다리
- 책 Part별 배치 원칙

## 이 디렉터리에서 다루지 않는 범위

- 실제 기업 로그 구조
- 내부 구현 전용 명칭
- 실제 운영 임계값
- 특정 장비나 특정 제품에 종속된 세부 진단 규칙

## 문서 목록

- `01-why-data-modeling-needs-an-ai-curriculum.md`
- `02-module-map-for-ai-data-modeling.md`
- `03-module-details-sample-feature-baseline.md`
- `04-book-placement-and-editing-principles.md`
- `05-additional-knowledge-required.md`
- `06-curriculum-sources-and-learning-path.md`
- `07-module-writing-template.md`
- `08-example-topics-expansion-map.md`
- `09-part-and-section-insertion-map.md`
- `10-next-writing-actions.md`
- `11-common-example-table-set.md`
- `12-part-draft-paragraphs.md`
- `13-common-python-example-plan.md`
- `14-python-example-draft-snippets.md`
- `15-note-integration-priority-map.md`
- `16-next-source-editing-queue.md`

## 현재 결론

이 주제는 새 Part를 만드는 것보다 `여러 Part에서 반복 호출하는 모듈`로 관리하는 편이 더 적절하다.

이 디렉터리는 그 모듈 체계를 고정하는 시작점이다.
