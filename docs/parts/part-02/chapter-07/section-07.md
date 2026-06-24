# P2-7.7 보충학습: Python 설치는 언제 필요한가

P2-7.6에서는 Windows, macOS, Linux에서 터미널을 열고 현재 위치를 확인하는 방법을 봤습니다. 이제 남는 질문은 이것입니다.

내 컴퓨터에 Python을 꼭 설치해야 할까요?

처음부터 반드시 설치해야 하는 것은 아닙니다. 이 책의 초반 실습은 Colab 같은 브라우저 실행 환경으로도 따라갈 수 있습니다. 하지만 어느 시점부터는 로컬 PC(local PC)에 Python을 설치하고, 가상환경(virtual environment)을 만들고, 패키지(package)를 직접 관리해야 하는 이유가 생깁니다.

이 절은 설치 버튼을 하나씩 따라 누르는 안내서가 아닙니다. 운영체제별 화면은 계속 바뀔 수 있고, Python 배포 방식도 시간이 지나며 바뀔 수 있습니다. 이 절의 목적은 “언제 설치가 필요한지”, “설치 뒤 무엇을 확인해야 하는지”, “설치와 가상환경을 어떻게 구분해야 하는지”를 판단하게 만드는 것입니다.

## 공식 설치 매뉴얼 링크

링크 수집일: 2026-06-24

설치 화면과 권장 방식은 시간이 지나며 바뀔 수 있습니다. 실제 설치를 진행할 때는 이 절의 설명만 보지 말고, 아래 공식 문서를 함께 확인합니다.

- 전체 설치와 사용 안내: Python Software Foundation, [Python Setup and Usage](https://docs.python.org/3/using/index.html){: target="_blank" rel="noopener noreferrer" }.
- 다운로드 페이지: Python Software Foundation, [Download Python](https://www.python.org/downloads/){: target="_blank" rel="noopener noreferrer" }.
- Windows 설치와 실행: Python Software Foundation, [Using Python on Windows](https://docs.python.org/3/using/windows.html){: target="_blank" rel="noopener noreferrer" }.
- macOS 설치와 실행: Python Software Foundation, [Using Python on macOS](https://docs.python.org/3/using/mac.html){: target="_blank" rel="noopener noreferrer" }.
- Linux/Unix 계열 사용: Python Software Foundation, [Using Python on Unix platforms](https://docs.python.org/3/using/unix.html){: target="_blank" rel="noopener noreferrer" }.
- 가상환경: Python Software Foundation, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html){: target="_blank" rel="noopener noreferrer" }.

## 이 절의 범위

이 절은 Python 설치의 필요성과 확인 기준을 다룹니다.

여기서는 다음 질문에 답합니다.

- Colab만으로 충분한 단계는 언제인가?
- 로컬 PC에 Python 설치가 필요한 단계는 언제인가?
- Windows, macOS, Linux에서 설치 방식은 왜 다르게 보이는가?
- 설치 뒤 어떤 명령으로 확인해야 하는가?
- Python 설치와 가상환경 생성은 어떻게 다른가?
- 설치가 꼬였을 때 무엇을 먼저 확인해야 하는가?

이 절은 운영체제별 설치 화면을 길게 따라 하지 않습니다. 특정 버전 설치, PATH 문제 해결, Windows Store와 python.org 설치 방식 비교, Homebrew, pyenv, conda, Docker, WSL 설정은 깊게 다루지 않습니다. 그런 내용은 실제 프로젝트 환경을 만들 때 다시 다루는 편이 안전합니다.

## 이 절의 목표

- Colab과 로컬 Python 설치의 역할 차이를 설명할 수 있습니다.
- 로컬 설치가 필요한 시점을 판단할 수 있습니다.
- 설치 뒤 `python --version`, `python3 --version`, `py --version`으로 확인해야 함을 설명할 수 있습니다.
- Python 설치와 가상환경 생성이 같은 일이 아님을 설명할 수 있습니다.
- 운영체제별 설치 안내는 작성 시점에 공식 문서를 다시 확인해야 함을 설명할 수 있습니다.

## 처음에는 Colab으로 충분할 수 있다

초반 학습에서는 Colab으로 충분한 경우가 많습니다.

- 간단한 Python 코드 실행
- NumPy 배열 계산 확인
- 작은 표 데이터 다루기
- 그래프를 빠르게 그려 보기
- 책의 예제 코드를 셀 단위로 따라 하기

Colab은 브라우저에서 실행되므로 Python 설치 문제를 뒤로 미룰 수 있습니다. 초심자에게는 이것이 큰 장점입니다. 설치, PATH, 운영체제 권한, 터미널 차이를 만나기 전에 “코드가 실행된다”는 감각을 먼저 만들 수 있기 때문입니다.

하지만 Colab은 내 컴퓨터가 아닙니다. 런타임(runtime)은 외부 서비스가 제공하고, 세션이 초기화될 수 있으며, 파일과 패키지 상태가 계속 유지된다고 보장하기 어렵습니다. 그래서 학습이 다음 단계로 넘어가면 로컬 설치의 필요성이 커집니다.

## 로컬 설치가 필요해지는 시점

로컬 PC에 Python을 설치해야 하는 시점은 “Python을 배우기 시작하는 첫날”이 아니라, 실행 환경을 직접 관리해야 할 때입니다.

예를 들어 다음 상황에서는 로컬 설치가 필요해질 수 있습니다.

- `.py` 파일을 내 컴퓨터에서 직접 실행해야 한다.
- 프로젝트 폴더 안에서 여러 파일을 함께 관리해야 한다.
- 데이터 파일을 로컬 폴더에서 읽고 써야 한다.
- Git으로 받은 예제 프로젝트를 실행해야 한다.
- 가상환경을 만들고 프로젝트별 패키지를 분리해야 한다.
- 인터넷 연결이나 Colab 런타임 상태에 덜 의존하고 싶다.
- 에디터, 터미널, 테스트 도구, 문서 빌드 도구를 함께 사용해야 한다.

반대로 다음 단계에서는 아직 Colab으로 충분할 수 있습니다.

- 한두 줄 계산을 확인한다.
- 작은 코드 셀을 실행한다.
- 설치보다 개념 이해가 목적이다.
- 결과를 저장하거나 프로젝트 구조를 관리할 필요가 없다.

따라서 이 책에서는 먼저 Colab으로 실행 감각을 만들고, 이후 로컬 PC에서 프로젝트 단위 실습을 할 때 Python 설치를 본격적으로 생각합니다.

## 설치는 Python 인터프리터를 준비하는 일이다

Python 설치는 Python 인터프리터(Python interpreter)를 내 컴퓨터에 준비하는 일입니다. Python 공식 문서는 플랫폼별 Python 환경 설정, 인터프리터 실행, 작업을 쉽게 만드는 정보를 따로 안내합니다.

설치를 했다는 말은 보통 다음이 가능해졌다는 뜻입니다.

- 터미널에서 Python 명령을 실행할 수 있다.
- `.py` 파일을 Python으로 실행할 수 있다.
- `pip`를 통해 패키지를 설치할 수 있다.
- 가상환경을 만들 수 있다.

하지만 설치만으로 모든 것이 끝나지는 않습니다.

Python을 설치했더라도 다음 문제가 남을 수 있습니다.

- 터미널에서 `python` 명령이 동작하지 않을 수 있습니다.
- macOS/Linux에서는 `python3` 명령을 써야 할 수 있습니다.
- Windows에서는 `py` 명령을 만날 수 있습니다.
- 여러 버전의 Python이 설치되어 있을 수 있습니다.
- 가상환경을 쓰지 않으면 프로젝트별 패키지가 섞일 수 있습니다.

그래서 설치 직후에는 “설치했다”보다 “어떤 명령이 어떤 Python을 가리키는가”를 확인해야 합니다.

## 설치 뒤에는 버전을 먼저 확인한다

터미널에서 다음 명령을 확인합니다.

```bash
python --version
```

macOS나 Linux에서는 다음 명령이 더 자연스러울 수 있습니다.

```bash
python3 --version
```

Windows에서는 Python 설치 방식에 따라 다음 명령을 만날 수 있습니다.

```powershell
py --version
```

이 중 하나가 동작한다고 해서 나머지가 반드시 동작한다는 뜻은 아닙니다. 중요한 것은 내 환경에서 어떤 명령이 Python 인터프리터를 실행하는지 확인하는 것입니다.

다음 질문을 남깁니다.

- `python`은 실행되는가?
- `python3`는 실행되는가?
- Windows라면 `py`는 실행되는가?
- 출력되는 버전은 책의 예제와 크게 다르지 않은가?
- 가상환경을 켠 뒤에도 같은 명령이 같은 Python을 가리키는가?

초심자는 여기서 막힐 수 있습니다. 이때 Python 코드를 고치기 전에 설치와 명령 연결 문제를 먼저 의심해야 합니다.

## Windows에서는 Python Install Manager를 만날 수 있다

Python 공식 Windows 문서는 Windows가 대부분의 Unix 시스템과 달리 시스템이 지원하는 Python 설치를 포함하지 않는다고 설명합니다. Python은 여러 배포처에서 얻을 수 있으며, CPython 팀의 배포판을 쓰려면 Python Install Manager를 사용할 수 있다고 안내합니다.

입문 단계에서는 다음 정도만 기억합니다.

- Windows에는 기본으로 믿고 쓸 수 있는 시스템 Python이 없을 수 있습니다.
- Python은 python.org 다운로드 페이지나 Microsoft Store를 통해 설치할 수 있습니다.
- 설치 뒤 `python`, `py` 명령이 동작하는지 확인합니다.
- 공식 문서는 프로젝트마다 가상환경을 만들 것을 권장합니다.

Windows에서 자주 생기는 문제는 “설치는 했는데 터미널에서 명령을 찾지 못한다”입니다. 이 경우 Python 코드의 문제가 아니라 설치 경로 또는 PATH 설정 문제일 수 있습니다. 이 절에서는 PATH를 직접 수정하는 절차까지 다루지 않습니다. 그런 문제가 생기면 공식 문서의 Troubleshooting을 확인하거나, 설치 방식을 다시 점검합니다.

## macOS에서는 python.org 설치와 다른 배포판을 구분한다

Python 공식 macOS 문서는 macOS에서 Python을 얻고 설치하는 방법이 여러 가지이며, python.org에서 제공하는 설치 패키지와 다른 배포판이 있을 수 있다고 설명합니다. 현재 지원되는 Python 버전은 python.org에서 macOS 설치 패키지를 제공합니다.

입문 단계에서는 다음 정도만 기억합니다.

- macOS에는 시스템 도구가 쓰는 Python 관련 구성요소가 있을 수 있으므로, 무작정 시스템 영역을 바꾸지 않습니다.
- 학습용 Python은 python.org 설치 패키지나 잘 알려진 배포 방식을 사용합니다.
- 터미널에서는 `python3 --version`을 먼저 확인하는 경우가 많습니다.
- 설치 뒤에도 프로젝트 실습은 가상환경으로 분리하는 편이 안전합니다.

macOS 문서는 터미널에서 스크립트를 실행하는 방법과 Finder에서 실행하는 방법이 다를 수 있음을 안내합니다. 초심자에게는 터미널에서 현재 폴더를 확인하고 실행하는 방식이 더 투명합니다.

## Linux에서는 이미 설치되어 있을 수 있다

Python 공식 Unix 플랫폼 문서는 Python이 대부분의 Linux 배포판에 미리 설치되어 있고, 그렇지 않은 경우에도 패키지로 제공된다고 설명합니다.

입문 단계에서는 다음 정도만 기억합니다.

- Linux에서는 `python3 --version`이 이미 동작할 수 있습니다.
- 배포판의 패키지 관리자에서 Python을 관리하는 경우가 많습니다.
- 시스템 Python은 운영체제 도구가 사용할 수 있으므로 함부로 지우거나 바꾸지 않습니다.
- 프로젝트 실습은 가상환경을 만들어 분리하는 편이 안전합니다.

Linux 자료에서 `sudo apt install python3` 같은 명령을 볼 수 있습니다. 하지만 배포판마다 패키지 관리자와 패키지 이름이 다를 수 있습니다. 따라서 Linux 설치 명령은 자신의 배포판 공식 문서를 기준으로 확인해야 합니다.

## Python 설치와 가상환경 생성은 다르다

Python 설치와 가상환경 생성은 같은 일이 아닙니다.

| 구분 | 무엇을 하는가 | 예시 |
| --- | --- | --- |
| Python 설치 | 컴퓨터에 Python 인터프리터를 준비한다 | python.org 설치, OS 패키지 설치 |
| 가상환경 생성 | 특정 프로젝트용 Python 실행 공간을 만든다 | `python -m venv .venv` |
| 패키지 설치 | 그 환경에 외부 패키지를 준비한다 | `python -m pip install numpy` |

Python 공식 `venv` 문서는 가상환경을 활성화하면 해당 환경의 Python 인터프리터가 실행되도록 경로가 앞에 붙는다고 설명합니다. 또 가상환경은 필요하면 다시 만들 수 있어야 하며, `requirements.txt` 같은 기록을 사용해 패키지를 다시 설치할 수 있어야 한다고 경고합니다.

입문 단계에서는 다음 흐름으로 이해합니다.

1. Python을 설치한다.
2. 프로젝트 폴더로 이동한다.
3. 가상환경을 만든다.
4. 가상환경을 활성화한다.
5. 필요한 패키지를 설치한다.
6. Python 코드를 실행한다.

이 절에서는 4번의 운영체제별 활성화 명령을 외우게 하지 않습니다. 활성화 명령은 Windows, macOS, Linux, 셸 종류에 따라 다르게 보일 수 있습니다. 지금은 “설치한 Python 하나를 모든 프로젝트가 같이 쓰지 않고, 프로젝트별 환경을 만든다”는 방향을 기억합니다.

## 설치가 꼬였을 때 먼저 확인할 것

Python 설치가 꼬였을 때는 바로 재설치부터 하지 않습니다. 먼저 확인합니다.

- 지금 어느 터미널을 열었는가?
- 현재 작업 폴더는 어디인가?
- `python --version`은 동작하는가?
- `python3 --version`은 동작하는가?
- Windows라면 `py --version`은 동작하는가?
- 여러 Python 버전이 설치되어 있지는 않은가?
- 가상환경을 켠 상태인가?
- 패키지를 설치한 Python과 코드를 실행하는 Python이 같은가?

특히 다음 상황은 흔합니다.

- 시스템 Python에는 패키지를 설치했지만, 가상환경 Python으로 실행하고 있다.
- 가상환경에 패키지를 설치했지만, 가상환경을 끄고 실행하고 있다.
- Colab에서 설치한 패키지를 로컬 PC에도 설치된 것으로 착각한다.
- Windows에서 `python`은 동작하지 않지만 `py`는 동작한다.
- macOS/Linux에서 `python`은 없거나 Python 2를 가리키고, `python3`가 실제 Python 3을 가리킨다.

오류 메시지를 볼 때는 “Python 코드 오류”와 “실행 환경 오류”를 나누어 보는 습관이 필요합니다.

## 이 절에서 기억할 관점

Python 설치는 학습의 시작점이 아니라 실행 환경을 직접 관리하기 위한 준비입니다.

처음에는 Colab으로도 충분할 수 있습니다. 하지만 프로젝트 폴더, 데이터 파일, 가상환경, 패키지 버전, 재현성을 직접 관리해야 할 때는 로컬 설치가 필요해집니다.

설치 뒤에는 다음 질문을 먼저 확인합니다.

1. 내 터미널에서 Python은 어떤 명령으로 실행되는가?
2. 그 명령은 어떤 버전의 Python을 가리키는가?
3. 프로젝트별 가상환경을 만들 준비가 되어 있는가?
4. 패키지를 설치한 환경과 코드를 실행하는 환경이 같은가?

## 체크리스트

- Colab으로 충분한 학습 단계와 로컬 설치가 필요한 단계를 구분할 수 있다.
- Python 설치가 Python 인터프리터를 컴퓨터에 준비하는 일임을 설명할 수 있다.
- `python --version`, `python3 --version`, `py --version`의 목적을 설명할 수 있다.
- Windows, macOS, Linux에서 Python 설치 방식이 다르게 보일 수 있음을 설명할 수 있다.
- Python 설치, 가상환경 생성, 패키지 설치를 구분할 수 있다.
- 설치 오류가 났을 때 코드보다 실행 환경을 먼저 확인해야 함을 설명할 수 있다.

## 출처와 참고 자료

- Python Software Foundation, [Python Setup and Usage](https://docs.python.org/3/using/index.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-06-24.
- Python Software Foundation, [Download Python](https://www.python.org/downloads/){: target="_blank" rel="noopener noreferrer" }, Python.org, 확인 날짜: 2026-06-24.
- Python Software Foundation, [Using Python on Windows](https://docs.python.org/3/using/windows.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-06-24.
- Python Software Foundation, [Using Python on macOS](https://docs.python.org/3/using/mac.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-06-24.
- Python Software Foundation, [Using Python on Unix platforms](https://docs.python.org/3/using/unix.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-06-24.
- Python Software Foundation, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-06-24.
