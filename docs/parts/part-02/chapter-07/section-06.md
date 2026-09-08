# P2-7.6 보충학습: 운영체제별 터미널 진입

> Section ID: `P2-7.6`
> Version: `v2026.09.08`

Windows PowerShell에서는 `Get-Location`, macOS/Linux의 셸에서는 `pwd`로 현재 위치를 확인합니다. 터미널을 여는 방법과 경로 표기는 달라도 위치 확인, 파일 목록 확인, 폴더 이동이라는 작업은 같습니다.

| 용어 | 뜻 |
| --- | --- |
| Windows Terminal / PowerShell | Windows에서 명령 입력을 시작할 때 자주 만나는 터미널 앱과 셸 조합입니다. |
| Terminal / zsh | macOS에서 자주 만나는 기본 터미널 앱과 셸 조합입니다. |
| `pwd`, `ls`, `cd` | 현재 위치 확인, 목록 확인, 폴더 이동을 위한 기본 명령입니다. |
| `Get-Location`, `Get-ChildItem`, `Set-Location` | PowerShell에서 같은 목적을 수행하는 명령입니다. |
| 경로(path) 차이 | Windows의 `C:\...`와 macOS/Linux의 `/...`처럼 운영체제별 위치 표기 차이입니다. |

## 운영체제·경로·단축키

| 기준 | 왜 중요한가 |
| --- | --- |
| 운영체제가 다르면 터미널 앱, 기본 셸, 경로 표기가 조금씩 다르다 | 다른 운영체제 예제를 그대로 복사하면 경로와 명령이 어긋날 수 있다 |
| 그래도 공통으로 먼저 보는 것은 현재 위치와 파일 목록이다 | 운영체제가 달라도 실습 전 점검 순서는 크게 다르지 않다 |
| 터미널 단축키는 일반 앱과 다르게 동작할 수 있다 | 복사·붙여넣기와 실행 중단을 혼동하면 작업이 끊길 수 있다 |

## 운영체제별 터미널과 셸

터미널 사용에서 가장 먼저 생기는 혼동은 “터미널 앱”과 “그 안에서 실행되는 셸”이 섞이는 것입니다.

Microsoft 문서는 Windows Terminal을 Command Prompt, PowerShell, WSL의 bash 같은 명령줄 셸을 실행하는 현대적인 호스트 애플리케이션으로 설명합니다. 즉 Windows Terminal은 하나의 셸만 뜻하지 않습니다. 여러 셸을 탭으로 열 수 있는 앱에 가깝습니다.

Apple의 Terminal User Guide는 macOS의 Terminal을 셸 스크립트를 만들고 관리하는 도구로 안내합니다. macOS에서 Terminal을 열면 일반적으로 Unix 계열 셸을 사용합니다.

Ubuntu 문서는 Linux에서 GUI도 있지만 전통적인 Unix 환경은 명령줄 인터페이스(command line interface, CLI)를 사용하며, 대부분의 Linux 배포판에서 터미널에 비슷한 명령을 입력할 수 있다고 설명합니다.

터미널 앱과 셸의 예는 다음과 같습니다.

| 운영체제 | 자주 만나는 터미널 앱 | 자주 만나는 셸 |
| --- | --- | --- |
| Windows | Windows Terminal, VS Code Terminal | PowerShell, cmd.exe, WSL의 bash |
| macOS | Terminal, iTerm2, VS Code Terminal | zsh, bash |
| Linux | GNOME Terminal, Konsole, VS Code Terminal | bash, zsh |

## Windows에서 PowerShell 열기

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
Set-Location C:\Users\someone\ws\project-name
```

PowerShell에서는 짧은 별칭(alias)도 자주 쓰입니다.

```powershell
pwd
ls
cd C:\Users\someone\ws\project-name
```

하지만 처음 공부할 때는 공식 명령 이름도 함께 알아두는 편이 좋습니다. 나중에 문서를 찾을 때 `Get-Location`, `Get-ChildItem`, `Set-Location`으로 검색하면 더 정확한 자료를 찾기 쉽습니다.

## macOS에서 Terminal 열기

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
cd /Users/someone/ws/project-name
```

macOS에서는 경로가 `/Users/...` 형태로 보이는 경우가 많습니다. Windows의 `C:\Users\...` 형태와 다르므로, 다른 운영체제의 예제를 그대로 복사하면 경로가 맞지 않을 수 있습니다.

macOS에서 터미널 명령을 붙여넣을 때는 특히 `sudo`가 붙은 명령을 조심합니다. `sudo`는 관리자 권한으로 명령을 실행하게 만들 수 있습니다. 이 파트의 초반 실습에서는 대부분 `sudo`가 필요하지 않습니다.

## Linux에서 터미널 열기

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
cd /home/someone/ws/project-name
```

Linux에서는 사용자 홈 폴더가 `/home/사용자이름` 형태인 경우가 많습니다. macOS의 `/Users/사용자이름`과 다릅니다.

Linux 자료에서는 `sudo apt install ...` 같은 명령도 자주 보입니다. 이런 명령은 시스템 패키지를 설치할 수 있습니다. 이 Python 입문 구간에서는 무작정 실행하지 말고, 왜 필요한 명령인지 먼저 확인합니다.

## 터미널 단축키

터미널에서는 복사와 실행 중단이 다른 단축키에 배정될 수 있습니다.

| 상황 | Windows Terminal | macOS Terminal | Linux/Ubuntu 계열 |
| --- | --- | --- | --- |
| 새 탭 열기 | `Ctrl + Shift + T` | `Command + T` | 터미널 앱마다 다르지만 `Ctrl + Shift + T`를 자주 만납니다 |
| 복사 | `Ctrl + Shift + C` | `Command + C` | `Ctrl + Shift + C`를 자주 만납니다 |
| 붙여넣기 | `Ctrl + Shift + V`를 자주 씁니다 | `Command + V` | `Ctrl + Shift + V`를 자주 만납니다 |
| 명령 실행 중단 | `Ctrl + C` | `Control + C` 또는 `Command + .` | `Ctrl + C` |
| 파일·폴더 이름 자동완성 | `Tab` | `Tab` | `Tab` |
| 이전 명령 다시 보기 | `↑` | `↑` | `↑` |

이 표는 “모든 환경에서 반드시 같다”는 뜻이 아닙니다. 터미널 앱, 셸, 키보드 레이아웃, VS Code 같은 편집기 안의 터미널 여부에 따라 달라질 수 있습니다. 실제 단축키가 다르면 앱 메뉴나 설정에서 확인합니다.

여기서 특히 유용한 것은 `Tab`입니다. 폴더 이름을 끝까지 입력하지 않고 앞부분만 입력한 뒤 `Tab`을 누르면 가능한 파일이나 폴더 이름을 보완할 수 있습니다.

예를 들어 `docs` 폴더로 이동하려고 할 때 다음처럼 입력하다가 `Tab`을 누를 수 있습니다.

```bash
cd do
```

터미널이 `docs`를 찾을 수 있으면 자동으로 보완합니다. 후보가 여러 개면 한 번에 완성되지 않을 수 있습니다. 이때는 조금 더 입력하거나, 일부 터미널에서는 `Tab`을 두 번 눌러 가능한 후보를 볼 수 있습니다.

`Ctrl + C`는 실행 중인 프로그램에 중단을 요청할 수 있습니다. 글자를 복사하려면 위 표의 복사 단축키를 사용합니다. 앱 설정과 선택된 텍스트 유무에 따라 동작이 달라질 수 있으므로 예상과 다르면 메뉴의 단축키를 확인합니다.

## 폴더 이동 후 위치 확인

실습 폴더로 이동한 뒤 현재 위치와 파일 목록을 다시 확인하면 경로를 잘못 입력했는지 알 수 있습니다.

Windows PowerShell 기준으로는 다음 흐름입니다.

```powershell
Get-Location
Get-ChildItem
Set-Location C:\Users\someone\ws\project-name
Get-Location
Get-ChildItem
```

macOS/Linux 기준으로는 다음 흐름입니다.

```bash
pwd
ls
cd /Users/someone/ws/project-name
pwd
ls
```

Linux에서는 이동 경로가 다음처럼 될 수 있습니다.

```bash
cd /home/someone/ws/project-name
```

## 운영체제별 경로 표기

Windows와 macOS/Linux는 경로 표기가 다릅니다.

| 구분 | Windows 예시 | macOS/Linux 예시 |
| --- | --- | --- |
| 사용자 폴더 | `C:\Users\someone` | `/Users/someone`, `/home/someone` |
| 폴더 구분자 | `\` | `/` |
| 프로젝트 예시 | `C:\Users\someone\ws\project-name` | `/Users/someone/ws/project-name` |

문서에서 `/Users/someone/ws/project-name` 같은 경로를 보면 macOS 예시일 가능성이 큽니다. Linux에서는 `/home/someone/ws/project-name`에 가까울 수 있고, Windows에서는 `C:\Users\someone\ws\project-name`에 가까울 수 있습니다.

따라서 경로 예제를 복사할 때는 자기 컴퓨터의 실제 폴더 위치로 바꿔야 합니다.

## Python 명령 확인

터미널에서 Python을 실행하기 전에는 다음을 확인합니다.

- 지금 터미널이 프로젝트 폴더를 기준으로 열려 있는가?
- 실행하려는 `.py` 파일이 현재 폴더에 있는가?
- 필요한 데이터 파일이 같은 폴더 또는 지정한 경로에 있는가?
- 가상환경을 쓴다면 그 환경의 Python을 선택했는가?
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

출력된 버전으로 어떤 명령이 Python을 실행하는지 확인합니다. 설치가 필요한 경우에는 [Python 설치](section-07.md)를 참고합니다.

## 프롬프트와 실제 명령

문서의 명령을 복사해서 붙여넣는 경우는 흔합니다. 이것 자체가 나쁜 습관은 아닙니다. Ubuntu 문서도 숙련된 사용자도 종종 명령을 복사해 붙여넣는다고 설명합니다.

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

## 오류별 확인 항목

오류 메시지가 가리키는 대상을 확인합니다.

| 오류 상황 | 먼저 볼 것 |
| --- | --- |
| 파일을 찾을 수 없다 | 현재 작업 폴더와 파일 목록 |
| 명령을 찾을 수 없다 | 프로그램 설치 여부와 PATH 설정 |
| 패키지를 찾을 수 없다 | 현재 Python 환경과 패키지 설치 여부 |
| 권한 오류가 난다 | 실행 위치, 파일 권한, 관리자 권한 필요 여부 |
| Colab에서는 되는데 로컬에서는 안 된다 | 로컬 Python과 패키지 설치 상태 |

## 공백이 있는 프로젝트 경로

프로젝트 폴더 이름이 `ai practice`라면 공백까지 하나의 경로로 전달해야 합니다. 실제 사용자 이름과 폴더 위치로 바꾼 뒤 경로 전체를 따옴표로 감쌉니다.

Windows PowerShell:

```powershell
Set-Location "C:\Users\someone\ws\ai practice"
Get-Location
```

macOS:

```bash
cd "/Users/someone/ws/ai practice"
pwd
```

Linux:

```bash
cd "/home/someone/ws/ai practice"
pwd
```

각 결과가 `ai practice`로 끝나는 프로젝트 위치인지 확인합니다. 따옴표 없이 공백이 있는 경로를 넣으면 셸이 여러 인자로 나눠 해석해 이동에 실패할 수 있습니다. 명령의 목적이 같아도 실제 경로와 인자 구분은 맞춰야 합니다.

## 체크리스트

- Windows Terminal이 여러 명령줄 셸을 실행할 수 있는 호스트 앱이라는 점을 설명할 수 있다.
- macOS Terminal에서 `pwd`, `ls`, `cd`로 위치 확인과 이동을 할 수 있다.
- Linux에서 터미널을 열고 현재 위치와 파일 목록을 확인할 수 있다.
- Windows PowerShell의 `Get-Location`, `Get-ChildItem`, `Set-Location`의 목적을 설명할 수 있다.
- Windows와 macOS/Linux의 경로 표기 차이를 설명할 수 있다.
- 터미널 단축키는 환경마다 다를 수 있으며, `Tab`, `Ctrl + C`, 복사·붙여넣기 정도를 먼저 확인해야 한다는 점을 설명할 수 있다.
- 일반 앱의 `Ctrl + C`, `Ctrl + V`와 터미널의 복사·붙여넣기·실행 중단 단축키가 다를 수 있음을 설명할 수 있다.
- 복사한 명령에서 프롬프트 기호와 실제 입력할 명령을 구분할 수 있다.
- `sudo`, `rm`, `del`, `Remove-Item` 같은 명령은 의미를 확인하기 전에는 실행하지 않아야 함을 설명할 수 있다.
- `터미널을 연다 -> 현재 위치를 확인한다 -> 파일 목록을 확인한다 -> 실습 폴더로 이동한다 -> 다시 위치와 파일 목록을 확인한다 -> Python 명령을 실행한다` 순서를 설명할 수 있다.

## 출처와 참고 자료

- Microsoft, [What is Windows Terminal?](https://learn.microsoft.com/en-us/windows/terminal/){: target="_blank" rel="noopener noreferrer" }, Microsoft Learn, 확인 날짜: 2026-07-20. Windows Terminal이 Command Prompt, PowerShell, WSL bash 같은 여러 명령줄 셸을 실행하는 호스트 앱이라는 설명 확인에 사용했다.
- Apple, [Keyboard shortcuts in Terminal on Mac](https://support.apple.com/guide/terminal/keyboard-shortcuts-trmlshtcts/mac){: target="_blank" rel="noopener noreferrer" }, Apple Support, 확인 날짜: 2026-07-20. macOS Terminal에서 새 창/탭, 복사·붙여넣기, `Tab`, `Ctrl-C` 계열 단축키를 확인하는 근거로 사용했다.
- Apple, [Terminal User Guide](https://support.apple.com/guide/terminal/welcome/mac){: target="_blank" rel="noopener noreferrer" }, Apple Support, 확인 날짜: 2026-07-20. macOS Terminal의 역할과 명령 실행·파일/폴더 지정 안내 확인에 사용했다.
- Ubuntu Documentation, [UsingTheTerminal](https://help.ubuntu.com/community/UsingTheTerminal){: target="_blank" rel="noopener noreferrer" }, Ubuntu Community Help Wiki, 확인 날짜: 2026-07-20. Ubuntu/Linux에서 터미널을 열고 명령줄 작업을 수행하는 입문 맥락 확인에 사용했다.
- Microsoft, [Get-Location](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-location?view=powershell-7.5){: target="_blank" rel="noopener noreferrer" }, PowerShell documentation, 확인 날짜: 2026-07-20. PowerShell에서 현재 작업 위치를 확인하는 명령과 `pwd` 별칭 확인에 사용했다.
- Microsoft, [Set-Location](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-location?view=powershell-7.5){: target="_blank" rel="noopener noreferrer" }, PowerShell documentation, 확인 날짜: 2026-07-20. PowerShell에서 현재 작업 위치를 바꾸는 명령과 `cd` 별칭 확인에 사용했다.
- Microsoft, [Get-ChildItem](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.5){: target="_blank" rel="noopener noreferrer" }, PowerShell documentation, 확인 날짜: 2026-07-20. PowerShell에서 파일과 폴더 목록을 확인하는 명령과 `ls` 별칭 확인에 사용했다.
