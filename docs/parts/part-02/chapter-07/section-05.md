# P2-7.5 의존성(dependency)과 재현성(reproducibility)

P2-7.4에서는 가상환경(virtual environment)과 패키지(package)를 봤습니다. 이제 한 가지 질문이 남습니다.

패키지를 설치하면 끝일까요?

처음에는 그렇게 보일 수 있습니다. 하지만 학습 코드가 조금만 길어져도 다음 문제가 생깁니다.

- 내 컴퓨터에서는 실행된다.
- 다른 사람 컴퓨터에서는 실행되지 않는다.
- 어제는 실행됐다.
- 오늘은 패키지 버전이 달라져 결과가 달라졌다.
- Colab에서는 된다.
- 로컬 PC에서는 안 된다.

이 문제는 코드 자체보다 실행 환경을 다시 만들 수 있는가와 관련됩니다. 그래서 의존성(dependency)과 재현성(reproducibility)을 따로 봐야 합니다.

## 이 절의 범위

이 절은 의존성과 재현성의 입문 개념을 다룹니다. 패키지 배포, lock 파일, dependency resolver, 컨테이너(container), CI 환경은 깊게 다루지 않습니다.

여기서는 다음 질문에 답합니다.

- 의존성은 무엇인가?
- 재현성은 왜 필요한가?
- requirements 파일은 무엇을 기록하는가?
- 버전을 고정한다는 말은 무엇인가?

운영체제별 터미널 사용법은 P2-7.6에서, Python 설치는 P2-7.7에서 보충수업으로 다룹니다.

## 이 절의 목표

- 의존성(dependency)을 내 코드가 실행되기 위해 필요한 외부 패키지로 설명할 수 있습니다.
- 재현성(reproducibility)을 같은 코드를 나중에 다시 실행할 수 있는 조건으로 설명할 수 있습니다.
- `requirements.txt`가 설치할 패키지 목록을 담는 파일이라는 점을 설명할 수 있습니다.
- 버전 고정(version pinning)의 필요성과 한계를 입문 수준에서 설명할 수 있습니다.
- “내 컴퓨터에서는 된다”가 충분한 설명이 아님을 이해할 수 있습니다.

## 의존성은 내 코드가 기대고 있는 외부 조건이다

의존성(dependency)은 내 코드가 실행되기 위해 필요로 하는 외부 조건입니다. Python 실습에서는 주로 패키지 의존성을 먼저 만납니다.

예를 들어 다음 코드는 NumPy가 필요합니다.

```python
import numpy as np

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

처음부터 이 구조를 모두 외울 필요는 없습니다. 다만 “내가 설치한 하나의 패키지 뒤에 여러 패키지가 함께 따라올 수 있다”는 감각은 필요합니다.

## 예시: 같은 코드인데 어떤 곳에서는 실패한다

다음 상황을 생각해 봅니다. 책의 예제를 내려받아 평균을 계산하는 Python 파일을 실행했습니다.

```python
import numpy as np

scores = np.array([82, 91, 77, 88])
print(scores.mean())
```

Colab에서는 실행됩니다. 그런데 로컬 PC 터미널에서는 다음과 비슷한 오류가 날 수 있습니다.

```text
ModuleNotFoundError: No module named 'numpy'
```

이 오류는 코드의 평균 계산이 틀렸다는 뜻이 아닙니다. 현재 Python 환경에 NumPy가 준비되어 있지 않다는 뜻입니다.

이때 문제를 다음처럼 나눠 보면 원인을 찾기 쉽습니다.

- 코드가 요구하는 것: NumPy
- 현재 환경에 없는 것: NumPy 패키지
- 해결 방향: 현재 사용 중인 Python 환경에 NumPy를 설치하거나, 필요한 패키지 목록을 보고 환경을 다시 만든다

그래서 패키지를 설치했다는 기억만으로는 부족합니다. 어느 환경에, 어떤 패키지를, 어떤 버전으로 설치했는지 남겨야 합니다.

## 재현성은 나중에 다시 실행할 수 있는 조건이다

재현성(reproducibility)은 같은 코드와 같은 조건에서 다시 실행했을 때, 같은 동작을 기대할 수 있는 성질입니다.

AI와 데이터 실습에서 재현성은 중요합니다. 수학 설명을 읽는 단계에서는 큰 문제가 없어 보이지만, 코드를 실행하는 순간 환경 차이가 결과를 바꿀 수 있습니다.

- Python 버전이 다를 수 있습니다.
- 패키지 버전이 다를 수 있습니다.
- 운영체제가 다를 수 있습니다.
- 데이터 파일 위치가 다를 수 있습니다.
- Colab 런타임이 초기화되었을 수 있습니다.

따라서 실습을 공유하려면 코드만 주는 것으로는 부족할 수 있습니다. “어떤 환경에서 실행했는가”를 함께 남겨야 합니다.

## 예시: 학습 노트북을 한 달 뒤 다시 열었을 때

AI 학습에서는 “오늘 실행한 노트북”을 한 달 뒤 다시 열어보는 일이 자주 생깁니다.

처음 실행한 날에는 다음 조건이 맞아 있었습니다.

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

## requirements 파일은 설치 목록을 남기는 방법이다

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

입문 단계에서는 이렇게 이해합니다.

- `requirements.txt`는 Python 코드가 아닙니다.
- 터미널 명령도 아닙니다.
- 설치해야 할 패키지 목록을 적어 둔 파일입니다.

이 파일이 있으면 다른 사람은 “이 프로젝트가 어떤 패키지를 요구하는가”를 더 쉽게 알 수 있습니다.

## 예시: 작은 실습 폴더를 다른 사람에게 전달한다

작은 실습 폴더가 다음처럼 구성되어 있다고 가정합니다.

```text
score-summary/
  summary.py
  scores.csv
  requirements.txt
```

`summary.py`는 CSV 파일을 읽고 평균을 계산합니다.

```python
import pandas as pd

scores = pd.read_csv("scores.csv")
print(scores["score"].mean())
```

이 파일만 전달하면 받는 사람은 `pandas`가 필요한지 바로 알기 어렵습니다. 그래서 `requirements.txt`에 필요한 패키지를 적습니다.

```text
pandas
```

받는 사람은 폴더로 이동한 뒤 다음 명령으로 필요한 패키지를 준비할 수 있습니다.

```bash
python -m pip install -r requirements.txt
```

이 예시에서 중요한 점은 `requirements.txt`가 코드를 실행하는 파일이 아니라는 것입니다. 코드가 기대는 외부 패키지 목록을 남기는 파일입니다.

## 버전을 고정한다는 것은 범위를 좁히는 일이다

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
python -m pip freeze > requirements.txt
```

그리고 다른 환경에서 다음처럼 설치할 수 있습니다.

```bash
python -m pip install -r requirements.txt
```

하지만 버전을 고정한다고 모든 문제가 사라지는 것은 아닙니다. 운영체제, Python 버전, 하드웨어, 패키지 배포 상태가 영향을 줄 수 있습니다. 이 절에서는 “재현성을 높이는 출발점”으로만 이해합니다.

예를 들어 학습 자료를 만들 때는 다음 두 방식의 차이를 생각할 수 있습니다.

- `pandas`: 최신 버전이 설치될 수 있으므로 시간이 지나면 환경이 달라질 수 있습니다.
- `pandas==2.2.2`: 특정 버전을 요구하므로 당시 환경에 더 가깝게 맞출 수 있습니다.

처음 공부할 때는 모든 패키지를 엄격하게 고정하지 않아도 됩니다. 다만 책의 예제, 수업 자료, 팀 프로젝트처럼 다른 사람이 다시 실행해야 하는 코드라면 버전 기록의 중요성이 커집니다.

## requirements 파일과 프로젝트 설정 파일은 역할이 다르다

Python Packaging User Guide는 requirements 파일과 패키지의 설치 요구사항을 구분합니다. 입문 단계에서 깊게 들어갈 필요는 없지만, 다음 차이는 기억할 만합니다.

- requirements 파일: 특정 환경을 구성하기 위해 설치할 목록입니다.
- 프로젝트 설정 파일: 패키지를 배포하거나 프로젝트 메타데이터를 설명하는 파일입니다.

이 책의 실습에서는 처음부터 복잡한 패키지 배포 구조를 다루지 않습니다. 따라서 우선은 `requirements.txt`를 “실습 환경을 다시 만들기 위한 설치 목록”으로 이해하면 충분합니다.

## Colab에서도 재현성은 사라지지 않는다

Colab은 시작이 쉽습니다. 하지만 재현성 문제가 사라지는 것은 아닙니다.

Colab 런타임은 초기화될 수 있습니다. 그때 설치했던 패키지는 사라질 수 있습니다. 또 Colab이 제공하는 기본 패키지 버전이 시간이 지나 바뀔 수도 있습니다.

그래서 노트북 상단에 필요한 설치 명령을 남기거나, 어떤 환경에서 실행했는지 기록하는 습관이 필요합니다.

```python
%pip install numpy pandas matplotlib
```

이 명령은 편리하지만, 장기적으로는 패키지 버전과 실행 날짜를 함께 남기는 편이 더 안전합니다.

예를 들어 노트북 맨 위에 다음처럼 짧은 메모를 둘 수 있습니다.

- 작성일: 2026-06-24
- 실행 환경: Google Colab
- 주요 패키지: numpy, pandas, matplotlib
- 다시 실행할 때 확인할 것: 런타임 초기화 여부, 데이터 파일 업로드 여부

이 정도의 메모만 있어도 나중에 같은 오류를 반복해서 추적하는 시간을 줄일 수 있습니다.

## 실습 프로젝트에서 남겨야 할 최소 정보

처음부터 완벽한 재현 환경을 만들 필요는 없습니다. 하지만 다음 정보는 남기는 습관이 좋습니다.

- 어떤 Python 버전에서 실행했는가
- 어떤 패키지가 필요한가
- 중요한 패키지의 버전은 무엇인가
- 코드는 어느 폴더를 기준으로 실행하는가
- 데이터 파일은 어디에 있어야 하는가
- Colab인지 로컬 PC인지

이 정보가 있으면 나중에 오류가 생겼을 때 원인을 좁히기 쉽습니다.

## 이 절에서 기억할 관점

의존성과 재현성을 볼 때는 다음 질문을 먼저 합니다.

1. 이 코드는 어떤 외부 패키지에 기대고 있는가?
2. 그 패키지는 어떤 Python 환경에 설치되어 있는가?
3. 나중에 같은 환경을 다시 만들 수 있는 기록이 있는가?

코드는 글자만으로 실행되지 않습니다. 코드가 기대고 있는 환경을 함께 남기는 것이 재현성의 출발점입니다.

## 체크리스트

- 의존성(dependency)을 내 코드가 실행되기 위해 필요한 외부 패키지로 설명할 수 있다.
- 재현성(reproducibility)을 같은 코드를 나중에 다시 실행할 수 있는 조건으로 설명할 수 있다.
- `requirements.txt`가 설치할 패키지 목록을 담는 파일이라는 점을 설명할 수 있다.
- `python -m pip install -r requirements.txt`가 requirements 파일을 기준으로 패키지를 설치하는 명령임을 설명할 수 있다.
- `pip freeze`가 현재 환경에 설치된 패키지와 버전을 기록하는 데 쓰일 수 있음을 설명할 수 있다.
- 버전 고정이 재현성을 높일 수 있지만 모든 문제를 해결하지는 않는다는 점을 설명할 수 있다.

## 출처와 참고 자료

- Python Packaging Authority, [User Guide](https://pip.pypa.io/en/stable/user_guide/){: target="_blank" rel="noopener noreferrer" }, pip documentation, 확인 날짜: 2026-06-24.
- Python Packaging Authority, [pip freeze](https://pip.pypa.io/en/stable/cli/pip_freeze/){: target="_blank" rel="noopener noreferrer" }, pip documentation, 확인 날짜: 2026-06-24.
- Python Packaging Authority, [install_requires vs requirements files](https://packaging.python.org/en/latest/discussions/install-requires-vs-requirements/){: target="_blank" rel="noopener noreferrer" }, Python Packaging User Guide, 확인 날짜: 2026-06-24.
