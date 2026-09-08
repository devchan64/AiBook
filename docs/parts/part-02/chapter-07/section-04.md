# P2-7.4 가상환경(virtual environment)과 패키지(package)

> Section ID: `P2-7.4`
> Version: `v2026.09.08`

가상환경(virtual environment)은 프로젝트마다 별도의 Python 패키지 집합을 갖게 합니다. 패키지를 설치한 Python과 코드를 실행하는 Python이 다르면 설치가 성공해도 `import`가 실패할 수 있습니다.

| 용어 | 뜻 |
| --- | --- |
| 가상환경(virtual environment) | 프로젝트별로 분리한 Python 실행 공간입니다. |
| 패키지(package) | Python에서 가져다 쓰는 코드 묶음입니다. |
| `pip` | 패키지를 설치하는 도구입니다. |
| `import` | 이미 준비된 패키지를 Python 코드 안에서 불러오는 문장입니다. |
| `.venv` | 프로젝트 폴더 안에 두는 대표적인 로컬 가상환경 디렉터리 이름입니다. |

## 프로젝트 분리와 설치 위치

| 기준 | 왜 중요한가 |
| --- | --- |
| 가상환경은 프로젝트별 Python 실행 공간이다 | 프로젝트마다 필요한 도구 버전이 다를 수 있기 때문이다 |
| 설치와 `import`는 서로 다른 단계다 | 설치는 준비이고 `import`는 코드 안에서 실제로 불러오는 일이다 |
| 가장 흔한 실수는 설치한 환경과 실행한 환경이 다른 경우다 | 같은 컴퓨터 안에도 여러 Python 공간이 있을 수 있다 |

## venv가 도입된 배경

PEP 405는 Python 표준 라이브러리에 `venv`를 추가하기 위한 제안입니다. 이 문서는 2011년에 만들어졌고, Python 3.3을 대상으로 했습니다. PEP 405의 동기(motivation)는 이미 `virtualenv` 같은 서드파티 가상환경 도구가 의존성 관리(dependency management), 격리(isolation), 시스템 관리자 권한 없이 패키지를 설치하고 사용하는 일, 여러 Python 버전에서 자동 테스트하는 일 등에 널리 쓰이고 있었다고 설명합니다.

이 배경을 입문자 관점으로 줄이면 다음과 같습니다.

- Python 패키지가 많아졌다: 프로젝트마다 필요한 외부 코드가 달라졌습니다.
- 시스템 Python을 함부로 바꾸기 어려웠다: 운영체제나 다른 프로그램이 쓰는 Python 환경을 깨뜨릴 수 있었습니다.
- 관리자 권한 없이 설치해야 하는 경우가 많았다: 개인 프로젝트나 서버 계정에서 자유롭게 시스템 전체를 바꿀 수 없었습니다.
- 여러 프로젝트와 Python 버전을 시험해야 했다: 하나의 전역 설치 공간만으로는 충돌을 피하기 어려웠습니다.

## 프로젝트별 패키지 버전

프로젝트에 따라 필요한 패키지 버전이 다를 수 있습니다.

- 프로젝트 A는 `numpy 1.x` 기준으로 작성되었습니다.
- 프로젝트 B는 `numpy 2.x` 기준으로 작성되었습니다.
- 둘을 같은 공간에 섞으면 어느 한쪽이 깨질 수 있습니다.

가상환경(virtual environment)은 이런 충돌을 줄이기 위해 프로젝트별로 Python 실행 공간을 나누는 방법입니다. Python 공식 문서는 `venv`가 가벼운 가상환경을 만들며, 각 가상환경은 독립된 Python 패키지 집합을 가질 수 있다고 설명합니다.

- 프로젝트 A의 가상환경: 프로젝트 A에 필요한 패키지를 설치합니다.
- 프로젝트 B의 가상환경: 프로젝트 B에 필요한 패키지를 따로 설치합니다.

## 가상환경과 공유할 파일

가상환경은 프로젝트를 실행하기 위한 주변 환경입니다. 프로젝트의 원고나 코드 자체와는 다릅니다.

예를 들어 어떤 프로젝트 폴더 안에서 `.venv`라는 폴더를 볼 수 있습니다. 이 폴더는 Python 실행이나 문서 빌드에 필요한 패키지를 담는 로컬 실행 환경입니다. 프로젝트의 본문 파일이나 코드 자체는 아닙니다.

그래서 보통 가상환경 폴더는 Git에 커밋하지 않습니다. Python 공식 문서도 가상환경은 보통 프로젝트 디렉터리 안의 `.venv` 같은 이름으로 만들 수 있고, 소스 관리 시스템에는 넣지 않는다고 설명합니다.

그래서 보통 다음처럼 나눕니다.

- 커밋할 것: 원고, 코드, 설정 파일, 예제 파일
- 커밋하지 않을 것: 내 컴퓨터에서 만든 가상환경 폴더

가상환경 자체를 공유하는 대신, 어떤 패키지가 필요한지 기록하고 다시 설치할 수 있게 만드는 방향이 더 안전합니다.

## Python 패키지

패키지(package)는 Python에서 가져다 쓸 수 있도록 배포되는 코드 묶음입니다. NumPy, Pandas, Matplotlib 같은 도구가 여기에 해당합니다.

여기서도 세 층을 구분해 둡니다.

- Python: 언어와 실행 프로그램입니다.
- 패키지: Python에서 가져다 쓰는 코드 묶음입니다.
- 패키지 저장소: 패키지를 내려받을 수 있는 곳입니다.

Python Packaging User Guide는 `pip`와 `venv`를 사용해 가상환경 안에 패키지를 설치하는 흐름을 안내합니다. 여기서 중요한 것은 패키지를 설치하는 일과 코드에서 불러오는 일이 다르다는 점입니다.

## pip 설치와 import

다음 명령은 패키지를 설치하는 터미널 명령입니다.

```bash
python -m pip install numpy
```

이 명령은 Python 코드 파일 안에 쓰는 문장이 아닙니다. 터미널에서 실행하는 명령입니다. `python -m`은 지정한 Python으로 모듈을 실행합니다. 이 명령에서는 pip를 실행해 NumPy를 설치합니다.

반면 다음은 Python 코드입니다.

NumPy가 설치된 Python에서 `import numpy as np`를 실행하면 별도 출력 없이 `np`라는 이름으로 NumPy를 사용할 수 있습니다.

```python
# 현재 환경에 설치된 NumPy 패키지를 Python 코드에서 불러옵니다.
import numpy as np
```

이 코드는 이미 설치된 NumPy를 현재 Python 코드에서 사용하겠다고 불러오는 문장입니다.

두 문장을 섞으면 안 됩니다.

| 목적 | 예시 | 입력 위치 |
| --- | --- | --- |
| 패키지 설치 | `python -m pip install numpy` | 터미널 |
| 패키지 사용 | `import numpy as np` | Python 코드 |

## 설치 환경과 실행 환경

입문자가 자주 만나는 오류는 `분명히 설치했는데 Python에서는 없다고 한다`는 상황입니다.

이럴 때는 “어디에 설치했는가”와 “어디에서 실행하는가”를 나누어 봐야 합니다.

예를 들어 다음처럼 설치한 곳과 실행한 곳이 어긋날 수 있습니다.

- 시스템 Python에 설치했지만 가상환경 Python으로 실행하고 있습니다.
- 가상환경 A에 설치했지만 가상환경 B에서 실행하고 있습니다.
- Colab에 설치했지만 로컬 PC에서 실행하고 있습니다.

패키지는 추상적으로 “컴퓨터 어딘가”에 설치되는 것이 아닙니다. 특정 Python 실행 환경에 설치됩니다. 그래서 가상환경을 사용하면 패키지를 설치할 때도, 코드를 실행할 때도 같은 가상환경을 기준으로 해야 합니다.

## 가상환경의 Python으로 설치·실행

프로젝트 폴더에서 가상환경을 만든 뒤, 그 안의 Python 경로를 직접 지정해 패키지를 설치하고 불러올 수 있습니다. 이 방식은 활성화 여부에 의존하지 않습니다.

macOS/Linux 터미널에서는 다음 명령을 순서대로 실행합니다. `python3`가 설치되어 있어야 합니다.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install numpy
.venv/bin/python -c "import numpy; print(numpy.__version__)"
```

Windows PowerShell에서 `python` 명령으로 Python을 실행할 수 있다면 다음과 같이 사용합니다.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install numpy
.\.venv\Scripts\python.exe -c "import numpy; print(numpy.__version__)"
```

첫 명령은 `.venv`를 만들고, 두 번째 명령은 그 환경에 NumPy를 설치합니다. 마지막 명령의 `-c`는 뒤 문자열을 Python 코드로 실행하는 옵션이며, 설치된 NumPy 버전이 출력됩니다.

`.venv`를 만들기만 한 뒤 일반 `python -m pip install numpy`를 실행하면 새 환경이 아닌 다른 Python에 설치할 수 있습니다. 활성화(activate)를 사용하는 방법도 있지만, 위처럼 실행 파일 경로를 직접 지정하면 어느 환경을 사용하는지 명령에서 확인할 수 있습니다.

## Colab 런타임의 패키지

Colab은 브라우저에서 코드를 편집하고 런타임에서 실행하는 노트북 환경입니다. 호스팅 런타임을 사용하면 로컬에 Python을 설치하지 않아도 실행할 수 있습니다.

하지만 Colab에서도 패키지 설치와 실행 환경 문제는 사라지지 않습니다.

Colab 코드 셀의 `%pip`는 현재 노트북 커널에 패키지를 설치합니다. 다음 셀을 실행하면 해당 환경에 NumPy가 준비됩니다.

```python
# Colab/Jupyter 코드 셀에서 현재 런타임에 NumPy를 설치하는 명령입니다.
%pip install numpy
```

이 명령은 현재 노트북 런타임에 패키지를 설치합니다. 런타임이 초기화되면 설치한 패키지를 다시 설치해야 할 수 있습니다. 또한 로컬 PC의 `.venv`와 Colab 런타임은 같은 공간이 아닙니다.

정리하면 두 공간은 다릅니다.

- Colab 런타임: 브라우저 밖의 외부 실행 환경입니다.
- 로컬 가상환경: 내 컴퓨터 프로젝트 폴더 주변의 실행 환경입니다.

## 같은 폴더 이름, 다른 환경

두 프로젝트에 각각 `.venv`가 있다고 가정합니다.

```text
project-a/.venv/
project-b/.venv/
```

`project-a/.venv`의 Python에 NumPy를 설치해도 `project-b/.venv`에는 자동으로 설치되지 않습니다. 두 환경이 기본 설정으로 만들어졌고 B에는 NumPy가 없다면, B의 Python에서 `import numpy`를 실행할 때 `ModuleNotFoundError`가 납니다.

폴더 이름이 모두 `.venv`여도 전체 경로가 다르면 별개의 환경입니다. `sys.executable`로 출력한 Python 경로와 설치 명령에 사용한 경로를 비교하면 어느 프로젝트 환경에 설치했는지 확인할 수 있습니다.

## 체크리스트

- 가상환경(virtual environment)을 프로젝트별 Python 실행 공간으로 설명할 수 있다.
- 가상환경 폴더가 프로젝트 원고나 코드 자체가 아니라 실행 환경임을 설명할 수 있다.
- 패키지(package)를 Python에서 가져다 쓰는 코드 묶음으로 설명할 수 있다.
- `pip`가 패키지를 설치하는 도구라는 점을 설명할 수 있다.
- `python -m pip install numpy`는 터미널 명령이고, `import numpy as np`는 Python 코드라는 점을 구분할 수 있다.
- 패키지는 특정 Python 실행 환경에 설치된다는 점을 설명할 수 있다.
- Colab 런타임과 로컬 가상환경이 같은 공간이 아니라는 점을 설명할 수 있다.
- `지금 어떤 Python 환경을 쓰고 있는가`, `필요한 패키지는 그 환경에 설치되어 있는가`, `설치 명령과 Python 코드 실행이 같은 환경을 보고 있는가`를 점검할 수 있다.

## 출처와 참고 자료

- Carl Meyer, [PEP 405 – Python Virtual Environments](https://peps.python.org/pep-0405/){: target="_blank" rel="noopener noreferrer" }, Python Enhancement Proposals, 확인 날짜: 2026-07-20. 가상환경이 독립된 패키지 집합과 자체 Python 실행 파일을 갖고 시스템 site-packages와 격리될 수 있다는 설계 근거로 사용했다.
- Python Software Foundation, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, 확인 날짜: 2026-09-08. `venv`로 가상환경을 만들고 활성화하며, 환경 안에 Python과 패키지 상태가 분리된다는 설명 확인에 사용했다.
- Python Packaging Authority, [Install packages in a virtual environment using pip and venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/){: target="_blank" rel="noopener noreferrer" }, Python Packaging User Guide, 확인 날짜: 2026-07-20. 프로젝트별 가상환경 생성과 `python -m pip install`을 통한 패키지 설치 흐름 확인에 사용했다.
- Python Software Foundation, [Installing Python Modules](https://docs.python.org/3/installing/index.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. `pip`, `venv`, PyPI, `python -m pip install`의 기본 역할과 시스템 설치 대신 가상환경을 우선 고려해야 하는 맥락 확인에 사용했다.
