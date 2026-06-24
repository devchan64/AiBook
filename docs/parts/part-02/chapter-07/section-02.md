# P2-7.2 터미널(terminal), 셸(shell), 작업 폴더(working directory)

P2-7.1에서는 코드가 실행되는 자리를 먼저 봤습니다. 이제는 로컬 PC에서 명령을 입력할 때 가장 먼저 만나는 화면을 봅니다.

프로그래밍을 처음 배우면 다음 문장이 자주 나옵니다.

```text
터미널을 열고 실행하세요.
프로젝트 폴더로 이동하세요.
아래 명령을 입력하세요.
```

이 문장은 짧지만 초심자에게는 여러 개념이 한꺼번에 들어 있습니다. 터미널(terminal), 셸(shell), 명령(command), 작업 폴더(working directory)를 구분하지 못하면 “나는 분명히 똑같이 입력했는데 왜 안 되지?”라는 상황을 자주 만납니다.

## 이 절의 범위

이 절은 터미널 사용법 전체를 가르치지 않습니다. 운영체제별 터미널을 여는 방법, 화면 구성, 기본 단축키, Windows와 macOS/Linux 명령 차이는 P2-7.7 보충수업으로 넘깁니다. 셸 스크립트(shell script), 파이프(pipe), 리다이렉션(redirection), 권한(permission), 환경 변수(environment variable)도 깊게 다루지 않습니다.

여기서는 다음 질문에만 답합니다.

```text
터미널은 무엇인가?
셸은 무엇인가?
왜 오래된 용어가 지금도 남아 있는가?
명령은 어디에서 해석되는가?
작업 폴더는 왜 중요한가?
```

Python 파일 실행은 P2-7.3에서, 가상환경과 패키지 설치는 P2-7.4에서 다시 다룹니다. 이 절에서는 그 전에 필요한 최소 언어를 만듭니다.

실제로 Windows, macOS, Linux에서 터미널을 어떻게 열고 어떤 명령을 먼저 입력해야 하는지는 P2-7.7에서 보충수업으로 다룹니다. 여기서는 운영체제별 절차보다 공통 개념을 먼저 잡습니다.

## 이 절의 목표

- 터미널(terminal)을 명령을 입력하고 결과를 보는 화면으로 설명할 수 있습니다.
- 셸(shell)을 명령을 해석하고 실행하는 프로그램으로 설명할 수 있습니다.
- 터미널과 셸이라는 용어가 오래된 컴퓨터 사용 방식에서 이어졌음을 설명할 수 있습니다.
- 작업 폴더(working directory)를 현재 명령이 기준으로 삼는 폴더로 설명할 수 있습니다.
- `pwd`, `cd`, `ls` 또는 `dir` 같은 기본 명령이 왜 필요한지 설명할 수 있습니다.
- 명령이 실패했을 때 코드 문제인지, 위치 문제인지 먼저 나누어 볼 수 있습니다.

## 왜 터미널과 셸이라는 말이 남아 있을까

터미널과 셸은 최근에 생긴 앱 이름이 아닙니다. 둘 다 컴퓨터를 여러 사람이 문자 기반으로 사용하던 시절의 흔적을 갖고 있습니다.

초기의 터미널(terminal)은 지금처럼 노트북 안에 있는 앱이 아니라, 중앙 컴퓨터에 연결된 입력·출력 장치였습니다. Text-Terminal-HOWTO는 실제 텍스트 터미널이 모니터와 키보드처럼 생겼지만 그림이 아니라 문자 기반 명령줄 인터페이스(command-line interface)를 표시했고, 1970년대 후반과 1980년대에 메인프레임 컴퓨터 접속에 널리 쓰였다고 설명합니다. 이후 실제 하드웨어 터미널은 줄어들었지만, 오늘날의 터미널 앱은 그 동작을 소프트웨어로 흉내 내는 터미널 에뮬레이터(terminal emulator)에 가깝습니다.

셸(shell)도 오래된 개념입니다. GNU Bash 매뉴얼은 Bash가 GNU 운영체제의 셸, 또는 명령 언어 해석기(command language interpreter)라고 설명합니다. 또 Unix 셸은 명령 해석기(command interpreter)이면서 프로그래밍 언어이기도 하다고 설명합니다.

입문 단계에서는 역사 전체를 외울 필요가 없습니다. 다만 다음 흐름을 기억하면 용어가 덜 낯섭니다.

```text
과거
-> 별도 터미널 장치에서 중앙 컴퓨터에 명령을 입력했다.

현재
-> 터미널 앱이 그 문자 기반 작업 방식을 소프트웨어로 제공한다.

셸
-> 사용자가 입력한 명령을 해석하고 실행하는 프로그램이다.
```

그래서 현대의 개발 환경에서도 `터미널을 연다`, `셸에서 실행한다`, `명령줄에 입력한다`는 표현이 남아 있습니다. 이 말들은 모두 “그래픽 버튼을 누르는 방식이 아니라, 문자로 명령을 입력해 실행한다”는 흐름과 연결됩니다.

## 터미널은 화면이고, 셸은 명령을 해석하는 프로그램이다

터미널(terminal)은 명령을 입력하고 결과를 보는 화면입니다. macOS의 Terminal, Windows Terminal, VS Code의 Terminal 패널이 여기에 해당합니다.

셸(shell)은 사용자가 입력한 명령을 읽고 해석해서 실행하는 프로그램입니다. 사용자는 셸을 통해 운영체제의 여러 유틸리티를 실행하고 조합할 수 있습니다.

입문 단계에서는 이렇게 구분하면 충분합니다.

```text
터미널
-> 명령을 입력하고 결과를 보는 창

셸
-> 터미널 안에서 명령을 읽고 실행하는 프로그램

명령
-> 셸에게 시키는 일
```

그래서 같은 “터미널을 열었다”는 말 안에도 여러 경우가 있습니다.

| 환경 | 터미널 앱 | 셸 예시 |
| --- | --- | --- |
| macOS | Terminal, iTerm2, VS Code Terminal | zsh, bash |
| Windows | Windows Terminal, PowerShell, VS Code Terminal | PowerShell, Command Prompt, WSL shell |
| Linux | GNOME Terminal, Konsole, VS Code Terminal | bash, zsh |

이 책에서는 운영체제별 셸 차이를 깊게 다루지 않습니다. 다만 명령 예제가 어디 기준인지 표시하려고 노력합니다.

## 명령은 문장이 아니라 실행 요청이다

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

처음에는 모든 명령을 외울 필요가 없습니다. 중요한 것은 명령이 “어디에서 실행되는가”입니다.

```text
같은 명령도
현재 폴더가 다르면
다른 파일을 대상으로 실행될 수 있다.
```

## 작업 폴더는 명령의 기준 위치다

작업 폴더(working directory)는 현재 명령이 기준으로 삼는 폴더입니다. 현재 작업 디렉터리(current working directory, CWD)라고도 부릅니다.

예를 들어 터미널에서 다음 명령을 실행한다고 생각해 봅니다.

```bash
python example.py
```

이 명령은 대체로 “현재 작업 폴더에서 `example.py`라는 파일을 찾아 Python으로 실행하라”는 뜻으로 읽을 수 있습니다. 그런데 현재 작업 폴더에 `example.py`가 없다면 명령은 실패합니다.

파일이 없어서 실패한 것일까요? 아닐 수 있습니다.

```text
파일은 있다.
하지만 내가 다른 폴더에 있다.
```

초심자에게 흔한 오류는 코드 문법보다 위치 문제에서 시작합니다. 파일은 `downloads/`에 있는데 터미널은 `home/`에 있을 수 있습니다. 프로젝트는 `AiBook/`에 있는데 터미널은 그 상위 폴더에 있을 수 있습니다.

그래서 실습 전에 현재 위치를 확인합니다.

```bash
pwd
```

그리고 필요한 폴더로 이동합니다.

```bash
cd /Users/someone/ws/AiBook
```

Windows PowerShell에서는 다음처럼 확인할 수 있습니다.

```powershell
Get-Location
```

그리고 이동할 수 있습니다.

```powershell
Set-Location C:\Users\someone\ws\AiBook
```

명령 이름은 달라도 핵심은 같습니다.

```text
현재 내가 어느 폴더에 있는가?
이 명령은 어느 폴더를 기준으로 실행되는가?
```

## 상대 경로와 절대 경로를 구분한다

경로(path)는 파일이나 폴더의 위치를 나타내는 문자열입니다. 입문 단계에서는 상대 경로(relative path)와 절대 경로(absolute path)를 구분하면 충분합니다.

```text
상대 경로
-> 현재 작업 폴더를 기준으로 찾는 위치

절대 경로
-> 파일 시스템의 시작점부터 적은 전체 위치
```

예를 들어 현재 작업 폴더가 `/Users/someone/ws/AiBook`라면 다음 상대 경로는 책 원고 폴더를 가리킬 수 있습니다.

```text
docs/parts
```

반면 절대 경로는 시작점부터 모두 적습니다.

```text
/Users/someone/ws/AiBook/docs/parts
```

상대 경로는 짧고 편합니다. 하지만 현재 작업 폴더가 달라지면 의미도 달라집니다.

```text
docs/parts
```

이 경로는 `AiBook` 폴더 안에서 실행하면 의미가 있습니다. 하지만 다른 프로젝트 폴더에서 실행하면 전혀 다른 위치를 찾거나, 존재하지 않는 경로가 됩니다.

## 파일 목록을 확인하는 습관이 중요하다

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

PowerShell에서는 `ls`가 `Get-ChildItem`의 별칭으로 동작하는 경우가 많습니다. 하지만 초심자에게는 별칭보다 본래 이름을 한 번 보는 것도 도움이 됩니다. 나중에 문서를 찾을 때 공식 이름으로 검색할 수 있기 때문입니다.

이 책에서는 macOS/Linux 기준 명령을 먼저 보이고, Windows에서 다른 명령이 필요하면 따로 표시합니다.

## Colab에는 터미널이 없는가

Colab도 명령을 실행할 수 있습니다. 다만 로컬 PC의 터미널과 똑같이 이해하면 오해가 생깁니다.

Colab 코드 셀에서 다음처럼 `!`를 붙이면 셸 명령을 실행할 수 있습니다.

```python
!pwd
```

이때 명령은 내 노트북 컴퓨터가 아니라 Colab 런타임에서 실행됩니다. 그래서 파일 위치, 설치된 패키지, 저장된 파일이 로컬 PC와 다를 수 있습니다.

```text
내 PC의 터미널
-> 내 컴퓨터의 파일과 환경을 기준으로 실행

Colab 코드 셀의 ! 명령
-> Colab 런타임의 파일과 환경을 기준으로 실행
```

P2-3.4에서 `!pip install numpy`와 `%pip install numpy`를 구분했던 이유도 여기에 있습니다. 코드 셀 안에서 셸 명령을 실행할 수는 있지만, 그것이 Python 문법이라는 뜻은 아닙니다.

## 터미널에서 자주 생기는 초심자 오류

터미널 오류는 복잡해 보이지만, 처음에는 몇 가지로 나누어 볼 수 있습니다.

| 상황 | 먼저 확인할 질문 |
| --- | --- |
| 파일을 찾을 수 없다고 나온다 | 현재 작업 폴더가 맞는가 |
| 명령을 찾을 수 없다고 나온다 | 해당 프로그램이 설치되어 있고 PATH에서 찾을 수 있는가 |
| Python 파일이 실행되지 않는다 | 터미널 명령과 Python 코드를 섞어 쓰지 않았는가 |
| Colab에서는 되는데 로컬에서는 안 된다 | 로컬 환경에 같은 패키지가 설치되어 있는가 |
| 로컬에서는 되는데 Colab에서는 안 된다 | Colab 런타임에 파일이 올라가 있는가 |

이 절에서 모든 오류를 해결하지는 않습니다. 다만 오류를 볼 때 “코드 자체의 오류”와 “명령을 실행한 위치의 오류”를 나누어 생각하는 습관을 만듭니다.

## 이 절에서 기억할 관점

터미널을 볼 때는 세 가지를 먼저 확인합니다.

```text
1. 나는 어떤 셸을 쓰고 있는가?
2. 나는 지금 어느 폴더에 있는가?
3. 이 명령은 어떤 파일이나 프로그램을 찾으려고 하는가?
```

이 세 질문은 단순해 보이지만, 이후 Python 스크립트 실행, 가상환경 활성화, 패키지 설치, 데이터 파일 읽기에서 계속 반복됩니다.

## 체크리스트

- 터미널(terminal)을 명령 입력과 결과 확인을 위한 화면으로 설명할 수 있다.
- 셸(shell)을 명령을 해석하고 실행하는 프로그램으로 설명할 수 있다.
- 터미널 앱이 과거 문자 기반 터미널 장치의 역할을 소프트웨어로 이어받은 것임을 설명할 수 있다.
- 작업 폴더(working directory)를 현재 명령의 기준 위치로 설명할 수 있다.
- 상대 경로(relative path)와 절대 경로(absolute path)의 차이를 입문 수준에서 설명할 수 있다.
- `pwd`, `cd`, `ls`가 왜 필요한지 설명할 수 있다.
- PowerShell에서는 `Get-Location`, `Set-Location`, `Get-ChildItem` 같은 공식 명령 이름이 있다는 점을 알고 있다.
- Colab 코드 셀의 `!` 명령이 로컬 PC가 아니라 Colab 런타임에서 실행된다는 점을 설명할 수 있다.

## 출처와 참고 자료

- David S. Lawyer, [Text-Terminal-HOWTO](https://tldp.org/HOWTO/Text-Terminal-HOWTO.html){: target="_blank" rel="noopener noreferrer" }, The Linux Documentation Project, 확인 날짜: 2026-06-24.
- Free Software Foundation, [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html){: target="_blank" rel="noopener noreferrer" }, GNU Bash 5.3 manual, 확인 날짜: 2026-06-24.
- Microsoft, [Get-Location](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-location?view=powershell-7.5){: target="_blank" rel="noopener noreferrer" }, PowerShell documentation, 확인 날짜: 2026-06-24.
- Microsoft, [Set-Location](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-location?view=powershell-7.5){: target="_blank" rel="noopener noreferrer" }, PowerShell documentation, 확인 날짜: 2026-06-24.
- Python Software Foundation, [os.getcwd](https://docs.python.org/3/library/os.html#os.getcwd){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-06-24.
