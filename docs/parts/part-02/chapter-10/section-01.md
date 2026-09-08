# P2-10.1 노트북(notebook)은 왜 학습에 유용한가

> Section ID: `P2-10.1`
> Version: `v2026.09.08`

노트북(notebook)은 코드, 실행 결과, 설명을 함께 저장하는 계산 문서(computational notebook)입니다. Jupyter Notebook이나 Google Colab에서는 코드를 셀 단위로 실행하고, 바로 아래의 숫자·표·차트를 보면서 해석을 적을 수 있습니다.

## 코드 셀과 마크다운 셀

셀(cell)은 문서의 작은 블록입니다. 코드 셀은 계산을 실행하고, 마크다운 셀은 제목·설명·수식·링크를 기록합니다. 출력은 코드 셀의 실행 결과로 붙으며 별도의 셀 종류는 아닙니다.

| 구성 | 역할 | 예시 |
| --- | --- | --- |
| 마크다운 셀 | 질문과 해석 기록 | 세 학생의 평균과 낮은 점수를 함께 확인한다 |
| 코드 셀 | 계산 실행 | `sum(scores) / len(scores)` |
| 코드 셀의 출력 | 결과 표시 | `67.33333333333333` |

```mermaid
--8<-- "assets/part-02/chapter-10/notebook-cell-learning-flow-ko.mmd"
```

점수 `[82, 75, 45]`의 평균은 약 67.33입니다. Python 스크립트에서는 `print()`로 값을 표시할 수 있습니다.

```python
scores = [82, 75, 45]
average = sum(scores) / len(scores)
print(average)
```

Python 노트북 코드 셀에서는 마지막 표현식의 값도 표시됩니다. 다음 셀은 계산 결과를 `average`에 저장하고 마지막 줄에서 그 값을 표시합니다. 출력은 앞 코드와 같습니다.

```python
scores = [82, 75, 45]
average = sum(scores) / len(scores)
average
```

계산 뒤의 마크다운 셀에 “평균은 약 67.33이지만, 45점인 학생도 있다”라고 적으면 대표값과 개별 값의 차이를 함께 남길 수 있습니다. 코드를 바꿔도 이 해석 문장은 자동으로 갱신되지 않습니다.

## 셀별 실험

데이터 준비와 계산, 조건 변경을 나누면 어느 단계의 결과인지 확인하기 쉽습니다.

```mermaid
--8<-- "assets/part-02/chapter-10/notebook-experiment-flow-ko.mmd"
```

첫 코드 셀에서 다섯 학생의 점수를 준비합니다. 대입문만 있으므로 표시되는 출력은 없고, 실행 중인 Python 커널에 `scores`가 생깁니다. 커널(kernel)은 코드를 실행하고 변수 등의 상태를 유지하는 프로세스입니다.

```python
scores = [82, 75, 45, 90, 61]
```

두 번째 코드 셀에서 앞의 점수로 평균을 계산하면 `70.6`이 표시됩니다.

```python
mean_score = sum(scores) / len(scores)
mean_score
```

세 번째 코드 셀은 기준 `60` 이상인 점수를 골라 `[82, 75, 90, 61]`을 표시합니다.

```python
threshold = 60
passed = [score for score in scores if score >= threshold]
passed
```

세 번째 셀의 `threshold`를 `80`으로 바꾸고 그 셀만 다시 실행하면 `[82, 90]`이 표시됩니다. 점수 데이터와 평균은 그대로이며 선택 기준과 결과만 달라집니다.

## 셀 실행 순서와 남은 상태

노트북 화면의 셀 순서와 실제 실행 순서는 다를 수 있습니다. 아래 첫 셀을 실행하면 커널에 `x = 10`이 저장됩니다.

```python
x = 10
```

그다음 셀을 실행하면 `15`가 표시됩니다.

```python
x + 5
```

첫 셀의 코드를 `x = 100`으로 고치기만 하고 실행하지 않으면, 두 번째 셀을 다시 실행해도 `15`입니다. 커널에는 이전 값 `10`이 남아 있기 때문입니다. 첫 셀과 두 번째 셀을 차례로 실행해야 `105`가 됩니다.

커널을 재시작하면 이전 변수 상태가 사라집니다. 이때 두 번째 셀만 실행하면 `x`가 정의되지 않아 `NameError`가 발생합니다. 커널을 재시작한 뒤 위에서 아래로 모두 실행하면 문서에 남은 코드만으로 결과를 다시 만들 수 있는지 확인할 수 있습니다.

| 확인 대상 | 확인하는 이유 |
| --- | --- |
| import와 데이터 준비 셀 | 계산에 필요한 입력과 패키지 확인 |
| 커널 재시작 후 전체 실행 | 이전 실행에서 남은 값에 의존하는지 확인 |
| 코드와 출력의 일치 | 수정한 코드가 실제로 실행됐는지 확인 |
| 출력과 해석의 일치 | 결과 변경이 설명에도 반영됐는지 확인 |

## 사례: 평균은 같고 퍼짐은 다른 점수

다음 두 점수 목록은 모두 평균이 12입니다. 평균만 비교하면 차이가 보이지 않으므로, 평균에서 얼마나 떨어져 있는지도 계산합니다. 각 편차의 제곱을 항목 수로 나눈 기술 통계용 분산을 사용합니다.

```python
sample_a = [10, 12, 13, 11, 14]
sample_b = [8, 16, 9, 15, 12]

mean_a = sum(sample_a) / len(sample_a)
mean_b = sum(sample_b) / len(sample_b)
variance_a = sum((value - mean_a) ** 2 for value in sample_a) / len(sample_a)
variance_b = sum((value - mean_b) ** 2 for value in sample_b) / len(sample_b)

print("means:", mean_a, mean_b)
print("variances:", variance_a, variance_b)
```

```text
means: 12.0 12.0
variances: 2.0 10.0
```

마크다운 셀에는 “평균은 같지만 B의 분산이 5배 크다”라고 해석을 붙일 수 있습니다. B의 값을 `[10, 14, 11, 13, 12]`로 바꾸고 다시 실행하면 평균은 여전히 12이고 분산은 2가 됩니다. 이제 두 목록의 평균과 분산이 같으므로 기존 해석도 수정해야 합니다.

노트북에는 입력, 계산, 출력, 해석을 함께 남길 수 있습니다. 다만 입력을 고친 뒤 계산 셀을 실행하거나 해석을 수정하는 일은 별도로 해야 합니다.

## 노트북과 스크립트의 용도

노트북은 중간 결과와 설명을 함께 살피는 탐색에 적합합니다. 같은 작업을 반복 실행하거나 함수를 여러 곳에서 재사용할 때는 `.py` 스크립트나 모듈(module)로 분리할 수 있습니다.

| 작업 | 구성 예시 |
| --- | --- |
| 데이터와 차트를 보며 해석 | 노트북에 코드·출력·해석을 배치 |
| 실험 조건 비교 | 조건별 결과와 설명을 노트북에 기록 |
| 같은 처리를 여러 실험에서 사용 | 공통 함수를 Python 모듈로 분리 |
| 정해진 작업 반복 실행 | 입력과 실행 순서가 명확한 스크립트로 구성 |

예를 들어 점수 통계 함수를 모듈에 두고, 노트북에서는 그 함수를 호출해 두 입력의 결과와 해석을 비교할 수 있습니다.

## 체크리스트

- 노트북(notebook)을 코드, 설명, 출력이 함께 있는 계산 문서로 설명할 수 있다.
- 코드 셀(code cell)과 마크다운 셀(markdown cell)을 구분할 수 있다.
- 노트북이 AI 수학과 Python 실습 기록에 유용한 이유를 설명할 수 있다.
- 셀 실행 순서가 결과에 영향을 줄 수 있음을 설명할 수 있다.
- 노트북이 스크립트를 완전히 대체하지 않는다는 점을 설명할 수 있다.
- 학습 노트북에서 질문, 코드, 출력, 해석을 함께 남길 수 있다.
- 노트북을 실행 도구이면서 학습 기록 문서로 설명할 수 있다.

## 출처와 참고 자료

- Project Jupyter, [Project Jupyter Documentation](https://docs.jupyter.org/en/latest/){: target="_blank" rel="noopener noreferrer" }, Jupyter Documentation 4.1.1 alpha, 확인 날짜: 2026-07-20. 노트북이 코드, 설명, 데이터, 시각화, 상호작용을 함께 담는 문서라는 설명 확인에 사용했다.
- Project Jupyter, [Architecture](https://docs.jupyter.org/en/latest/projects/architecture/content-architecture.html){: target="_blank" rel="noopener noreferrer" }, Jupyter Documentation 4.1.1 alpha, 확인 날짜: 2026-07-20. 노트북 문서, 사용자 인터페이스, 커널 등 구성 요소를 구분하는 배경 근거로 사용했다.
- Google, [Welcome to Colab](https://colab.research.google.com/notebooks/intro.ipynb){: target="_blank" rel="noopener noreferrer" }, Google Colab, 확인 날짜: 2026-07-20. 브라우저 기반 노트북 환경에서 코드와 설명을 함께 실행·기록하는 예시 확인에 사용했다.
