# P2-3.5 파이썬 실행 환경: Colab과 로컬 PC

> Section ID: `P2-3.5`
> Version: `v2026.07.19`

P2-3.1부터 P2-3.4까지는 선형대수(linear algebra)를 수식과 비교 기준 중심으로 봤습니다. 다음 절에서는 NumPy로 벡터(vector), 행렬(matrix), 행렬 곱(matrix multiplication)을 직접 확인합니다. 그 전에 파이썬(Python) 코드를 어디에서 실행하는지 먼저 구분해야 합니다.

이 파트의 초반 실습은 두 실행 환경을 기준으로 설명합니다.

1. Google Colab은 브라우저에서 바로 실행합니다.
2. 로컬 PC는 내 컴퓨터의 터미널과 파이썬 설치 환경에서 실행합니다.

따라서 여기서는 Colab 자체를 깊게 배우거나 로컬 설치법을 자세히 다루기보다, 이후 Python/NumPy 실습을 따라가기 위해 `코드 셀(code cell)에서 실행하는 명령`, `개인 PC 터미널에서 실행하는 명령`, `파이썬 코드 안에 쓰는 문장`을 구분하는 데 집중합니다.

여기서는 `Colab`, `로컬 PC`, `코드 셀(code cell)`, `터미널(terminal)`, `import`와 설치 명령의 차이를 다시 정리합니다. 3.1부터 3.4까지 수식과 선형대수 구조를 읽었다면, 이제 그 구조를 실제 코드로 옮길 실행 자리를 먼저 정리합니다.

개인 PC에 파이썬을 설치하고 가상환경을 관리하는 방법은 `P2-7.1`, `P2-7.6`, `P2-7.7`, `P2-7.8`에서 다시 다룹니다. 여기서는 Colab과 로컬 PC의 실행 위치 차이를 먼저 잡습니다. 용어를 다시 빠르게 확인할 때는 [개념사전](../../../reference/concept-glossary.md)도 함께 봅니다.

이 문서는 2026년 7월 19일 확인한 Google Colab 공식 안내와 FAQ, IPython `%pip` 문서, pip 사용자 가이드를 기준으로 작성했습니다. Colab은 외부 서비스이므로 앞으로 UI, 사용 조건, 무료 제공 범위, 런타임 정책, 서비스 지속 여부가 바뀔 수 있습니다. 이 절을 읽는 시점에 Colab이 제공되지 않거나 안내와 다르게 보인다면, Google Colab 공식 문서와 현재 서비스 상태를 별도로 확인해야 합니다.

## 이 절의 범위

여기서는 다음 NumPy 실습을 준비하기 위해 Colab과 로컬 PC의 실행 위치를 구분하고, 필요한 경우 NumPy를 설치하는 명령이 환경별로 어떻게 달라지는지만 다룹니다.

이번 절은 Colab과 로컬 PC의 `실행 위치 차이`와 `어디에 무엇을 입력하는가`까지를 먼저 닫습니다. 로컬 설치와 터미널, 가상환경 절차는 `P2-7.1`, `P2-7.6`, `P2-7.7`, `P2-7.8`에서 다시 정리합니다.

여기서는 다음 질문에 집중합니다.

- Colab은 무엇을 하기 위한 도구인가?
- 로컬 PC에서 실행한다는 말은 무엇인가?
- 코드 셀은 어떻게 실행하는가?
- `%pip install numpy`는 어디에서 쓰는 명령인가?
- 개인 PC 터미널 명령과 Colab 명령은 어떻게 다른가?

## 이 절의 목표

- Google Colab을 설치 없는 브라우저 기반 실행 환경으로 이해할 수 있습니다.
- 로컬 PC 실행을 내 컴퓨터의 터미널과 파이썬 설치 환경에서 실행하는 방식으로 이해할 수 있습니다.
- `Welcome to Colab` 안내서를 열어 코드 셀(code cell)을 실행해 볼 수 있습니다.
- Colab/Jupyter의 `%pip`가 일반 파이썬 문법이 아니라 매직 명령(magic command)임을 설명할 수 있습니다.
- Colab 코드 셀 명령과 개인 PC 터미널 명령을 구분할 수 있습니다.
- 다음 절의 NumPy 예제를 Colab에서 실행할 준비를 할 수 있습니다.

## 먼저 붙잡을 한 장면

이 절에서 가장 먼저 붙잡아야 할 장면은 `NumPy를 쓰려면 어디에 무엇을 입력하는가`입니다.

| 하고 싶은 일 | Colab 코드 셀 | 로컬 PC 터미널 | Python 코드 |
| --- | --- | --- | --- |
| NumPy 설치 | `%pip install numpy` | `python -m pip install numpy` | 쓰지 않음 |
| NumPy 불러오기 | `import numpy as np` | 쓰지 않음 | `import numpy as np` |
| 간단한 계산 실행 | `print(np.array([1, 2]))` | `python example.py`처럼 실행 가능 | `print(np.array([1, 2]))` |

즉 독자가 제일 먼저 구분해야 할 것은 `무슨 명령인가`보다 `어디에 쓰는 문장인가`입니다.

## 세 가지 기준

| 기준 | 왜 중요한가 | 이 절에서 필요한 이해 수준 |
| --- | --- | --- |
| Colab은 브라우저 기반 실습 공간이다 | 파이썬 설치 전에도 예제를 바로 실행해 볼 수 있기 때문입니다. | 코드 셀에서 Python과 노트북용 설치 명령을 실행하는 자리라고 이해합니다. |
| 로컬 PC는 터미널과 설치 환경을 쓴다 | 같은 NumPy 준비 작업도 실행 위치가 바뀌면 명령 형태가 달라지기 때문입니다. | 터미널에서 `python -m pip`, 코드 안에서 `import`를 쓴다고 이해합니다. |
| 설치 명령과 Python 코드는 자리가 다르다 | 실행 위치를 혼동하면 문법 오류와 환경 오류를 반복하게 되기 때문입니다. | Colab 셀, 로컬 터미널, Python 코드의 세 자리를 구분한다고 이해합니다. |

## 실행 환경을 먼저 구분한다

파이썬 코드를 실행한다는 말은 하나의 뜻만 갖지 않습니다. 같은 예제라도 어디에서 실행하는지에 따라 명령의 모양이 달라집니다.

| 실행 위치 | 영어 | 무엇을 뜻하는가 | 명령 예 |
| --- | --- | --- | --- |
| Colab 코드 셀 | Colab code cell | 브라우저 노트북 안의 코드 셀에서 실행한다. | `%pip install numpy` |
| 로컬 PC 터미널 | local terminal | 내 컴퓨터의 터미널 앱에서 실행한다. | `python -m pip install numpy` |
| 파이썬 코드 | Python code | `.py` 파일이나 코드 셀 안의 파이썬 문장으로 실행한다. | `import numpy as np` |

이 구분을 놓치면 `%pip`, `python -m pip`, `import`를 같은 것으로 오해하기 쉽습니다. 세 표현은 모두 NumPy와 관련될 수 있지만 실행 위치와 역할이 다릅니다.

1. 패키지는 Colab 코드 셀 또는 로컬 PC 터미널에서 설치합니다.
2. 설치된 패키지는 파이썬 코드 안에서 `import`로 불러옵니다.

여기서 가장 자주 막히는 혼동을 한 번 더 짧게 적으면 다음과 같습니다.

| 혼동 장면 | 왜 막히는가 | 먼저 고칠 질문 |
| --- | --- | --- |
| `%pip install numpy`를 `.py` 파일에 적는다 | 설치 명령과 Python 코드를 섞었기 때문 | 지금 쓰는 곳이 코드 셀인가, Python 파일인가 |
| `import numpy as np`를 터미널에 그대로 실행하려 한다 | Python 문장을 셸 명령처럼 본 것 | 지금 쓰는 곳이 터미널인가, Python 실행기인가 |
| Colab 예제를 로컬에서 그대로 복사한다 | 실행 위치가 바뀌었는데 문법을 안 바꿨기 때문 | 지금 환경이 브라우저 노트북인가, 내 PC인가 |

## Colab은 브라우저에서 여는 노트북 환경이다

Google Colab은 브라우저에서 Jupyter Notebook 형태로 파이썬 코드를 실행할 수 있는 hosted 서비스입니다. 개인 PC에 파이썬을 설치하지 않아도 코드 셀을 만들고 실행해 볼 수 있습니다.

- [Google Colab](https://colab.research.google.com/){: target="_blank" rel="noopener noreferrer" }
- [Welcome to Colab](https://colab.research.google.com/notebooks/intro.ipynb){: target="_blank" rel="noopener noreferrer" }
- [Google Colab FAQ](https://research.google.com/colaboratory/faq.html){: target="_blank" rel="noopener noreferrer" }

`Welcome to Colab` 안내서를 열어 코드 셀을 실행하는 방식을 먼저 확인합니다. 이 절의 예제는 매우 작기 때문에 GPU나 TPU는 필요하지 않습니다. 다만 Colab은 Google 계정, 런타임 제한, 자원 제한이 있을 수 있습니다.

## 로컬 PC는 내 컴퓨터에서 실행하는 환경이다

로컬 PC(local PC)에서 실행한다는 말은 내 컴퓨터에 설치된 파이썬과 터미널을 사용한다는 뜻입니다. macOS의 Terminal, Windows Terminal, PowerShell, Linux shell 같은 프로그램에서 명령을 실행합니다.

예를 들어 로컬 PC 터미널에서는 다음처럼 NumPy를 설치할 수 있습니다.

```bash
python -m pip install numpy
```

그리고 파이썬 파일 안에서는 다음처럼 NumPy를 불러옵니다.

```python
import numpy as np
```

여기서는 로컬 설치 과정을 자세히 다루지 않습니다. 설치 자체는 P2-7.7 보충학습에서, 터미널과 환경 변수 문법은 P2-7.6과 P2-7.8에서 다시 봅니다. 지금 필요한 것은 `Colab 코드 셀 명령과 로컬 PC 터미널 명령은 다르다`는 구분입니다.

## 코드 셀에 파이썬 코드를 넣는다

Colab 노트북에는 글을 쓰는 셀과 코드를 실행하는 셀이 있습니다. 파이썬 코드는 코드 셀(code cell)에 넣어 실행합니다.

예를 들어 다음 코드를 코드 셀에 넣고 실행할 수 있습니다.

```python
print("hello, colab")
```

실행 결과는 다음처럼 나옵니다.

```text
hello, colab
```

이때 `print(...)`는 파이썬 코드입니다. 반면 패키지를 설치하는 명령은 일반 파이썬 코드와 성격이 조금 다릅니다.

## Colab에서는 `%pip`를 사용할 수 있다

Colab 환경에는 NumPy가 이미 준비되어 있는 경우가 많습니다. 하지만 환경이 달라질 수 있으므로 필요하면 코드 셀에서 다음 명령을 실행합니다.

```python
%pip install numpy
```

여기서 `%pip`는 일반 파이썬 문법이 아니라 Jupyter Notebook 계열 환경에서 쓰는 매직 명령(magic command)입니다. 현재 노트북 커널(kernel)에 패키지를 설치하라는 뜻입니다.

Colab이나 Jupyter 문서에서는 셸 명령을 실행할 때 다음처럼 느낌표(`!`)를 붙인 예제도 볼 수 있습니다.

```python
!pip install numpy
```

여기서는 노트북 환경에 설치한다는 뜻이 더 분명한 `%pip install numpy`를 우선 사용합니다.

이 차이를 흐름으로 다시 쓰면 다음과 같습니다.

```mermaid
--8<-- "assets/part-02/chapter-03/execution-location-flow-ko.mmd"
```

## 개인 PC 터미널 명령과 섞지 않는다

개인 PC의 터미널에서는 `%pip`나 `!pip`를 쓰지 않습니다. 이 표시는 Colab/Jupyter 코드 셀에서 쓰는 방식입니다.

개인 PC 터미널에서는 보통 다음처럼 실행합니다.

```bash
python -m pip install numpy
```

따라서 실행 위치를 먼저 구분합니다.

1. Colab 코드 셀에서는 `%pip install numpy`를 씁니다.
2. 개인 PC 터미널에서는 `python -m pip install numpy`를 씁니다.
3. 파이썬 코드 안에서는 `import numpy as np`를 씁니다.

다음 절에서는 이 구분을 전제로 NumPy 코드를 확인합니다.

독자가 여기서 남겨야 할 최소 문장은 다음 한 줄입니다.

- `설치는 코드 셀이나 터미널에서 하고, import와 계산은 Python 코드에서 한다.`

## 체크리스트

- Colab과 로컬 PC 실행의 차이를 한 문장으로 설명할 수 있는가?
- `%pip install numpy`와 `python -m pip install numpy`가 왜 같은 자리에 쓰이지 않는지 말할 수 있는가?
- `import numpy as np`가 설치 명령이 아니라 Python 코드라는 점을 설명할 수 있는가?
- 지금 보는 문장이 코드 셀용인지, 터미널용인지, Python 코드용인지 구분할 수 있는가?
- 환경을 고르기 전에 문법을 외우기보다 먼저 실행 위치를 구분해야 하는 이유를 설명할 수 있는가?

## 출처와 참고 자료

- Google, `Google Colab`. Colab이 브라우저 기반 노트북 환경이라는 점과 기본 사용 흐름을 직접 확인할 수 있습니다. [https://colab.research.google.com/](https://colab.research.google.com/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-19
- Google, `Welcome to Colab`. 코드 셀 실행 방식과 노트북 기본 흐름을 직접 확인할 수 있습니다. [https://colab.research.google.com/notebooks/intro.ipynb](https://colab.research.google.com/notebooks/intro.ipynb){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-19
- Google, `Google Colab FAQ`. Colab이 설치 없이 쓰는 hosted Jupyter Notebook 서비스이며 런타임과 사용 제한이 바뀔 수 있다는 점을 확인할 수 있습니다. [https://research.google.com/colaboratory/faq.html](https://research.google.com/colaboratory/faq.html){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-19
- IPython Development Team, `Built-in magic commands - %pip`. `%pip install`이 현재 커널 안에서 pip 패키지 관리자를 실행하는 매직 명령이라는 점을 확인할 수 있습니다. [https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-pip](https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-pip){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-19
- Python Packaging Authority, `pip User Guide`. 로컬 터미널에서 `python -m pip install ...` 형태로 패키지를 설치하는 공식 예시를 확인할 수 있습니다. [https://pip.pypa.io/en/stable/user_guide/](https://pip.pypa.io/en/stable/user_guide/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-19
