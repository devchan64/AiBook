# P2-7.6 보충학습: Windows, macOS, Linux 터미널 사용법

P2-7.2에서는 터미널(terminal), 셸(shell), 작업 폴더(working directory)의 개념을 봤습니다. 이 절은 그 개념을 실제 운영체제에서 어떻게 확인하는지 다룹니다.

이 절은 Python 문법을 설명하지 않습니다. Python 설치도 깊게 다루지 않습니다. Python 설치는 P2-7.7에서 따로 봅니다. 여기서는 “명령을 어디에 입력하고, 현재 위치를 어떻게 확인하며, 실습 폴더로 어떻게 이동하는가”를 연습합니다.

## 이 절의 범위

이 절은 Windows, macOS, Linux에서 터미널을 처음 열고 실습 전에 확인할 최소 절차를 다룹니다.

여기서는 다음 질문에 답합니다.

- Windows에서는 어떤 터미널을 열 수 있는가?
- macOS에서는 Terminal을 어떻게 이해하면 되는가?
- Linux에서는 왜 터미널 사용이 자주 등장하는가?
- 현재 위치와 파일 목록은 어떻게 확인하는가?
- Windows 명령과 macOS/Linux 명령은 왜 조금 다른가?
- 복사해서 붙여넣는 명령을 실행할 때 무엇을 조심해야 하는가?

셸 스크립트(shell script), 파이프(pipe), 리다이렉션(redirection), 관리자 권한, 환경 변수(environment variable)는 깊게 다루지 않습니다. 이 내용은 나중에 프로젝트 실습에서 필요할 때 다시 다룹니다.

## 이 절의 목표

- Windows, macOS, Linux에서 터미널을 여는 방법을 입문 수준에서 설명할 수 있습니다.
- 터미널을 열었을 때 먼저 현재 위치를 확인해야 함을 설명할 수 있습니다.
- Windows PowerShell과 macOS/Linux 셸 명령이 일부 다르다는 점을 설명할 수 있습니다.
- `pwd`, `ls`, `cd`, `Get-Location`, `Get-ChildItem`, `Set-Location`이 어떤 목적의 명령인지 설명할 수 있습니다.
- 명령을 복사해서 실행하기 전에 현재 폴더와 명령의 목적을 확인할 수 있습니다.

## 운영체제마다 터미널 앱과 셸이 다를 수 있다

터미널 사용에서 가장 먼저 생기는 혼동은 “터미널 앱”과 “그 안에서 실행되는 셸”이 섞이는 것입니다.

Microsoft 문서는 Windows Terminal을 Command Prompt, PowerShell, WSL의 bash 같은 명령줄 셸을 실행하는 현대적인 호스트 애플리케이션으로 설명합니다. 즉 Windows Terminal은 하나의 셸만 뜻하지 않습니다. 여러 셸을 탭으로 열 수 있는 앱에 가깝습니다.

Apple의 Terminal User Guide는 macOS의 Terminal을 셸 스크립트를 만들고 관리하는 도구로 안내합니다. macOS에서 Terminal을 열면 일반적으로 Unix 계열 셸을 사용합니다.

Ubuntu 문서는 Linux에서 GUI도 있지만 전통적인 Unix 환경은 명령줄 인터페이스(command line interface, CLI)를 사용하며, 대부분의 Linux 배포판에서 터미널에 비슷한 명령을 입력할 수 있다고 설명합니다.

입문 단계에서는 다음처럼 정리하면 충분합니다.

| 운영체제 | 자주 만나는 터미널 앱 | 자주 만나는 셸 |
| --- | --- | --- |
| Windows | Windows Terminal, PowerShell, Command Prompt | PowerShell, Command Prompt, WSL의 bash |
| macOS | Terminal, iTerm2, VS Code Terminal | zsh, bash |
| Linux | GNOME Terminal, Konsole, VS Code Terminal | bash, zsh |

이 책의 실습은 가능한 한 명령이 어느 환경 기준인지 표시합니다. 표시가 없다면 macOS/Linux 계열 셸을 기준으로 보는 경우가 많습니다.

## Windows에서는 PowerShell을 먼저 기준으로 삼는다

Windows에서 초심자가 만나는 명령 입력 창은 여러 가지입니다.

- Windows Terminal
- PowerShell
- Command Prompt
- VS Code의 Terminal 패널
- WSL을 설치한 경우 Linux 셸

이 책에서는 Windows 설명이 필요할 때 PowerShell을 우선 기준으로 삼습니다. Command Prompt는 오래된 자료에서 자주 만나지만, Python 학습과 현대 개발 환경에서는 PowerShell이나 Windows Terminal을 더 자주 접할 수 있습니다.

Windows에서 터미널을 여는 가장 쉬운 방법은 다음 중 하나입니다.

1. 시작 메뉴에서 `Terminal` 또는 `PowerShell`을 검색합니다.
2. VS Code를 사용 중이라면 상단 메뉴에서 `Terminal > New Terminal`을 선택합니다.
3. 프로젝트 폴더에서 마우스 오른쪽 버튼 메뉴를 통해 터미널을 여는 기능을 사용할 수 있습니다. 이 메뉴 이름은 Windows 버전과 설치된 도구에 따라 달라질 수 있습니다.

터미널을 열었으면 먼저 현재 위치를 확인합니다.

```powershell
Get-Location
```

파일과 폴더 목록을 확인합니다.

```powershell
Get-ChildItem
```

폴더를 이동합니다.

```powershell
Set-Location C:\Users\someone\ws\AiBook
```

PowerShell에서는 짧은 별칭(alias)도 자주 쓰입니다.

```powershell
pwd
ls
cd C:\Users\someone\ws\AiBook
```

하지만 처음 공부할 때는 공식 명령 이름도 함께 알아두는 편이 좋습니다. 나중에 문서를 찾을 때 `Get-Location`, `Get-ChildItem`, `Set-Location`으로 검색하면 더 정확한 자료를 찾기 쉽습니다.

## macOS에서는 Terminal을 열고 zsh 셸을 만나는 경우가 많다

macOS에서는 기본 앱인 Terminal을 사용할 수 있습니다.

Terminal을 여는 방법은 여러 가지입니다.

1. Spotlight 검색에서 `Terminal`을 입력합니다.
2. Finder에서 `Applications > Utilities > Terminal`을 엽니다.
3. VS Code를 사용 중이라면 `Terminal > New Terminal`을 선택합니다.

터미널을 열었으면 현재 위치를 확인합니다.

```bash
pwd
```

파일과 폴더 목록을 확인합니다.

```bash
ls
```

프로젝트 폴더로 이동합니다.

```bash
cd /Users/someone/ws/AiBook
```

macOS에서는 경로가 `/Users/...` 형태로 보이는 경우가 많습니다. Windows의 `C:\Users\...` 형태와 다르므로, 다른 운영체제의 예제를 그대로 복사하면 경로가 맞지 않을 수 있습니다.

macOS에서 터미널 명령을 붙여넣을 때는 특히 `sudo`가 붙은 명령을 조심합니다. `sudo`는 관리자 권한으로 명령을 실행하게 만들 수 있습니다. 이 책의 초반 실습에서는 대부분 `sudo`가 필요하지 않습니다.

## Linux에서는 터미널이 학습 자료에 자주 등장한다

Linux 배포판에서는 터미널 사용이 학습 자료에 자주 등장합니다. Ubuntu 문서는 터미널을 여는 방법으로 검색 기능과 `Ctrl + Alt + T` 같은 단축키를 안내합니다. 데스크톱 환경에 따라 메뉴 이름은 다를 수 있지만, 많은 Linux 환경에서 터미널 앱을 검색해 열 수 있습니다.

Linux에서 터미널을 열었으면 먼저 현재 위치를 확인합니다.

```bash
pwd
```

파일과 폴더 목록을 확인합니다.

```bash
ls
```

프로젝트 폴더로 이동합니다.

```bash
cd /home/someone/ws/AiBook
```

Linux에서는 사용자 홈 폴더가 `/home/사용자이름` 형태인 경우가 많습니다. macOS의 `/Users/사용자이름`과 다릅니다.

Linux 자료에서는 `sudo apt install ...` 같은 명령도 자주 보입니다. 이런 명령은 시스템 패키지를 설치할 수 있습니다. 이 책의 Python 입문 구간에서는 무작정 실행하지 말고, 왜 필요한 명령인지 먼저 확인합니다.

## Tip: 터미널 단축키는 적게만 기억한다

터미널 단축키는 모두 외울 필요가 없습니다. 처음에는 “열기, 복사·붙여넣기, 탭, 명령 보완, 실행 중단” 정도만 알아도 충분합니다.

| 상황 | Windows Terminal | macOS Terminal | Linux/Ubuntu 계열 |
| --- | --- | --- | --- |
| 새 탭 열기 | `Ctrl + Shift + T` | `Command + T` | 터미널 앱마다 다르지만 `Ctrl + Shift + T`를 자주 만납니다 |
| 복사 | `Ctrl + Shift + C` | `Command + C` | `Ctrl + Shift + C`를 자주 만납니다 |
| 붙여넣기 | `Ctrl + Shift + V`를 자주 씁니다 | `Command + V` | `Ctrl + Shift + V`를 자주 만납니다 |
| 명령 실행 중단 | `Ctrl + C` | `Control + C` 또는 `Command + .` | `Ctrl + C` |
| 파일·폴더 이름 자동완성 | `Tab` | `Tab` | `Tab` |
| 이전 명령 다시 보기 | `↑` | `↑` | `↑` |

이 표는 “모든 환경에서 반드시 같다”는 뜻이 아닙니다. 터미널 앱, 셸, 키보드 레이아웃, VS Code 같은 편집기 안의 터미널 여부에 따라 달라질 수 있습니다. 실제 단축키가 다르면 앱 메뉴나 설정에서 확인합니다.

입문 단계에서 특히 유용한 것은 `Tab`입니다. 폴더 이름을 끝까지 입력하지 않고 앞부분만 입력한 뒤 `Tab`을 누르면 가능한 파일이나 폴더 이름을 보완할 수 있습니다.

예를 들어 `docs` 폴더로 이동하려고 할 때 다음처럼 입력하다가 `Tab`을 누를 수 있습니다.

```bash
cd do
```

터미널이 `docs`를 찾을 수 있으면 자동으로 보완합니다. 후보가 여러 개면 한 번에 완성되지 않을 수 있습니다. 이때는 조금 더 입력하거나, 일부 터미널에서는 `Tab`을 두 번 눌러 가능한 후보를 볼 수 있습니다.

단축키는 속도를 높이는 도구입니다. 하지만 처음에는 속도보다 현재 위치와 실행하려는 명령을 확인하는 일이 더 중요합니다.

## Tip: Ctrl+C와 Ctrl+V는 터미널에서 다르게 보일 수 있다

일반 앱에서는 `Ctrl + C`가 복사, `Ctrl + V`가 붙여넣기로 익숙합니다. 하지만 터미널에서는 다르게 동작할 수 있습니다. 특히 `Ctrl + C`는 실행 중인 명령을 중단하는 신호로 쓰이는 경우가 많습니다.

예를 들어 Python 서버, 오래 걸리는 설치 명령, 무한 반복되는 프로그램을 터미널에서 실행하고 있을 때 `Ctrl + C`를 누르면 복사가 아니라 실행 중단을 요청할 수 있습니다.

그래서 터미널에서는 복사와 붙여넣기 단축키를 따로 기억하는 편이 안전합니다.

| 환경 | 복사 | 붙여넣기 | 실행 중단 |
| --- | --- | --- | --- |
| Windows Terminal | `Ctrl + Shift + C` | `Ctrl + Shift + V`를 자주 씁니다 | `Ctrl + C` |
| macOS Terminal | `Command + C` | `Command + V` | `Control + C` 또는 `Command + .` |
| Linux/Ubuntu 계열 터미널 | `Ctrl + Shift + C`를 자주 씁니다 | `Ctrl + Shift + V`를 자주 씁니다 | `Ctrl + C` |

이 구분은 중요합니다.

- 일반 문서에서 글자를 복사할 때는 `Ctrl + C` 또는 `Command + C`를 씁니다.
- 터미널 안에서 실행 중인 명령을 멈출 때는 보통 `Ctrl + C`를 씁니다.
- 터미널 안의 글자를 복사할 때는 Windows/Linux 계열에서 `Ctrl + Shift + C`를 자주 씁니다.
- 터미널에 붙여넣을 때는 Windows/Linux 계열에서 `Ctrl + Shift + V`를 자주 씁니다.

단, 터미널 앱 설정에 따라 단축키는 바뀔 수 있습니다. Windows Terminal은 키보드 단축키를 바꿀 수 있고, macOS Terminal도 메뉴에 실제 단축키를 표시합니다. 단축키가 예상대로 동작하지 않으면 현재 사용하는 터미널 앱의 메뉴와 설정을 확인합니다.

처음에는 다음 기준만 기억해도 충분합니다.

- `Ctrl + C`를 눌렀는데 복사가 안 된다면, 터미널에서는 실행 중단 의미일 수 있습니다.
- Windows/Linux 터미널에서 복사·붙여넣기가 안 되면 `Ctrl + Shift + C`, `Ctrl + Shift + V`를 확인합니다.
- macOS Terminal에서는 일반 Mac 앱처럼 `Command + C`, `Command + V`를 먼저 생각합니다.

## 세 운영체제에서 공통으로 먼저 확인할 것

운영체제가 달라도 실습 전 확인 순서는 비슷합니다.

1. 터미널을 열었습니다.
2. 현재 위치를 확인합니다.
3. 파일 목록을 확인합니다.
4. 실습 폴더로 이동합니다.
5. 다시 현재 위치와 파일 목록을 확인합니다.
6. Python 명령이나 패키지 설치 명령을 실행합니다.

Windows PowerShell 기준으로는 다음 흐름입니다.

```powershell
Get-Location
Get-ChildItem
Set-Location C:\Users\someone\ws\AiBook
Get-Location
Get-ChildItem
```

macOS/Linux 기준으로는 다음 흐름입니다.

```bash
pwd
ls
cd /Users/someone/ws/AiBook
pwd
ls
```

Linux에서는 이동 경로가 다음처럼 될 수 있습니다.

```bash
cd /home/someone/ws/AiBook
```

중요한 것은 명령 이름을 많이 외우는 것이 아닙니다. “내가 지금 어느 폴더에 있는가”를 먼저 확인하는 습관입니다.

## 경로 구분자가 다르다

Windows와 macOS/Linux는 경로 표기가 다릅니다.

| 구분 | Windows 예시 | macOS/Linux 예시 |
| --- | --- | --- |
| 사용자 폴더 | `C:\Users\someone` | `/Users/someone`, `/home/someone` |
| 폴더 구분자 | `\` | `/` |
| 프로젝트 예시 | `C:\Users\someone\ws\AiBook` | `/Users/someone/ws/AiBook` |

문서에서 `/Users/someone/ws/AiBook` 같은 경로를 보면 macOS 예시일 가능성이 큽니다. Linux에서는 `/home/someone/ws/AiBook`에 가까울 수 있고, Windows에서는 `C:\Users\someone\ws\AiBook`에 가까울 수 있습니다.

따라서 경로 예제를 복사할 때는 자기 컴퓨터의 실제 폴더 위치로 바꿔야 합니다.

## Python 명령을 실행하기 전 확인할 것

터미널에서 Python을 실행하기 전에는 다음을 확인합니다.

- 지금 터미널이 프로젝트 폴더를 기준으로 열려 있는가?
- 실행하려는 `.py` 파일이 현재 폴더에 있는가?
- 필요한 데이터 파일이 같은 폴더 또는 지정한 경로에 있는가?
- 가상환경을 써야 한다면 현재 가상환경이 활성화되어 있는가?
- `python`, `python3`, `py` 중 어떤 명령이 내 환경에서 동작하는가?

운영체제와 설치 방식에 따라 Python 실행 명령이 다를 수 있습니다.

```bash
python --version
```

```bash
python3 --version
```

Windows에서는 Python Launcher가 설치되어 있다면 다음 명령을 만날 수도 있습니다.

```powershell
py --version
```

이 절에서는 Python 설치 자체를 해결하지 않습니다. “어떤 명령이 내 환경에서 Python을 가리키는가”를 확인하는 정도로만 봅니다. 설치가 필요해지는 시점은 P2-7.7에서 따로 다룹니다.

## 복사해서 붙여넣는 명령은 읽고 실행한다

초심자는 문서의 명령을 복사해서 붙여넣는 경우가 많습니다. 이것 자체가 나쁜 습관은 아닙니다. Ubuntu 문서도 숙련된 사용자도 종종 명령을 복사해 붙여넣는다고 설명합니다.

다만 복사한 명령은 실행 전에 읽어야 합니다.

먼저 다음을 확인합니다.

- 이 명령은 어느 운영체제 기준인가?
- 이 명령은 현재 폴더에서 실행해도 되는가?
- 경로가 내 컴퓨터와 맞는가?
- `sudo`, `Remove-Item`, `rm`, `del`처럼 파일 삭제나 관리자 권한과 관련된 명령이 포함되어 있는가?
- 명령 앞에 `$`, `>`, `PS>` 같은 프롬프트 기호가 포함되어 있지는 않은가?

문서에서는 터미널 프롬프트를 설명하려고 다음처럼 보일 수 있습니다.

```text
$ python example.py
```

이때 `$`는 입력하라는 문자가 아닐 수 있습니다. 보통 프롬프트 기호를 표현한 것입니다. 실제로 입력할 것은 다음 부분입니다.

```bash
python example.py
```

PowerShell 문서에서는 다음처럼 보일 수 있습니다.

```text
PS C:\Users\someone> python example.py
```

이때도 `PS C:\Users\someone>` 전체를 입력하는 것이 아닙니다. 실제 명령은 `python example.py`입니다.

## 오류가 나면 먼저 위치와 환경을 나눈다

터미널 오류를 만나면 바로 “Python을 못한다”고 판단하지 않습니다. 먼저 문제를 나눕니다.

| 오류 상황 | 먼저 볼 것 |
| --- | --- |
| 파일을 찾을 수 없다 | 현재 작업 폴더와 파일 목록 |
| 명령을 찾을 수 없다 | 프로그램 설치 여부와 PATH 설정 |
| 패키지를 찾을 수 없다 | 현재 Python 환경과 패키지 설치 여부 |
| 권한 오류가 난다 | 실행 위치, 파일 권한, 관리자 권한 필요 여부 |
| Colab에서는 되는데 로컬에서는 안 된다 | 로컬 Python과 패키지 설치 상태 |

초반 실습에서 가장 자주 발생하는 문제는 코드의 깊은 오류가 아닙니다. 현재 폴더가 다르거나, 패키지가 다른 환경에 설치되어 있거나, Colab과 로컬 PC를 같은 환경으로 착각하는 문제입니다.

## 이 절에서 기억할 관점

터미널은 외울 명령 목록이 아니라 실행 위치를 확인하는 도구입니다.

실습 전에는 다음 순서만 기억해도 많은 오류를 줄일 수 있습니다.

1. 터미널을 연다.
2. 현재 위치를 확인한다.
3. 파일 목록을 확인한다.
4. 실습 폴더로 이동한다.
5. 다시 위치와 파일 목록을 확인한다.
6. Python 명령을 실행한다.

운영체제가 달라도 핵심 질문은 같습니다.

- 나는 지금 어느 폴더에 있는가?
- 이 명령은 어느 셸 기준인가?
- 이 명령은 어떤 파일이나 프로그램을 찾으려 하는가?
- 이 명령은 내 컴퓨터에서 실행되는가, Colab 런타임에서 실행되는가?

## 체크리스트

- Windows Terminal이 여러 명령줄 셸을 실행할 수 있는 호스트 앱이라는 점을 설명할 수 있다.
- macOS Terminal에서 `pwd`, `ls`, `cd`로 위치 확인과 이동을 할 수 있다.
- Linux에서 터미널을 열고 현재 위치와 파일 목록을 확인할 수 있다.
- Windows PowerShell의 `Get-Location`, `Get-ChildItem`, `Set-Location`의 목적을 설명할 수 있다.
- Windows와 macOS/Linux의 경로 표기 차이를 설명할 수 있다.
- 터미널 단축키는 환경마다 다를 수 있으며, 처음에는 `Tab`, `Ctrl + C`, 복사·붙여넣기 정도만 알아도 충분하다는 점을 설명할 수 있다.
- 일반 앱의 `Ctrl + C`, `Ctrl + V`와 터미널의 복사·붙여넣기·실행 중단 단축키가 다를 수 있음을 설명할 수 있다.
- 복사한 명령에서 프롬프트 기호와 실제 입력할 명령을 구분할 수 있다.
- `sudo`, `rm`, `del`, `Remove-Item` 같은 명령은 의미를 확인하기 전에는 실행하지 않아야 함을 설명할 수 있다.

## 출처와 참고 자료

- Microsoft, [What is Windows Terminal?](https://learn.microsoft.com/en-us/windows/terminal/){: target="_blank" rel="noopener noreferrer" }, Microsoft Learn, 확인 날짜: 2026-06-24.
- Apple, [Keyboard shortcuts in Terminal on Mac](https://support.apple.com/guide/terminal/keyboard-shortcuts-trmlshtcts/mac){: target="_blank" rel="noopener noreferrer" }, Apple Support, 확인 날짜: 2026-06-24.
- Apple, [Terminal User Guide](https://support.apple.com/guide/terminal/welcome/mac){: target="_blank" rel="noopener noreferrer" }, Apple Support, 확인 날짜: 2026-06-24.
- Ubuntu Documentation, [UsingTheTerminal](https://help.ubuntu.com/community/UsingTheTerminal){: target="_blank" rel="noopener noreferrer" }, Ubuntu Community Help Wiki, 확인 날짜: 2026-06-24.
- Microsoft, [Get-Location](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-location?view=powershell-7.5){: target="_blank" rel="noopener noreferrer" }, PowerShell documentation, 확인 날짜: 2026-06-24.
- Microsoft, [Set-Location](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-location?view=powershell-7.5){: target="_blank" rel="noopener noreferrer" }, PowerShell documentation, 확인 날짜: 2026-06-24.
- Microsoft, [Get-ChildItem](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.5){: target="_blank" rel="noopener noreferrer" }, PowerShell documentation, 확인 날짜: 2026-06-24.
