# P2-7.5 의존성(dependency)과 재현성(reproducibility)

> Section ID: `P2-7.5`
> Version: `v2026.09.08`

같은 코드를 다시 실행하려면 필요한 패키지, Python 버전, 데이터 파일과 실행 위치도 맞아야 합니다. 의존성(dependency)은 코드가 필요로 하는 외부 요소이며, 재현성(reproducibility)은 실행 조건을 다시 구성했을 때 같은 동작이나 결과를 확인할 수 있는 성질입니다.

| 용어 | 뜻 |
| --- | --- |
| 의존성(dependency) | 내 코드가 기대고 있는 외부 패키지와 실행 조건입니다. |
| 재현성(reproducibility) | 같은 코드를 나중에 다시 실행할 수 있게 조건을 남기는 성질입니다. |
| `requirements.txt` | 필요한 패키지 목록과 버전을 기록하는 대표 파일입니다. |
| 버전 고정(version pinning) | 특정 패키지 버전을 명시해 환경 차이를 줄이려는 방법입니다. |
| 환경 기록(environment record) | Python 버전, 패키지 목록, 실행 위치처럼 재실행에 필요한 메모입니다. |

## 코드와 실행 조건의 기록

| 기준 | 왜 중요한가 |
| --- | --- |
| 의존성은 코드가 기대고 있는 외부 패키지와 실행 조건이다 | 코드만 보고는 실행되지 않는 이유를 설명해 준다 |
| 재현성은 같은 코드를 나중에 다시 실행할 수 있게 조건을 남기는 일이다 | 학습과 협업은 한 번 실행되고 끝나지 않기 때문이다 |
| requirements 파일은 필요한 패키지 목록과 버전 범위를 기록한다 | 다른 사람이 환경을 다시 만들 때 출발점이 된다 |

## 직접 의존성과 간접 의존성

의존성(dependency)은 내 코드가 실행되기 위해 필요로 하는 외부 조건입니다. Python 실습에서는 주로 패키지 의존성을 먼저 만납니다.

예를 들어 다음 코드는 NumPy가 필요합니다.

NumPy 배열 `[1, 2, 3]`의 평균을 계산하면 `2.0`이 출력됩니다. `import numpy`를 사용하므로 실행 환경에 NumPy가 필요합니다.

```python
# 배열 계산에 필요한 NumPy를 불러옵니다.
import numpy as np

# values는 NumPy 설치와 평균 계산이 모두 되는지 확인할 작은 배열입니다.
values = np.array([1, 2, 3])
print(values.mean())
```

이 코드는 Python만 있으면 충분하지 않습니다. NumPy가 설치되어 있어야 합니다.

- 내 코드: `import numpy as np`를 사용합니다.
- 필요한 외부 패키지: NumPy입니다.
- 따라서 NumPy는 이 코드의 의존성입니다.

의존성은 직접 의존성과 간접 의존성으로 나눠 볼 수 있습니다.

- 직접 의존성: 내가 코드에서 직접 사용하는 패키지입니다.
- 간접 의존성: 내가 설치한 패키지가 내부적으로 필요로 하는 다른 패키지입니다.

패키지 하나를 설치할 때 그 패키지가 요구하는 다른 패키지도 함께 설치될 수 있습니다.

## 재실행에 필요한 조건

재현성(reproducibility)은 같은 코드와 같은 조건에서 다시 실행했을 때, 같은 동작을 기대할 수 있는 성질입니다.

AI와 데이터 실습에서 재현성은 중요합니다. 수학 설명을 읽는 단계에서는 큰 문제가 없어 보이지만, 코드를 실행하는 순간 환경 차이가 결과를 바꿀 수 있습니다.

- Python 버전이 다를 수 있습니다.
- 패키지 버전이 다를 수 있습니다.
- 운영체제가 다를 수 있습니다.
- 데이터 파일 위치가 다를 수 있습니다.
- Colab 런타임이 초기화되었을 수 있습니다.

따라서 실습을 공유하려면 코드만 주는 것으로는 부족할 수 있습니다. “어떤 환경에서 실행했는가”를 함께 남겨야 합니다.

## 초기화된 노트북 런타임

AI 학습에서는 “오늘 실행한 노트북”을 한 달 뒤 다시 열어보는 일이 자주 생깁니다.

실행한 날에는 다음 조건이 맞아 있었습니다.

- Colab 런타임이 켜져 있었습니다.
- `numpy`, `pandas`, `matplotlib`이 이미 설치되어 있었습니다.
- 데이터 파일을 `/content/data/` 폴더에 올려 두었습니다.
- 코드 셀을 위에서부터 차례대로 실행했습니다.

한 달 뒤에는 상황이 달라질 수 있습니다.

- Colab 런타임이 초기화되어 직접 설치한 패키지가 사라졌습니다.
- 데이터 파일을 다시 업로드하지 않았습니다.
- 중간 셀부터 실행해서 앞에서 만든 변수가 없습니다.
- 패키지 기본 버전이 바뀌었습니다.

이때 “코드가 틀렸다”고 바로 판단하면 원인을 놓칠 수 있습니다. 먼저 실행 조건이 다시 만들어졌는지 확인해야 합니다. 재현성은 이 확인을 쉽게 만드는 기록 습관입니다.

## requirements.txt 설치 목록

pip 문서는 requirements files를 `pip install`에 전달할 설치 항목 목록을 담은 파일로 설명합니다. 흔히 `requirements.txt`라는 이름을 사용합니다.

예를 들어 다음과 같은 파일을 만들 수 있습니다.

```text
numpy
pandas
matplotlib
```

그리고 다음처럼 설치할 수 있습니다.

```bash
python -m pip install -r requirements.txt
```

이 파일의 역할은 다음과 같습니다.

- `requirements.txt`는 Python 코드가 아닙니다.
- 터미널 명령도 아닙니다.
- 설치해야 할 패키지 목록을 적어 둔 파일입니다.

이 파일이 있으면 다른 사람은 “이 프로젝트가 어떤 패키지를 요구하는가”를 더 쉽게 알 수 있습니다.

## CSV 평균 계산 프로젝트

작은 실습 폴더가 다음처럼 구성되어 있다고 가정합니다.

```text
score-summary/
  summary.py
  scores.csv
  requirements.txt
```

`summary.py`는 CSV 파일을 읽고 평균을 계산합니다.

[scores.csv](../../../assets/part-02/chapter-07/scores.csv)를 내려받아 `summary.py`와 같은 폴더에 둡니다. CSV의 한 행은 학생 한 명이며 `score` 열에는 `82, 91, 77, 88`이 들어 있습니다. `score-summary` 폴더에서 실행하면 평균 `84.5`가 출력됩니다.

```python
# CSV를 표 형태로 읽기 위해 pandas를 불러옵니다.
import pandas as pd

# scores.csv를 읽어 표 데이터의 score 열 평균을 계산합니다.
scores = pd.read_csv("scores.csv")
print(scores["score"].mean())
```

`requirements.txt`에는 이 코드가 직접 사용하는 패키지 `pandas`를 적습니다.

```text
pandas
```

받는 사람은 폴더로 이동한 뒤 다음 명령으로 필요한 패키지를 준비할 수 있습니다.

```bash
python -m pip install -r requirements.txt
```

설치와 실행에는 프로젝트의 같은 Python을 사용합니다. 준비가 끝나면 `python summary.py`로 계산을 실행합니다. `requirements.txt`만 설치해도 CSV가 없으면 파일을 읽을 수 없으므로 데이터 파일도 함께 필요합니다.

## 버전 지정과 설치 목록 기록

패키지는 시간이 지나며 바뀝니다. 오늘 설치한 NumPy와 1년 뒤 설치한 NumPy가 같은 버전이라는 보장은 없습니다.

그래서 버전을 적어 둘 수 있습니다.

```text
numpy==2.0.0
pandas==2.2.2
matplotlib==3.9.0
```

`==`는 특정 버전을 지정한다는 뜻입니다. 이런 방식을 버전 고정(version pinning)이라고 부를 수 있습니다.

pip 사용자 가이드는 `pip freeze` 결과를 requirements 파일에 담아 반복 가능한 설치(repeatable installs)에 사용할 수 있다고 설명합니다. 이때 파일에는 `pip freeze`를 실행한 시점에 설치되어 있던 패키지와 버전이 기록됩니다.

예를 들어 다음 명령을 만날 수 있습니다.

```bash
python -m pip freeze > requirements-snapshot.txt
```

그리고 다른 환경에서 다음처럼 설치할 수 있습니다.

```bash
python -m pip install -r requirements-snapshot.txt
```

`>`는 출력 내용을 파일에 저장하며, 같은 이름의 파일이 있으면 덮어씁니다. `pip freeze`는 설치된 환경의 목록을 출력하므로 프로젝트가 쓰지 않는 패키지가 섞여 있을 수도 있습니다.

버전 고정만으로 모든 실행 조건이 같아지지는 않습니다. 운영체제, Python 버전, 하드웨어, 패키지 배포 상태가 영향을 줄 수 있습니다.

예를 들어 학습 자료를 만들 때는 다음 두 방식의 차이를 생각할 수 있습니다.

- `pandas`: 최신 버전이 설치될 수 있으므로 시간이 지나면 환경이 달라질 수 있습니다.
- `pandas==2.2.2`: 특정 버전을 요구하므로 당시 환경에 더 가깝게 맞출 수 있습니다.

위 버전 번호는 표기법을 설명하는 예시입니다. 실제 설치 목록은 프로젝트를 실행해 확인한 버전으로 기록합니다.

## 설치 목록과 프로젝트 메타데이터

requirements 파일과 프로젝트의 배포용 설치 요구사항은 목적이 다릅니다.

- requirements 파일: 특정 환경을 구성하기 위해 설치할 목록입니다.
- 프로젝트 설정 파일: 패키지를 배포하거나 프로젝트 메타데이터를 설명하는 파일입니다.

## 노트북의 설치 명령과 환경 기록

Colab은 시작이 쉽습니다. 하지만 재현성 문제가 사라지는 것은 아닙니다.

Colab 런타임은 초기화될 수 있습니다. 그때 설치했던 패키지는 사라질 수 있습니다. 또 Colab이 제공하는 기본 패키지 버전이 시간이 지나 바뀔 수도 있습니다.

그래서 노트북 상단에 필요한 설치 명령을 남기거나, 어떤 환경에서 실행했는지 기록하는 습관이 필요합니다.

다음 셀은 현재 노트북 커널에 NumPy, pandas, Matplotlib을 설치합니다. 런타임을 새로 만들었다면 필요한 패키지를 다시 준비할 수 있습니다.

```python
# 노트북 재현에 필요한 주요 패키지를 현재 코드 셀 환경에 설치합니다.
%pip install numpy pandas matplotlib
```

이 명령은 편리하지만, 장기적으로는 패키지 버전과 실행 날짜를 함께 남기는 편이 더 안전합니다.

예를 들어 노트북 맨 위에 다음처럼 짧은 메모를 둘 수 있습니다.

- 작성일: 2026-07-20
- 실행 환경: Google Colab
- 주요 패키지: numpy, pandas, matplotlib
- 다시 실행할 때 확인할 것: 런타임 초기화 여부, 데이터 파일 업로드 여부

이 정도의 메모만 있어도 나중에 같은 오류를 반복해서 추적하는 시간을 줄일 수 있습니다.

## 실행 기록 항목

실행 기록에는 다음 항목을 포함합니다.

- 어떤 Python 버전에서 실행했는가
- 어떤 패키지가 필요한가
- 중요한 패키지의 버전은 무엇인가
- 코드는 어느 폴더를 기준으로 실행하는가
- 데이터 파일은 어디에 있어야 하는가
- Colab인지 로컬 PC인지

이 정보가 있으면 나중에 오류가 생겼을 때 원인을 좁히기 쉽습니다.

## 파일과 패키지를 빠뜨렸을 때의 차이

CSV 평균 계산 프로젝트에서 하나씩 빠뜨려 보면 실패 지점이 달라집니다.

| 실행 조건 | 결과 | 복구할 항목 |
| --- | --- | --- |
| pandas가 없음 | `import pandas`에서 `ModuleNotFoundError` | 실행 중인 Python에 패키지 설치 |
| pandas는 있지만 scores.csv가 없음 | `read_csv`에서 `FileNotFoundError` | 데이터 파일과 현재 작업 폴더 확인 |
| 패키지와 CSV가 모두 준비됨 | 평균 `84.5` 출력 | 이 조건과 실행 명령 기록 |

CSV의 점수 `82`를 `100`으로 바꾸면 같은 코드와 패키지에서도 평균은 `89.0`이 됩니다. 결과를 비교하려면 환경뿐 아니라 입력 데이터가 같은지도 확인해야 합니다.

## 체크리스트

- 의존성(dependency)을 내 코드가 실행되기 위해 필요한 외부 패키지로 설명할 수 있다.
- 재현성(reproducibility)을 같은 코드를 나중에 다시 실행할 수 있는 조건으로 설명할 수 있다.
- `requirements.txt`가 설치할 패키지 목록을 담는 파일이라는 점을 설명할 수 있다.
- `python -m pip install -r requirements.txt`가 requirements 파일을 기준으로 패키지를 설치하는 명령임을 설명할 수 있다.
- `pip freeze`가 현재 환경에 설치된 패키지와 버전을 기록하는 데 쓰일 수 있음을 설명할 수 있다.
- 버전 고정이 재현성을 높일 수 있지만 모든 문제를 해결하지는 않는다는 점을 설명할 수 있다.
- `이 코드는 어떤 외부 패키지에 기대고 있는가`, `그 패키지는 어떤 Python 환경에 설치되어 있는가`, `나중에 같은 환경을 다시 만들 수 있는 기록이 있는가`를 점검할 수 있다.

## 출처와 참고 자료

- Python Packaging Authority, [User Guide](https://pip.pypa.io/en/stable/user_guide/){: target="_blank" rel="noopener noreferrer" }, pip documentation v26.1.2, 확인 날짜: 2026-07-20. `python -m pip`, 패키지 설치, requirements 파일, repeatable installs를 위한 `pip freeze` 사용 맥락 확인에 사용했다.
- Python Packaging Authority, [pip freeze](https://pip.pypa.io/en/stable/cli/pip_freeze/){: target="_blank" rel="noopener noreferrer" }, pip documentation v26.1.2, 확인 날짜: 2026-07-20. 현재 환경에 설치된 패키지 목록을 requirements 형식으로 출력한다는 설명 확인에 사용했다.
- Python Packaging Authority, [install_requires vs requirements files](https://packaging.python.org/en/latest/discussions/install-requires-vs-requirements/){: target="_blank" rel="noopener noreferrer" }, Python Packaging User Guide, 확인 날짜: 2026-07-20. 프로젝트 배포용 의존성 메타데이터와 실행 환경 재현을 위한 requirements 파일의 역할 차이 확인에 사용했다.
