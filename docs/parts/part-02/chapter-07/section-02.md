# P2-7.2 터미널(terminal), 셸(shell), 작업 폴더(working directory)

> Section ID: `P2-7.2`
> Version: `v2026.09.08`

`python example.py`를 실행할 때는 명령을 해석하는 셸과 파일을 찾는 기준 폴더가 관여합니다. 파일이 존재해도 다른 폴더에서 같은 명령을 실행하면 찾지 못할 수 있습니다.

| 용어 | 뜻 |
| --- | --- |
| 터미널(terminal) | 명령을 입력하고 결과를 보는 창 또는 앱입니다. |
| 셸(shell) | 터미널 안에서 명령을 읽고 해석해 실행하는 프로그램입니다. |
| 작업 폴더(working directory) | 현재 명령이 기준으로 삼는 폴더입니다. |
| 경로(path) | 파일이나 폴더가 어디에 있는지 가리키는 문자열입니다. |
| 명령(command) | 셸에게 지금 수행하라고 요청하는 실행 문장입니다. |

## 명령의 해석과 기준 위치

| 기준 | 왜 중요한가 |
| --- | --- |
| 터미널은 화면이고 셸은 그 안에서 명령을 해석하는 프로그램이다 | 입력하는 자리와 해석하는 주체를 분리해야 혼동이 줄어든다 |
| 작업 폴더가 명령의 기준 위치를 정한다 | 같은 명령도 현재 위치에 따라 다른 파일을 가리킬 수 있다 |
| 가장 먼저 확인할 것은 현재 위치와 파일 목록이다 | 많은 실패가 문법이 아니라 위치 문제에서 시작된다 |

## 터미널과 셸의 유래

터미널과 셸은 최근에 생긴 앱 이름이 아닙니다. 둘 다 컴퓨터를 여러 사람이 문자 기반으로 사용하던 시절의 흔적을 갖고 있습니다.

초기의 터미널(terminal)은 지금처럼 노트북 안에 있는 앱이 아니라, 중앙 컴퓨터에 연결된 입력·출력 장치였습니다. Text-Terminal-HOWTO는 실제 텍스트 터미널이 모니터와 키보드처럼 생겼지만 그림이 아니라 문자 기반 명령줄 인터페이스(command-line interface)를 표시했고, 1970년대 후반과 1980년대에 메인프레임 컴퓨터 접속에 널리 쓰였다고 설명합니다. 이후 실제 하드웨어 터미널은 줄어들었지만, 오늘날의 터미널 앱은 그 동작을 소프트웨어로 흉내 내는 터미널 에뮬레이터(terminal emulator)에 가깝습니다.

셸(shell)도 오래된 개념입니다. GNU Bash 매뉴얼은 Bash가 GNU 운영체제의 셸, 또는 명령 언어 해석기(command language interpreter)라고 설명합니다. 또 Unix 셸은 명령 해석기(command interpreter)이면서 프로그래밍 언어이기도 하다고 설명합니다.

터미널 장치와 현대의 앱은 다음처럼 연결됩니다.

- 과거: 별도 터미널 장치에서 중앙 컴퓨터에 명령을 입력했습니다.
- 현재: 터미널 앱이 그 문자 기반 작업 방식을 소프트웨어로 제공합니다.
- 셸: 사용자가 입력한 명령을 해석하고 실행하는 프로그램입니다.

그래서 현대의 개발 환경에서도 `터미널을 연다`, `셸에서 실행한다`, `명령줄에 입력한다`는 표현이 남아 있습니다. 이 말들은 모두 “그래픽 버튼을 누르는 방식이 아니라, 문자로 명령을 입력해 실행한다”는 흐름과 연결됩니다.

## 터미널 앱과 셸

터미널(terminal)은 명령을 입력하고 결과를 보는 화면입니다. macOS의 Terminal, Windows Terminal, VS Code의 Terminal 패널이 여기에 해당합니다.

셸(shell)은 사용자가 입력한 명령을 읽고 해석해서 실행하는 프로그램입니다. 사용자는 셸을 통해 운영체제의 여러 유틸리티를 실행하고 조합할 수 있습니다.

여기서는 다음처럼 구분합니다.

- 터미널: 명령을 입력하고 결과를 보는 창입니다.
- 셸: 터미널 안에서 명령을 읽고 실행하는 프로그램입니다.
- 명령: 셸에게 시키는 일입니다.

그래서 같은 “터미널을 열었다”는 말 안에도 여러 경우가 있습니다.

| 환경 | 터미널 앱 | 셸 예시 |
| --- | --- | --- |
| macOS | Terminal, iTerm2, VS Code Terminal | zsh, bash |
| Windows | Windows Terminal, VS Code Terminal | PowerShell, cmd.exe, WSL의 bash 등 |
| Linux | GNOME Terminal, Konsole, VS Code Terminal | bash, zsh |

## 현재 위치·이동·파일 목록

터미널에 입력하는 문장은 자연어 문장이 아닙니다. 셸이 정해진 규칙에 따라 읽는 실행 요청입니다.

예를 들어 다음은 현재 위치를 확인하는 명령입니다.

```bash
pwd
```

다음은 폴더를 이동하는 명령입니다.

```bash
cd docs
```

다음은 현재 폴더의 파일 목록을 보는 명령입니다.

```bash
ls
```

Windows PowerShell에서는 현재 위치 확인에 `Get-Location`, 위치 이동에 `Set-Location`을 사용할 수 있습니다. 다만 PowerShell에서도 `pwd`, `cd` 같은 별칭(alias)을 자주 만납니다. Microsoft 문서는 `Get-Location`이 현재 위치를 표시하고, `Set-Location`이 현재 작업 위치를 지정한다고 설명합니다.

같은 명령도 현재 폴더가 다르면 다른 파일을 대상으로 실행될 수 있습니다.

## 작업 폴더와 파일 실행

작업 폴더(working directory)는 현재 명령이 기준으로 삼는 폴더입니다. 현재 작업 디렉터리(current working directory, CWD)라고도 부릅니다.

예를 들어 터미널에서 다음 명령을 실행한다고 생각해 봅니다.

```bash
python example.py
```

이 명령은 대체로 “현재 작업 폴더에서 `example.py`라는 파일을 찾아 Python으로 실행하라”는 뜻으로 읽을 수 있습니다. 그런데 현재 작업 폴더에 `example.py`가 없다면 명령은 실패합니다.

파일이 없어서 실패한 것일까요? 아닐 수 있습니다.

이때 흔한 상황은 파일이 없는 것이 아니라, 파일은 있지만 내가 다른 폴더에 있는 경우입니다.

흔한 오류는 코드 문법보다 위치 문제에서 시작합니다. 파일은 `downloads/`에 있는데 터미널은 `home/`에 있을 수 있습니다. 프로젝트 폴더는 `project-name/`에 있는데 터미널은 그 상위 폴더에 있을 수 있습니다.

그래서 실습 전에 현재 위치를 확인합니다.

```bash
pwd
```

그리고 필요한 폴더로 이동합니다.

```bash
cd /Users/someone/ws/project-name
```

Windows PowerShell에서는 다음처럼 확인할 수 있습니다.

```powershell
Get-Location
```

그리고 이동할 수 있습니다.

```powershell
Set-Location C:\Users\someone\ws\project-name
```

명령 이름은 달라도 핵심은 같습니다.

그래서 먼저 두 질문을 확인합니다.

- 현재 내가 어느 폴더에 있는가?
- 이 명령은 어느 폴더를 기준으로 실행되는가?

## 상대 경로와 절대 경로

경로(path)는 파일이나 폴더의 위치를 나타내는 문자열입니다. 여기서는 상대 경로(relative path)와 절대 경로(absolute path)를 구분합니다.

두 용어는 다음처럼 구분합니다.

- 상대 경로: 현재 작업 폴더를 기준으로 찾는 위치입니다.
- 절대 경로: 파일 시스템의 시작점부터 적은 전체 위치입니다.

현재 작업 폴더가 `/Users/someone/ws/project-name`이면 상대 경로 `docs/parts`는 그 아래의 `docs/parts` 폴더를 가리킵니다.

반면 절대 경로는 시작점부터 모두 적습니다.

```text
/Users/someone/ws/project-name/docs/parts
```

상대 경로는 짧고 편합니다. 하지만 현재 작업 폴더가 달라지면 의미도 달라집니다.

`docs/parts`는 `project-name` 폴더 안에서 실행하면 의미가 있습니다. 하지만 다른 프로젝트 폴더에서 실행하면 전혀 다른 위치를 찾거나, 존재하지 않는 경로가 됩니다.

## 파일 목록 확인

명령이 실패했을 때 바로 코드를 고치기 전에 현재 폴더와 파일 목록을 확인합니다.

Unix 계열 셸에서는 보통 다음 명령을 씁니다.

```bash
pwd
ls
```

Windows PowerShell에서는 다음 명령을 쓸 수 있습니다.

```powershell
Get-Location
Get-ChildItem
```

PowerShell에서는 `ls`가 `Get-ChildItem`의 별칭으로 동작하는 경우가 많습니다. 하지만 별칭보다 본래 이름을 한 번 보는 것도 도움이 됩니다. 나중에 문서를 찾을 때 공식 이름으로 검색할 수 있기 때문입니다.

## Colab 런타임의 셸 명령

Colab도 명령을 실행할 수 있습니다. 다만 로컬 PC의 터미널과 똑같이 이해하면 오해가 생깁니다.

Colab 코드 셀에서 다음처럼 `!`를 붙이면 셸 명령을 실행할 수 있습니다.

호스팅 런타임에 연결된 Colab 셀에서 `!pwd`를 실행하면 그 런타임의 현재 폴더 경로가 출력됩니다.

```python
# Colab 코드 셀에서 현재 작업 폴더를 확인하는 셸 명령입니다.
!pwd
```

이때 명령은 내 노트북 컴퓨터가 아니라 Colab 런타임에서 실행됩니다. 그래서 파일 위치, 설치된 패키지, 저장된 파일이 로컬 PC와 다를 수 있습니다.

정리하면 다음과 같습니다.

- 내 PC의 터미널: 내 컴퓨터의 파일과 환경을 기준으로 실행합니다.
- Colab 코드 셀의 `!` 명령: Colab 런타임의 파일과 환경을 기준으로 실행합니다.

`!`는 IPython 기반 노트북에서 셸 명령을 실행하는 표기이며, 일반 Python 파일의 문법은 아닙니다.

## 터미널에서 자주 생기는 오류

터미널 오류는 복잡해 보여도 몇 가지로 나누어 볼 수 있습니다.

| 상황 | 먼저 확인할 질문 |
| --- | --- |
| 파일을 찾을 수 없다고 나온다 | 현재 작업 폴더가 맞는가 |
| 명령을 찾을 수 없다고 나온다 | 해당 프로그램이 설치되어 있고 PATH에서 찾을 수 있는가 |
| Python 파일이 실행되지 않는다 | 터미널 명령과 Python 코드를 섞어 쓰지 않았는가 |
| Colab에서는 되는데 로컬에서는 안 된다 | 로컬 환경에 같은 패키지가 설치되어 있는가 |
| 로컬에서는 되는데 Colab에서는 안 된다 | Colab 런타임에 파일이 올라가 있는가 |

## 파일이 있는데 실행하지 못하는 경우

아래처럼 `workspace` 폴더 안에 `project` 폴더가 있고 그 안에 `example.py`가 있다고 가정합니다.

```text
workspace/
└── project/
    └── example.py
```

현재 작업 폴더가 `workspace`라면 `python example.py`는 `workspace/example.py`를 찾습니다. 그 위치에는 파일이 없으므로 실행하지 못합니다. `ls project`로 파일을 확인한 뒤 두 방법 중 하나를 사용할 수 있습니다.

```bash
# project 폴더로 이동한 뒤 실행
cd project
python example.py
```

또는 `workspace`에 머문 상태에서 파일의 상대 경로를 지정합니다.

```bash
python project/example.py
```

둘 다 같은 스크립트를 실행하지만 현재 작업 폴더는 다릅니다. 스크립트가 `data.csv`처럼 상대 경로로 데이터를 읽는다면, 첫 방법에서는 `project/data.csv`, 두 번째 방법에서는 `workspace/data.csv`를 찾습니다. 실행 파일을 찾는 문제와 그 파일 안에서 데이터를 찾는 문제를 구분해야 합니다.

## 체크리스트

- 터미널(terminal)을 명령 입력과 결과 확인을 위한 화면으로 설명할 수 있다.
- 셸(shell)을 명령을 해석하고 실행하는 프로그램으로 설명할 수 있다.
- 터미널 앱이 과거 문자 기반 터미널 장치의 역할을 소프트웨어로 이어받은 것임을 설명할 수 있다.
- 작업 폴더(working directory)를 현재 명령의 기준 위치로 설명할 수 있다.
- 상대 경로(relative path)와 절대 경로(absolute path)의 차이를 입문 수준에서 설명할 수 있다.
- `pwd`, `cd`, `ls`가 왜 필요한지 설명할 수 있다.
- PowerShell에서는 `Get-Location`, `Set-Location`, `Get-ChildItem` 같은 공식 명령 이름이 있다는 점을 알고 있다.
- Colab 코드 셀의 `!` 명령이 로컬 PC가 아니라 Colab 런타임에서 실행된다는 점을 설명할 수 있다.
- `나는 어떤 셸을 쓰고 있는가`, `나는 지금 어느 폴더에 있는가`, `이 명령은 어떤 파일이나 프로그램을 찾으려고 하는가`를 먼저 확인할 수 있다.

## 출처와 참고 자료

- David S. Lawyer, [Text-Terminal-HOWTO](https://tldp.org/HOWTO/Text-Terminal-HOWTO.html){: target="_blank" rel="noopener noreferrer" }, The Linux Documentation Project, 확인 날짜: 2026-07-20. 과거 문자 기반 터미널과 현대 명령줄 인터페이스의 관계를 설명하는 역사적 보조 근거로 사용했다.
- Free Software Foundation, [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html){: target="_blank" rel="noopener noreferrer" }, GNU Bash 5.3 manual, 확인 날짜: 2026-07-20. 셸이 명령 인터프리터이자 프로그래밍 언어라는 설명과 Bash 명령 처리 맥락 확인에 사용했다.
- Microsoft, [Get-Location](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-location?view=powershell-7.5){: target="_blank" rel="noopener noreferrer" }, PowerShell documentation, 확인 날짜: 2026-07-20. PowerShell에서 현재 작업 위치를 확인하는 공식 명령과 `pwd` 별칭 맥락 확인에 사용했다.
- Microsoft, [Set-Location](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-location?view=powershell-7.5){: target="_blank" rel="noopener noreferrer" }, PowerShell documentation, 확인 날짜: 2026-07-20. PowerShell에서 현재 작업 위치를 바꾸는 공식 명령과 `cd` 별칭 맥락 확인에 사용했다.
- Python Software Foundation, [os.getcwd](https://docs.python.org/3/library/os.html#os.getcwd){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. Python 코드 안에서 현재 작업 폴더를 문자열로 확인할 수 있다는 설명의 근거로 사용했다.
