# P2-3.4 파이썬 실행 환경: Colab과 로컬 PC

P2-3.1부터 P2-3.3까지는 선형대수(linear algebra)를 수식과 그림 중심으로 봤습니다. 다음 절에서는 NumPy로 벡터(vector), 행렬(matrix), 행렬 곱(matrix multiplication)을 직접 확인합니다. 그 전에 파이썬(Python) 코드를 어디에서 실행하는지 먼저 구분해야 합니다.

이 책의 초반 실습은 두 실행 환경을 기준으로 설명합니다.

> Google Colab
> -> 브라우저에서 바로 실행한다.
>
> 로컬 PC
> -> 내 컴퓨터의 터미널과 파이썬 설치 환경에서 실행한다.

따라서 이 절의 목적은 Colab 자체를 깊게 배우거나 로컬 설치법을 자세히 다루는 것이 아닙니다. 이후 Python/NumPy 실습을 따라가기 위해 “코드 셀에서 실행하는 명령”, “개인 PC 터미널에서 실행하는 명령”, “파이썬 코드 안에 쓰는 문장”을 구분하는 사전 안내입니다.

개인 PC에 파이썬을 설치하고 가상환경을 관리하는 방법은 뒤의 P2-7장과 보충학습 P2-7.6, P2-7.7, P2-7.8에서 다시 다룹니다. 여기서는 Colab과 로컬 PC의 실행 위치 차이를 먼저 잡습니다.

이 문서는 2026년 6월 24일 확인한 Google Colab 공식 안내와 FAQ를 기준으로 작성했습니다. Colab은 외부 서비스이므로 앞으로 UI, 사용 조건, 무료 제공 범위, 런타임 정책, 서비스 지속 여부가 바뀔 수 있습니다. 이 절을 읽는 시점에 Colab이 제공되지 않거나 안내와 다르게 보인다면, Google Colab 공식 문서와 현재 서비스 상태를 별도로 확인해야 합니다.

지금 읽는 층위는 `Python 설치와 개발환경 전체를 끝내는 절`이 아니라 `다음 NumPy 실습을 읽기 전에 실행 위치를 구분하는 입문 층위`입니다. 여기서 Colab 셀, 로컬 터미널, Python 코드의 자리를 구분해 두면, 뒤에서 `왜 같은 NumPy 준비 작업인데 명령이 다르게 보이는가`를 덜 헷갈리고 따라갈 수 있습니다.

처음 읽을 때는 설치 세부 절차를 다 외우기보다 `이 명령은 어디에서 실행하는가`만 먼저 구분하면 충분합니다.

| 지금 이 절에서 잡을 것 | 바로 다음에 이어질 질문 | 이후 다시 쓰이는 위치 |
| --- | --- | --- |
| Colab 셀, 로컬 터미널, Python 코드의 구분 | 다음 절에서 NumPy 배열 예제를 어느 자리에서 실행하는지 확인합니다. | Part 2의 이후 모든 Python 실습에서 설치 명령과 코드 문장을 구분할 때 다시 씁니다. |
| `%pip`, `python -m pip`, `import`의 역할 차이 | P2-3.5에서 실제 NumPy 배열과 shape를 실행해 봅니다. | P2-7의 가상환경, 패키지 설치, 터미널 보충학습으로 이어집니다. |
| Colab을 빠른 실습 공간으로 쓰는 이유 | 뒤 절에서 작은 예제를 바로 실행해 결과를 확인합니다. | Part 3 이후의 Pandas, Matplotlib, 모델 실습을 따라갈 때도 같은 실행 감각이 필요합니다. |

## 이 절의 범위

이 절은 다음 Python/NumPy 실습을 준비하기 위해 Colab과 로컬 PC의 실행 위치를 구분하고, 필요한 경우 NumPy를 설치하는 명령이 환경별로 어떻게 달라지는지만 다룹니다.

Colab의 파일 관리, Google Drive 연동, GPU/TPU 런타임, 노트북 공유 권한, 장시간 실행 제한은 다루지 않습니다. 로컬 PC의 파이썬 설치, 가상환경(virtual environment), 패키지 관리 세부 절차도 이 절에서 깊게 다루지 않습니다. 로컬 설치와 터미널, 가상환경 절차는 뒤의 P2-7장과 보충학습 P2-7.6, P2-7.7, P2-7.8에서 다시 정리합니다.

여기서는 다음 질문에 집중합니다.

> Colab은 무엇을 하기 위한 도구인가?
> 로컬 PC에서 실행한다는 말은 무엇인가?
> 코드 셀은 어떻게 실행하는가?
> %pip install numpy는 어디에서 쓰는 명령인가?
> 개인 PC 터미널 명령과 Colab 명령은 어떻게 다른가?

## 실행 환경을 먼저 구분한다

파이썬 코드를 실행한다는 말은 하나의 뜻만 갖지 않습니다. 같은 예제라도 어디에서 실행하는지에 따라 명령의 모양이 달라집니다.

| 실행 위치 | 영어 | 무엇을 뜻하는가 | 명령 예 |
| --- | --- | --- | --- |
| Colab 코드 셀 | Colab code cell | 브라우저 노트북 안의 코드 셀에서 실행한다. | `%pip install numpy` |
| 로컬 PC 터미널 | local terminal | 내 컴퓨터의 터미널 앱에서 실행한다. | `python -m pip install numpy` |
| 파이썬 코드 | Python code | `.py` 파일이나 코드 셀 안의 파이썬 문장으로 실행한다. | `import numpy as np` |

이 구분을 놓치면 `%pip`, `python -m pip`, `import`를 같은 것으로 오해하기 쉽습니다. 세 표현은 모두 NumPy와 관련될 수 있지만 실행 위치와 역할이 다릅니다.

> 패키지를 설치한다.
> -> Colab 코드 셀 또는 로컬 PC 터미널에서 한다.
>
> 설치된 패키지를 코드에서 불러온다.
> -> 파이썬 코드 안에서 import한다.

## 이 절의 목표

- Google Colab을 설치 없는 브라우저 기반 실행 환경으로 이해할 수 있습니다.
- 로컬 PC 실행을 내 컴퓨터의 터미널과 파이썬 설치 환경에서 실행하는 방식으로 이해할 수 있습니다.
- `Welcome to Colab` 안내서를 열어 코드 셀(code cell)을 실행해 볼 수 있습니다.
- Colab/Jupyter의 `%pip`가 일반 파이썬 문법이 아니라 매직 명령(magic command)임을 설명할 수 있습니다.
- Colab 코드 셀 명령과 개인 PC 터미널 명령을 구분할 수 있습니다.
- 다음 절의 NumPy 예제를 Colab에서 실행할 준비를 할 수 있습니다.

## 먼저 볼 세 가지

| 질문 | 먼저 잡을 관점 |
| --- | --- |
| Colab은 무엇인가? | 브라우저 안에서 Python 코드를 실행할 수 있는 실습 공간입니다. |
| 왜 여기서 먼저 소개하는가? | 로컬 설치 없이도 뒤의 Python 예제를 바로 실험해 볼 수 있기 때문입니다. |
| 무엇을 조심해야 하는가? | Colab 셀 명령과 로컬 터미널 명령은 같은 자리에 쓰지 않습니다. |

## Colab은 브라우저에서 여는 노트북 환경이다

Google Colab은 브라우저에서 Jupyter Notebook 형태로 파이썬 코드를 실행할 수 있는 hosted 서비스입니다. 개인 PC에 파이썬을 설치하지 않아도 코드 셀을 만들고 실행해 볼 수 있습니다.

- [Google Colab](https://colab.research.google.com/){: target="_blank" rel="noopener noreferrer" }
- [Welcome to Colab](https://colab.research.google.com/notebooks/intro.ipynb){: target="_blank" rel="noopener noreferrer" }
- [Google Colab FAQ](https://research.google.com/colaboratory/faq.html){: target="_blank" rel="noopener noreferrer" }

처음 사용할 때는 `Welcome to Colab` 안내서를 먼저 열어 코드 셀을 실행하는 방식을 확인합니다. 이 책의 예제는 매우 작기 때문에 GPU나 TPU는 필요하지 않습니다. 다만 Colab은 Google 계정, 런타임 제한, 자원 제한이 있을 수 있습니다.

## 로컬 PC는 내 컴퓨터에서 실행하는 환경이다

로컬 PC(local PC)에서 실행한다는 말은 내 컴퓨터에 설치된 파이썬과 터미널을 사용한다는 뜻입니다. macOS의 Terminal, Windows Terminal, PowerShell, Linux shell 같은 프로그램에서 명령을 실행합니다.

예를 들어 로컬 PC 터미널에서는 다음처럼 NumPy를 설치할 수 있습니다.

```bash
python -m pip install numpy
```

그리고 파이썬 파일 안에서는 다음처럼 NumPy를 불러옵니다.

문제 상황: 설치가 끝난 뒤 실제 Python 코드 안에서는 어떤 문장으로 NumPy를 불러오는지 확인합니다.
입력(input): NumPy를 `np`라는 별칭으로 import하는 코드입니다.
기대 출력(output): 출력은 없지만 이후 코드에서 `np`를 사용할 준비가 됩니다.
확인할 개념: 설치 명령과 import 문장은 역할이 다르며, import는 Python 코드 안에서 실행된다는 점을 봅니다.

```python
import numpy as np
```

이 절에서는 로컬 설치 과정을 자세히 다루지 않습니다. 설치 자체는 P2-7.7 보충학습에서, 터미널과 환경 변수 문법은 P2-7.6과 P2-7.8에서 다시 봅니다. 지금 필요한 것은 “Colab 코드 셀 명령과 로컬 PC 터미널 명령은 다르다”는 구분입니다.

## 코드 셀에 파이썬 코드를 넣는다

Colab 노트북에는 글을 쓰는 셀과 코드를 실행하는 셀이 있습니다. 파이썬 코드는 코드 셀(code cell)에 넣어 실행합니다.

예를 들어 다음 코드를 코드 셀에 넣고 실행할 수 있습니다.

문제 상황: Colab 코드 셀에서 가장 단순한 Python 코드가 어떻게 실행되는지 확인합니다.
입력(input): 문자열을 출력하는 `print` 문장입니다.
기대 출력(output): `hello, colab`이 화면에 출력됩니다.
확인할 개념: 코드 셀에는 터미널 명령이 아니라 일반 Python 문장을 넣어 실행할 수 있다는 점을 봅니다.

```python
print("hello, colab")
```

실행 결과는 다음처럼 나옵니다.

> hello, colab

이때 `print(...)`는 파이썬 코드입니다. 반면 패키지를 설치하는 명령은 일반 파이썬 코드와 성격이 조금 다릅니다.

## Colab에서는 `%pip`를 사용할 수 있다

Colab 환경에는 NumPy가 이미 준비되어 있는 경우가 많습니다. 하지만 환경이 달라질 수 있으므로 필요하면 코드 셀에서 다음 명령을 실행합니다.

문제 상황: Colab 코드 셀에서 NumPy 패키지를 준비해야 할 때 어떤 명령을 쓰는지 확인합니다.
입력(input): 노트북 환경의 매직 명령 `%pip install numpy`입니다.
기대 출력(output): 현재 노트북 커널에 NumPy가 설치됩니다.
확인할 개념: `%pip`는 일반 Python 문법이 아니라 Colab/Jupyter 코드 셀에서 쓰는 설치 명령이라는 점을 봅니다.

```python
%pip install numpy
```

여기서 `%pip`는 일반 파이썬 문법이 아니라 Jupyter Notebook 계열 환경에서 쓰는 매직 명령(magic command)입니다. 현재 노트북 커널(kernel)에 패키지를 설치하라는 뜻입니다.

Colab이나 Jupyter 문서에서는 셸 명령을 실행할 때 다음처럼 느낌표(`!`)를 붙인 예제도 볼 수 있습니다.

문제 상황: Colab 문서에서 자주 보이는 `!pip` 형태가 어떤 자리에서 쓰이는지 확인합니다.
입력(input): 코드 셀에서 셸 명령처럼 실행하는 `!pip install numpy` 예시입니다.
기대 출력(output): NumPy 설치 명령이 실행됩니다.
확인할 개념: `!pip`와 `%pip`는 모두 노트북 셀에서 쓰이지만, 이 책에서는 `%pip` 표기를 우선 사용한다는 점을 봅니다.

```python
!pip install numpy
```

이 책에서는 노트북 환경에 설치한다는 뜻이 더 분명한 `%pip install numpy`를 우선 사용합니다.

## 개인 PC 터미널 명령과 섞지 않는다

개인 PC의 터미널에서는 `%pip`나 `!pip`를 쓰지 않습니다. 이 표시는 Colab/Jupyter 코드 셀에서 쓰는 방식입니다.

개인 PC 터미널에서는 보통 다음처럼 실행합니다.

```bash
python -m pip install numpy
```

따라서 실행 위치를 먼저 구분합니다.

> Colab 코드 셀: %pip install numpy
> 개인 PC 터미널: python -m pip install numpy
> 파이썬 코드 안: import numpy as np

다음 절에서는 이 구분을 전제로 NumPy 코드를 확인합니다.

## 이 절에서 기억할 관점

Colab은 파이썬 설치 전에 코드를 먼저 실행해 볼 수 있는 브라우저 기반 환경입니다. 로컬 PC는 내 컴퓨터에 설치된 파이썬으로 실행하는 환경입니다. 두 환경은 모두 유용하지만, 명령을 쓰는 위치가 다릅니다.

> 코드 셀에서 실행하는가?
> 터미널에서 실행하는가?
> 파이썬 코드 안에서 import하는가?

이 세 가지를 구분하면 다음 절의 NumPy 실습을 덜 헷갈리게 읽을 수 있습니다.

## 사례로 보기

### 사례 1. 같은 설치 명령인데 왜 어떤 곳에서는 되고 어떤 곳에서는 안 될까

학습자가 NumPy를 설치하려고 할 때, Colab 코드 셀에 터미널 명령을 그대로 넣거나 반대로 개인 PC 터미널에 `%pip install numpy`를 쓰는 상황이 자주 생깁니다. 겉보기에는 모두 설치 명령처럼 보여도, 실제로는 실행 위치가 다르면 문법도 달라집니다.

예를 들어 Colab 코드 셀에서는 `%pip install numpy`가 자연스럽지만, 개인 PC 터미널에서는 `python -m pip install numpy`를 써야 합니다. 파이썬 코드 안에서는 설치가 아니라 `import numpy as np`로 불러옵니다. 즉 같은 NumPy 준비 작업도 `어디에서 실행하는가`에 따라 자리가 바뀝니다.

이 사례는 왜 환경 구분이 실습보다 먼저 나오는지를 보여 줍니다. 코드가 틀린 것이 아니라 실행 위치를 혼동해서 생기는 오류가 매우 많기 때문입니다.

따라서 뒤의 Python/NumPy 실습에서는 항상 먼저 묻습니다. `지금 나는 코드 셀에 있는가`, `터미널에 있는가`, `파이썬 코드 안에 있는가`. 이 질문이 잡혀야 설치, import, 실행 흐름이 한 번에 정리됩니다.

## 체크리스트

- Google Colab을 브라우저 기반 파이썬 실행 환경으로 설명할 수 있다.
- 로컬 PC 실행을 내 컴퓨터의 터미널과 파이썬 설치 환경에서 실행하는 방식으로 설명할 수 있다.
- `Welcome to Colab` 안내서를 열어 코드 셀을 실행해 볼 수 있다.
- `%pip install numpy`가 Colab/Jupyter 코드 셀에서 쓰는 매직 명령임을 설명할 수 있다.
- 개인 PC 터미널에서는 `python -m pip install numpy`를 사용한다는 점을 구분할 수 있다.
- 파이썬 코드에서는 `import numpy as np`로 NumPy를 불러온다는 점을 설명할 수 있다.

## 출처와 참고 자료

- Google, [Welcome to Colab](https://colab.research.google.com/notebooks/intro.ipynb){: target="_blank" rel="noopener noreferrer" }, 확인 날짜: 2026-06-24.
- Google, [Google Colab FAQ](https://research.google.com/colaboratory/faq.html){: target="_blank" rel="noopener noreferrer" }, 확인 날짜: 2026-06-24.
