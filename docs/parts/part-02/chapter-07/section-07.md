# P2-7.7 보충학습: Python 설치는 언제 필요한가

> Section ID: `P2-7.7`
> Version: `v2026.09.08`

Colab의 호스팅 런타임에서 실행할 때는 내 컴퓨터에 Python이 없어도 됩니다. 내 컴퓨터에서 `.py` 파일을 실행하거나 로컬 파일을 Python으로 처리하려면 로컬 인터프리터가 필요합니다. 이미 설치되어 있을 수 있으므로 먼저 실행 명령과 버전을 확인합니다.

## 공식 설치 매뉴얼 링크

링크 수집일: 2026-07-20

설치 화면과 권장 방식은 시간이 지나며 바뀔 수 있습니다. 실제 설치를 진행할 때는 이 절의 설명만 보지 말고, 아래 공식 문서를 함께 확인합니다.

- 전체 설치와 사용 안내: Python Software Foundation, [Python Setup and Usage](https://docs.python.org/3/using/index.html){: target="_blank" rel="noopener noreferrer" }.
- 다운로드 페이지: Python Software Foundation, [Download Python](https://www.python.org/downloads/){: target="_blank" rel="noopener noreferrer" }.
- Windows 설치와 실행: Python Software Foundation, [Using Python on Windows](https://docs.python.org/3/using/windows.html){: target="_blank" rel="noopener noreferrer" }.
- macOS 설치와 실행: Python Software Foundation, [Using Python on macOS](https://docs.python.org/3/using/mac.html){: target="_blank" rel="noopener noreferrer" }.
- Linux/Unix 계열 사용: Python Software Foundation, [Using Python on Unix platforms](https://docs.python.org/3/using/unix.html){: target="_blank" rel="noopener noreferrer" }.
- 가상환경: Python Software Foundation, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html){: target="_blank" rel="noopener noreferrer" }.

## 실행 위치와 설치 여부

| 기준 | 왜 중요한가 |
| --- | --- |
| 처음부터 로컬 설치가 꼭 필요한 것은 아니다 | 작은 실습은 Colab만으로도 시작할 수 있기 때문이다 |
| 로컬 설치는 내 컴퓨터에서 Python 인터프리터를 실행할 기반을 만드는 일이다 | 설치와 가상환경, 패키지 준비를 한 덩어리로 보면 판단이 흐려진다 |
| 설치 뒤 가장 먼저 확인할 것은 버전과 실행 명령이다 | 설치 성공과 명령 연결 성공은 같은 일이 아니다 |

## Colab 호스팅 런타임

초반 학습에서는 Colab으로 충분한 경우가 많습니다.

- 간단한 Python 코드 실행
- NumPy 배열 계산 확인
- 작은 표 데이터 다루기
- 그래프를 빠르게 그려 보기
- 책의 예제 코드를 셀 단위로 따라 하기

브라우저는 코드 입력과 결과 표시를 맡고, 호스팅 런타임이 Python 코드를 실행합니다. 로컬 Python 설치 없이 위 작업을 할 수 있습니다.

하지만 Colab은 내 컴퓨터가 아닙니다. 런타임(runtime)은 외부 서비스가 제공하고, 세션이 초기화될 수 있으며, 파일과 패키지 상태가 계속 유지된다고 보장하기 어렵습니다.

## 로컬 인터프리터가 필요한 작업

다음 작업을 내 컴퓨터에서 실행하려면 로컬 Python이 필요합니다.

- `.py` 파일을 터미널이나 편집기에서 실행한다.
- 로컬 데이터 파일을 읽고 결과를 같은 컴퓨터에 저장한다.
- 프로젝트별 가상환경을 만들고 패키지를 관리한다.
- 인터넷 연결 없이 Python 계산을 실행한다.

여러 파일로 된 프로젝트나 Git 저장소라는 이유만으로 반드시 로컬에서 실행해야 하는 것은 아닙니다. 원격 실행 환경에서도 프로젝트와 패키지를 관리할 수 있습니다. 설치 여부를 가르는 조건은 파일 수보다 실제로 코드를 실행할 위치입니다.

## Python 설치와 명령 연결

Python 설치는 Python 인터프리터(Python interpreter)를 내 컴퓨터에 준비하는 일입니다. Python 공식 문서는 플랫폼별 Python 환경 설정, 인터프리터 실행, 작업을 쉽게 만드는 정보를 따로 안내합니다.

설치와 명령 연결, 필요한 구성요소 준비가 끝나면 다음 작업을 할 수 있습니다.

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

## 명령별 Python 버전 확인

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

버전이 출력되지 않으면 코드보다 설치 상태와 명령 연결을 확인합니다. 서로 다른 명령에서 다른 버전이 출력될 수도 있으므로 프로젝트에서 사용할 Python을 정해야 합니다.

## Windows 설치 경로

Python 공식 Windows 문서는 Windows가 대부분의 Unix 시스템과 달리 시스템이 지원하는 Python 설치를 포함하지 않는다고 설명합니다. Python은 여러 배포처에서 얻을 수 있으며, CPython 팀의 배포판을 쓰려면 Python Install Manager를 사용할 수 있다고 안내합니다.

설치와 실행에서 확인할 사항은 다음과 같습니다.

- Windows에는 기본으로 믿고 쓸 수 있는 시스템 Python이 없을 수 있습니다.
- Python은 python.org 다운로드 페이지나 Microsoft Store를 통해 설치할 수 있습니다.
- 설치 뒤 `python`, `py` 명령이 동작하는지 확인합니다.
- 공식 문서는 프로젝트마다 가상환경을 만들 것을 권장합니다.

설치했는데 명령을 찾지 못한다면 설치 경로, 실행 별칭, PATH 설정을 확인합니다. 설치 방식에 따른 점검 항목은 위 공식 Windows 문서의 Troubleshooting에 나와 있습니다.

## macOS 설치 경로

Python 공식 macOS 문서는 macOS에서 Python을 얻고 설치하는 방법이 여러 가지이며, python.org에서 제공하는 설치 패키지와 다른 배포판이 있을 수 있다고 설명합니다. 현재 지원되는 Python 버전은 python.org에서 macOS 설치 패키지를 제공합니다.

설치와 실행에서 확인할 사항은 다음과 같습니다.

- macOS에는 시스템 도구가 쓰는 Python 관련 구성요소가 있을 수 있으므로, 무작정 시스템 영역을 바꾸지 않습니다.
- 학습용 Python은 python.org 설치 패키지나 잘 알려진 배포 방식을 사용합니다.
- 터미널에서는 `python3 --version`을 먼저 확인하는 경우가 많습니다.
- 설치 뒤에도 프로젝트 실습은 가상환경으로 분리하는 편이 안전합니다.

macOS 문서는 터미널에서 스크립트를 실행하는 방법과 Finder에서 실행하는 방법이 다를 수 있음을 안내합니다. 터미널에서 현재 폴더를 확인하고 실행하는 방식이 더 투명합니다.

## Linux의 배포판 Python

Python 공식 Unix 플랫폼 문서는 Python이 대부분의 Linux 배포판에 미리 설치되어 있고, 그렇지 않은 경우에도 패키지로 제공된다고 설명합니다.

설치와 실행에서 확인할 사항은 다음과 같습니다.

- Linux에서는 `python3 --version`이 이미 동작할 수 있습니다.
- 배포판의 패키지 관리자에서 Python을 관리하는 경우가 많습니다.
- 시스템 Python은 운영체제 도구가 사용할 수 있으므로 함부로 지우거나 바꾸지 않습니다.
- 프로젝트 실습은 가상환경을 만들어 분리하는 편이 안전합니다.

Linux 자료에서 `sudo apt install python3` 같은 명령을 볼 수 있습니다. 하지만 배포판마다 패키지 관리자와 패키지 이름이 다를 수 있습니다. 따라서 Linux 설치 명령은 자신의 배포판 공식 문서를 기준으로 확인해야 합니다.

## 인터프리터·가상환경·패키지

Python 설치와 가상환경 생성은 같은 일이 아닙니다.

| 구분 | 무엇을 하는가 | 예시 |
| --- | --- | --- |
| Python 설치 | 컴퓨터에 Python 인터프리터를 준비한다 | python.org 설치, OS 패키지 설치 |
| 가상환경 생성 | 특정 프로젝트용 Python 실행 공간을 만든다 | `python -m venv .venv` |
| 패키지 설치 | 그 환경에 외부 패키지를 준비한다 | `python -m pip install numpy` |

Python 공식 `venv` 문서는 가상환경을 활성화하면 해당 환경의 Python 인터프리터가 실행되도록 경로가 앞에 붙는다고 설명합니다. 또 가상환경은 필요하면 다시 만들 수 있어야 하며, `requirements.txt` 같은 기록을 사용해 패키지를 다시 설치할 수 있어야 한다고 경고합니다.

프로젝트 환경을 준비하는 순서는 다음과 같습니다.

1. Python을 설치한다.
2. 프로젝트 폴더로 이동한다.
3. 가상환경을 만든다.
4. 가상환경을 활성화하거나 그 환경의 Python 경로를 직접 지정한다.
5. 필요한 패키지를 설치한다.
6. Python 코드를 실행한다.

## 설치와 실행 환경 점검

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

## 명령 하나가 없다고 재설치해야 할까

Linux 터미널에서 다음처럼 나온다고 가정합니다. 버전 번호는 출력 형태를 보여 주기 위한 예시입니다.

```text
$ python --version
bash: python: command not found
$ python3 --version
Python 3.12.3
```

이 환경에는 `python`이라는 명령이 없지만 `python3`로 실행되는 인터프리터는 있습니다. 다시 설치하기 전에 `python3 example.py`로 스크립트를 실행하거나 `python3 -m venv .venv`로 프로젝트 환경을 만들 수 있습니다.

반대로 사용할 Python 명령이 모두 없고 로컬 실행이 필요하다면 운영체제에 맞는 설치 절차를 진행합니다. 명령 하나의 실패와 인터프리터 자체의 부재를 구분하면 불필요한 재설치를 줄일 수 있습니다.

## 체크리스트

- Colab으로 충분한 학습 단계와 로컬 설치가 필요한 단계를 구분할 수 있다.
- Python 설치가 Python 인터프리터를 컴퓨터에 준비하는 일임을 설명할 수 있다.
- `python --version`, `python3 --version`, `py --version`의 목적을 설명할 수 있다.
- Windows, macOS, Linux에서 Python 설치 방식이 다르게 보일 수 있음을 설명할 수 있다.
- Python 설치, 가상환경 생성, 패키지 설치를 구분할 수 있다.
- 설치 오류가 났을 때 코드보다 실행 환경을 먼저 확인해야 함을 설명할 수 있다.
- `내 터미널에서 Python은 어떤 명령으로 실행되는가`, `그 명령은 어떤 버전의 Python을 가리키는가`, `프로젝트별 가상환경을 만들 준비가 되어 있는가`, `패키지를 설치한 환경과 코드를 실행하는 환경이 같은가`를 점검할 수 있다.

## 출처와 참고 자료

- Python Software Foundation, [Python Setup and Usage](https://docs.python.org/3/using/index.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. 플랫폼별 Python 환경 설정, 인터프리터 호출, 설치 관련 문서 구조 확인에 사용했다.
- Python Software Foundation, [Download Python](https://www.python.org/downloads/){: target="_blank" rel="noopener noreferrer" }, Python.org, 확인 날짜: 2026-07-20. 최신 Python 다운로드와 운영체제별 다운로드 진입점 확인에 사용했다.
- Python Software Foundation, [Using Python on Windows](https://docs.python.org/3/using/windows.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. Windows에서 Python 설치와 실행 방식이 별도 안내된다는 점을 확인하는 근거로 사용했다.
- Python Software Foundation, [Using Python on macOS](https://docs.python.org/3/using/mac.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. macOS에서 python.org 배포판과 설치 뒤 패키지 사용 안내를 확인하는 근거로 사용했다.
- Python Software Foundation, [Using Python on Unix platforms](https://docs.python.org/3/using/unix.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. Linux/Unix 계열에서 배포판 패키지와 소스 빌드 등 설치 경로가 운영체제별로 다를 수 있음을 확인하는 근거로 사용했다.
- Python Software Foundation, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. Python 설치와 별개로 프로젝트별 가상환경을 만드는 단계가 필요할 수 있음을 확인하는 근거로 사용했다.
