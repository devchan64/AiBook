# P2-7.3 Python 인터프리터(interpreter)와 스크립트(script)

> Section ID: `P2-7.3`
> Version: `v2026.09.15`

`python`은 대화형 Python을 여는 터미널 명령이고, `python hello.py`는 파일에 저장한 코드를 실행하는 명령입니다. `print("hello")`는 인터프리터가 읽는 Python 코드입니다. 실행 방식에 따라 입력할 위치와 결과를 남기는 방법이 달라집니다.

## Python 인터프리터

Python 인터프리터(Python interpreter)는 Python 코드를 읽고 실행하는 프로그램입니다. Python 공식 문서는 인터프리터를 명령줄(command line)에서 호출할 수 있고, 파일이나 다른 실행 옵션을 지정하지 않고 터미널에서 실행하면 대화형 모드(interactive mode)에 들어간다고 설명합니다.

## 대화형 모드와 프롬프트

터미널에서 Python을 실행하면 대화형 모드(interactive mode)를 사용할 수 있습니다.

```bash
python
```

환경에 따라 명령 이름이 `python3`일 수도 있습니다.

```bash
python3
```

대화형 모드에 들어가면 보통 `>>>` 프롬프트가 보입니다. Python 공식 문서도 대화형 모드에서 기본 프롬프트가 `>>>`라고 설명합니다.

`>>>` 뒤에 계산식이나 함수를 입력하면 결과가 바로 표시됩니다. 아래의 `>>>`는 입력할 코드가 아니라 프롬프트 표시입니다.

```pycon
>>> 1 + 2
3
>>> print("hello")
hello
```

대화형 모드는 계산을 바로 확인하기 좋습니다.

대화형 모드는 다음 상황에 특히 잘 맞습니다.

- 짧은 계산을 확인합니다.
- 문법을 시험해 봅니다.
- 작은 값을 바로 출력해 봅니다.

하지만 대화형 모드에 입력한 내용은 보통 파일로 남지 않습니다. 다시 실행하려면 다시 입력해야 합니다. 그래서 여러 줄의 코드를 반복해서 실행해야 할 때는 스크립트(script) 파일을 사용합니다.

## 파일에 저장한 스크립트

스크립트(script)는 실행할 코드를 파일에 저장해 둔 것입니다. Python 파일은 보통 `.py` 확장자를 사용합니다.

아래 두 줄을 `hello.py`에 저장해 실행하면 `hello`와 `3`이 차례로 출력됩니다.

```python
# 스크립트는 위에서 아래로 여러 문장을 차례대로 실행합니다.
print("hello")
print(1 + 2)
```

터미널에서 같은 폴더에 있다면 다음처럼 실행할 수 있습니다.

```bash
python hello.py
```

환경에 따라 다음 명령을 쓸 수도 있습니다.

```bash
python3 hello.py
```

스크립트 실행은 대화형 실행과 다릅니다.

| 실행 방식 | 입력 위치 | 장점 | 주의할 점 |
| --- | --- | --- | --- |
| 대화형 실행 | `>>>` 프롬프트 | 한 줄씩 바로 확인하기 좋다 | 입력 기록이 파일로 남지 않을 수 있다 |
| 스크립트 실행 | `.py` 파일 | 저장, 수정, 재실행, 공유가 쉽다 | 현재 작업 폴더와 파일 경로를 확인해야 한다 |

AI 학습에서는 작은 계산을 바로 확인할 때도 있고, 같은 코드를 여러 번 고쳐 실행할 때도 있습니다. 그래서 두 방식을 모두 만납니다.

## 셸과 Python의 입력 위치

셸 프롬프트에서는 `python hello.py`로 파일 실행을 요청합니다. Python의 `>>>`에서는 `print("hello")`처럼 Python 코드를 입력합니다.

Python 대화형 모드에서 파일 실행 명령을 잘못 입력하면 다음과 같은 오류가 납니다.

```pycon
>>> python hello.py
  File "<stdin>", line 1
    python hello.py
           ^^^^^
SyntaxError: invalid syntax
```

이 경우 `hello.py` 파일을 고칠 필요는 없습니다. `>>>`에서 `exit()`를 입력해 셸로 돌아간 뒤 `python hello.py`를 실행합니다. 오류 메시지의 세부 모양은 Python 버전에 따라 달라질 수 있습니다.

## 노트북 셀과 실행 상태

Colab이나 Jupyter의 코드 셀(code cell)은 Python 코드를 셀 단위로 실행합니다.

코드 셀은 대화형 실행처럼 즉시 결과를 보여 주면서도 노트북에 기록을 남긴다는 점을 봅니다.

```python
# 터미널에서 실행하든 코드 셀에서 실행하든 출력 확인용 코드는 같습니다.
print("hello")
```

코드 셀은 대화형 실행처럼 즉시 결과를 확인하기 좋습니다. 동시에 노트북 파일에 코드와 결과, 설명을 함께 남길 수 있습니다. 그래서 학습용으로 편합니다.

하지만 코드 셀은 스크립트 파일과도 다릅니다. 셀 실행 순서가 바뀌면 결과가 달라질 수 있고, 앞 셀에서 만든 변수를 뒤 셀이 사용하기도 합니다.

세 실행 자리를 다시 나누면 다음과 같습니다.

- 대화형 모드: 한 줄씩 빠르게 확인합니다.
- 스크립트 파일: 파일 전체를 저장하고 반복 실행합니다.
- 노트북 코드 셀: 설명과 결과를 함께 남기며 셀 단위로 실행합니다.

나중에 실습이 길어지면 “노트북에서는 됐는데 스크립트로 옮기면 안 된다”는 상황이 생길 수 있습니다. 그때는 셀 실행 순서, 파일 경로, 필요한 import, 패키지 설치 상태를 나누어 확인해야 합니다.

## 모듈 실행 옵션 -m

터미널에서 다음 명령을 자주 보게 됩니다.

```bash
python -m pip install numpy
```

여기서 `-m`은 Python에게 특정 모듈(module)을 스크립트처럼 실행하라고 요청하는 방식입니다. Python 공식 문서는 `python -m module` 형식이 라이브러리 모듈을 스크립트로 실행한다고 설명합니다.

두 명령은 실행 대상을 지정하는 방법이 다릅니다.

- `python hello.py`: 파일을 실행합니다.
- `python -m pip ...`: `pip`라는 모듈을 Python을 통해 실행합니다.

`-m`은 Python 코드 문법이 아니라 인터프리터의 실행 옵션입니다. `python -m pip`는 명령 앞에 지정한 Python에서 pip를 실행합니다.

## 실행 방식별 오류 확인

같은 Python 코드라도 실행 방식에 따라 확인할 지점이 달라집니다.

| 상황 | 먼저 확인할 것 |
| --- | --- |
| 대화형 모드에서 안 된다 | 지금 `>>>` 프롬프트 안에 있는가 |
| 스크립트 파일이 안 열린다 | 현재 작업 폴더에 파일이 있는가 |
| `python` 명령을 찾을 수 없다 | Python이 설치되어 있고 명령 이름이 맞는가 |
| Colab에서는 되는데 로컬에서 안 된다 | 로컬에 같은 파일과 패키지가 있는가 |
| 스크립트로 옮기니 안 된다 | 노트북 셀 실행 순서에 의존하던 값이 있는가 |

## 노트북에서만 남아 있던 변수

노트북의 앞 셀에서 `name = "Mina"`를 실행한 뒤 다른 셀에서 `print(name)`을 실행하면 `Mina`가 출력됩니다. 그러나 `hello.py`에 `print(name)`만 옮기면 새 Python 실행에는 `name`이 없으므로 `NameError`가 납니다.

```python
# 새 실행에서도 필요한 값을 먼저 정의합니다.
name = "Mina"
print(name)
```

두 줄을 함께 저장하면 스크립트에서도 `Mina`가 출력됩니다. 노트북 코드를 파일로 옮길 때는 출력 셀뿐 아니라 그 셀이 사용하는 변수 정의와 import도 포함해야 합니다.

## 계산 결과와 화면 출력

대화형 Python에서 `1 + 2`를 입력하면 3이 표시되지만, 그 식만 저장한 스크립트는 값을 계산하고도 화면에는 표시하지 않습니다. 아래 내용을 `display.py`에 저장해 실행하면 마지막 줄의 `print` 때문에 3이 한 번 출력됩니다.

```python
1 + 2
result = 1 + 2
print(result)
```

```bash
python display.py
```

`print(result)`를 지우고 다시 실행하면 출력이 없습니다. 출력이 없다는 사실만으로 실행 실패라고 판단하면 안 됩니다. 노트북에 저장된 과거 출력도 현재 커널 상태를 보장하지 않으므로, 공유 전에는 커널을 재시작하고 셀을 위에서부터 다시 실행해 결과를 확인합니다.

## 체크리스트

- Python 인터프리터(Python interpreter)를 Python 코드를 읽고 실행하는 프로그램으로 설명할 수 있다.
- 대화형 모드(interactive mode)에서 `>>>` 프롬프트에 Python 코드를 입력한다는 점을 설명할 수 있다.
- 스크립트(script)가 `.py` 파일에 저장한 실행 단위라는 점을 설명할 수 있다.
- `python hello.py`는 터미널 명령이고, `print("hello")`는 Python 코드라는 점을 구분할 수 있다.
- Colab/Jupyter 코드 셀은 Python 코드를 셀 단위로 실행한다는 점을 설명할 수 있다.
- `python -m pip ...`에서 `-m`이 터미널에서 Python 인터프리터에게 주는 실행 옵션이라는 점을 설명할 수 있다.
- 지금 입력하는 곳이 셸인지, Python 프롬프트인지, 코드 셀인지 구분할 수 있다.

## 출처와 참고 자료

- Python Software Foundation, [General Python FAQ](https://docs.python.org/3/faq/general.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, 확인 날짜: 2026-07-20. Python을 해석형·대화형 프로그래밍 언어로 설명하고, Guido van Rossum의 초기 개발 배경을 확인하는 근거로 사용했다.
- Python Software Foundation, [Using the Python Interpreter](https://docs.python.org/3/tutorial/interpreter.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, 확인 날짜: 2026-07-20. Python 인터프리터 호출, 대화형 모드, 스크립트 파일 실행의 차이를 확인하는 근거로 사용했다.
- Python Software Foundation, [Command line and environment](https://docs.python.org/3/using/cmdline.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, 확인 날짜: 2026-07-20. `python script.py`, `python -c`, `python -m module-name` 같은 명령줄 실행 방식 확인에 사용했다.

- [Python tutorial: Modules](https://docs.python.org/3/tutorial/modules.html){: target="_blank" rel="noopener noreferrer" }, 확인 날짜: 2026-09-15.
