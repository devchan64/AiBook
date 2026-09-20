# Part 3. 데이터 모델링

> Section ID: `P3-index`
> Version: `v2026.09.20`

Part 2에서 우리는 수학, Python, 배열, 표, 그래프를 다시 읽는 기초를 복구했습니다. Part 3에서는 그 도구로 **모델에 앞서 데이터를 이해하고 다루는 방법**을 배웁니다. `AI에 데이터를 넣는다`고 할 때, 무엇을 기록했고 무엇을 한 사례로 묶었으며 어떤 정보를 남겼는지부터 살펴봅니다. 이런 선택을 알아야 모델이 어떤 정보를 보고 무엇을 맞히려는지 설명할 수 있습니다.

이 책에서 `데이터 모델링`은 질문에 맞게 기록을 샘플·표·특징·목표로 구성하는 일을 가리킵니다. 여기서 샘플은 분석이나 학습에서 한 사례로 다룰 단위이고, 특징은 그 사례를 나타내는 입력 정보입니다. 데이터베이스의 저장 구조 설계보다 넓게 쓰는 이 책의 설명 범위이며, 데이터과학 전체를 대신하는 정의는 아닙니다. Part 3은 이러한 구성 과정과 함께 데이터의 의미, 품질, 표현 방식, 비교 결과의 해석을 다룹니다.

## 같은 센서 기록에서 무엇을 알아낼 수 있을까

장비가 물을 흘려보내는 동작을 여러 번 수행한다고 가정해 봅시다. 매번 동작 중 센서가 측정한 유량과 측정 시각, 장비에 지정한 설정값이 남습니다. 최근 기록의 끝부분에서 유량이 낮아지는 모습이 보인다면, 곧바로 고장이라고 부르기 전에 다음을 확인해야 합니다.

| 확인할 질문 | 이 사례에서 살펴볼 것 |
| --- | --- |
| 무엇을 기록했나 | 물의 양 자체인지, 일정 시간에 흐르는 양인지, 언제 어떤 설정에서 측정했는지 확인한다. |
| 어떻게 묶나 | 동작 한 번의 변화를 보려면 시작부터 끝까지의 기록을 한 사례로 묶는다. |
| 무엇을 남기나 | 끝부분의 하강을 살피려면 시간 순서와 그 구간의 변화를 남긴다. 동작 전체를 숫자 하나로 줄일 때 무엇이 사라지는지도 본다. |
| 무엇을 알 수 있나 | 설정과 측정 방식이 같은 과거 동작과 비교해 차이를 살핀다. 차이가 있다는 관찰과 고장 원인에 대한 설명은 구분한다. |

센서 기록의 마지막 부분이 빠져 있다면 하강 여부를 판단하기 어렵습니다. 과거와 최근의 장비 설정이 달랐다면 그 차이도 함께 살펴야 합니다. 이것이 데이터의 품질과 관측 조건을 배우는 이유입니다. 관찰한 차이를 일정한 기준으로 비교하려면 수치가 필요하므로, 뒤에서는 질문에 맞는 **지표**를 고르고 계산하는 방법을 배웁니다. 지표는 현상의 특정 면을 수치로 살피는 기준이며, 이름을 아는 것에 더해 무엇을 어떻게 셌는지 설명할 수 있어야 합니다.

이 기록으로 향후 고장을 예측하려면 학습에 사용할 결과도 필요합니다. 예를 들어 `동작 뒤 7일 안에 고장이 발생했고 이후 확인되었는가`를 결과로 정할 수 있습니다. 학습에서 맞힐 결과로 제공하는 값을 **라벨**이라고 합니다. 사람이 검토한 적이 있다는 기록과 실제 고장이 확인됐다는 기록은 다르므로, 어느 쪽을 라벨로 삼는지에 따라 학습 목표도 달라집니다.

위 장면은 이 책의 설명을 위한 가상 사례입니다. 실제 고장의 원인이나 판단 기준을 정한 것은 아닙니다. 구체적인 지표의 뜻과 계산은 [P3-1.1](chapter-01/section-01.md)에서 기록과 함께 살펴봅니다.

## 데이터를 다룰 때 이어지는 여섯 가지 질문

Part 3의 9개 Chapter는 다음 질문을 연결합니다. 앞의 선택이 뒤에서 어떤 입력과 해석을 가능하게 하는지 따라가 보세요.

| 질문 | 배울 내용 | 연결되는 Chapter |
| --- | --- | --- |
| 현실의 무엇을 기록했는가 | 기록의 뜻, 측정 조건·시점·단위를 읽는다. | Chapter 1~3 |
| 무엇을 한 건으로 볼 것인가 | 질문에 맞게 샘플을 정하고 행·열·시간 구간을 구성한다. | Chapter 2~5 |
| 기록은 어디까지 믿고 쓸 수 있는가 | 빠진 값, 겹친 기록, 부족한 조건, 측정 방식의 차이를 확인한다. | Chapter 4~6 |
| 어떤 정보를 남기고 무엇을 잃는가 | 요약값과 시간 순서 등 표현에 따라 보존되는 정보가 어떻게 달라지는지 비교한다. | Chapter 5~6 |
| 무엇과 비교하고 어디까지 해석할 것인가 | 지표와 비교 기준을 정하고, 관찰한 차이와 원인에 대한 판단을 구분한다. | Chapter 7~8 |
| AI가 무엇을 보고 무엇을 맞히게 할 것인가 | 입력, 목표, 라벨, 사용 가능한 시점과 평가할 대상을 구분한다. | Chapter 9 |

이 순서는 이 책의 학습 흐름입니다. 모든 분석에서 한 번씩만 거치는 필수 절차는 아닙니다. 비교 중에 빠진 기록을 발견하면 처음의 질문이나 샘플 구성을 다시 살필 수 있습니다.

## 원시 기록도 데이터셋이며, 요약은 선택이다

원시 로그도 데이터셋입니다. 다만 데이터가 모여 있다는 사실과 현재 질문에 맞게 사용할 준비가 되었다는 판단은 구분해야 합니다. 센서값을 시간 순서대로 모아 둔 자료에서도 어떤 동작의 어느 구간인지, 빠진 기록은 없는지, 어떤 결과와 연결되는지 확인할 필요가 있습니다.

이 책에서는 같은 센서 기록을 동작별 요약 표로 바꾸고, 여러 동작을 과거의 비교 기준인 기준선과 대조하는 사례를 이어 갑니다. 각 단계에서 한 행의 뜻이 어떻게 바뀌는지, 원래 기록을 어떻게 추적할 수 있는지를 살핍니다. 요약 표는 비교를 설명하기 위한 한 가지 표현입니다.

질문과 모델에 따라 시간 순서를 가진 원시 시계열, 이미지 한 장, 문서 한 건도 입력으로 사용할 수 있습니다. 모두를 사람이 계산한 요약값으로 바꿔야 하는 것은 아닙니다. 이미지라면 한 장이 무엇을 담는지, 문서라면 전체를 한 사례로 볼지 일부 구간을 볼지처럼 데이터의 경계와 의미를 확인하는 질문이 이어집니다. 사람이 만든 특징과 모델이 학습하는 표현의 관계는 Chapter 6에서 살펴봅니다.

## Part 4로 넘길 입력과 목표

Part 3에서는 데이터를 읽고 구성한 뒤 그 자료로 무엇을 말할 수 있는지 확인합니다. 결과는 사람이 읽는 비교 리포트로 남을 수도 있고, 먼저 확인할 사례를 모은 검토 목록이 될 수도 있습니다. 예측이 필요한 문제라면 어떤 정보를 입력으로 쓰고 어떤 결과를 맞힐지 정리합니다.

Part 4에서는 이 입력과 목표를 바탕으로 머신러닝의 학습과 평가를 다룹니다. Part 3에서는 예측할 순간에 알 수 있는 정보와 나중에 확인되는 결과를 구분하고, 어떤 대상에서 성능을 확인하려는지까지 적습니다. 구체적인 학습 알고리즘과 평가용 데이터 분할 절차는 Part 4에서 이어 갑니다.

## 체크리스트

- 센서 사례에서 무엇을 기록하고, 무엇을 한 사례로 묶고, 어떤 정보를 남기는지 설명할 수 있는가?
- 지표는 무엇을 비교하기 위해, 품질 점검은 어떤 판단의 한계를 알기 위해, 라벨은 어떤 학습 목표를 정하기 위해 필요한지 각각 한 문장으로 말할 수 있는가?
- 원시 기록도 데이터셋이라는 점과 현재 질문에 맞는 준비 상태를 구분할 수 있는가?
- 같은 질문을 이미지 한 장이나 문서 한 건에 적용했을 때 확인할 경계나 부가 정보를 하나 제안할 수 있는가?

## 출처와 참고 자료

- National Academies of Sciences, Engineering, and Medicine, *Data Science for Undergraduates: Opportunities and Options*, 2018. 데이터 수집, 정리, 표현, 모델링, 해석을 하나의 데이터과학 흐름으로 묶어 설명하므로, 데이터 이해·구성·표현·해석을 연결하는 이 페이지의 교육적 범위를 참고하는 자료입니다. 위 여섯 질문의 배열은 이 책의 집필 판단입니다. [https://nap.nationalacademies.org/catalog/25104/data-science-for-undergraduates-opportunities-and-options](https://nap.nationalacademies.org/catalog/25104/data-science-for-undergraduates-opportunities-and-options){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Google for Developers, `Machine Learning Glossary`. example, feature, label 항목을 통해 한 사례, 입력 정보, 학습에서 맞힐 결과를 구분하는 설명을 확인했습니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-09-19
- W3C, `PROV-Overview`. provenance와 derivation을 함께 다루므로, 원천데이터를 문제 표현 구조로 다시 만들 때 어떤 규칙으로 파생 표가 생겼는지 추적 가능해야 한다는 Part 3의 공통 전제를 뒷받침합니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-09-19
- Usama Fayyad, Gregory Piatetsky-Shapiro, Padhraic Smyth, `Knowledge Discovery and Data Mining: Towards a Unifying Framework`, Microsoft Research publication page, 1996. KDD 과정을 데이터 준비와 발견 흐름으로 설명하는 고전적 근거이므로, 데이터 준비와 이후 분석을 연결하는 배경 자료입니다. [https://www.microsoft.com/en-us/research/publication/knowledge-discovery-and-data-mining-towards-a-unifying-framework/](https://www.microsoft.com/en-us/research/publication/knowledge-discovery-and-data-mining-towards-a-unifying-framework/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- U.S. Bureau of Labor Statistics, `Consumer Price Index: Concepts`, Handbook of Methods. CPI index values and base periods 설명을 통해 기준 기간을 정해 현재 값을 비교하는 관점을 확인하는 참고 자료입니다. [https://www.bls.gov/opub/hom/cpi/concepts.htm](https://www.bls.gov/opub/hom/cpi/concepts.htm){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
