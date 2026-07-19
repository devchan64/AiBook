# Part 3. 데이터 모델링

> Section ID: `P3-index`
> Version: `v2026.07.20`

Part 2에서 우리는 수학, Python, 배열, 표, 그래프를 다시 읽는 기초를 복구했습니다. 그러나 계산 도구를 다시 읽을 수 있게 되었다고 해서 곧바로 AI 문제를 제대로 만들 수 있는 것은 아닙니다. 실제 원천데이터를 만나면 먼저 부딪히는 질문은 `어떤 모델을 쓸까`보다 `무엇을 한 건의 데이터로 볼까`에 가깝습니다. 이 책의 전체 구조에서는 Part 2와 Part 3이 함께 기본기 점검 구간을 이루며, Part 3은 그중 `데이터과학 문제 구조 복구`를 맡습니다.

Part 3의 대표 사례는 특정 장비 이름보다 더 일반적인 구조로 설명합니다. 자동으로 실행되는 동작 1회가 있고, 그 동작에서 사용한 제어 파라미터 시계열과 동작 중 관측된 센서 데이터 시계열이 함께 남고, 여러 동작을 다시 묶어 최근 구간과 기준선으로 비교하는 구조입니다. 이때 한 시점의 측정값 하나를 샘플로 볼 수도 있고, 동작 1회를 샘플로 볼 수도 있고, 여러 동작을 묶은 최근 구간을 샘플로 볼 수도 있습니다. 어떤 선택을 하느냐에 따라 만들어지는 데이터셋, 비교 방식, 해석 가능한 질문, 그리고 실제 행동이 몇 갈래로 나뉘는지에 대한 운영 흐름 구조가 모두 달라집니다. 같은 원천데이터라도 어떻게 묶고, 무엇을 남기고, 무엇과 비교하고, 어떤 행동 흐름 구조로 넘길지에 따라 전혀 다른 AI 문제가 됩니다.

대표 사례가 Part 안에서 어떻게 진화하는지는 아래 기준표로 먼저 붙잡아 둘 수 있습니다.

| 단계 | 한 행이 뜻하는 것 | 이 단계에서 주로 남기는 것 |
| --- | --- | --- |
| 원천 로그 | 동작 중 한 시점의 기록 | 센서값, 제어값, 시간 순서 |
| 동작 요약 표 | 동작 1회 | 평균, 기울기, 변동성, 구간 차이 |
| 최근/기준선 비교표 | 여러 동작을 묶은 상태 비교 | 최근 평균, 기준선 평균, 차이값 |
| 운영 산출물 | 사람이 읽거나 다음 단계가 이어받는 결과 | 경고, 검토 후보, 목표 라벨 후보 |

여기서 데이터 모델링은 저장 구조를 정리하는 일만을 뜻하지 않습니다. 데이터 모델링은 현실에서 발생한 원천데이터를 사람이 비교하고 AI가 활용할 수 있는 샘플, 특징, 기준선, 출력 구조로 다시 표현하는 일입니다. 더 정확히 말하면 `주어진 표를 읽는 일`이 아니라 `어떤 사건을 한 샘플로 볼지`, `원시 로그를 어떤 요약 표로 다시 묶을지`, `어떤 특징과 비교 구조를 남길지`, `어디까지 보수적으로 말할지`, `무엇을 아직 비교 리포트로 남기고 무엇을 예측 문제로 올릴지`를 설계하는 일에 가깝습니다.

Part 3은 데이터과학 커리큘럼에서 따로따로 보이는 데이터 정리(data wrangling), 특징 설계(feature engineering), 샘플 설계(sample design), 추론(inference), 문제 구조화(problem framing)를 재학습 흐름으로 다시 묶어 설명합니다. 여기서는 이 항목들을 이름별 절차로 나열하지 않고, 하나의 사례를 따라 `무엇을 샘플로 만들고`, `어떤 표로 다시 묶고`, `무엇과 비교하고`, `어디까지 말할 수 있는가`를 차례로 확인합니다. 따라서 Part 3의 초점은 알고리즘보다 먼저 `문제 표현 구조`를 세우는 데 있습니다.

아래 기준표를 보면 Part 3의 spine이 임의로 붙인 순서가 아니라, 데이터과학과 머신러닝에서 따로 설명되는 표준 개념 묶음을 `문제 구조 복구` 관점으로 다시 배열한 것임을 더 짧게 확인할 수 있습니다.

| 이 Part의 묶음 | 대응 표준 개념 | 대표 근거 축 |
| --- | --- | --- |
| 원천데이터를 다시 묶는 구간 | data wrangling, sample design | W3C PROV, Fayyad/KDD |
| 특징과 기준선을 세우는 구간 | feature engineering, labeled example, base period | Google ML Glossary, BLS |
| 해석 강도와 산출물 경계를 닫는 구간 | problem framing, conservative interpretation, output structure | Google ML Glossary, NASEM |

Part 3 안에서는 `데이터 모델링` 자체의 큰 정의를 3.1에서 먼저 잡고, 3.2에서 진행 순서를 고정합니다. 이후 Section에서는 같은 용어의 상세 정의를 반복하기보다 현재 질문에 필요한 최소 연결만 남깁니다. [샘플(sample)](../../reference/concept-glossary.md#glossary-sample), [특징(feature)](../../reference/concept-glossary.md#glossary-feature), [기준선(baseline)](../../reference/concept-glossary.md#glossary-baseline), [비교 리포트(comparison report)](../../reference/concept-glossary.md#glossary-comparison-report), [타깃(target)](../../reference/concept-glossary.md#glossary-target)은 필요할 때 개념사전에서 다시 확인할 수 있습니다.

Part 3에서는 먼저 데이터 모델링이 무엇을 달성하려는지와 어떤 순서로 진행되는지부터 고정합니다. 그 다음 저장된 기록을 왜 곧바로 데이터셋처럼 읽으면 안 되는지 확인하고, 한 행과 한 샘플의 뜻을 정한 뒤, 원시 로그를 비교 가능한 표로 다시 묶습니다. 이어서 특징과 중간 표현을 설계하고, 어떤 열이 식별용인지, 비교용인지, 목표 후보용인지 역할을 나눕니다. 그 다음 최근 구간과 기준선을 비교하는 구조를 세우고, 적은 표본과 흔들리는 반복성 앞에서 어디까지 해석할 수 있는지 경계를 둡니다. 마지막에는 비교 리포트로 남길 문제와 예측 문제로 올릴 문제를 구분하고, 입력/결과 경계와 시간 경계를 닫습니다.

## Part 3의 목적

- 데이터 모델링을 DB 설계로만 오해하지 않게 한다.
- 원천데이터를 샘플, 요약 표, 특징, 기준선으로 다시 표현하는 흐름을 익히게 한다.
- 데이터 정리, 특징 공학, 보수적 해석, 문제 설정이 하나의 흐름임을 이해하게 한다.
- 비교 리포트와 예측 문제를 섞지 않고, 어떤 문제 구조를 먼저 닫아야 하는지 익히게 한다.

## 왜 필요한가

- 원시 로그가 곧바로 데이터셋이 아니라는 점을 먼저 배워야 하기 때문이다.
- 샘플 단위와 비교 기준이 정해지지 않으면 feature와 label 설명이 흔들리기 때문이다.
- 경고 후보와 진단 확정, 기준선 비교와 절대값 판단을 자주 혼동하기 때문이다.
- 같은 평균이라도 구간 패턴과 변동성은 다를 수 있는데, 대표값 하나로 너무 빨리 단정하기 쉽기 때문이다.
- 샘플 구조와 입력 경계가 흐리면 이후의 학습 설명도 문제 구조 없이 이름만 남기기 쉽기 때문이다.

## 주요 질문

- 데이터 모델링은 데이터과학 전체 흐름에서 어떤 역할을 맡는가
- 저장된 기록은 왜 곧바로 데이터셋이 아닌가
- 한 행과 한 샘플은 어떻게 다르며, 어떤 표 구조가 필요한가
- 특징과 중간 표현은 무엇을 남기기 위해 설계하는가
- 기준선과 비교 구조는 왜 모델보다 먼저 정해져야 하는가
- 표본 수와 반복성 앞에서 어디까지 해석할 수 있는가
- 무엇을 비교 리포트로 두고 무엇을 학습 문제로 넘겨야 하는가

## 읽는 순서

Part 3은 9개 Chapter를 따라 진행되지만, 그 흐름은 세 묶음으로 요약할 수 있습니다.

1. 데이터 모델링의 역할과 진행 순서를 고정한다.
2. 저장 구조를 샘플, 표 구조, 특징, 기준선이 있는 비교 구조로 다시 만든다.
3. 해석 경계를 세운 뒤, 비교 리포트와 예측 문제를 구분하고 입력/결과 경계를 닫는다.

이 순서를 지키는 이유는 저장 구조를 문제 구조로 바꾸기 전에 feature와 label을 말하면 용어가 공중에 뜨고, 해석 경계가 세워지기 전에 예측 문제부터 꺼내면 데이터 구조보다 모델 이름이 먼저 보이기 쉽기 때문입니다. 아래 표는 이 세 묶음이 각각 무엇을 정리하는지 짧게 다시 보여 줍니다.

| 흐름 묶음 | 여기서 붙잡는 질문 | 남기는 구조 |
| --- | --- | --- |
| 역할과 순서 고정 | 데이터 모델링은 무엇을 맡고 어떤 순서로 판단하는가 | 문제 구조 설계의 위치, 작업 순서 지도 |
| 비교 구조 재구성 | 저장된 기록을 어떤 샘플, 표, 특징, 기준선 구조로 다시 읽을 것인가 | 데이터셋 후보, 요약 표, 특징 열, 기준선 비교표 |
| 해석과 문제 마감 | 어디까지 말할 수 있고 무엇을 아직 리포트로 둘 것인가 | 보수적 문장, 운영 산출물, 입력/결과 경계, 시간 경계 |

Part 3에서 반복해서 다루는 질문은 몇 갈래로 묶입니다. 무엇을 한 샘플로 볼지, 원시 로그를 어떤 표로 다시 묶을지, 어떤 특징과 기준선을 남길지, 어디까지를 비교 리포트로 두고 어디부터를 목표 후보로 올릴지, 입력 구조와 관측 경계가 닫혔는지입니다. 각 Chapter는 이 질문 묶음 가운데 하나를 더 분명하게 만드는 역할을 맡습니다.

## 범위와 비범위

Part 3에서는 샘플 단위, 원시 로그와 요약 표, 특징과 중간 표현, 기준선 비교, 표본 수와 반복성, 경고 후보와 라벨 예측의 경계를 다룹니다.

반면 특정 머신러닝 알고리즘의 학습 방식, train/validation/test 분리의 세부 절차, 복잡한 시계열 딥러닝 구조 자체는 여기서 중심으로 다루지 않습니다.

이 범위 제한의 이유는 단순합니다. Part 3의 책임은 `어떤 데이터를 어떤 구조로 만들어야 하는가`를 먼저 분명히 하는 데 있기 때문입니다.

## Part 3을 읽고 나면 생겨야 할 이해

데이터셋은 주어진 표가 아니라 설계된 비교 구조이며, 머신러닝은 그 구조 위에서만 제대로 읽힌다는 감각이 남아야 합니다. 샘플 구조, 특징, 목표 후보, 시간 경계가 먼저 정리되어야 이후 학습 설명도 `무엇을 예측하는가`와 `어떤 입력을 쓰는가`가 분명한 상태에서 읽힙니다.

## 출처와 참고 자료

- National Academies of Sciences, Engineering, and Medicine, *Data Science for Undergraduates: Opportunities and Options*, 2018. 데이터 수집, 정리, 표현, 모델링, 해석을 하나의 데이터과학 흐름으로 묶어 설명하므로, Part 3을 `문제 구조 복구` 구간으로 두는 이 페이지의 커리큘럼 관점을 뒷받침합니다. [https://nap.nationalacademies.org/catalog/25104/data-science-for-undergraduates-opportunities-and-options](https://nap.nationalacademies.org/catalog/25104/data-science-for-undergraduates-opportunities-and-options){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Google for Developers, `Machine Learning Glossary`. sample, feature, label, label leakage 같은 핵심 용어의 역할 구분을 제공하므로, Part 3이 모델 이름보다 먼저 샘플 구조와 입력/결과 경계를 고정해야 한다는 설명을 보강합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- W3C, `PROV-Overview`. provenance와 derivation을 함께 다루므로, 원천데이터를 문제 표현 구조로 다시 만들 때 어떤 규칙으로 파생 표가 생겼는지 추적 가능해야 한다는 Part 3의 공통 전제를 뒷받침합니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Usama Fayyad, Gregory Piatetsky-Shapiro, Padhraic Smyth, `Knowledge Discovery and Data Mining: Towards a Unifying Framework`, Microsoft Research publication page, 1996. KDD 과정을 데이터 준비와 발견 흐름으로 설명하는 고전적 근거이므로, 원천데이터를 다시 묶는 구간을 별도 축으로 둔 근거입니다. [https://www.microsoft.com/en-us/research/publication/knowledge-discovery-and-data-mining-towards-a-unifying-framework/](https://www.microsoft.com/en-us/research/publication/knowledge-discovery-and-data-mining-towards-a-unifying-framework/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- U.S. Bureau of Labor Statistics, `Consumer Price Index: Concepts`, Handbook of Methods. CPI index values and base periods 설명을 통해 기준 기간을 정해 현재 값을 비교하는 관점을 확인하는 참고 자료입니다. [https://www.bls.gov/opub/hom/cpi/concepts.htm](https://www.bls.gov/opub/hom/cpi/concepts.htm){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
