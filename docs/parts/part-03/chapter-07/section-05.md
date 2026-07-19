# P3-7.5 기준선은 고정해야 하는가, 최근 평소 기준으로 갱신해야 하는가

> Section ID: `P3-7.5`
> Version: `v2026.07.19`

기준선 후보를 고른 뒤에는 또 다른 질문이 남습니다. `이 기준을 한동안 고정해 둘 것인가, 아니면 최근 평소 구간에 맞춰 함께 움직일 것인가?` 같은 조건의 구간을 골랐더라도, 기준을 유지하는 방식이 달라지면 비교 문장의 뜻도 달라집니다.

기준선 운영 방식은 정답 하나를 미리 정해 두는 문제가 아닙니다. 어떤 변화를 보고 싶은지에 따라 더 자연스러운 선택이 달라집니다.

| 기준선 형태 | 더 잘 맞는 질문 | 주의할 점 |
| --- | --- | --- |
| 고정 기준선 | 특정 기준 시점 대비 얼마나 달라졌는가 | 현재 운영이 이미 바뀌었으면 너무 오래된 기준이 될 수 있다 |
| 최근 평소 기준선 | 최근 흐름 안에서 지금만 달라졌는가 | 너무 짧게 잡으면 기준선이 불안정해진다 |

예를 들어 설비 교정 직후의 안정 구간을 대표 기준으로 오래 두고 싶다면 고정 기준선이 자연스럽습니다. 반대로 운영 환경이 조금씩 변하는 시스템에서는 최근 평소 구간을 기준선으로 두는 편이 더 현실적일 수 있습니다. 중요한 점은 어떤 방식을 쓰든 `지금 무엇과 비교하고 있는가`를 문장으로 설명할 수 있어야 한다는 사실입니다.

이 선택은 일반화해서 보면 `참조 기준을 유지할 것인가, 굴릴 것인가`의 문제입니다. BLS의 `base period`는 비교를 위한 기준 시점을 두는 일반 원리를 보여 주고, FPP3의 rolling forecasting origin은 시간이 앞으로 갈수록 기준이 되는 과거 구간도 함께 이동할 수 있다는 점을 보여 줍니다. 여기서는 이 개념들을 그대로 옮기기보다, `질문이 기준 유지 방식을 결정한다`는 수준으로만 연결해 두면 충분합니다.

## 근거가 본문 주장과 어떻게 연결되는가

외부 근거를 붙일 때는 `기준선`이라는 단어 자체보다, 기준이 어떤 역할을 맡는지 연결하는 편이 안전합니다.

| 본문의 핵심 주장 | 일반화 관점에서 필요한 근거 | 현재 붙일 수 있는 근거의 역할 |
| --- | --- | --- |
| 기준선은 비교를 위한 참조 구간이어야 한다 | baseline 또는 base period가 비교용 기준점이라는 설명 | NCI의 baseline 정의와 BLS의 base period 정의가 이 점을 뒷받침한다 |
| 기준선은 질문에 따라 고정하거나 최근 구간으로 갱신할 수 있다 | 시간이 흐르며 기준이 이동하는 비교 구조도 가능하다는 설명 | FPP3의 rolling forecasting origin은 `기준이 고정만 되는 것은 아니다`라는 점을 보여 주는 유사 개념이다 |

여기서 rolling origin은 예측 평가 문맥의 개념이므로, 현재 절에서는 직접 등치하지 않습니다. 이 책에서는 `최근 평소 기준선`이 왜 자연스러운 선택일 수 있는지를 설명하는 비유적 근거로만 사용합니다.

## 여기서 단정하지 않는 것

다음과 같은 주장은 여기서 단정하지 않습니다.

- 기준선은 언제나 최근 구간으로 계속 갱신해야 한다
- 표본 수 기준은 어느 도메인에서나 같은 숫자로 정해진다
- 고정 기준선이 최근 평소 기준선보다 항상 더 신뢰할 만하다

기준선 운영 방식이 잘못 잡히면 비교 리포트와 현재 비교 문장의 뜻이 함께 흔들립니다. 같은 변화라도 무엇과 비교했는지가 바뀌면 `검토 필요`, `주의`, `정상/이상 후보` 같은 현재 판단의 무게도 달라질 수 있습니다. 이 절을 고정 기준선과 최근 평소 기준선의 취향 차이가 아니라, `참조 기준을 유지할 것인가 이동시킬 것인가(reference maintenance strategy)`의 문제로 다시 보면, 기준선 운영 방식은 정답 경쟁이 아니라 비교 질문에 맞는 참조 유지 방식을 고르는 선택이라는 점이 더 분명해집니다.

## 작은 도식으로 보기

이 절의 핵심은 기준선 형태 자체보다 `비교 질문`이 어떤 기준 유지 방식을 더 자연스럽게 만드는가에 있습니다. 고정 기준선과 최근 평소 기준선은 서로 다른 질문을 더 잘 받쳐 주고, 그에 따라 비교 문장의 뜻도 달라집니다.

--8<-- "assets/part-03/chapter-07/p3-7-5-mermaid-01-ko.mmd"

## 출처와 참고 자료

- U.S. Bureau of Labor Statistics, `Base period`. 특정 시점이나 기간을 comparison reference로 두는 일반 원리를 제공하므로, 고정 기준선의 역할을 설명하는 근거가 됩니다. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
- National Cancer Institute, `baseline`. baseline을 초기 측정값을 정한 뒤 시간에 따른 변화를 비교하는 기준으로 설명하므로, 기준선이 먼저 비교용 참조 측정이라는 이 절의 전제를 보강합니다. [https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-19
- NIST/SEMATECH e-Handbook of Statistical Methods, `What are Variables Control Charts?`. control chart가 현재 공정 특성을 과거 성능과 비교하며, control limit은 타당하고 강한 이유가 있을 때만 바꾸라고 설명하므로, 기준선을 고정할지 갱신할지는 질문과 운영 변화 근거에 맞춰 정해야 한다는 이 절의 설명을 직접 보강합니다. [https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-19
- Hyndman, Athanasopoulos et al., `Forecasting: Principles and Practice (3rd ed)`, `Time series cross-validation`. rolling forecasting origin처럼 기준이 시간이 흐르며 앞으로 이동하는 구조를 설명하므로, 최근 평소 기준선처럼 참조 구간이 함께 이동하는 운영 방식이 가능하다는 유사 개념의 근거가 됩니다. 다만 이 자료는 예측 평가 문맥이므로, 현재 절에서는 `이동하는 참조 기준`이라는 상위 개념만 비유적으로 가져옵니다. [https://otexts.com/fpp3/tscv.html](https://otexts.com/fpp3/tscv.html){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
