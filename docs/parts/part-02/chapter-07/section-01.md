# P2-7.1 로컬 환경(local environment)과 실행 환경(runtime)

> Section ID: `P2-7.1`
> Version: `v2026.09.08`

Python 코드는 인터프리터(interpreter)가 읽고 실행합니다. 로컬 환경(local environment)은 내 컴퓨터의 Python, 패키지, 파일, 설정을 가리키고, 실행 환경(runtime)은 코드가 실제로 동작하는 프로그램과 자원을 가리킵니다. 브라우저에서 코드를 입력해도 실행은 다른 컴퓨터에서 이루어질 수 있습니다.

## AI 실험과 Python

AI를 공부하다 보면 Python이 자주 나옵니다. 이때 “왜 하필 Python인가?”라는 질문이 생길 수 있습니다.

Python은 1980년대 말 Guido van Rossum이 만들기 시작했고, 1991년에 공개된 언어입니다. Python 공식 FAQ는 Python이 ABC 언어의 경험에서 영향을 받았고, 시스템 관리 작업을 C 프로그램이나 셸 스크립트만으로 처리하기 어려웠던 상황에서 더 확장 가능한 스크립팅 언어가 필요했다는 배경을 설명합니다.

이 역사에서 중요한 점은 Python이 처음부터 사람이 읽고 쓰기 쉬운 고수준 언어이면서, 실제 시스템 작업에도 연결되는 실행 도구였다는 점입니다.

그래서 Python은 학습, 자동화, 데이터 처리, 실험 코드에 잘 맞습니다. Python 공식 FAQ도 Python이 명확한 문법, 큰 표준 라이브러리, 대화형 인터프리터를 갖고 있어 처음 배우는 언어로도 적합하다고 설명합니다.

AI 분야에서 Python이 자주 보이는 이유도 이 흐름과 연결됩니다.

- 수식을 코드로 옮기기 쉽습니다.
- 작은 실험을 빠르게 실행할 수 있습니다.
- NumPy, Pandas, Matplotlib 같은 도구가 많습니다.
- 머신러닝과 딥러닝 라이브러리가 Python 생태계에 많이 모여 있습니다.

물론 Python이 유일한 언어라는 뜻은 아닙니다. 실제 서비스 내부에서는 C++, Java, JavaScript, Go, Rust 같은 언어도 함께 쓰입니다. 하지만 AI 학습과 실험의 입구에서는 Python을 만날 가능성이 높습니다.

## 터미널 명령과 Python 코드

터미널(terminal)은 명령과 결과를 주고받는 창이고, 셸(shell)은 입력한 명령을 해석하는 프로그램입니다. macOS의 Terminal이나 Windows Terminal에서 셸을 사용할 수 있으며, Bash와 PowerShell은 셸의 예입니다.

터미널의 셸 프롬프트에 다음 명령을 넣으면 Python 버전이 출력됩니다.

```bash
python --version
```

`print("hello")`는 Python 코드입니다. 노트북 코드 셀이나 Python 인터프리터에 입력하면 `hello`가 출력됩니다.

```python
# 문자열을 출력하는 Python 문장입니다.
print("hello")
```

같은 문장을 메모장에 적어 두기만 하면 실행되지 않습니다. Python 코드를 읽고 실행하는 프로그램이 필요합니다. 터미널에 `python --version`을 입력하는 것과 Python에 `print("hello")`를 입력하는 것은 서로 다른 작업입니다.

| 문장 | 입력 위치 | 결과 |
| --- | --- | --- |
| `python --version` | 터미널의 셸 프롬프트 | Python 버전 출력 |
| `python example.py` | 터미널의 셸 프롬프트 | example.py 실행 |
| `print("hello")` | Python 코드 또는 노트북 코드 셀 | hello 출력 |
| `%pip install numpy` | IPython 기반 노트북 코드 셀 | 해당 커널에 NumPy 설치 |

## 인터프리터의 실행 방식

Python 인터프리터(Python interpreter)는 Python 코드를 읽고 실행하는 프로그램입니다. 실행 방식에 따라 코드를 전달하는 자리가 달라집니다.

| 방식 | 사용 방법 |
| --- | --- |
| 대화형 실행 | 터미널에서 `python`을 실행한 뒤 `>>>`에 Python 코드 입력 |
| 스크립트 실행 | 코드를 example.py에 저장하고 터미널에서 `python example.py` 실행 |
| 노트북 실행 | Python 커널에 연결된 코드 셀을 실행 |

대화형 실행을 끝내고 셸로 돌아가려면 `>>>`에서 `exit()`를 입력합니다. 프롬프트 `>>>` 자체는 입력할 코드가 아닙니다.

## 로컬 환경의 구성

로컬 환경(local environment)은 내 컴퓨터 안에서 코드가 실행되는 조건을 말합니다. 여기에는 운영체제, Python 설치 위치, 패키지 설치 상태, 현재 작업 폴더, 환경 변수 같은 것들이 포함될 수 있습니다.

같은 코드라도 컴퓨터마다 결과가 달라질 수 있습니다.

예를 들어 다음처럼 컴퓨터마다 조건이 달라질 수 있습니다.

- 내 컴퓨터에는 NumPy가 설치되어 있지만, 다른 컴퓨터에는 없을 수 있습니다.
- 내 컴퓨터는 Python 3.12를 쓰지만, 다른 컴퓨터는 Python 3.10을 쓸 수 있습니다.
- 내 컴퓨터에서는 파일 경로가 맞지만, 다른 컴퓨터에서는 파일 위치가 다를 수 있습니다.

그래서 실습 문서에서는 “코드”만큼이나 “어디에서 실행하는가”가 중요합니다.

## 로컬 실행과 Colab 런타임

실행 환경(runtime)은 코드가 실제로 실행되는 자리입니다. 로컬 PC에서 실행하면 내 컴퓨터가 실행 환경이 됩니다. Colab의 호스팅 런타임에서 실행하면 Google이 제공하는 환경이 코드를 처리합니다.

| 실행 방식 | 실행 환경 |
| --- | --- |
| Colab 코드 셀 실행 | Colab 런타임 |
| 내 컴퓨터 터미널에서 실행 | 로컬 Python 환경 |
| 가상환경을 켜고 실행 | 해당 가상환경의 Python과 패키지 |

Colab은 편합니다. Python 설치 없이 브라우저에서 실행할 수 있습니다. 하지만 런타임이 끊기거나, 파일이 사라지거나, 제공 정책이 바뀔 수 있습니다.

로컬 PC는 처음 설정이 번거롭습니다. 하지만 내 프로젝트 파일, 패키지 버전, 실행 방식을 직접 관리할 수 있습니다.

정리하면 다음과 같습니다.

- Colab: 시작하기 쉽고, 실행 환경은 외부 서비스가 관리합니다.
- 로컬 PC: 처음 설정이 필요하지만, 실행 환경을 내가 관리합니다.

## 프로젝트별 가상환경

가상환경(virtual environment)은 Python 프로젝트마다 별도의 실행 공간을 만들어 주는 장치입니다. Python 공식 문서는 `venv`가 가벼운 가상환경을 만들고, 각 가상환경이 독립된 Python 패키지 집합을 가질 수 있다고 설명합니다.

왜 필요할까요? 프로젝트 A는 `numpy 1.x`가 필요하고 프로젝트 B는 `numpy 2.x`가 필요할 수 있습니다. 이 둘을 한 컴퓨터에 모두 섞어 설치하면 충돌할 수 있으므로, 프로젝트별로 공간을 나눕니다.

가상환경은 프로젝트 코드 자체가 아닙니다. Python 공식 문서도 가상환경은 보통 `.venv` 또는 `venv` 같은 디렉터리에 만들며, 소스 관리 시스템에 넣지 않는다고 설명합니다. 어떤 프로젝트에서든 `.venv`는 실행을 위한 로컬 환경이지 본문 파일이나 코드 자체가 아닙니다.

프로젝트 폴더의 터미널에서 다음 명령을 실행하면 `.venv` 디렉터리에 가상환경이 만들어집니다.

```bash
python -m venv .venv
```

생성한 가상환경의 Python을 선택해 실행해야 그 환경에 설치한 패키지를 사용합니다. 생성·활성화 명령은 [가상환경과 패키지 설치](section-04.md)에서 확인할 수 있습니다.

## 패키지 설치와 import

패키지(package)는 관련 코드를 묶어 재사용할 수 있게 한 단위입니다. NumPy, Pandas, Matplotlib 같은 도구가 여기에 해당합니다.

역할은 다음과 같이 나뉩니다.

- Python: 언어와 실행 프로그램입니다.
- 패키지: Python에서 가져다 쓰는 코드 묶음입니다.
- `pip`: 패키지를 설치하는 도구입니다.

예를 들어 NumPy를 설치하는 명령과 불러오는 코드는 다릅니다.

```bash
python -m pip install numpy
```

NumPy가 설치된 Python에서 다음 코드를 실행하면 `np`라는 이름으로 불러옵니다. 성공하면 별도 출력 없이 다음 코드로 넘어갑니다.

```python
# NumPy를 현재 실행 환경에서 불러올 수 있는지 확인합니다.
import numpy as np
```

첫 번째는 설치입니다. 두 번째는 Python 코드 안에서 사용하겠다고 불러오는 일입니다.

## Colab에서 되던 import가 로컬에서 실패할 때

Colab에서는 `import numpy as np`가 실행되는데 로컬에서는 다음 오류가 난다고 가정합니다.

```text
ModuleNotFoundError: No module named 'numpy'
```

이 오류는 실행 중인 Python이 NumPy를 찾지 못했다는 뜻입니다. 다른 Python이나 가상환경에 설치되어 있을 수도 있으므로, 실제 인터프리터부터 확인합니다. 오류가 난 코드와 같은 노트북 커널이나 Python 실행 방식에서 다음 코드를 실행하면 인터프리터 파일 경로가 출력됩니다.

```python
import sys

# 현재 코드를 실행하는 Python의 위치입니다.
print(sys.executable)
```

그 경로가 프로젝트에서 사용하려던 Python인지 확인합니다. 터미널에서 해당 Python을 선택했다면 `python -m pip show numpy`로 설치 상태를 확인할 수 있습니다. 설치되어 있지 않다면 `python -m pip install numpy`로 그 Python에 설치합니다.

설치 명령이 성공했는데도 같은 오류가 나면, 설치에 쓴 Python과 코드 실행에 쓴 Python의 경로가 같은지 비교합니다. 패키지 이름만 확인해서는 서로 다른 실행 환경에 설치된 경우를 구분할 수 없습니다.

## 실행 문제별 확인 위치

| 문제 | 확인할 내용 |
| --- | --- |
| 파일을 찾지 못함 | [터미널과 작업 폴더](section-02.md) |
| Python 코드의 실행 방법을 모름 | [인터프리터와 스크립트 실행](section-03.md) |
| 설치했는데 패키지를 불러오지 못함 | [가상환경과 패키지 설치](section-04.md) |
| 다른 컴퓨터에서 결과가 달라짐 | [의존성과 재현성](section-05.md) |

## 체크리스트

- 로컬 환경(local environment)을 내 컴퓨터에서 코드가 실행되는 조건으로 설명할 수 있다.
- 실행 환경(runtime)을 코드가 실제로 실행되는 자리로 설명할 수 있다.
- 터미널 명령과 Python 코드를 구분할 수 있다.
- Python 인터프리터(Python interpreter)를 Python 코드를 읽고 실행하는 프로그램으로 설명할 수 있다.
- 가상환경(virtual environment)이 프로젝트별 실행 공간이라는 정도로 설명할 수 있다.
- 패키지 설치와 `import`가 다른 일임을 입문 수준에서 설명할 수 있다.
- Colab과 로컬 PC가 모두 실행 환경이지만 관리 방식이 다르다는 점을 설명할 수 있다.
- `어디에서 실행하는가`, `무엇이 실행하는가`, `어떤 패키지가 필요한가`, `그 패키지는 어디에 설치되어 있는가`를 먼저 점검할 수 있다.

## 출처와 참고 자료

- Python Software Foundation, [Using the Python Interpreter](https://docs.python.org/3/tutorial/interpreter.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. Python 인터프리터를 호출하고, 대화형 입력과 스크립트 실행을 구분하는 근거로 사용했다.
- Python Software Foundation, [General Python FAQ](https://docs.python.org/3/faq/general.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. Python이 인터프리터형·대화형 프로그래밍 언어이며 여러 운영체제에서 사용할 수 있다는 기본 설명 확인에 사용했다.
- Python Software Foundation, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. 가상환경이 독립된 디렉터리 안에 Python 설치와 패키지 상태를 갖는다는 설명 확인에 사용했다.
- Python Packaging Authority, [Install packages in a virtual environment using pip and venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/){: target="_blank" rel="noopener noreferrer" }, Python Packaging User Guide, 확인 날짜: 2026-07-20. 프로젝트별 가상환경 생성, 활성화, 패키지 설치 흐름을 확인하는 근거로 사용했다.

- Python Software Foundation, [sys.executable](https://docs.python.org/3/library/sys.html#sys.executable){: target="_blank" rel="noopener noreferrer" }, 확인 날짜: 2026-09-08. 현재 Python 인터프리터의 실행 파일 경로를 확인하는 근거.
