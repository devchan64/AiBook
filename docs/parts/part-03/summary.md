# Part 3 마무리

> Section ID: `P3-summary`
> Version: `v2026.07.31`

이 Part에서는 [데이터 모델링(data modeling)](../../reference/concept-glossary-parts/03-digeut.md#data-modeling)을 저장 구조 설명이 아니라 문제 표현 구조 설계로 읽었습니다. 핵심은 [원천데이터(source data)](../../reference/concept-glossary-parts/08-ieung.md#glossary-source-data)가 곧바로 [데이터셋(dataset)](../../reference/concept-glossary-parts/03-digeut.md#glossary-dataset)이 아니라는 점입니다. Part 2와 Part 3은 함께 기본기 점검 구간을 이루며, Part 3은 그중 `데이터과학 문제 구조 복구`를 맡습니다. 먼저 데이터 모델링의 목표와 범위를 고정하고, 저장된 기록을 데이터셋 후보로 다시 읽고, 샘플과 표 구조를 정하고, [특징(feature)](../../reference/concept-glossary-parts/12-tieut.md#glossary-feature)과 [기준선(baseline)](../../reference/concept-glossary-parts/01-giyeok.md#glossary-baseline)을 설계하고, 해석 경계를 세운 뒤에야 뒤의 머신러닝 설명이 제대로 읽힙니다.

이 마무리 페이지의 재점검 계획은 `무엇을 한 샘플로 보았는가`, `어떤 특징과 기준선을 남겼는가`, `어디까지 비교 리포트로 두었는가`, `무엇을 학습 문제 후보로 올렸는가`를 다시 묶는 것입니다. 이 네 질문이 정리되어야 Part 4의 학습·평가 설명이 데이터 구조 위에 놓입니다.

대표 사례는 자동으로 실행되는 동작 1회가 있고, 그 안에 제어 파라미터 시계열과 센서 시계열이 남으며, 여러 동작을 최근 구간과 기준선으로 다시 비교하는 구조입니다. Part 3은 이 구조를 사람이 읽고 모델이 이어받을 수 있는 표 구조로 바꾸는 과정을 설명했습니다.

Part 3의 흐름은 Chapter 번호보다 다음 세 묶음으로 기억하는 편이 더 중요합니다.

| 흐름 묶음 | 이 Part에서 회수한 질문 | 남긴 결과 |
| --- | --- | --- |
| 역할과 순서 고정 | 데이터 모델링은 무엇을 맡고 어떤 순서로 판단하는가 | 문제 구조 설계의 위치, 작업 순서 지도 |
| 비교 구조 재구성 | 저장된 기록을 어떤 샘플, 표, 특징, 기준선 구조로 다시 읽을 것인가 | 데이터셋 후보, 요약 표, 특징(feature), 기준선 비교표 |
| 해석과 문제 마감 | 어디까지 말하고 무엇을 아직 [비교 리포트(comparison report)](../../reference/concept-glossary-parts/05-mieum.md#output-structure)로 둘 것인가 | 보수적 문장, 운영 산출물, 입력/결과 경계, 시간 경계 |

이 세 줄만 남겨도 Part 3을 `문제를 표현 가능한 구조로 바꾸는 판단의 연쇄`로 다시 읽을 수 있습니다.

## 이 Part의 핵심 흐름

- 저장 구조와 문제 표현 구조를 구분한다.
- 샘플, 특징, 기준선이 있는 비교 가능한 표를 다시 만든다.
- 해석 경계를 세운 뒤, 비교 리포트와 예측 문제를 구분한다.
- 입력/결과 경계와 시간 경계를 확인해 이후 학습 설명의 출발점을 만든다.

## 남겨야 할 핵심 개념

- 샘플 단위
- 저장 구조와 문제 표현 구조의 차이
- 요약 표와 특징(feature)
- 기준선과 비교 구조
- 비교 리포트와 예측 문제의 차이
- 목표 라벨 후보와 산출물 간 추적 기준
- 누수 방지와 운영 시점 재현성
- 표 벡터 입력과 시계열 입력 표현의 갈림길

Part 3이 끝나면 남는 것은 `아무 표나`가 아닙니다. 샘플 단위가 고정되어 있고, 입력으로 줄 특징과 나중에 맞히고 싶은 결과 후보가 구분되어 있으며, 아직 비교 리포트로 남겨 둘 범위도 함께 정리된 구조입니다. 한 줄로 줄이면 `원천데이터 -> 비교 가능한 표 -> 보수적 해석 -> 문제 구조 마감`의 연쇄가 남아 있어야 합니다. 따라서 Part 3의 마무리에서 확인할 최소 전제는 세 가지입니다.

- 특징(feature)과 결과 후보가 섞이지 않았는가
- 학습 때 만든 특징을 운영 시점에도 같은 규칙으로 다시 만들 수 있는가
- 어디까지의 정보를 보고 언제의 결과를 맞히는지 시간축이 분명한가

이 전제가 분명하면 이후의 학습 설명도 `정리된 문제 구조 위에서 무엇을 배우는가`라는 질문으로 자연스럽게 이어집니다. 즉 Part 3의 역할은 다음 Part를 미리 설명하는 것이 아니라, 현재 데이터와 문제를 흔들리지 않는 구조로 정리해 두는 데 있습니다.

## 출처와 참고 자료

- National Academies of Sciences, Engineering, and Medicine, *Data Science for Undergraduates: Opportunities and Options*, 2018. 데이터 수집, 정리, 표현, 모델링, 해석을 한 흐름으로 제시하므로, Part 3 마무리를 `데이터과학 문제 구조 복구`의 요약으로 묶는 이 페이지의 관점을 뒷받침합니다. [https://nap.nationalacademies.org/catalog/25104/data-science-for-undergraduates-opportunities-and-options](https://nap.nationalacademies.org/catalog/25104/data-science-for-undergraduates-opportunities-and-options){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
- Google for Developers, `Machine Learning Glossary`. feature, label, label leakage, example 같은 용어 구분을 제공하므로, 특징과 결과 후보를 섞지 않고 입력/결과 경계를 분명히 해야 한다는 Part 3의 최소 전제를 보강합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
- W3C, `PROV-Overview`. derivation과 reproducibility를 함께 다루므로, Part 3 끝에서 남기는 비교 구조와 특징 정의가 나중에도 같은 규칙으로 재현 가능해야 한다는 요약 판단을 뒷받침합니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
