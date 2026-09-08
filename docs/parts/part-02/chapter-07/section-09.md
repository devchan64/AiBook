# P2-7.9 보충학습: 로컬 Python 환경 문제 점검

> Section ID: `P2-7.9`
> Version: `v2026.09.08`

`python` 명령을 찾지 못하는 오류와 `import numpy`가 실패하는 오류는 발생 위치가 다릅니다. 전자는 셸의 명령 연결을, 후자는 실행 중인 Python의 패키지 상태를 확인해야 합니다. Python 버전이 같아도 서로 다른 가상환경일 수 있으므로 실행 파일 경로까지 비교합니다.

## 오류 메시지와 확인 대상

| 메시지 또는 상황 | 확인 대상 |
| --- | --- |
| `python: command not found` | 실행 명령 이름, 설치 상태, PATH |
| `ModuleNotFoundError: No module named 'numpy'` | 현재 Python의 NumPy 설치 상태 |
| `FileNotFoundError` | 현재 작업 폴더와 데이터 경로 |
| `Permission denied` | 쓰려는 위치와 접근 권한 |
| `SyntaxError` | Python 문법, 셸 명령을 Python에 입력했는지 여부 |

## 실행되는 Python 명령

터미널에서 사용하는 Python 명령의 버전을 확인합니다.

```bash
python --version
```

macOS/Linux에서는 `python3 --version`, Windows에서는 설치 방식에 따라 `py --version`이 동작할 수 있습니다. 하나가 실패했다고 인터프리터가 전혀 없다고 단정하지 않습니다.

PATH는 셸이 실행 파일을 찾을 때 사용하는 디렉터리 목록입니다. 설치된 Python이 있어도 명령 이름이나 PATH, 실행 별칭에 따라 호출되지 않을 수 있습니다. 설치와 명령 연결에 대한 운영체제별 점검은 [Python 설치](section-07.md)의 공식 문서 링크를 참고합니다.

## 실제 인터프리터와 작업 폴더

오류가 난 노트북 커널이나 스크립트 실행 환경에서 다음 코드를 실행합니다. 현재 Python의 실행 파일, 환경 경로, 작업 폴더가 출력됩니다.

```python
import os
import sys

print("Python:", sys.executable)
print("환경:", sys.prefix)
print("가상환경:", sys.prefix != sys.base_prefix)
print("작업 폴더:", os.getcwd())
```

표준 `venv` 환경에서는 `sys.prefix`와 `sys.base_prefix`가 다릅니다. 활성화 여부를 기억하는 것보다 실행 중인 Python이 어떤 환경에 속하는지 직접 확인하는 방법입니다. 에디터나 노트북에서 선택한 인터프리터가 터미널의 Python과 다를 수 있습니다.

## 같은 버전의 서로 다른 가상환경

다음은 서로 다른 두 프로젝트의 Python을 실행한 예시 출력입니다.

| 항목 | 설치에 쓴 환경 | 예제 실행에 쓴 환경 |
| --- | --- | --- |
| Python 버전 | 3.12.3 | 3.12.3 |
| 실행 파일 | `/home/user/project-a/.venv/bin/python` | `/home/user/project-b/.venv/bin/python` |
| NumPy | 설치됨 | 설치되지 않음 |

버전이 같아도 경로가 다르므로 다른 환경입니다. A에서 설치가 성공해도 B에서 `import numpy`는 실패할 수 있습니다. 프로젝트 B를 실행하려는 경우 B의 Python에 필요한 패키지를 설치합니다. 경로가 다르다는 이유만으로 항상 오류라는 뜻은 아니며, 실행할 프로젝트가 요구하는 환경인지가 기준입니다.

## pip와 패키지 위치

사용할 Python을 선택한 터미널에서 다음 명령을 실행합니다.

```bash
python -m pip --version
python -m pip show numpy
```

첫 명령은 pip 버전과 설치 위치를 보여 줍니다. 두 번째 명령은 NumPy가 있다면 버전과 `Location`을 표시합니다. 없다면 패키지를 찾지 못했다는 메시지가 나옵니다.

`python -m pip`는 명령 앞의 Python으로 pip를 실행합니다. 실제 코드도 같은 Python으로 실행해야 설치 상태가 연결됩니다. 가상환경 경로를 직접 지정하는 방법은 [가상환경의 Python으로 설치·실행](section-04.md)을 참고합니다.

필요한 NumPy가 없다면 같은 Python에서 설치합니다.

```bash
python -m pip install numpy
```

그 환경에서 다음 코드를 실행하면 NumPy 버전과 불러온 파일의 위치가 출력됩니다.

```python
import numpy as np

print("NumPy:", np.__version__)
print("파일:", np.__file__)
```

설치 목록이 있다면 개별 설치 대신 `python -m pip install -r requirements.txt`로 프로젝트 요구사항을 준비할 수 있습니다.

## 권한 오류와 패키지 누락

시스템 영역에 패키지를 설치하려다가 쓰기 권한이 없어 실패할 수 있습니다. 이 경우 프로젝트 폴더에서 가상환경을 만들고 그 환경의 Python으로 설치하면 시스템 패키지를 변경하지 않고 준비할 수 있습니다.

`Permission denied`는 접근 권한의 문제이고, `ModuleNotFoundError`는 실행 중인 Python이 모듈을 찾지 못했다는 뜻입니다. 후자는 다른 환경에 설치했거나, 설치가 완료되지 않았거나, 불러오는 이름이 잘못된 경우 등을 확인합니다.

## 점검 결과에 따른 조치

| 확인 결과 | 다음 조치 |
| --- | --- |
| 사용할 Python 명령이 없음 | 설치 상태와 운영체제별 실행 명령 확인 |
| 에디터가 다른 프로젝트의 Python을 사용함 | 해당 프로젝트의 인터프리터 선택 |
| 선택한 환경에 필요한 패키지가 없음 | 같은 Python의 pip로 설치 |
| 패키지는 있지만 데이터 파일이 없음 | 파일 위치·작업 폴더·입력 데이터 준비 확인 |
| 환경과 입력이 맞는데 오류가 계속됨 | 전체 오류 메시지와 코드가 요구하는 버전 확인 |

실행 환경을 확인한 기록은 [의존성과 재현성](section-05.md)의 설치 목록·데이터·실행 위치 기록과 함께 남기면 재실행 때 비교할 수 있습니다.

## 체크리스트

- 명령을 찾지 못하는 오류와 패키지를 찾지 못하는 오류를 구분할 수 있다.
- Python 버전이 같아도 실행 파일 경로가 다를 수 있음을 설명할 수 있다.
- `sys.executable`과 `sys.prefix`로 현재 실행 환경을 확인할 수 있다.
- 설치에 쓴 Python과 코드 실행에 쓴 Python을 비교할 수 있다.
- `pip show`와 import 결과로 패키지 설치·사용 위치를 확인할 수 있다.
- 오류 메시지에 따라 명령·환경·권한·파일 문제를 나누어 점검할 수 있다.

## 출처와 참고 자료

- Python Software Foundation, [Python Setup and Usage](https://docs.python.org/3/using/index.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. 플랫폼별 Python 설정과 인터프리터 호출 문서 구조를 로컬 환경 점검 순서의 배경으로 사용했다.
- Python Software Foundation, [Using Python on Windows](https://docs.python.org/3/using/windows.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. Windows에서 Python 실행 명령과 설치 방식이 별도 안내된다는 점을 확인하는 근거로 사용했다.
- Python Software Foundation, [Using Python on Unix platforms](https://docs.python.org/3/using/unix.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. Unix/Linux 계열에서 Python 실행 명령과 설치 경로가 환경별로 달라질 수 있음을 확인하는 근거로 사용했다.
- Python Software Foundation, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. 가상환경 활성화 여부와 패키지 설치 위치를 함께 점검해야 한다는 설명의 근거로 사용했다.

- Python Software Foundation, [sys — System-specific parameters and functions](https://docs.python.org/3/library/sys.html){: target="_blank" rel="noopener noreferrer" }, 확인 날짜: 2026-09-08. 인터프리터 실행 파일과 가상환경 경로를 확인하는 sys.executable, sys.prefix, sys.base_prefix의 근거.
